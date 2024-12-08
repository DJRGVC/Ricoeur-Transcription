import os
import random
from PIL import Image
from paddleocr import draw_ocr
import easyocr


class EasyOCRProcessor:
    """
    A utility class for performing OCR using EasyOCR and processing results.
    """

    def __init__(self, images_path, save_path, font_path="/Library/Fonts/Arial.ttf"):
        """
        Initialize the OCRProcessor with paths for images and saving results.
        
        Args:
            images_path (str): Path to the directory containing input images.
            save_path (str): Path to save processed images.
            font_path (str, optional): Path to the font file for drawing text.
        """
        self.images_path = images_path
        self.save_path = save_path
        self.font_path = font_path
        os.makedirs(save_path, exist_ok=True)

    def get_random_image(self):
        """
        Select and return a random image from the specified directory.
        """
        all_images = [img for img in os.listdir(self.images_path) if img.endswith(('.png', '.jpg'))]
        if not all_images:
            raise FileNotFoundError("No images found in the specified directory.")
        image_name = random.choice(all_images)
        img_path = os.path.join(self.images_path, image_name)
        return image_name, Image.open(img_path).convert('RGB')

    def get_image(self, img_path):
        """
        Load and preprocess the image for OCR.
        
        Args:
            img_path (str): Path to the image file.
        
        Returns:
            PIL.Image: Preprocessed image.
        """
        img = Image.open(img_path).convert('RGB')
        return img

    def perform_easyocr(self, img_path):
        """
        Perform OCR using EasyOCR.

        Args:
            img_path (str): Path to the image file.
        
        Returns:
            list: List of detected text and bounding boxes.
        """
        reader = easyocr.Reader(['en'])
        return reader.readtext(img_path)

    def draw_results(self, image, results, show=False, save=False, output_name="ocr_paddle"):
        """
        Draw bounding boxes and text using results from EasyOCR.

        Args:
            img_path (str): Path to the image file.
            results (tuple): OCR results including bounding boxes and text.
            save (bool): Whether to save the processed image.
            output_name (str): Name for the saved image.
        """
        boxes, words = [], []
        for line in results:
            boxes.append(line[0])
            words.append(line[1])

        draw_img = draw_ocr(image, boxes, words, font_path=self.font_path)
        draw_img_pil = Image.fromarray(draw_img)
        if show:
            draw_img_pil.show()

        if save:
            save_path = os.path.join(self.save_path, f"{output_name}.png")
            draw_img_pil.save(save_path)
            print(f"Saved PaddleOCR result to {save_path}")


# Example Usage
if __name__ == "__main__":

    print("Running OCR Processor Example...")

    images_path = "../raw_data/images"
    save_path = "../updates/images"
    font_path = "/Library/Fonts/Arial.ttf"  # Adjust to the correct path for your system

    print("Initializing OCR Processor...")

    ocr_processor = EasyOCRProcessor(images_path, save_path, font_path)

    print("Performing OCR on a random image...")
    
    # Load a random image
    image_name, img = ocr_processor.get_random_image()

    print(f"Processing image: {image_name}")

    # Perform OCR with EasyOCR
    img_path = os.path.join(images_path, image_name)
    easyocr_results = ocr_processor.perform_easyocr(img_path)
    ocr_processor.draw_results(img, easyocr_results, show=True, save=False, output_name=f"{image_name}_easyOCR")
