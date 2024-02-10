
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import cv2
import os



from kMSB import extract_msb
from DCT import  compress_image

root = tk.Tk()
root.withdraw()  # Hide the main window

# Prompt user to select an image file
image_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.jpg; *.jpeg; *.png; *.bmp; *.gif")])

if image_path:
   
    # Prompt user for number of bits
    k = int(input("Enter the number of most significant bits to extract (1-8): "))
 
    # Call the function to extract MSB and save the new image
    result_image_path, msb_matrix = extract_msb(image_path, k)
    print(f"New image compresed {k} most significant bits extracted saved at: {result_image_path}")
    
    block_size = 8
    compressed_image = compress_image(result_image_path, block_size)

     # Create the output folder if it doesn't exist
    os.makedirs("compressed-images", exist_ok=True)
    
    # Get the filename and extension
    filename, ext = os.path.splitext(os.path.basename(image_path))
    
    # Save the compressed image to the output folder
    output_path = os.path.join("compressed-images", filename + "_compressed" + ext)

    cv2.imwrite(output_path, compressed_image)
    

   

    # Display the resulting image
    # result_img = Image.open(result_image_path)
    # plt.imshow(result_img)
    # plt.axis('off')
    # plt.show()
else:
    print("No image selected.")



  # Adjust block size as needed



