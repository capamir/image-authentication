import cv2
import numpy as np
import os
import tempfile
import io
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

# def extract_msb(image_path, k):
#     try:
#         # Open the image
#         img = cv2.imread(image_path)
#         if img is None:
#             raise ValueError("Failed to read the image")

#         # Extract MSB for each pixel and create a new image
#         new_img = np.zeros_like(img)
#         for i in range(3):  # Loop through RGB channels
#             # Extract k most significant bits
#             msb = img[:, :, i] >> (8 - k)
#             # Add the MSB to the new image
#             new_img[:, :, i] = msb
#         return new_img
#     except Exception as e:
#         raise ValueError(f"Error in extracting MSB: {str(e)}")
    
def compress_grayscale_image(image, block_size, percentage, quantization_matrix=default_quantization_matrix):
    img_bytes = image.read()
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print("Error: Unable to read the image.")
        return None
    
    # Process the grayscale image
    compressed_img = process_channel(img, block_size, percentage, quantization_matrix)
    
    # Encode the compressed image as bytes
    _, img_encoded = cv2.imencode('.jpg', compressed_img)
    
    # Convert encoded image bytes to HttpResponse object
    response = HttpResponse(img_encoded.tobytes(), content_type='image/jpeg')
    response['Content-Disposition'] = 'attachment; filename="compressed_image.jpg"'
    
    return response

# Function to process a single channel of the image
def process_channel(channel, block_size, percentage, quantization_matrix=default_quantization_matrix):
    # Pad channel if necessary
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

# Function to process a block using DCT and quantization
def block_process(block, percentage, quantization_matrix=default_quantization_matrix):
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

# Function to keep a certain percentage of coefficients using zigzag traversal
def keep_percentage_zigzag(matrix, percentage):
    # Perform zigzag traversal
    result = zigzag_traversal(matrix)
    
    # Calculate the number of elements to keep
    total_elements = len(result)
    elements_to_keep = int(total_elements * percentage / 100)
    
    # Create a new list with kept elements and zeros for the rest
    kept_elements = result[:elements_to_keep]
    zero_elements = [0] * (total_elements - elements_to_keep)
    
    # Combine the kept elements and zeros
    new_result = kept_elements + zero_elements
    
    # Put the new_result back into the matrix
    rows = len(matrix)
    cols = len(matrix[0])
    index = 0
    row, col = 0, 0
    going_up = True
    for i in range(len(new_result)):
        matrix[row][col] = new_result[i]
        
        # Move diagonally up and to the right
        if going_up:
            if col == 0 or row == rows - 1:
                going_up = False
                if row < rows - 1:
                    row += 1
                else:
                    col += 1
            else:
                row += 1
                col -= 1
        # Move diagonally down and to the left
        else:
            if row == 0 or col == cols - 1:
                going_up = True
                if col < cols - 1:
                    col += 1
                else:
                    row += 1
            else:
                row -= 1
                col += 1
    
    return matrix

# Function to perform zigzag traversal
def zigzag_traversal(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Initialize variables for traversing
    row, col = 0, 0
    going_up = True
    result = []
    
    while row < rows and col < cols:
        result.append(matrix[row][col])
        
        # Move diagonally up and to the right
        if going_up:
            if col == 0 or row == rows - 1:
                going_up = False
                if row < rows - 1:
                    row += 1
                else:
                    col += 1
            else:
                row += 1
                col -= 1
        # Move diagonally down and to the left
        else:
            if row == 0 or col == cols - 1:
                going_up = True
                if col < cols - 1:
                    col += 1
                else:
                    row += 1
            else:
                row -= 1
                col += 1
    
    return result

@api_view(['POST'])
def uploadImage(request):
    try:
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform compression with kMSB extraction and DCT
        # k = 1  # Number of most significant bits to extract
        block_size = 8  # Block size for DCT compression
        percentage = 8  # Percentage of coefficients to kee

        #do kmsb here

        # Compress the grayscale image
        compressed_image = compress_grayscale_image(image_file, block_size, percentage)

        return compressed_image
    except Exception as e:
        error_message = str(e)
        return Response({'error': f'Internal server error: {error_message}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
