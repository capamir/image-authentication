import cv2
import numpy as np
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from scipy.ndimage import zoom
import pickle 




quantization_matrix = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ])


def extract_msb(image_array, k):
    try:
        if k < 1 or k > 8:
            raise ValueError("k must be between 1 and 8")
        
        if len(image_array.shape) == 2:  # Grayscale image
            msb = image_array >> (8 - k)
            new_img = (msb / (2**k - 1)) * 255
            new_img = new_img.astype(np.uint8)
        elif len(image_array.shape) == 3:  # Color image
            msb = image_array >> (8 - k)
            new_img = (msb / (2**k - 1)) * 255
            new_img = new_img.astype(np.uint8)
        else:
            raise ValueError("Unsupported image format")
        return new_img
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def zigzag(input, percentage):

    if percentage <= 0 or percentage >= 100:
        raise ValueError("Percentage should be between 0 and 100 (exclusive)")

    total_elements = input.size
    num_elements_to_keep = int(total_elements * (percentage / 100))
    
    # Initialize variables
    h = 0  # horizontal index
    v = 0  # vertical index

    vmax = input.shape[0]  # maximum vertical index
    hmax = input.shape[1]  # maximum horizontal index

    i = 0  # index for output array

    output = np.zeros(num_elements_to_keep, dtype=input.dtype)  # output array
    
    # Zigzag traversal
    while ((v < vmax) and (h < hmax) and (i < num_elements_to_keep)):
        
        # Going up
        if ((h + v) % 2) == 0:
            if (v == 0):  # If at the first row
                output[i] = input[v, h]  # Store the current element
                if (h == hmax - 1):
                    v = v + 1
                else:
                    h = h + 1
                i = i + 1
            
            elif ((h == hmax - 1) and (v < vmax)):  # If at the last column
                output[i] = input[v, h]
                v = v + 1
                i = i + 1
            
            elif ((v > 0) and (h < hmax - 1)):  # All other cases
                output[i] = input[v, h]
                v = v - 1
                h = h + 1
                i = i + 1
        
        else:  # Going down
            if ((v == vmax - 1) and (h <= hmax - 1)):  # If at the last row
                output[i] = input[v, h]
                h = h + 1
                i = i + 1
            
            elif (h == 0):  # If at the first column
                output[i] = input[v, h]
                if (v == vmax - 1):
                    h = h + 1
                else:
                    v = v + 1
                i = i + 1
            
            elif ((v < vmax - 1) and (h > 0)):  # All other cases
                output[i] = input[v, h]
                v = v + 1
                h = h - 1
                i = i + 1
        
        if ((v == vmax - 1) and (h == hmax - 1)):  # Bottom-right element
            output[i] = input[v, h]
            break

    return output



def inverse_zigzag(zigzag_block, block_shape):
    block = np.zeros(block_shape, dtype=np.float32)
    h, v = 0, 0
    
    for i in range(len(zigzag_block)):
        if v >= block_shape[0] or h >= block_shape[1]:
            break  
        block[v, h] = zigzag_block[i]


        if (h + v) % 2 == 0:  # Going up
            if v == 0:
                if h == block_shape[1] - 1:
                    v += 1
                else:
                    h += 1
            elif h == block_shape[1] - 1:
                v += 1
            else:
                v -= 1
                h += 1
        else:  # Going down
            if h == 0:
                if v == block_shape[0] - 1:
                    h += 1
                else:
                    v += 1
            elif v == block_shape[0] - 1:
                h += 1
            else:
                v += 1
                h -= 1
    return block


def block_dct_zigzag_y_channel(image, block_size, zigzag_percentage,quantization_matrix=quantization_matrix):
    
    scale_factor = block_size / 8
    quantization_matrix_n_N = zoom(quantization_matrix, scale_factor, order=1)
    quantization_matrix_n_N = np.round(quantization_matrix_n_N).astype(int)

    # Convert image to YCrCb color space
    image_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

    # Extract Y channel
    y_channel = image_ycrcb[:, :, 0]

    # Image dimensions
    h, w = y_channel.shape[:2]
    num_blocks_h = h // block_size
    num_blocks_w = w // block_size

    # Initialize columns dictionary for Y channel
    columns_dict = {j: [] for j in range(num_blocks_w)}

    # Process Y channel
    for i in range(num_blocks_h):
        for j in range(num_blocks_w):
            # Extract the block
            block = y_channel[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size]

            # Apply DCT
            block_dct = cv2.dct(np.float32(block))

            # Quantize DCT coefficients
            block_dct_quantized = np.round(block_dct / quantization_matrix_n_N) * quantization_matrix_n_N

            # Perform zigzag traversal
            zigzag_block = zigzag(block_dct_quantized, zigzag_percentage)

            # Add to the respective column
            columns_dict[j].append(np.abs(zigzag_block))

    return columns_dict


