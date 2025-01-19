# Image Authentication and Verification Platform

## Description

This platform provides a secure and efficient solution for image authentication and verification. It is built as a web application using **Django** for the backend and **React.js** for the frontend. The backend, powered by **Django REST Framework (DRF)**, manages image processing, encryption, and blockchain integration. React.js delivers a dynamic and user-friendly interface, while the platform ensures the integrity and security of images through advanced cryptographic techniques.

## Technologies

- **Backend**: Django, Django REST Framework (DRF)
- **Frontend**: React.js, React Router DOM, Axios
- **Image Processing**: Grayscale Conversion, MSB Extraction, Discrete Cosine Transform (DCT), Zigzag Reduction
- **Encryption**: AES Encryption
- **Blockchain**: Private Blockchain for tamper-proof storage and traceability

## Features

- **Image Authentication**: Secure image uploads and verification using advanced cryptographic techniques.
- **Image Integrity**: Detects and restores tampered images to their original authenticated state.
- **Efficient Storage**: Uses blockchain to securely store image hashes and encrypted data.
- **Scalable**: Designed to handle large datasets with high security and reliability.

## Workflow

1. **Authentication (Step 1)**: 
   1. Image Preprocessing:

      - Convert the image to the YCbCr color space.

      - Separate the Y (luminance), Cb (blue-difference), and Cr (red-difference) channels.

   2. Block-Based DCT on the Y Channel:

      - Divide the Y channel into smaller blocks (e.g., 8x8 or 16x16 pixels).

      - Apply DCT to each block individually.

      - Use the Zigzag algorithm to reduce the number of DCT coefficients 

   3. Global DCT on Cb and Cr Channels:

      - Apply DCT to the entire Cb and Cr channels (without dividing them into blocks).

      - Use the Zigzag algorithm to reduce the DCT coefficients for these channels.

      - Encryption of DCT Coefficients:

      - Encrypt the reduced DCT coefficients of the Y, Cb, and Cr channels using AES encryption.

   4. Hashing:

      - Hash the encrypted DCT coefficients' channel Y to create a unique identifier for the image.

   5. Blockchain Storage:
      - store the hash and the encrypted DCT coefficients in a private blockchain for tamper-proof storage.


2. **Verification (Step 2)**:
   1. Image Upload:

      -The client uploads an image for verification.

   2. Preprocessing:

      - Convert the uploaded image to YCbCr and separate the Y, Cb, and Cr channels.

   3. Block-Based DCT on the Y Channel:

      - Divide the Y channel into blocks and apply DCT to each block.

      - Reduce the coefficients using the Zigzag algorithm.

   4. Global DCT on Cb and Cr Channels:

      - Apply DCT to the entire Cb and Cr channels.

      - Reduce the coefficients using the Zigzag algorithm.

   5. Encryption of DCT Coefficients:

      - Encrypt the reduced DCT coefficients of the Y, Cb, and Cr channels using AES.

   6. Hashing:

     - Generate a hash from the encrypted DCT coefficients channel Y.

   7. Comparison:

      - Import the original image’s hash from the blockchain.

      - Compare the generated hash with the original hash.

      - Identify discrepancies (if any).

   8. Tampering Detection and Restoration:

      - If discrepancies are found:

      - Identify the specific columns (or blocks) in the Y  channels that have been tampered with.

      - Decrypt the corresponding DCT coefficients from the blockchain.

      - Replace the tampered columns in the uploaded image with the original data.

      - Restore the image to its original state.
## Requirements

- Python 3.x
- Node.js
- npm or yarn
- Pipenv (for backend)
- Blockchain setup (refer to the platform documentation for setup)

## Installation

### Backend 

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository

2. Navigate to the backend folder:
   ```bash

    cd backend

3. Install Pipenv if you haven't already:
   ```bash
    pip install pipenv

4. Install the backend dependencies:
   ```bash
    pipenv install

5. Activate the virtual environment:
   ```bash

    pipenv shell

6. Run the Django development server:
   ```bash
    python manage.py runserver


### Frontend 

1. Navigate to the frontend folder in another terminal:
    ```bash
    cd frontend

2. Install the frontend dependencies:
    ```bash
    npm install

3. Run the React development server:
    ```bash
    npm run dev
