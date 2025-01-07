import cv2
import numpy as np
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from scipy.ndimage import zoom
import json


def extract_msb(image_array, k):
    try:
        if len(image_array.shape) == 2:  # Grayscale image
            msb = image_array >> (8 - k)
            new_img = msb
        elif len(image_array.shape) == 3:  # RGB image
            # Vectorized operation for RGB channels
            new_img = image_array >> (8 - k)
        else:
            raise ValueError("Unsupported image format")
        return new_img
    except Exception as e:
        raise ValueError(f"Error in extracting MSB: {str(e)}")


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


def inverse_zigzag(input_1d, shape):
    vmax, hmax = shape

    h = 0  # horizontal index
    v = 0  # vertical index
    i = 0  # index for input_1d array

    output = np.zeros((vmax, hmax), dtype=input_1d.dtype)  # output matrix

    while ((v < vmax) and (h < hmax) and (i < len(input_1d))):
        
        # Going up
        if ((h + v) % 2) == 0:
            if (v == 0):  # If at the first row
                output[v, h] = input_1d[i]  # Store the current element
                if (h == hmax - 1):
                    v = v + 1
                else:
                    h = h + 1
                i = i + 1
            
            elif ((h == hmax - 1) and (v < vmax)):  # If at the last column
                output[v, h] = input_1d[i]
                v = v + 1
                i = i + 1
            
            elif ((v > 0) and (h < hmax - 1)):  # All other cases
                output[v, h] = input_1d[i]
                v = v - 1
                h = h + 1
                i = i + 1
        
        else:  # Going down
            if ((v == vmax - 1) and (h <= hmax - 1)):  # If at the last row
                output[v, h] = input_1d[i]
                h = h + 1
                i = i + 1
            
            elif (h == 0):  # If at the first column
                output[v, h] = input_1d[i]
                if (v == vmax - 1):
                    h = h + 1
                else:
                    v = v + 1
                i = i + 1
            
            elif ((v < vmax - 1) and (h > 0)):  # All other cases
                output[v, h] = input_1d[i]
                v = v + 1
                h = h - 1
                i = i + 1
        
        if ((v == vmax - 1) and (h == hmax - 1)):  # Bottom-right element
            output[v, h] = input_1d[i]
            break

    return output


def block_dct_zigzag(image, block_size, zigzag_percentage):

    # Define the quantization matrix 
    base_matrix = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ])
    scale_factor = block_size / 8
    quantization_matrix_n_N = zoom(base_matrix, scale_factor, order=1)
    quantization_matrix_n_N = np.round(quantization_matrix_n_N).astype(int)

    # Image dimensions
    h, w = image.shape[:2]
    num_blocks_h = h // block_size
    num_blocks_w = w // block_size

    # Initialize columns dictionary
    columns_dict = {j: [] for j in range(num_blocks_w)}

    # Process each block
    for i in range(num_blocks_h):
        for j in range(num_blocks_w):
            # Extract the block
            block = image[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size]

            # Apply DCT
            block_dct = cv2.dct(np.float32(block))

            # Quantize DCT coefficients
            block_dct_quantized = np.round(block_dct / quantization_matrix_n_N) * quantization_matrix_n_N

            # Perform zigzag traversal
            zigzag_block = zigzag(block_dct_quantized, zigzag_percentage)

            # Add to the respective column
            columns_dict[j].append(np.abs(zigzag_block))

    return columns_dict


def reconstruct_image_from_columns(columns_dict, block_size, original_shape):
    if not isinstance(columns_dict, dict):
        raise TypeError("Expected 'columns_dict' to be a dictionary.")

    num_blocks_h = original_shape[0] // block_size
    num_blocks_w = original_shape[1] // block_size

    reconstructed_image = np.zeros(original_shape, dtype=np.float32)

    for j in range(num_blocks_w):
        column_data = columns_dict.get(j, None)
        if not isinstance(column_data, list):
            continue  # Skip missing or invalid columns

        for i, zigzag_block in enumerate(column_data):
            if i >= num_blocks_h:
                break  # Avoid processing extra rows in the column
            
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

def hash_dictionary_elements_sha256(input_dict):

    hashed_dict = {}
    
    for key, value in input_dict.items():
        # Ensure the value is a string before hashing
        value_str = str(value)
        hash_obj = hashlib.sha256()
        hash_obj.update(value_str.encode('utf-8'))
        hashed_value = hash_obj.hexdigest()
        hashed_dict[key] = hashed_value
    
    return hashed_dict