def dct_zigzag_entire_channel(channel,percentage,quantization_matrix=quantization_matrix):
 
    h, w = channel.shape
    scale_factor_h = h / 8
    scale_factor_w = w / 8
    quantization_matrix = zoom(quantization_matrix, (scale_factor_h, scale_factor_w), order=1)
    quantization_matrix = np.round(quantization_matrix).astype(int)
    quantization_matrix[quantization_matrix == 0] = 1


    # Apply DCT on the entire channel
    channel_dct = cv2.dct(np.float32(channel))
    if np.any(np.isnan(channel_dct)) or np.any(np.isinf(channel_dct)):
        raise ValueError("channel_dct contains NaN or Inf values.")


    # Quantize DCT 
    channel_dct_quantized = np.round(channel_dct / quantization_matrix) * quantization_matrix
    zigzag_channel = zigzag(channel_dct_quantized, percentage)

    return zigzag_channel


def reconstruct_image_from_columns(columns_dict, block_size, original_shape):
    if not isinstance(columns_dict, dict):
        raise TypeError("Expected 'columns_dict' to be a dictionary.")

    num_blocks_h = original_shape[0] // block_size
    num_blocks_w = original_shape[1] // block_size

    reconstructed_image = np.zeros(original_shape, dtype=np.float32)

    for j in range(num_blocks_w):
        column_data = columns_dict.get(j, None)
        if not isinstance(column_data, list):
            continue 

        for i, zigzag_block in enumerate(column_data):
            if i >= num_blocks_h:
                break 
            
            # Precompute block positions
            row_start = i * block_size
            row_end = row_start + block_size
            col_start = j * block_size
            col_end = col_start + block_size
           

            # Reconstruct the block
            dct_block = inverse_zigzag(zigzag_block, (block_size, block_size))
            block = cv2.idct(dct_block.astype(np.float32))
           

            # Insert block into the image
            reconstructed_image[row_start:row_end, col_start:col_end] = block

    return reconstructed_image


def calculate_column_hashes(columns_dict):

    column_hashes = {}
    for j, column in columns_dict.items():
        # Serialize the column (list of numpy arrays) to bytes
        column_bytes = pickle.dumps(column)

        # Calculate the SHA-256 hash of the column bytes
        hash_object = hashlib.sha256(column_bytes)
        column_hash = hash_object.hexdigest()  # Get the hash as a hexadecimal string

        # Store the hash in the dictionary
        column_hashes[j] = column_hash

    return column_hashes


def encrypt_dct_zigzag_output(zigzag_output, key):

    # Initialize AES cipher in ECB mode
    cipher = AES.new(key, AES.MODE_ECB)

    # Serialize the zigzag_output (list of numpy arrays) to bytes
    zigzag_bytes = pickle.dumps(zigzag_output)

    # Pad the data to be a multiple of 16 bytes (AES block size)
    padded_data = pad(zigzag_bytes, AES.block_size)

    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)

    return encrypted_data

def decrypt_dct_zigzag_output(encrypted_output, key):

    # Initialize AES cipher in ECB mode
    cipher = AES.new(key, AES.MODE_ECB)

    # Decrypt the data
    decrypted_data = cipher.decrypt(encrypted_output)

    # Unpad the data
    unpadded_data = unpad(decrypted_data, AES.block_size)

    # Deserialize the bytes back to the original structure (list of numpy arrays)
    zigzag_output = pickle.loads(unpadded_data)

    return zigzag_output


def reconstruct_y_channel_image(columns_dict, block_size, original_shape):
    # Reconstruct Y channel
    restored_y_channel = reconstruct_image_from_columns(columns_dict, block_size, original_shape[:2])

    restored_y_channel = np.clip(restored_y_channel, 0, 255).astype(np.uint8)

    return restored_y_channel

def reconstruct_entire_channel(zigzag_channel, original_shape):
 
    # Inverse zigzag to get the quantized DCT coefficients
    dct_coeffs = inverse_zigzag(zigzag_channel, original_shape)

    # Apply inverse DCT
    channel = cv2.idct(dct_coeffs.astype(np.float32))

    # Clip values to valid range
    channel = np.clip(channel, 0, 255).astype(np.uint8)

    return channel


def normalize_column(column):
    
    min_val = np.min(column)
    max_val = np.max(column)
    return (column - min_val) / (max_val - min_val)


def calculate_column_hashes(columns_dict):
    column_hashes = {}
    for j, column in columns_dict.items():
        # Normalize the column
        normalized_column = normalize_column(column)
        
        # Serialize the normalized column
        column_bytes = pickle.dumps(normalized_column)

        # Calculate the SHA-256 hash of the column bytes
        hash_object = hashlib.sha256(column_bytes)
        column_hash = hash_object.hexdigest()  

        # Store the hash in the dictionary
        column_hashes[j] = column_hash

    return column_hashes


def calculate_column_hashes(columns_dict):

    column_hashes = {}
    for j, column in columns_dict.items():
        
        column_bytes = pickle.dumps(column)

        # Calculate the SHA-256 hash of the column bytes
        hash_object = hashlib.sha256(column_bytes)
        column_hash = hash_object.hexdigest()  

        # Store the hash in the dictionary
        column_hashes[j] = column_hash

    return column_hashes


