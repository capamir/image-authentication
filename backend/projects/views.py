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
import matplotlib.pyplot as plt



logger = logging.getLogger(__name__)



@api_view(['POST'])
@transaction.atomic
def uploadImage(request):
    try:
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        gray_image = extract_msb(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 4)
        block_size = 8
        percentage = 25

        reconstructed_image, dct_columns = process_image_blocks(gray_image, block_size, percentage)

        
        original_shapes = {col_index: col.shape for col_index, col in dct_columns.items()}
        print(original_shapes)
        key = b'_^4\x887ja\xb0\xdd\x97"\xc2\x82\xcb\x0fc'



        
        reconstructed_image_d = reconstruct_image_from_dct_columns(dct_columns, image.shape[0], image.shape[1])

        plt.imshow(reconstructed_image_d, cmap="gray")
        plt.show()

        columns_dict_with_double_quotes = change_quotes_to_double(dct_columns)
        columns_hashed = hash_columns_dict(columns_dict_with_double_quotes)
        
        encrypted_columns = encrypt_dct_columns(columns_dict_with_double_quotes, key)

        decrypted_columns = decrypt_dct_columns(encrypted_columns, key, original_shapes)

        print(decrypted_columns)
        new_block = Block.objects.create(
            index=Block.objects.count(),
            data=columns_hashed,
            encrypted_data=encrypted_columns,
            original_shapes=original_shapes
        )

        logger.debug(f"Length of compressed image data: {len(columns_hashed)}")
        reconstructed_image_base64 = base64.b64encode(reconstructed_image_d).decode('utf-8')

        return Response({
            'message': 'Image uploaded successfully',
            'block_index': new_block.index,
            'compressed_image': reconstructed_image_base64
        }, status=status.HTTP_200_OK)

    except Exception as e:
        error_message = str(e)
        logger.error(f"Internal server error: {error_message}")
        return Response({'error': f'Internal server error: {error_message}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ImageAddressViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ImageAddressSerializer(data=request.data)
        image_file = request.FILES.get('image')

       
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        gray_image = extract_msb(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 4)

        block_size = 8
        percentage = 25  # Percentage of DCT coefficients to keep

        # Process the image blocks
        reconstructed_image, columns_dict = process_image_blocks(gray_image, block_size, percentage)

        columns_dict_with_double_quotes = change_quotes_to_double(columns_dict)
        columns_hashed1 = hash_columns_dict(columns_dict_with_double_quotes)


        # Define block size (e.g., 8x8)
        block_size = (8, 8)

        
        block_index = 3

        # Retrieve block data by index
        block = Block.objects.get(index=block_index)
        orginal_hash= eval(block.data)

        difrence=compare_dictionaries(orginal_hash,columns_hashed1)
        print(difrence)
        # Debugging prints to check the content
         
        original_shapes = eval(block.original_shapes)
        
        # Deserialize JSON string to dictionary
        block_encrypted = eval(block.encrypted_data)  # Deserialize JSON string to dictionary

        # Define your encryption key
        key = b'_^4\x887ja\xb0\xdd\x97"\xc2\x82\xcb\x0fc'

        # Decrypt the columns
        decrypted_columns = decrypt_dct_columns2(block_encrypted, key, original_shapes, difrence)
        # print(decrypted_columns)



        recoverd_image=replace_columns(columns_dict,decrypted_columns)

        reconstructed_image_d = reconstruct_image_from_dct_columns(recoverd_image, image.shape[0], image.shape[1])
        plt.imshow(reconstructed_image_d, cmap="gray")
        plt.show()

        if serializer.is_valid():
            filename = image_file.name
            return Response({"image": filename}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



