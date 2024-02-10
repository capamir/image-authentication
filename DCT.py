import cv2
import numpy as np


# Default quantization matrix (for quality factor 50)
default_quantization_matrix = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                        [12, 12, 14, 19, 26, 58, 60, 55],
                                        [14, 13, 16, 24, 40, 57, 69, 56],
                                        [14, 17, 22, 29, 51, 87, 80, 62],
                                        [18, 22, 37, 56, 68, 109, 103, 77],
                                        [24, 35, 55, 64, 81, 104, 113, 92],
                                        [49, 64, 78, 87, 103, 121, 120, 101],
                                        [72, 92, 95, 98, 112, 100, 103, 99]])

def block_process(block, quantization_matrix=default_quantization_matrix):
    # Apply DCT to the block
    block_dct = cv2.dct(np.float32(block))
    
    # Apply quantization using the default quantization matrix
    block_dct_quantized = np.round(block_dct / quantization_matrix) * quantization_matrix
    
    # Inverse DCT for the block
    block_compressed = cv2.idct(block_dct_quantized)
    
    # Clip values to 0-255
    block_compressed = np.clip(block_compressed, 0, 255)
    
    # Convert to uint8
    block_compressed = np.uint8(block_compressed)
    
    return block_compressed

def compress_image(image_path, block_size, quantization_matrix=default_quantization_matrix,output_folder="compressed-images"):
    # Load image
    img = cv2.imread(image_path)
    
    # Convert image to YUV color space
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    
    # Split YUV channels
    y, u, v = cv2.split(img_yuv)
    
    # Process each channel separately
    y_compressed = process_channel(y, block_size, quantization_matrix)
    u_compressed = process_channel(u, block_size, quantization_matrix)
    v_compressed = process_channel(v, block_size, quantization_matrix)
    
    # Merge compressed channels
    compressed_img_yuv = cv2.merge((y_compressed, u_compressed, v_compressed))
    
    # Convert back to BGR color space
    compressed_img = cv2.cvtColor(compressed_img_yuv, cv2.COLOR_YUV2BGR)
    
    return compressed_img

def process_channel(channel, block_size, quantization_matrix=default_quantization_matrix):
    # Pad channel if necessary
    height, width = channel.shape
    new_height = height + (block_size - height % block_size) % block_size
    new_width = width + (block_size - width % block_size) % block_size
    padded_channel = np.pad(channel, ((0, new_height - height), (0, new_width - width)), mode='constant')
    
    # Divide channel into blocks
    blocks = [padded_channel[i:i+block_size, j:j+block_size] for i in range(0, new_height, block_size) for j in range(0, new_width, block_size)]
    
    # Apply block processing
    compressed_blocks = [block_process(block, quantization_matrix) for block in blocks]
    
    # Reconstruct compressed channel
    compressed_channel = np.concatenate([np.concatenate(compressed_blocks[row*int(new_width/block_size):(row+1)*int(new_width/block_size)], axis=1) for row in range(int(new_height/block_size))], axis=0)
    
    return compressed_channel

# Example usage
# image_path = '1.jpg'
# block_size = 8  # Adjust block size as needed

# compressed_image = compress_image(image_path, block_size)

# Save compressed image
# cv2.imwrite('compressed_image.jpg', compressed_image)
