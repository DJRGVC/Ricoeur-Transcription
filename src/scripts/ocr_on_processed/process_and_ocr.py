import os
import sys

# Add the src directory to the Python path
# Add the path to the 'modules' folder relative to the script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'modules')))



from modules.easy_ocr_processor import EasyOCRProcessor
from modules.image_preprocessor import ImagePreprocessor

def process_and_ocr():

    print("Processing and OCRing a random image...")

    # Define paths
    images_path = "../../raw_data/images"
    processed_images_path = "../../raw_data/processed_images"
    save_path = "../../updates/images"
    font_path = "/Library/Fonts/Arial.ttf"  # Adjust to the correct path for your system

    print(f"Images path: {images_path}")

    # Initialize the image preprocessor
    image_preprocessor = ImagePreprocessor(images_path, processed_images_path)

    print("Loading a random image and preprocessing it...")

    # Load a random image and preprocess it
    image_name, img = image_preprocessor.load_random_image()
    processed_img, _ = image_preprocessor.process_image(img, threshold_offset=15, gaussian_blur=False, save_skew=True, image_name=image_name)

    print("Initializing EasyOCR processor...")

    # Initialize the EasyOCR processor
    ocr_processor = EasyOCRProcessor(images_path, save_path, font_path)

    print("Saving the processed image...")

    # Save or show the processed image
    image_preprocessor.save_image(processed_img, f"{image_name}_processed.jpg")

    print("Performing OCR with EasyOCR...")

    # Use EasyOCR on the processed image
    processed_img_path = os.path.join(processed_images_path, f"{image_name}_processed.jpg")
    easyocr_results = ocr_processor.perform_easyocr(processed_img_path)

    print("Drawing bounding boxes on the processed image...")
    
    # Draw bounding boxes on the processed image
    ocr_processor.draw_results_easyocr(processed_img, easyocr_results, save=True, output_name=f"{image_name}_easyOCR")

if __name__ == "__main__":
    process_and_ocr()
