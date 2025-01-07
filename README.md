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
   - Uploaded images are processed by converting them to grayscale.
   - The **Most Significant Bit (MSB)** is extracted and the image is divided into blocks.
   - Each block undergoes **Discrete Cosine Transform (DCT)**, and a percentage of coefficients are removed using the **Zigzag algorithm** for data reduction.
   - The processed blocks are hashed to create a unique identifier.
   - This hash and the encrypted DCT coefficients are stored in a **private blockchain**, ensuring tamper-proof storage.

2. **Verification (Step 2)**:
   - The client uploads an image for verification.
   - The same processing steps are applied to the uploaded image to generate its hash.
   - The generated hash is compared with the original image’s hash stored in the blockchain.
   - Discrepancies are identified, and the columns with differences are decrypted using **AES** and restored to their original state, ensuring the integrity of the image.

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
