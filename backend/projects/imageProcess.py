
import cv2
import numpy as np
from projects.imageProcess import *
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



def change_quotes_to_double(dictionary):
    new_dict = {}
    for key, value in dictionary.items():
        new_key = key.replace("'", "\"") if isinstance(key, str) else key
        new_value = value.replace("'", "\"") if isinstance(value, str) else value
        new_dict[new_key] = new_value
    return new_dict

def dct2(block):
    return cv2.dct(block.astype(np.float32))

def idct2(block):
    return cv2.idct(block)

def zigzag_keep_percentage_matrix(matrix, percentage):
    if percentage <= 0 or percentage >= 100:
        raise ValueError("Percentage should be between 0 and 100 (exclusive)")

    num_elements_to_keep = int(len(matrix) * len(matrix[0]) * (percentage / 100))
    result = np.zeros_like(matrix)

    direction = 1  # Start from the top-left corner
    row, col = 0, 0
    count = 0
    for _ in range(num_elements_to_keep):
        result[row][col] = matrix[row][col]
        count += 1
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

def process_image_blocks(image, block_size=8, percentage=50):
    h, w = image.shape
    dct_image = np.zeros((h, w), np.float32)
    dct_columns = {}  # Dictionary to store DCT coefficients

    for j in range(0, w, block_size):
        column_blocks = []
        for i in range(0, h, block_size):
            block = image[i : i + block_size, j : j + block_size]
            dct_block = dct2(block)
            kept_dct_block = zigzag_keep_percentage_matrix(dct_block, percentage)
            dct_image[i : i + block_size, j : j + block_size] = kept_dct_block
            column_blocks.append(kept_dct_block)

        dct_column = np.vstack(column_blocks)
        dct_columns[j // block_size] = dct_column

    return dct_image, dct_columns

def reconstruct_image_from_dct_columns(dct_columns, h, w, block_size=8):
    reconstructed_image = np.zeros((h, w), np.float32)
    for j in range(0, w, block_size):
        dct_column = dct_columns[j // block_size]
        for i in range(0, h, block_size):
            dct_block = dct_column[i : i + block_size, :]
            idct_block = idct2(dct_block)
            reconstructed_image[i : i + block_size, j : j + block_size] = idct_block
    return reconstructed_image



def hash_columns_dict(columns_dict):
    hashed_columns_dict = {}
    for key, matrix in columns_dict.items():
        matrix_bytes = matrix.tobytes()
        sha256 = hashlib.sha256()
        sha256.update(matrix_bytes)
        hashed_columns_dict[key] = sha256.hexdigest()
    return hashed_columns_dict


def encrypt_column(column_data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(column_data.tobytes(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    # Return base64 encoded string of encrypted data
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_column(encrypted_data, key, original_shape):
    # Decode base64 string to bytes
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_padded_data = cipher.decrypt(encrypted_data_bytes)
    decrypted_data = unpad(decrypted_padded_data, AES.block_size)
    decrypted_array = np.frombuffer(decrypted_data, dtype=np.float32).reshape(original_shape)
    return decrypted_array

def encrypt_dct_columns(dct_columns, key):
    encrypted_columns = {}
    for col_index, column_data in dct_columns.items():
        encrypted_columns[col_index] = encrypt_column(column_data, key)
    return encrypted_columns

def decrypt_dct_columns(encrypted_columns, key, original_shapes):
    decrypted_columns = {}
    for col_index, encrypted_data in encrypted_columns.items():
        decrypted_columns[col_index] = decrypt_column(encrypted_data, key, original_shapes[col_index])
    return decrypted_columns

def decrypt_dct_columns2(encrypted_columns, key, original_shapes, columns_to_decrypt):
    decrypted_columns = {}
    for col_index in columns_to_decrypt:
        encrypted_data = encrypted_columns.get(col_index)
        if encrypted_data is not None:
            decrypted_columns[col_index] = decrypt_column(encrypted_data, key, original_shapes[col_index])
    return decrypted_columns



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