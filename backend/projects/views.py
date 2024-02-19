import cv2
import numpy as np
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Default quantization matrix (for quality factor 50)
default_quantization_matrix = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                        [12, 12, 14, 19, 26, 58, 60, 55],
                                        [14, 13, 16, 24, 40, 57, 69, 56],
                                        [14, 17, 22, 29, 51, 87, 80, 62],
                                        [18, 22, 37, 56, 68, 109, 103, 77],
                                        [24, 35, 55, 64, 81, 104, 113, 92],
                                        [49, 64, 78, 87, 103, 121, 120, 101],
                                        [72, 92, 95, 98, 112, 100, 103, 99]])

# Function to extract kMSB from the image


# Function to extract kMSB from the image
def extract_msb(image_array, k):
    try:
        new_img = np.zeros_like(image_array)
        for i in range(3):  # Loop through RGB channels
            # Extract k most significant bits
            msb = image_array[:, :, i] >> (8 - k)
            # Add the MSB to the new image
            new_img[:, :, i] = msb
        return new_img
    except Exception as e:
        raise ValueError(f"Error in extracting MSB: {str(e)}")

# Function to compress the grayscale image
def compress_grayscale_image(image_array, block_size, percentage, quantization_matrix):
    try:
        img = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        block_size = int(block_size)
        percentage = float(percentage)
        
        # Process the grayscale image
        compressed_img = process_channel(img, block_size, percentage, quantization_matrix)
        
        # Encode the compressed image as bytes
        _, img_encoded = cv2.imencode('.jpg', compressed_img)
        
        # Convert encoded image bytes to HttpResponse object
        response = HttpResponse(img_encoded.tobytes(), content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename="compressed_image.jpg"'
        
        return response
    except Exception as e:
        raise ValueError(f"Error in compressing image: {str(e)}")

# Function to process a single channel of the image
def process_channel(channel, block_size, percentage, quantization_matrix):
    try:
        height, width = channel.shape
        new_height = height + (block_size - height % block_size) % block_size
        new_width = width + (block_size - width % block_size) % block_size
        padded_channel = np.pad(channel, ((0, new_height - height), (0, new_width - width)), mode='constant')
        
        # Divide channel into blocks
        blocks = [padded_channel[i:i+block_size, j:j+block_size] for i in range(0, new_height, block_size) for j in range(0, new_width, block_size)]
        
        # Apply block processing
        compressed_blocks = [block_process(block, percentage, quantization_matrix) for block in blocks]
        
        # Reconstruct compressed channel
        compressed_channel = np.concatenate([np.concatenate(compressed_blocks[row*int(new_width/block_size):(row+1)*int(new_width/block_size)], axis=1) for row in range(int(new_height/block_size))], axis=0)
        
        return compressed_channel
    except Exception as e:
        raise ValueError(f"Error in processing channel: {str(e)}")

# Function to process a block using DCT and quantization
def block_process(block, percentage, quantization_matrix):
    try:
        # Apply DCT to the block
        block_dct = cv2.dct(np.float32(block))
        
        # Apply quantization using the default quantization matrix
        block_dct_quantized = np.round(block_dct / quantization_matrix) * quantization_matrix
        
        # Keep a certain percentage of the zigzag traversed coefficients
        compressed_block_dct_quantized = keep_percentage_zigzag(block_dct_quantized, percentage)
        
        # Inverse DCT for the block
        block_compressed = cv2.idct(compressed_block_dct_quantized)
        
        # Clip values to 0-255
        block_compressed = np.clip(block_compressed, 0, 255)
        
        # Convert to uint8
        block_compressed = np.uint8(block_compressed)
        
        return block_compressed
    except Exception as e:
        raise ValueError(f"Error in block processing: {str(e)}")

# Function to keep a certain percentage of coefficients using zigzag traversal
def keep_percentage_zigzag(matrix, percentage):
    try:
        total_elements = matrix.size
        elements_to_keep = int(total_elements * percentage / 100)
        flattened_matrix = matrix.flatten()
        sorted_indices = np.argsort(np.abs(flattened_matrix))[::-1]
        kept_indices = sorted_indices[:elements_to_keep]
        zeroed_indices = sorted_indices[elements_to_keep:]
        flattened_matrix[zeroed_indices] = 0
        return flattened_matrix.reshape(matrix.shape)
    except Exception as e:
        raise ValueError(f"Error in keeping percentage of coefficients: {str(e)}")

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
        k = 5  # Adjust as needed
        image_with_msb = extract_msb(image, k)

        # Compress the image
        compressed_image = compress_grayscale_image(image_with_msb, block_size, percentage, quantization_matrix)

        return compressed_image
    except Exception as e:
        error_message = str(e)
        return Response({'error': f'Internal server error: {error_message}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
