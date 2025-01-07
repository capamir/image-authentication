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
import base64
logger = logging.getLogger(__name__)


@api_view(['POST'])
@transaction.atomic
def uploadImage(request):
    try:
        # Log incoming request
        logger.debug(f"Request data: {request.data}")
        logger.debug(f"Request files: {request.FILES}")

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

        # Validate percentage
        try:
            percentage_received = int(percentage)
        except ValueError:
            return Response({'error': 'Invalid percentage value'}, status=status.HTTP_400_BAD_REQUEST)

        # Decode image
        image_bytes = image_file.read()
        image_np = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        if image is None:
            return Response({'error': 'Failed to decode image'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        #Extract MSB for compression
        msb_image = extract_msb(gray_image, 5)  
        logger.debug(f"MSB Image Shape: {msb_image.shape}")
        block_size = 16
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

        #encrypt reconstructed image
        if(uploaded_file!=None):
            key = generate_secret_key_from_file(uploaded_file,16)
        
            columns_hashed = hash_dictionary_elements_sha256(columns_dict)
            encrypted_columns = encrypt_dict(columns_dict, key)
            encrypted_columns=json.dumps(encrypted_columns, indent=2)
 
        # add to blockchain
        Block.create_genesis_block()
        block = Block(
            
            data=columns_hashed,
           
            hash="current_hash_value",
            
            encrypted_data=encrypted_columns
        )
        block.save()

        encoded_key =base64.b64encode(key).decode('utf-8')
     
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


         # Validate inputs
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not index:
            return Response({'error': 'index file not provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not percentage:
            return Response({'error': 'Percentage not provided'}, status=status.HTTP_400_BAD_REQUEST)


        key = generate_secret_key_from_file(image_key,16)
        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        gray_image = extract_msb(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),5)


        # process image
        block_size = 16
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

    

        if (key != None):
            
            # decrypting dct columns
            decrypted_columns = decrypt_dict(encrypted_data, key, differences)
            decrypted_columns = {int(key): value for key, value in decrypted_columns.items()}
            
        
            # restructure image
            recovered_columns = replace_values(columns_dict, decrypted_columns)
            reconstructed_image = reconstruct_image_from_columns(recovered_columns, block_size, gray_image.shape)

            # Normalize the highlighted image to ensure the brightness is retained
            reconstructed_image = cv2.normalize(reconstructed_image, None, 0, 255, cv2.NORM_MINMAX)
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






        