def replace_columns(original_dict, new_columns_dict):
    for j, column in new_columns_dict.items():
        # Convert the key to an integer if necessary
        key = int(j) if isinstance(j, str) and j.isdigit() else j
        
        if key in original_dict:
            
            original_dict[key] = column
    
    return original_dict


def compare_hash_arrays(hash_array_1, hash_array_2):
    differences = []
    
    # Ensure both inputs are dictionaries
    if not isinstance(hash_array_1, dict) or not isinstance(hash_array_2, dict):
        raise ValueError("Both inputs must be dictionaries")

    # Compare the two hash arrays
    for j in hash_array_1:
        if j in hash_array_2:
            if hash_array_1[j] != hash_array_2[j]:
                differences.append(j)
        else:
            differences.append(j)
    
    
    for j in hash_array_2:
        if j not in hash_array_1:
            differences.append(j)
    
    return differences


def blur_other_columns(image, differences, block_size, blur_strength=400):
    
    block_size = int(block_size)
    
    # Ensure differences contains integers
    differences = [int(column) for column in differences]  
    
    # Create a blurred version of the original image
    
    kernel_size = (2 * blur_strength + 1, 2 * blur_strength + 1)  
    blurred_image = cv2.GaussianBlur(image, kernel_size, blur_strength)
    
    # Create a mask to retain the specified differing columns
    mask = np.zeros_like(image, dtype=np.uint8)
    for column in differences:
        start_x = column * block_size
        end_x = start_x + block_size
        mask[:, start_x:end_x] = 1  

    # Combine the original image and blurred image using the mask
    highlighted_image = np.where(mask, image, blurred_image)
    
    # Normalize the highlighted image to retain brightness
    highlighted_image_normalized = cv2.normalize(highlighted_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Encode the image for JSON response
    _, highlighted_image_encoded = cv2.imencode('.png', highlighted_image_normalized)
    highlighted_image_base64 = base64.b64encode(highlighted_image_encoded).decode('utf-8')
    
    return highlighted_image_base64


def generate_secret_key_from_file(file_obj, length):
    if length not in [16, 24, 32]:
        raise ValueError("Key length must be 16, 24, or 32 bytes.")

    
    file_content = file_obj.read().decode().strip()  

    # Check if it's hexadecimal or binary and convert it to bytes
    if all(c in '01' for c in file_content):  # Binary
        bit_data = int(file_content, 2)
    elif all(c in '0123456789abcdefABCDEF' for c in file_content):  
        bit_data = int(file_content, 16)
    else:
        raise ValueError("File content must be a valid binary or hexadecimal string.")

    # Extract the first `length * 8` bits
    total_bits = length * 8
    extracted_bits = (bit_data >> max(0, bit_data.bit_length() - total_bits)) & ((1 << total_bits) - 1)
    extracted_bytes = extracted_bits.to_bytes(length, byteorder='big')

    return extracted_bytes


def encode_bytes_in_dict(data):
    if isinstance(data, dict):
        return {key: encode_bytes_in_dict(value) for key, value in data.items()}
    elif isinstance(data, bytes):
        return base64.b64encode(data).decode('utf-8')  # Encode bytes to base64 string
    elif isinstance(data, (list, tuple)):
        return [encode_bytes_in_dict(item) for item in data]
    else:
        return data  # Return as-is if not bytes


def decode_bytes_in_dict(data):
    if isinstance(data, dict):
        return {key: decode_bytes_in_dict(value) for key, value in data.items()}
    elif isinstance(data, str):
        try:
            # Attempt to decode base64 strings back into bytes
            return base64.b64decode(data.encode('utf-8'))
        except:
            
            return data
    elif isinstance(data, (list, tuple)):
        return [decode_bytes_in_dict(item) for item in data]
    else:
        return data  



def encrypt_columns_dict(columns_dict, key):
 
    # Initialize AES cipher in ECB mode
    cipher = AES.new(key, AES.MODE_ECB)

    # Encrypt each column
    encrypted_columns_dict = {}
    for j, column in columns_dict.items():
        
        column_bytes = pickle.dumps(column)

        # Pad 
        padded_data = pad(column_bytes, AES.block_size)

        # Encrypt the data
        encrypted_data = cipher.encrypt(padded_data)

        # Store the encrypted data
        encrypted_columns_dict[j] = encrypted_data

    return encrypted_columns_dict


def decrypt_selected_columns(encrypted_columns_dict, key, columns_to_decrypt):
    cipher = AES.new(key, AES.MODE_ECB)

    # Decrypt only the selected columns
    decrypted_columns_dict = {}
    
   
    for j in columns_to_decrypt:
        # Convert the column index to a string to match the keys in encrypted_columns_dict
        column_key = str(j)
        
        if column_key in encrypted_columns_dict:
            # Decrypt the data
            decrypted_data = cipher.decrypt(encrypted_columns_dict[column_key])

            # Unpad the data
            unpadded_data = unpad(decrypted_data, AES.block_size)

            # Deserialize the data
            column = pickle.loads(unpadded_data)

            # Store the decrypted column
            decrypted_columns_dict[column_key] = column
      
    return decrypted_columns_dict


