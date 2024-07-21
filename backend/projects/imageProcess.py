
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib



def extract_msb(image_array, k):
    try:
        if len(image_array.shape) == 2:  # Grayscale image
            msb = image_array >> (8 - k)
            new_img = msb
        elif len(image_array.shape) == 3:  # RGB image
            new_img = np.zeros_like(image_array)
            for i in range(3):  # Loop through RGB channels
                # Extract k most significant bits
                msb = image_array[:, :, i] >> (8 - k)
                # Add the MSB to the new image
                new_img[:, :, i] = msb
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

def block_dct_zigzag(image, block_size, zigzag_percentage):
    h, w = image.shape[:2]
    num_blocks_h = h // block_size
    num_blocks_w = w // block_size
    
    columns_dict = {j: [] for j in range(num_blocks_w)}
    
    for i in range(num_blocks_h):
        for j in range(num_blocks_w):
            block = image[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size]
            dct_block = cv2.dct(block.astype(np.float32))
            zigzag_block = zigzag(dct_block, zigzag_percentage)
            columns_dict[j].append(zigzag_block)
    
    return columns_dict




import numpy as np
import cv2



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


def format_dict_without_quotes(input_dict):
    formatted_pairs = []
    for key, value in input_dict.items():
        # Remove surrounding quotes from string values
        if isinstance(value, str):
            value = value.strip('"\'')

        # Format key-value pair
        formatted_pairs.append(f"{key}: {value}")

    # Join formatted pairs with commas and enclose in curly braces
    formatted_output = "{" + ", ".join(formatted_pairs) + "}"
    return formatted_output

import numpy as np
import cv2


def reconstruct_image_from_columns(columns_dict, block_size, original_shape):
    if not isinstance(columns_dict, dict):
        raise TypeError("Expected 'columns_dict' to be a dictionary.")
    
    num_blocks_h = original_shape[0] // block_size
    num_blocks_w = original_shape[1] // block_size
    
    reconstructed_image = np.zeros(original_shape, dtype=np.float32)
    
    for j in range(num_blocks_w):
        if j in columns_dict and isinstance(columns_dict[j], list):
            for i in range(num_blocks_h):
                if len(columns_dict[j]) > i:
                    zigzag_block = columns_dict[j][i]
                    
                    # Inverse zigzag to get block
                    zigzag_shape = (block_size, block_size)
                    dct_block = inverse_zigzag(zigzag_block, zigzag_shape)
                    
                    # Apply inverse DCT
                    block = cv2.idct(dct_block.astype(np.float32))
                    
                    # Place block in reconstructed image
                    reconstructed_image[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size] = block
                else:
                    print(f"Missing block at position ({i}, {j})")
        else:
            print(f"Missing or invalid data for column {j}")

    return reconstructed_image






import hashlib






def hashed_columns_dict(input_dict):
    hashed_dict = {}
    
    for key, value_list in input_dict.items():
        concatenated_str = ""
        for arr in value_list:
            for element in arr:
                element_str = str(element)
                concatenated_str += element_str
        
        # Compute SHA-256 hash of concatenated_str
        hash_value = hashlib.sha256(concatenated_str.encode()).hexdigest()
        
        # Store hash_value in hashed_dict
        hashed_dict[key] = hash_value
    
    return hashed_dict
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def encrypt_dictionary(dictionary, key):
    encrypted_dict = {}

    for k, v in dictionary.items():
        iv = os.urandom(16)  # Initialization vector
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        padder = padding.PKCS7(128).padder()
        data = str(v).encode('utf-8')  # Convert to bytes
        padded_data = padder.update(data) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Store the encrypted data and IV
        encrypted_dict[k] = (iv, encrypted_data)
    
    return encrypted_dict





from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import numpy as np


def decrypt_dictionary(encrypted_dict, key, indices):
    decrypted_dict = {}
    
    if indices is not None:
        # Convert indices to a set for faster lookup
        indices_set = set(indices)
    else:
        # If no indices are provided, decrypt all elements
        indices_set = set(range(len(encrypted_dict)))
    
    for i, (k, (iv, encrypted_data)) in enumerate(encrypted_dict.items()):
        if i in indices_set:
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
            
            unpadder = padding.PKCS7(128).unpadder()
            unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
            
            decrypted_dict[k] = unpadded_data.decode('utf-8')
    
    return decrypted_dict





def compare_dicts(dict1, dict2):
    differing_keys = []
    for key in dict1:
        if key in dict2:
            if str(dict2[key]) != str(dict1[key]) :
                differing_keys.append(key)


    for key in dict2:
        if key not in dict1:
            if str(dict2[key]) != str(dict1[key]) :
                differing_keys.append(key)
    
    return differing_keys




def replace_values(dict1, dict2):
    for key in dict2:
        if key in dict1:
            dict1[key] = dict2[key]
    return dict1



