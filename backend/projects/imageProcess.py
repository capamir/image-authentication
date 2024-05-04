import cv2
import numpy as np
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import numpy as np
from Crypto.Util.Padding import pad
import numpy as np
import base64
import secrets
from Crypto.Util.Padding import unpad
import struct
from projects.models import *



import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import matplotlib.pyplot as plt


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


def divide_array_into_columns_with_dct(arr, block_size):

    # Ensure array data type is float32 or float64
    if arr.dtype != np.float32 and arr.dtype != np.float64:
        arr = arr.astype(np.float32)  # Convert to float32 if not already
        # You can also use np.float64 if needed

    # Divide the array into columns
    columns = [arr[:, i:i+block_size[1]] for i in range(0, arr.shape[1], block_size[1])]

    # Create a dictionary to store DCT-transformed blocks
    dct_blocks_dict = {}

    # Apply DCT on each block and save the transformed blocks as elements of the dictionary
    for i, column in enumerate(columns):
        dct_blocks = []
        for block in column:
            # Apply 2D DCT using cv2
            dct_block = cv2.dct(cv2.dct(block.T).T)
            dct_blocks.append(dct_block)
        dct_blocks_dict[i] = zigzag_keep_percentage_matrix(combine_arrays_to_matrix(dct_blocks), 10)

    return dct_blocks_dict




def divide_array_into_columns(arr, block_size):
    # Ensure array data type is float32 or float64
    if arr.dtype != np.float32 and arr.dtype != np.float64:
        arr = arr.astype(np.float32)  # Convert to float32 if not already
        # You can also use np.float64 if needed

    # Divide the array into columns
    columns = [arr[:, i:i+block_size[1]] for i in range(0, arr.shape[1], block_size[1])]

    # Combine the columns into a dictionary
    columns_dict = {}
    for i, column in enumerate(columns):
        columns_dict[i] = combine_arrays_to_matrix(column)

    return columns_dict



def zigzag_keep_percentage_matrix(matrix, percentage):
    if percentage <= 0 or percentage >= 100:
        raise ValueError("Percentage should be between 0 and 100 (exclusive)")

    num_elements_to_keep = int(len(matrix) * len(matrix[0]) * (percentage / 100))
    result = []

    # Zigzag pattern iteration
    direction = 1  # Start from the top-left corner
    row, col = 0, 0
    for _ in range(num_elements_to_keep):
        result.append(matrix[row][col])
        if direction == 1:  # Moving upward
            if col == len(matrix[0]) - 1:  # If at the rightmost column
                row += 1  # Move to the next row
                direction = -1  # Change direction to move downward
            elif row == 0:  # If at the top row
                col += 1  # Move to the next column
                direction = -1  # Change direction to move downward
            else:
                row -= 1  # Move upward diagonally
                col += 1
        else:  # Moving downward
            if row == len(matrix) - 1:  # If at the bottom row
                col += 1  # Move to the next column
                direction = 1  # Change direction to move upward
            elif col == 0:  # If at the leftmost column
                row += 1  # Move to the next row
                direction = 1  # Change direction to move upward
            else:
                row += 1  # Move downward diagonally
                col -= 1

    return result



def combine_arrays_to_matrix(arrays):
    # Combine arrays into a single matrix
    matrix = np.concatenate(arrays, axis=0)
    return matrix

def hash_dictionary(original_dict):
    hashed_dict = {}
    for key, value in original_dict.items():
        concatenated_string = ''.join(map(str, value))
        hashed_value = hashlib.sha256(concatenated_string.encode()).hexdigest()
        hashed_dict[key] = hashed_value
    return hashed_dict


