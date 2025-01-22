from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
import logging
import cv2
import numpy as np
from projects.imageProcess import *
from django.db import transaction
from projects.models import Block
import base64
import json


logger = logging.getLogger(__name__)
@api_view(['POST'])
@transaction.atomic
def uploadImage(request):
    try:
        
        # Extract files and fields
        image_file = request.FILES.get('image')
        uploaded_file = request.FILES.get('file')
        percentage = request.data.get('percentage')

        # Validate inputs
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not uploaded_file:
            return Response({'error': 'Key file not provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not percentage:
            return Response({'error': 'Percentage not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            percentage_received = int(percentage)
        except ValueError:
            return Response({'error': 'Invalid percentage value'}, status=status.HTTP_400_BAD_REQUEST)

        # Decode image
        image_bytes = image_file.read()
        image_np = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_np, cv2.COLOR_BGR2YCrCb)
        key = generate_secret_key_from_file(uploaded_file, 16)

        if image is None:
            return Response({'error': 'Failed to decode image'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract MSB for compression
        k = 5
        image_msb = extract_msb(image, k)

        logger.debug(f"MSB Image Shape: {image_msb.shape}")
        block_size = 16
        percentage = percentage_received

        # Process the image using DCT Zigzag
        columns_dict_Y = block_dct_zigzag_y_channel(image_msb, block_size, percentage)
        logger.debug(f"Columns Dictionary: {columns_dict_Y}")

        # Apply hash function on channel Y
        channel_Y_hash = calculate_column_hashes(columns_dict_Y)

        # Encrypting channel Y
        channel_Y_en = encrypt_columns_dict(columns_dict_Y, key)

        # Extract Cb and Cr channels
        cb_channel = image_msb[:, :, 1]
        cr_channel = image_msb[:, :, 2]

       


        # Apply DCT, quantization, and zigzag traversal on the entire Cb and Cr channels
        zigzag_cb = dct_zigzag_entire_channel(cb_channel)
        zigzag_cr = dct_zigzag_entire_channel(cr_channel)

        # Encrypting channels entire Cb and Cr
        zigzag_cb_en = encrypt_dct_zigzag_output(zigzag_cb, key)
        zigzag_cr_en = encrypt_dct_zigzag_output(zigzag_cr, key)

        # Reconstruct the image from columns channels
        restored_y_channel = reconstruct_y_channel_image(columns_dict_Y, block_size, image.shape)
        logger.debug(f"Reconstructed Image Shape: {restored_y_channel.shape}")

        # Reconstruct the Cb and Cr channels
        restored_cb_channel = reconstruct_entire_channel(zigzag_cb, cb_channel.shape)
        restored_cr_channel = reconstruct_entire_channel(zigzag_cr, cr_channel.shape)

        # Combine the restored Y, Cb, and Cr channels to form the final image
        restored_image_ycrcb = cv2.merge([restored_y_channel, restored_cb_channel, restored_cr_channel])


        # Normalize the reconstructed image to ensure the brightness is retained
        reconstructed_image_normalized = cv2.normalize(restored_image_ycrcb, None, 0, 255, cv2.NORM_MINMAX)
        reconstructed_image_normalized = reconstructed_image_normalized.astype(np.uint8)  # Ensure data type is uint8

        # Encode reconstructed image for JSON response
        _, reconstructed_image_encoded = cv2.imencode('.png', reconstructed_image_normalized)
        reconstructed_image_base64 = base64.b64encode(reconstructed_image_encoded).decode('utf-8')

        # Encode bytes within dictionaries
        channel_Y_en_encoded = encode_bytes_in_dict(channel_Y_en) if channel_Y_en else None
        zigzag_cb_en_encoded = encode_bytes_in_dict(zigzag_cb_en) if zigzag_cb_en else None
        zigzag_cr_en_encoded = encode_bytes_in_dict(zigzag_cr_en) if zigzag_cr_en else None

        # Serialize dictionaries to JSON strings and encode to base64
        channel_Y_en_base64 = base64.b64encode(json.dumps(channel_Y_en_encoded).encode('utf-8')).decode('utf-8') if channel_Y_en_encoded else None
        zigzag_cb_en_base64 = base64.b64encode(json.dumps(zigzag_cb_en_encoded).encode('utf-8')).decode('utf-8') if zigzag_cb_en_encoded else None
        zigzag_cr_en_base64 = base64.b64encode(json.dumps(zigzag_cr_en_encoded).encode('utf-8')).decode('utf-8') if zigzag_cr_en_encoded else None

        # Add to blockchain
        Block.create_genesis_block()
        block = Block(
            hash="current_hash_value",
            column_hash=channel_Y_hash,
            encrypted_Y=channel_Y_en_base64,
            encrypted_Cb=zigzag_cb_en_base64,
            encrypted_Cr=zigzag_cr_en_base64,
        )
        block.save()

        encoded_key = base64.b64encode(key).decode('utf-8')

        return Response({
            'message': 'Image uploaded successfully',
            'block_index': block.index,
            'key': encoded_key,
            'percentage': percentage_received,
            'compressed_image': reconstructed_image_base64
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Internal server error: {str(e)}", exc_info=True)
        return Response({'error': f'Internal server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ImageAddressViewSet(viewsets.ViewSet):
    def create(self, request):
        image_file = request.FILES.get('image')
        image_key = request.data.get('key')
        index = int(request.data.get('address'))
        percentage = int(request.data.get('dct'))

        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not index:
            return Response({'error': 'index file not provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not percentage:
            return Response({'error': 'Percentage not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not image_key:
            return Response({'error': 'image_key not provided'}, status=status.HTTP_400_BAD_REQUEST)
        

        # Decode image
        image_bytes = image_file.read()
        image_np = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_np, cv2.COLOR_BGR2YCrCb)
        key = generate_secret_key_from_file(image_key, 16)

        # Extract MSB for compression
        k = 6
        image_msb = extract_msb(image, k)
        logger.debug(f"MSB Image Shape: {image_msb.shape}")
        block_size = 16
        percentage = percentage


        # Extract Cb and Cr channels
        cb_channel = image_msb[:, :, 1]
        cr_channel = image_msb[:, :, 2]

   

        # Process the channel Y 
        columns_dict_Y = block_dct_zigzag_y_channel(image_msb, block_size, percentage)
        logger.debug(f"Columns Dictionary: {columns_dict_Y}")

        # Apply hash function on channel Y
        channel_Y_hash = calculate_column_hashes(columns_dict_Y)

        # import block
        block_index = index
        block = Block.objects.get(index=block_index)
        orginal_hash = eval(block.column_hash)

        encrypted_Y_json = base64.b64decode(block.encrypted_Y.encode('utf-8')).decode('utf-8')
        encrypted_Cb_json = base64.b64decode(block.encrypted_Cb.encode('utf-8')).decode('utf-8')
        encrypted_Cr_json = base64.b64decode(block.encrypted_Cr.encode('utf-8')).decode('utf-8')

        encrypted_Y = json.loads(encrypted_Y_json)
        encrypted_Cb = json.loads(encrypted_Cb_json)
        encrypted_Cr = json.loads(encrypted_Cr_json)

        encrypted_Y_Original_image = decode_bytes_in_dict(encrypted_Y)
        encrypted_Cb_Original_image= decode_bytes_in_dict(encrypted_Cb)
        encrypted_Cr_Original_image= decode_bytes_in_dict(encrypted_Cr)



    
       #find tampered columns by compar hash
        differences = compare_hash_arrays(orginal_hash, channel_Y_hash)
    

        if (key != None):
            
            decrypt_columns_different = decrypt_selected_columns(encrypted_Y_Original_image, key,differences)
           

            updated_columns_dict = replace_columns(columns_dict_Y,decrypt_columns_different)


            decrypt_channel_cb=decrypt_dct_zigzag_output(encrypted_Cb_Original_image,key)
            decrypt_channel_cr=decrypt_dct_zigzag_output(encrypted_Cr_Original_image,key)

            restored_y_channel = reconstruct_y_channel_image(updated_columns_dict, block_size, image.shape)

            # Reconstruct the Cb and Cr channels
            restored_cb_channel = reconstruct_entire_channel(decrypt_channel_cb , cb_channel.shape)
            restored_cr_channel = reconstruct_entire_channel(decrypt_channel_cr, cr_channel.shape)

            # Combine the restored Y, Cb, and Cr channels to form the final image
            restored_image_ycrcb = cv2.merge([restored_y_channel, restored_cb_channel, restored_cr_channel])



            # Normalize the highlighted image to ensure the brightness is retained
            reconstructed_image = cv2.normalize(restored_image_ycrcb, None, 0, 255, cv2.NORM_MINMAX)
            reconstructed_image = reconstructed_image.astype(np.uint8)

            # Encode highlighted image for JSON response
            _, reconstructed_image_encoded = cv2.imencode('.png', reconstructed_image)
            reconstructed_base64 = base64.b64encode(reconstructed_image_encoded).decode('utf-8')
            highlighted_image_base64= blur_other_columns(reconstructed_image, differences, block_size)


            return Response({
            'original_image':reconstructed_base64,
            'compressed_image': highlighted_image_base64,
             "message":"image succesfully restored", 
                                                              }, status=status.HTTP_200_OK)






        


