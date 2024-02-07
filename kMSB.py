from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

def extract_msb(image_path, k):
    # Open the image
    img = Image.open(image_path)

    # Get image size
    width, height = img.size

    # Extract MSB for each pixel and create a new image
    new_img = Image.new("RGB", (width, height))
    
    # Matrix to store MSB values for each pixel
    msb_matrix = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            # Get RGB values of the pixel
            pixel_value = img.getpixel((x, y))
            
            
            # Extract k most significant bits for each color channel (R, G, B)

            msb_r = int(bin(pixel_value[0])[2:].zfill(8)[:k], 2)  # Extract k MSB for Red
            msb_g = int(bin(pixel_value[1])[2:].zfill(8)[:k], 2)  # Extract k MSB for Green
            msb_b = int(bin(pixel_value[2])[2:].zfill(8)[:k], 2)  # Extract k MSB for Blue

            # Store MSB values in the matrix
            msb_matrix[y, x] = (msb_r, msb_g, msb_b)

            # Create a grayscale color based on the extracted MSBs
            new_pixel_value = (msb_r, msb_g, msb_b)
            
            # Set the new pixel value in the new image
            new_img.putpixel((x, y), new_pixel_value)

    # Save the new image
    new_img_path = f"new_image_with_msb_{k}.jpg"
    new_img.save(new_img_path)

    return new_img_path, msb_matrix

# Create a Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Prompt user to select an image file
image_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.jpg; *.jpeg; *.png; *.bmp; *.gif")])

if image_path:
    # Prompt user for number of bits
    k = int(input("Enter the number of most significant bits to extract (1-8): "))

    # Call the function to extract MSB and save the new image
    result_image_path, msb_matrix = extract_msb(image_path, k)
    print(f"New image with {k} most significant bits extracted saved at: {result_image_path}")

    # Display the MSB matrix
    print("MSB Matrix:")
    print(msb_matrix)

    # Display the resulting image
    result_img = Image.open(result_image_path)
    plt.imshow(result_img)
    plt.axis('off')
    plt.show()
else:
    print("No image selected.")
