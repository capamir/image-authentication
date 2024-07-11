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

import json
import ast



import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib




logger = logging.getLogger(__name__)


def encode_bytes(obj):
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
    elif isinstance(obj, list):
        return [encode_bytes(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: encode_bytes(value) for key, value in obj.items()}
    return obj

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
        percentage = 20

        columns_dict = block_dct_zigzag(gray_image, block_size, percentage)
        print((columns_dict))
        key = b'_^4\x887ja\xb0\xdd\x97"\xc2\x82\xcb\x0fc'



        reconstructed_image = reconstruct_image_from_columns(columns_dict, block_size, gray_image.shape)


        

     
        plt.imshow(reconstructed_image, cmap="gray")
        plt.show()

        
        columns_hashed = hash_elements(columns_dict)
        print(columns_dict)
       
        encrypted_columns = encrypt_dictionary(columns_dict, key)
        # print(decrypt_dict(encrypted_columns))
        

        import json
        import base64






        block = Block(
            
            data=columns_hashed,
           
            hash="current_hash_value"
        )
        block.save_encrypted_data(encrypted_columns)
        return Response({
            'message': 'Image uploaded successfully',
            'block_index': block.index,
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
        percentage = 20 # Percentage of DCT coefficients to keep

        columns_dict = block_dct_zigzag(gray_image, block_size, percentage)
        # reconstructed_image = reconstruct_image_from_columns(columns_dict, block_size, gray_image.shape)



       



        #print(columns_dict)
      
        key = b'_^4\x887ja\xb0\xdd\x97"\xc2\x82\xcb\x0fc'



        
        # plt.imshow(reconstructed_image, cmap="gray")
        # plt.show()

        
        columns_hashed2 = hash_indices(columns_dict)

        print(columns_hashed2)
        


        block_index = 4

        # Retrieve block data by index
        block = Block.objects.get(index=block_index)
        orginal_hash= eval(block.data)

        # print(orginal_hash)
        print('--------------------------------')
        decrypted_block = block.deserialize_encrypted_data()
        decrypted_data = {int(key): value for key, value in decrypted_block.items()}

        
        difrence=compare_dicts(orginal_hash,columns_hashed2)
        print(difrence)
        # Debugging prints to check the content
         
     
        
        # Deserialize JSON string to dictionary

        # Define your encryption key
        key = b'_^4\x887ja\xb0\xdd\x97"\xc2\x82\xcb\x0fc'

        
        decrypted_columns = (format_dict_without_quotes(decrypt_dictionary(decrypted_data,key,difrence)))

       

        array = np.array
        float32 = np.float32

        decrypted_columns = decrypted_columns.replace('\n', '').replace(' ', '')
        decrypted_columns=eval(decrypted_columns)
        
        # print(decrypted_columns)
        
        
        
        recovered_columns = replace_values(columns_dict,decrypted_columns)
        # print(recovered_columns)

        

        
        reconstructed_image = reconstruct_image_from_columns((recovered_columns), block_size, gray_image.shape)

        plt.imshow(reconstructed_image, cmap="gray")
        plt.show()



        
        # print(reconstructed_image)


       
        if serializer.is_valid():
            filename = image_file.name
            return Response({"image": filename}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



