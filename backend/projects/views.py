from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
import logging
import cv2
import numpy as np
from projects.imageProcess import *
from .serializers import ImageAddressSerializer
from django.db import transaction
from projects.models import Block
import matplotlib.pyplot as plt
import base64
logger = logging.getLogger(__name__)

@api_view(['POST'])
@transaction.atomic
def uploadImage(request):
    try:
        # Read the image file from the request
        image_file = request.FILES.get('image')
        percentage = request.data.get('percentage')

        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        if percentage is None:
            return Response({'error': 'Percentage not provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate percentage
        try:
            percentage_received = int(percentage)
        except ValueError:
            return Response({'error': 'Invalid percentage value'}, status=status.HTTP_400_BAD_REQUEST)

        # Read image bytes and decode
        image_bytes = image_file.read()
        image_np = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)  # Ensure color image is read

        if image is None:
            return Response({'error': 'Failed to decode image'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        msb_image = extract_msb(gray_image, 4)  # Extract MSB for compression
        logger.debug(f"MSB Image Shape: {msb_image.shape}")

        block_size = 8
        percentage = percentage_received

        # Process the image using DCT Zigzag
        columns_dict = block_dct_zigzag(msb_image, block_size, percentage)
        logger.debug(f"Columns Dictionary: {columns_dict}")

        # Reconstruct the image from columns
        reconstructed_image = reconstruct_image_from_columns(columns_dict, block_size, msb_image.shape)
        logger.debug(f"Reconstructed Image Shape: {reconstructed_image.shape}")

        # Normalize the reconstructed image to ensure the brightness is retained
        reconstructed_image_normalized = cv2.normalize(reconstructed_image, None, 0, 255, cv2.NORM_MINMAX)
        reconstructed_image_normalized = reconstructed_image_normalized.astype(np.uint8)  # Ensure data type is uint8

        # Encode reconstructed image for JSON response
        _, reconstructed_image_encoded = cv2.imencode('.png', reconstructed_image_normalized)
        reconstructed_image_base64 = base64.b64encode(reconstructed_image_encoded).decode('utf-8')

        key = generate_secret_key(16)
       
        columns_hashed = hash_dictionary_elements_sha256(columns_dict)

        encrypted_columns = encrypt_dict(columns_dict, key)
        encrypted_columns=json.dumps(encrypted_columns, indent=2)
       

       

        
        

        Block.create_genesis_block()

        block = Block(
            
            data=columns_hashed,
           
            hash="current_hash_value",
            
            encrypted_data=encrypted_columns
        )
        block.save()




        encoded_key =base64.b64encode(key).decode('utf-8')

        # Prepare response with proper serialization of binary data
        return Response({
            'message': 'Image uploaded successfully',
            'block_index': block.index,  # Placeholder, adjust as necessary
            'key':encoded_key,  # Placeholder, adjust as necessary
            'percentage': percentage,
            'compressed_image': reconstructed_image_base64  # Base64 encoded image string
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Internal server error: {str(e)}", exc_info=True)
        return Response({'error': f'Internal server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ImageAddressViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ImageAddressSerializer(data=request.data)


        image_file = request.FILES.get('image')
        image_key = request.data.get('key')
        index = int(request.data.get('index'))
        percentage = int(request.data.get('percentage'))

       

        

        

        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        gray_image = extract_msb(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 4)

        # process image

        block_size = 8
        columns_dict = block_dct_zigzag(gray_image, block_size, percentage)

        

        # hashing dct columns
        columns_hashed2 = hash_dictionary_elements_sha256(columns_dict)

        # import block
        block_index = index
        block = Block.objects.get(index=block_index)
        orginal_hash = eval(block.data)
        encrypted_data=eval(block.encrypted_data)


       

        # compare images
        differences = compare_dicts(orginal_hash, columns_hashed2)
        print(differences)
    
        # If a key is provided, decrypt and reconstruct the image
        if (image_key != None):
            
            decoded_key = base64.b64decode(image_key)
            # decrypting dct columns
            
            
            decrypted_columns = decrypt_dict(encrypted_data, decoded_key, differences)
            decrypted_columns={int(key): value for key, value in decrypted_columns.items()}

            

         
            # print((decrypted_columns))
            # print("----------------------")
            # print(type(encrypted_data))

            
            # restructure image
            recovered_columns = replace_values(columns_dict, decrypted_columns)

        
            reconstructed_image = reconstruct_image_from_columns(recovered_columns, block_size, gray_image.shape)

            
            # Normalize the highlighted image to ensure the brightness is retained
            reconstructed_image = cv2.normalize(reconstructed_image, None, 0, 255, cv2.NORM_MINMAX)
            reconstructed_image = reconstructed_image.astype(np.uint8)

            # Encode highlighted image for JSON response
            _, reconstructed_image_encoded = cv2.imencode('.png', reconstructed_image)
            reconstructed_base64 = base64.b64encode(reconstructed_image_encoded).decode('utf-8')


            # Highlight differences
            highlighted_image = reconstructed_image.copy()
            for key in differences:
                column = int(key)
                # Assume block_size is 8x8 and column index starts from 0
                start_x = column * block_size
                end_x = start_x + block_size
                # Draw a red rectangle around the column
                cv2.rectangle(highlighted_image, (start_x, 0), (end_x, highlighted_image.shape[0]), (0, 0, 255), 2)

            logger.debug(f"Reconstructed Image Shape: {reconstructed_image.shape}")
            
            # Normalize the highlighted image to ensure the brightness is retained
            highlighted_image_normalized = cv2.normalize(highlighted_image, None, 0, 255, cv2.NORM_MINMAX)
            highlighted_image_normalized = highlighted_image_normalized.astype(np.uint8)

            # Encode highlighted image for JSON response
            _, highlighted_image_encoded = cv2.imencode('.png', highlighted_image_normalized)
            highlighted_image_base64 = base64.b64encode(highlighted_image_encoded).decode('utf-8')

            return Response({
            'original_image':reconstructed_base64,
            'compressed_image': highlighted_image_base64,
             "message":"image succesfully restored", # Base64 encoded image string
                                                              }, status=status.HTTP_200_OK)






        


