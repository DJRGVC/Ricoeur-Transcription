import os
import random
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
import easyocr


class EasyOCRProcessor:
    """
    A utility class for performing OCR using EasyOCR or PaddleOCR and processing results.
    """

    def __init__(self, images_path, save_path, font_path=None):
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
        return image_name, Image.open(img_path)

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

    def draw_results_easyocr(self, image, results, save=False, output_name="ocr_easy"):
        """
        Draw bounding boxes and text using results from EasyOCR.

        Args:
            image (PIL.Image.Image): The input image.
            results (list): OCR results with bounding boxes and text.
            save (bool): Whether to save the processed image.
            output_name (str): Name for the saved image.
        """
        boxes = [line[0] for line in results]
        words = [line[1] for line in results]
        if self.font_path is None:
            raise ValueError("Font path must be specified for EasyOCR visualization.")
        draw_img = draw_ocr(image, boxes, words, font_path=self.font_path)
        draw_img_pil = Image.fromarray(draw_img)
        draw_img_pil.show()

        if save:
            save_path = os.path.join(self.save_path, f"{output_name}.png")
            draw_img_pil.save(save_path)
            print(f"Saved EasyOCR result to {save_path}")

    def perform_paddleocr(self, img_path):
        """
        Perform OCR using PaddleOCR.

        Args:
            img_path (str): Path to the image file.
        
        Returns:
            tuple: OCR results including boxes, text, and confidence scores.
        """
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
        return ocr.ocr(img_path, cls=True)

    def draw_results_paddleocr(self, img_path, results, save=False, output_name="ocr_paddle"):
        """
        Draw bounding boxes and text using results from PaddleOCR.

        Args:
            img_path (str): Path to the image file.
            results (tuple): OCR results including bounding boxes and text.
            save (bool): Whether to save the processed image.
            output_name (str): Name for the saved image.
        """
        image = Image.open(img_path).convert('RGB')
        boxes, texts, scores = [], [], []
        for result in results[0]:
            boxes.append(result[0])
            texts.append(result[1][0])
            scores.append(result[1][1])

        draw_img = draw_ocr(image, boxes, texts, scores, font_path=self.font_path)
        draw_img_pil = Image.fromarray(draw_img)
        draw_img_pil.show()

        if save:
            save_path = os.path.join(self.save_path, f"{output_name}.png")
            draw_img_pil.save(save_path)
            print(f"Saved PaddleOCR result to {save_path}")


# Example Usage
if __name__ == "__main__":
    images_path = "../raw_data/images"
    save_path = "../updates/images"
    font_path = "/Library/Fonts/Arial.ttf"  # Adjust to the correct path for your system

    ocr_processor = EasyOCRProcessor(images_path, save_path, font_path)
    
    # Load a random image
    image_name, img = ocr_processor.get_random_image()

    # Perform OCR with EasyOCR
    img_path = os.path.join(images_path, image_name)
    easyocr_results = ocr_processor.perform_easyocr(img_path)
    ocr_processor.draw_results_easyocr(img, easyocr_results, save=True, output_name=f"{image_name}_easyOCR")

    # Perform OCR with PaddleOCR
    paddleocr_results = ocr_processor.perform_paddleocr(img_path)
    ocr_processor.draw_results_paddleocr(img_path, paddleocr_results, save=True, output_name=f"{image_name}_paddleOCR")

