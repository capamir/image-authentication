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
        percentage = 50

        columns_dict = block_dct_zigzag(gray_image, block_size, percentage)

        key = b'_^4\x887ja\xb0\xdd\x97"\xc2\x82\xcb\x0fc'

        reconstructed_image = reconstruct_image_from_columns(columns_dict, block_size, gray_image.shape)

        plt.imshow(reconstructed_image, cmap="gray")
        plt.show()

        
        columns_hashed = hash_dictionary_elements_sha256(columns_dict)
        print(columns_hashed[26])
       
        encrypted_columns = encrypt_dictionary(columns_dict, key)
        # print(decrypt_dict(encrypted_columns))
        

        Block.create_genesis_block()

        block = Block(
            
            data=columns_hashed,
           
            hash="current_hash_value"
        )
        block.save_encrypted_data(encrypted_columns)
        return Response({
            'message': 'Image uploaded successfully',
            'block_index': block.index,
            'compressed_image': reconstructed_image
        }, status=status.HTTP_200_OK)

    except Exception as e:
        error_message = str(e)
        logger.error(f"Internal server error: {error_message}")
        return Response({'error': f'Internal server error: {error_message}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ImageAddressViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ImageAddressSerializer(data=request.data)
        image_file = request.FILES.get('image')
        adress = request.FILES.get('address')

       
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        gray_image = extract_msb(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 4)

        block_size = 8
        percentage =50

        columns_dict = block_dct_zigzag(gray_image, block_size, percentage)
        
        # reconstructed_image = reconstruct_image_from_columns(columns_dict, block_size, gray_image.shape)

        # print(columns_dict)
      
        key = b'_^4\x887ja\xb0\xdd\x97"\xc2\x82\xcb\x0fc'

        # print (adress)

        
        # plt.imshow(reconstructed_image, cmap="gray")
        # plt.show()

        
        columns_hashed2 = hash_dictionary_elements_sha256(columns_dict)
        print(columns_hashed2)


        block_index =20
        block = Block.objects.get(index=block_index)
        orginal_hash= eval(block.data)

   
        print('--------------------------------')
        
        print(orginal_hash)
        decrypted_block = block.deserialize_encrypted_data()
        decrypted_data = {int(key): value for key, value in decrypted_block.items()}

      
        difference=compare_dicts(orginal_hash,columns_hashed2)
        print(difference)

        key = b'_^4\x887ja\xb0\xdd\x97"\xc2\x82\xcb\x0fc'

        
        decrypted_columns = (format_dict_without_quotes(decrypt_dictionary(decrypted_data,key,difference)))

        decrypted_columns = decrypted_columns.replace('\n', '').replace(' ', '')
        decrypted_columns=eval(decrypted_columns)
        
        recovered_columns = replace_values(columns_dict,decrypted_columns)
        # print(recovered_columns)

        
        reconstructed_image = reconstruct_image_from_columns((recovered_columns), block_size, gray_image.shape)

        plt.imshow(reconstructed_image, cmap="gray")
        plt.show()


        if serializer.is_valid():
            filename = image_file.name
            return Response({"image": filename}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
