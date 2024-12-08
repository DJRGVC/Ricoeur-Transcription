import os
import random
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skew_correction import SkewCorrection

class ImagePreprocessor:
    """
    A utility class for processing images, including shadow removal,
    thresholding, skew correction, and visualization.
    """

    def __init__(self, images_path, processed_images_path):
        self.images_path = images_path
        self.processed_images_path = processed_images_path
        os.makedirs(processed_images_path, exist_ok=True)

    def load_random_image(self):
        """
        Load a random image from the specified directory.
        """
        all_images = [img for img in os.listdir(self.images_path)
                      if img.endswith('.png') or img.endswith('.jpg')]
        if not all_images:
            raise FileNotFoundError("No images found in the specified directory.")
        
        image_name = random.choice(all_images)
        img_path = os.path.join(self.images_path, image_name)
        image_name = image_name.split('.')[0]
        return image_name, cv2.imread(img_path)

    def process_image(self, img, threshold_offset, gaussian_blur=False, save_skew=False, image_name="image"):
        """
        Process the image with options for threshold adjustment and Gaussian blur.
        """
        img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        orig_img = img.copy()

        # Convert to gray scale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Removing shadows
        rgb_planes = cv2.split(img)
        result_planes = []
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            result_planes.append(255 - cv2.absdiff(plane, bg_img))
        img = cv2.merge(result_planes)

        # Dilation and erosion
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        if gaussian_blur:
            img = cv2.GaussianBlur(img, (5, 5), 0)

        # Threshold adjustment
        otsu_threshold, _ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        adjusted_threshold = max(otsu_threshold + threshold_offset, 0)
        _, img = cv2.threshold(img, adjusted_threshold, 255, cv2.THRESH_BINARY)

        # Skew correction
        angle, img = SkewCorrection.nathan_skew_correction(img, orig_img)

        # Save skew-corrected images if required
        if save_skew:
            cv2.imwrite(f'{self.processed_images_path}/skew_corrected_{image_name}.jpg', img)
            cv2.imwrite(f'{self.processed_images_path}/original_{image_name}.jpg', orig_img)

        return img, angle

    def show_image(self, title, image):
        """
        Display an image using matplotlib.
        """
        plt.imshow(image, cmap='gray')
        plt.title(title)
        plt.axis('off')
        plt.show()

    def save_image(self, image, filename):
        """
        Save the processed image to the specified path.
        """
        save_path = os.path.join(self.processed_images_path, filename)
        Image.fromarray(image).save(save_path)

    def compare_offsets(self, img, offsets, gaussian_blur=False):
        """
        Compare results with different threshold offsets.
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 12))
        for i, offset in enumerate(offsets):
            processed_img, _ = self.process_image(img, offset, gaussian_blur)
            row, col = divmod(i, 2)
            ax = axes[row, col]
            ax.imshow(processed_img, cmap='gray')
            ax.set_title(f"Offset: {offset}")
            ax.axis('off')
        plt.tight_layout()
        plt.show()


# Example Usage:
if __name__ == "__main__":
    images_path = "../raw_data/images"
    processed_images_path = "../raw_data/processed_images"

    processor = ImagePreprocessor(images_path, processed_images_path)
    image_name, img = processor.load_random_image()
    processed_img, angle = processor.process_image(img, threshold_offset=15, gaussian_blur=False, save_skew=True, image_name=image_name)
    processor.show_image("Processed Image", processed_img)

