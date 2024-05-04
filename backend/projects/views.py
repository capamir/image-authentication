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


logger = logging.getLogger(__name__)


def change_quotes_to_double(dictionary):
    new_dict = {}
    for key, value in dictionary.items():
        new_key = key.replace("'", "\"")
        if isinstance(value, str):
            new_value = value.replace("'", "\"")
        else:
            new_value = value
        new_dict[new_key] = new_value
    return new_dict



@api_view(['POST'])
@transaction.atomic
def uploadImage(request):
    try:
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the blockchain is empty
        if not Block.objects.exists():
            # Create the genesis block
            Block.create_genesis_block(encrypted_data=None)  # Pass appropriate encrypted_data if needed

        # Load image
        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Convert image to grayscale
        gray_image =extract_msb( cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),4)

        # Define block size (e.g., 8x8)
        block_size = (8, 8)

        key_length = 16  # AES-128
        secret_key = generate_secret_key(key_length)
        key = b'_^4\x887ja\xb0\xdd\x97"\xc2\x82\xcb\x0fc'
       



        # Call the function to process the image
        dct_blocks_dict = divide_array_into_columns_with_dct(gray_image, block_size)

        print(dct_blocks_dict)



        columns_hashed = hash_dictionary(dct_blocks_dict)
        encrypt_image=get_dictionary_elements(dct_blocks_dict,key)
        
        encrypted_data_json = json.dumps(change_quotes_to_double(encrypt_image))
         

        # Create a new Block object and save it to the database
        new_block = Block.objects.create(
            index=Block.objects.count(),
            data=columns_hashed,
            encrypted_data =encrypted_data_json
           
        )

        # Log the length of the compressed image data for debugging
        logger.debug(f"Length of compressed image data: {len(columns_hashed)}")

        # Return success response with relevant data
        return Response({'message': 'Image uploaded successfully', 'block_index': new_block.index}, status=status.HTTP_200_OK)

    except Exception as e:
        error_message = str(e)
        logger.error(f"Internal server error: {error_message}")
        return Response({'error': f'Internal server error: {error_message}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ImageAddressViewSet(viewsets.ViewSet):   
    def create(self, request):
        serializer = ImageAddressSerializer(data=request.data)
        image_file = request.FILES.get('image')
        

        
        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

        gray_image = extract_msb(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),4)
       

                
        # Define block size (e.g., 8x8)
        block_size = (8, 8)

        # Call the function to process the image and hash
        dct_blocks_dict = divide_array_into_columns_with_dct(gray_image, block_size)
        # print('this is dct factor')
        # print(dct_blocks_dict)
        # print('=========================')
        # print(dct_blocks_dict)
        # columns_hashed1 = hash_dictionary(dct_blocks_dict)
        # print('=========================')
        # # print(columns_hashed1)

        block_index = 1

        block = Block.get_block_by_index(block_index)
        block_hash = block.data
        block_encrypted = block.encrypted_data 

        block_encrypted_dic = json.loads(block_encrypted)
        # dicripted=get_dictionary_elements2(block_encrypted)

    

        key = b'_^4\x887ja\xb0\xdd\x97"\xc2\x82\xcb\x0fc'
        
        difrence=compare_dictionaries(block_hash, columns_hashed1)
        
        print(difrence)

        decrypted=get_dictionary_element2(block_encrypted_dic,difrence,key)

        recoverd_image=replace_columns(dct_blocks_dict,decrypted)

        # print(recoverd_image)
        
       


        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            filename = image_file.name
            return Response({"image": filename}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

