from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging
import cv2
import numpy as np
from projects.imageProcess import *


logger = logging.getLogger(__name__)

@api_view(['POST'])
def uploadImage(request):
    try:
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Parameters for compression
        block_size = 8  # Block size for DCT compression
        percentage = 8  # Percentage of coefficients to keep
        quantization_matrix = default_quantization_matrix  # Your default quantization matrix

        # Read image as array
        image_array = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # Extract kMSB
        k = 8  # Adjust as needed
        image_with_msb = extract_msb(image, k)
        
        # Compress the image
        result = compress_grayscale_image(image_with_msb, block_size, percentage, quantization_matrix)
        compressed_image_data = result['image_data']
        dct_factors=result['dct_channel']

        # aes_key = get_random_bytes(16)
        aes_key=b"\xa9\xf1\x16Z\xf2\x9eA\x0e\xd9I\xf2\xb1\x16\x82\x85\xf4"
        print (aes_key)

        
        img_encypt=encrypt_array(block_connect(dct_factors,8),aes_key)

        image_hash=hash_blocks(block_connect(dct_factors,8))

        # Log the length of the compressed image data for debugging
        logger.debug(f"Length of compressed image data: {len(compressed_image_data)}")

        # Return only the compressed image data to the frontend
        return HttpResponse(compressed_image_data, content_type='image/jpeg')
        
    except Exception as e:
        error_message = str(e)
        logger.error(f"Internal server error: {error_message}")
        return Response({'error': f'Internal server error: {error_message}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