def encrypt_array(array, key):
    # Convert the array to bytes
    byte_data = array.tobytes()
    
    # Encrypt
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(byte_data, AES.block_size))
    
    # Encode for transport (single encode operation)
    ciphertext_encoded = base64.b64encode(ciphertext).decode('utf-8')
    dtype_encoded = base64.b64encode(str(array.dtype).encode()).decode('utf-8')
    shape_encoded = base64.b64encode(json.dumps(array.shape).encode()).decode('utf-8')
    iv_encoded = base64.b64encode(cipher.iv).decode('utf-8')  # Include IV
    
    return {
        'ciphertext': ciphertext_encoded,
        'dtype': dtype_encoded,
        'shape': shape_encoded,
        'iv': iv_encoded
    }

def encrypt_dict(data, key):
    return {
        k: [
            encrypt_array(array, key)
            for array in arrays
        ]
        for k, arrays in data.items()
    }

def decrypt_array(encrypted_data, key):
    # Assuming encrypted_data is a dictionary
    if isinstance(encrypted_data, list):
        # If it's a list, process each item in the list (assuming each item is a dictionary)
        decrypted_arrays = []
        for item in encrypted_data:
            ciphertext = base64.b64decode(item['ciphertext'])
            dtype = base64.b64decode(item['dtype']).decode()
            shape = json.loads(base64.b64decode(item['shape']).decode())
            iv = base64.b64decode(item['iv'])

            # Decrypt
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

            # Convert back to numpy array
            array = np.frombuffer(decrypted_data, dtype=dtype).reshape(shape)
            decrypted_arrays.append(array)
        
        return decrypted_arrays  # Return the list of decrypted arrays
    else:
        # If it's a single dictionary, proceed as before
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        dtype = base64.b64decode(encrypted_data['dtype']).decode()
        shape = json.loads(base64.b64decode(encrypted_data['shape']).decode())
        iv = base64.b64decode(encrypted_data['iv'])

        # Decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

        # Convert back to numpy array
        array = np.frombuffer(decrypted_data, dtype=dtype).reshape(shape)
        
        return array

def decrypt_dict(encrypted_data_dict, key, indices_to_decrypt):
    decrypted_dict = {}
    
    keys = list(encrypted_data_dict.keys())
        
    for index in indices_to_decrypt:
        # Check if the index is valid
        if isinstance(index, int) and 0 <= index < len(keys):
            key_at_index = keys[index]
            # Call decrypt_array on the encrypted data corresponding to this key
            decrypted_dict[key_at_index] = decrypt_array(encrypted_data_dict[key_at_index], key)
        else:
            return "Index out of range"

    return decrypted_dict

def compare_dicts(dict1, dict2):
    differing_keys = []
    for key in dict1:
        if key in dict2:
            if str(dict2[key]) != str(dict1[key]) :
                differing_keys.append(key)
    return differing_keys

def replace_values(dict1, dict2):

    keys1 = list(dict2.keys())
   
    for key in keys1:
        
        
        dict1[key] = dict2[key]
    return dict1

def blur_other_columns(image, differences, block_size, blur_strength=400):

    # Create a blurred version of the original image
    # Adjust the kernel size and sigma based on blur_strength
    kernel_size = (2 * blur_strength + 1, 2 * blur_strength + 1)  # Ensure kernel size is odd
    blurred_image = cv2.GaussianBlur(image, kernel_size, blur_strength)
    
    # Create a mask to retain the specified differing columns
    mask = np.zeros_like(image, dtype=np.uint8)
    for column in differences:
        start_x = column * block_size
        end_x = start_x + block_size
        mask[:, start_x:end_x] = 1  # Mark the differing columns

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
        raise ValueError("Key length must be 16, 24, or 32 bytes (corresponding to AES-128, AES-192, or AES-256).")

    # Read the file content directly from the file-like object
    file_content = file_obj.read().decode().strip()  # Read the content and decode it

    # Check if it's hexadecimal or binary and convert it to bytes
    if all(c in '01' for c in file_content):  # Binary
        bit_data = int(file_content, 2)
    elif all(c in '0123456789abcdefABCDEF' for c in file_content):  # Hexadecimal
        bit_data = int(file_content, 16)
    else:
        raise ValueError("File content must be a valid binary or hexadecimal string.")

    # Extract the first `length * 8` bits
    total_bits = length * 8
    extracted_bits = (bit_data >> max(0, bit_data.bit_length() - total_bits)) & ((1 << total_bits) - 1)
    extracted_bytes = extracted_bits.to_bytes(length, byteorder='big')

    return extracted_bytes






