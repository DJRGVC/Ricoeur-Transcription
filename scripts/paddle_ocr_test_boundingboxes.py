from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import matplotlib.pyplot as plt

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Initialize with English language support


image_path = 'slide_256_image_1.png'
image = Image.open(image_path)

# Perform OCR to detect text and bounding boxes
result = ocr.ocr(image_path, cls=True)

# Extract bounding boxes, text, and confidence scores
boxes = [line[0] for line in result[0]]
texts = [line[1][0] for line in result[0]]
scores = [line[1][1] for line in result[0]]

# Draw bounding boxes on the image
image_with_boxes = draw_ocr(image, boxes, texts, scores, font_path='path/to/your/font.ttf')

# Convert the result to a format that can be displayed
image_with_boxes = Image.fromarray(image_with_boxes)

# Display the image
plt.figure(figsize=(10, 10))
plt.imshow(image_with_boxes)
plt.axis('off')
plt.show()

