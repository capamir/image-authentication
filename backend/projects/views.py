import cv2
import numpy as np
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


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
        compressed_img, dct_channel = process_channel(img, block_size, percentage, quantization_matrix)
        
        # Encode the compressed image as bytes
        _, img_encoded = cv2.imencode('.jpg', compressed_img)
        
        # Convert image data to base64 string
        image_data = base64.b64encode(img_encoded).decode('utf-8')
        
        return {'image_data': image_data, 'dct_channel': dct_channel.tolist()}
        
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
        compressed_blocks, compressed_block_dct_quantized = [], []
        for block in blocks:
            block_compressed, block_dct_quantized = block_process(block, percentage, quantization_matrix)
            compressed_blocks.append(block_compressed)
            compressed_block_dct_quantized.append(block_dct_quantized)
        
        # Reconstruct compressed channel
        compressed_channel = np.concatenate([np.concatenate(compressed_blocks[row*int(new_width/block_size):(row+1)*int(new_width/block_size)], axis=1) for row in range(int(new_height/block_size))], axis=0)
        
        # Reconstruct dct factors channel
        dct_channel = np.concatenate([np.concatenate(compressed_block_dct_quantized[row*int(new_width/block_size):(row+1)*int(new_width/block_size)], axis=1) for row in range(int(new_height/block_size))], axis=0)

        return compressed_channel, dct_channel  
        
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
        
        return block_compressed, compressed_block_dct_quantized
    
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







def block_connect(dct_coeffs, block_size):
    try:
        # Convert dct_coeffs to NumPy array if it's a string
        if isinstance(dct_coeffs, str):
            dct_coeffs = np.fromstring(dct_coeffs[1:-1], dtype=float, sep=' ')
        
        # Convert dct_coeffs to NumPy array if it's a list
        if isinstance(dct_coeffs, list):
            dct_coeffs = np.array(dct_coeffs)
        
        # Get the shape of the DCT coefficients matrix
        rows, cols = dct_coeffs.shape
        
        # Calculate the number of blocks in each dimension
        num_blocks_row = rows // block_size
        num_blocks_col = cols // block_size
        
        # Reshape the DCT coefficients matrix into blocks
        blocks = dct_coeffs.reshape((num_blocks_row, block_size, num_blocks_col, block_size))
        
        # Initialize connected blocks dictionary
        connected_blocks_dict = {}
        
        # Connect blocks in each column
        for j in range(num_blocks_col):
            connected_blocks_dict[j] = blocks[:, :, j, :].reshape(-1, block_size, block_size)
        
        return connected_blocks_dict
    
    except Exception as e:
        raise ValueError(f"Error in block_connect: {str(e)}")


def encrypt_array(connected_blocks, key):
    encrypted_blocks = {}
    cipher = AES.new(key, AES.MODE_ECB)
    for column, array in connected_blocks.items():
        # Convert the array to C-contiguous bytes
        array_bytes = array.copy(order='C').tobytes()
        # Pad the data to be a multiple of 16 bytes (AES block size)
        padded_data = array_bytes + b'\0' * (16 - len(array_bytes) % 16)
        # Encrypt the padded data
        encrypted_data = cipher.encrypt(padded_data)
        encrypted_blocks[column] = encrypted_data

        # Print the encrypted outputs
          
        # print("encrypted Blocks:")
        # print("--------------------------------")
        # for col, encrypted_data in encrypted_blocks.items():
        #     hex_string = ''.join('{:02x}'.format(byte) for byte in encrypted_data)
        #     print(f"Encrypted data for column {col}: \n{hex_string}")
        # print("--------------------------------")

    return encrypted_blocks

def hash_blocks(connected_blocks_dict):
    hashed_blocks = {}
    for key, value in connected_blocks_dict.items():
        # Convert the array to C-contiguous buffer before hashing
        c_contiguous_array = value.copy(order='C')
        hashed_blocks[key] = hashlib.sha256(c_contiguous_array).hexdigest()

    # Print the output in the specified format
        
    print("Hashed Blocks:")
    print("--------------------------------")
    for key, value in hashed_blocks.items():
        print(f"Column {key}: {value}")
    print("--------------------------------")

    return hashed_blocks


import logging

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
        k = 5  # Adjust as needed
        image_with_msb = extract_msb(image, k)
        
        # Compress the image
        result = compress_grayscale_image(image_with_msb, block_size, percentage, quantization_matrix)
        compressed_image_data = result['image_data']
        dct_factors=result['dct_channel']

        aes_key = get_random_bytes(16)

        
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