def encrypt_dict(data_dict, key):
    # Check if the key is already in bytes format
    if isinstance(key, str):
        # Convert the key to bytes and ensure it's 16 bytes long
        key_bytes = key.encode('utf-8')
        if len(key_bytes) < 16:
            key_bytes = key_bytes.ljust(16, b'\0')
        elif len(key_bytes) > 16:
            key_bytes = key_bytes[:16]
    elif isinstance(key, bytes):
        # Ensure the key is 16 bytes long
        if len(key) != 16:
            raise ValueError("Key length must be 16 bytes (AES-128)")
        key_bytes = key
    else:
        raise ValueError("Key must be either a string or bytes")

    encrypted_dict = {}

    # Iterate over each key-value pair in the dictionary
    for k, v in data_dict.items():
        # Convert the numpy array to bytes
        v_bytes = v.tobytes()
        # Pad the data to be a multiple of 16 bytes (AES block size)
        padded_data = pad(v_bytes, AES.block_size)
        # Create an AES cipher object
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        # Encrypt the padded data
        encrypted_data = cipher.encrypt(padded_data)
        # Store the encrypted data in the encrypted dictionary
        encrypted_dict[k] = base64.b64encode(encrypted_data).decode('utf-8')

    return encrypted_dict


def generate_secret_key(length):

    if length not in [16, 24, 32]:
        raise ValueError("Key length must be 16, 24, or 32 bytes (corresponding to AES-128, AES-192, or AES-256)")

    return secrets.token_bytes(length)


def replace_columns(dic1,dic2):

    dict_keys = list(dic2.keys())  # Convert dictionary keys to a list

    for index in dict_keys:
        dic1[index] =dic2[index]

    return dic1


def compare_dictionaries(dict1, dict2):
    if not isinstance(dict1, dict):
        dict1 = eval(dict1)
    if not isinstance(dict2, dict):
        dict2 = eval(dict2)
    
    differing_keys = []
    for key in dict1.keys():
        if key in dict2:
            if dict1[key] != dict2[key]:
                differing_keys.append(key)
        else:
            differing_keys.append(key)
    
    for key in dict2.keys():
        if key not in dict1:
            differing_keys.append(key)
    
    return differing_keys




key = b'_^4\x887ja\xb0\xdd\x97"\xc2\x82\xcb\x0fc'  # Replace with your secret key



def get_dictionary_elements(my_dict, keyy):
    encrypted_dict = {}
    for key, value in my_dict.items():
        encrypted_dict[key] = encrypt_array(value, keyy)
    return {str(k): base64.b64encode(v).decode('utf-8') for k, v in encrypted_dict.items()}  # Encode to base64

def get_dictionary_element2(my_dict, indices, keyy):
    decrypted_elements = {}
    dict_keys = list(my_dict.keys())  # Convert dictionary keys to a list
    
    for index in indices:
        if index < 0 or index >= len(dict_keys):
            raise IndexError("Index out of range")
        
        key = dict_keys[index]
        value = my_dict[key]
        
        # Decode from base64 and decrypt using the provided key
        decrypted_value = decrypt_output(base64.b64decode(value.encode('utf-8')), keyy)
        
        decrypted_elements[key] = decrypted_value
    
    return decrypted_elements

def decrypt_output(encrypted_output, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(encrypted_output)
    decrypted_data = unpad(decrypted_data, AES.block_size)
    array = []
    num_floats = len(decrypted_data) // 4
    for i in range(num_floats):
        float_bytes = decrypted_data[i * 4: (i + 1) * 4]
        num = struct.unpack('f', float_bytes)[0]
        array.append(num)
    return array

def encrypt_array(array, key):
    byte_array = b''.join(struct.pack('f', float(num)) for num in array)
    byte_array = pad(byte_array, AES.block_size)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(byte_array)
    return encrypted_data


def decrypt_output(encrypted_output, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(encrypted_output)
    decrypted_data = unpad(decrypted_data, AES.block_size)
    array = []
    num_floats = len(decrypted_data) // 4
    for i in range(num_floats):
        float_bytes = decrypted_data[i * 4: (i + 1) * 4]
        num = struct.unpack('f', float_bytes)[0]
        array.append(num)
    return array