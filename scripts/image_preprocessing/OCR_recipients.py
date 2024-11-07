import os
import random
import cv2
import numpy as np
from PIL import Image
import tempfile
import matplotlib.pyplot as plt

# import SkewCorrection module to use static method correct_skew() from file skew_correction.py
from skew_correction import SkewCorrection

# Define path to the directory containing images
images_path = '../../raw_data/images'

# define path to save the processed images
processed_images_path = '../../updates/images'

# Get a list of all image files in the directory
all_images = [img for img in os.listdir(images_path) if img.endswith('.png') or img.endswith('.jpg')]

# Select a random image
image_name = random.choice(all_images)
img_path = os.path.join(images_path, image_name)

# Load the random image
img = cv2.imread(img_path)

def process_image(img, threshhold_offset, gaussian_blur=False, save_skew=False):
    # Rescale the image, if needed.
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    orig_img = img.copy()



    # Converting to gray scale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Removing Shadows
    rgb_planes = cv2.split(img)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)
    img = cv2.merge(result_planes)

    #Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)#increases the white region in the image 
    img = cv2.erode(img, kernel, iterations=1) #erodes away the boundaries of foreground object


    #Apply blur to smooth out the edges
    if gaussian_blur:
        img = cv2.GaussianBlur(img, (5, 5), 0)

    # Apply threshold to get image with only b&w (binarization)
    # Apply a custom threshold for black-and-white conversion
    # custom_threshold = 100  # Adjust this value as needed (range: 0 to 255)
    # _, img = cv2.threshold(img, custom_threshold, 255, cv2.THRESH_BINARY)
    # img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


    # Calculate Otsu's threshold and subtract an offset
    otsu_threshold, _ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    adjusted_threshold = max(otsu_threshold + threshhold_offset, 0) 
    _, img = cv2.threshold(img, adjusted_threshold, 255, cv2.THRESH_BINARY)

    # correct skew
    show_image("Skewed Image", img)
    original_img = img
    angle, img = SkewCorrection.nathan_skew_correction(img, orig_img)
    print(f"Angle of rotation: {angle}")
    show_image("Unskewed Image", img)

    # Save the skew corrected image
    if save_skew:
        # save the skew corrected image
        cv2.imwrite(f'{processed_images_path}/skew_corrected_{image_name}', img)
        # save the original image
        cv2.imwrite(f'{processed_images_path}/original_{image_name}', original_img)

    return img

# Function to display the image
def show_image(title, image, save=False):
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

def show_original_image(image, save=False):
    plt.imshow(image, cmap='gray')
    plt.title("Original Image")
    plt.axis('off')
    plt.show()
    if save:
        plt.savefig(f'{processed_images_path}/original_{image_name}.png')
    return image

def show_multiple_offsets(img, offsets, gaussian_blur=False, save=False):
    # Display 3x3 grid of images
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    if gaussian_blur:
        fig.suptitle("Processed Images with Different Threshold Offsets and Gaussian Blur", fontsize=16)
    else:
        fig.suptitle("Processed Images with Different Threshold Offsets", fontsize=16)

    # Iterate over the offsets and plot each processed image
    for i, offset in enumerate(offsets):
        # Process the image with the current offset
        processed_img = process_image(img, offset, gaussian_blur)
        
        # Determine row and column in the 2x2 grid
        row, col = divmod(i, 2)
        ax = axes[row, col]
        ax.imshow(processed_img, cmap='gray')
        ax.set_title(f"Offset: {offset}")
        ax.axis('off')

    # Hide any unused subplots 
    for j in range(i + 1, 4):
        row, col = divmod(j, 2)
        axes[row, col].axis('off')

    # Adjust space between images
    plt.subplots_adjust(hspace=0.05, wspace=0.05)
    plt.show()
    # convert offsets to string
    offsets = [str(offset) for offset in offsets]
    if save:
        if gaussian_blur:
            plt.savefig(f'{processed_images_path}/processed_{image_name}_{offsets}_gaussian.png')
        else:
            plt.savefig(f'{processed_images_path}/processed_{image_name}_{offsets}.png')

# def show_multiple_offsets(img, offsets): # Threshold offsets to use
#     # Display 3x3 grid of images
#     fig, axes = plt.subplots(3, 3, figsize=(12, 12))
#     fig.suptitle("Processed Images with Different Threshold Offsets", fontsize=16)
# 
#     # Iterate over the offsets and plot each processed image
#     for i, offset in enumerate(offsets):
#         # Process the image with the current offset
#         processed_img = process_image(img, offset)
#         
#         # Determine row and column in the 3x3 grid
#         row, col = divmod(i, 3)
#         ax = axes[row, col]
#         ax.imshow(processed_img, cmap='gray')
#         ax.set_title(f"Offset: {offset}")
#         ax.axis('off')
# 
#     # Hide any unused subplots (since we only have 8 offsets)
#     for j in range(i + 1, 9):
#         row, col = divmod(j, 3)
#         axes[row, col].axis('off')
# 
#     plt.tight_layout()
#     plt.show()


# img = process_image(img)
# show_image("Processed Image", img)

img = process_image(img, 15, False, True)




## TO GENERATE IMAGES FOR REPORT COMPARING OFFSETS AND GAUSSIAN BLUR
# offsets = [40, 20, 0, -20]
# show_multiple_offsets(img, offsets, False, False)
# show_multiple_offsets(img, offsets, True, False)
# 
# offsets = [30, 23, 16, 11]
# show_multiple_offsets(img, offsets, False, False)
# show_multiple_offsets(img, offsets, True, False)


