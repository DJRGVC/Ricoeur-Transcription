# Update 3: Testing: OCR on Preprocessed images, Training Data Generation

**Date**: December 8, 2024  
**Author**: Daniel Grant  
**Institution**: Bowdoin College  

## Summary

This week, I focused on restructuring my project into a series of importable modules to assist in further development. As such, I did not make quite as much progress on the OCR pipeline. However, I did manage to test the OCR pipeline on the preprocessed images from the last update. The results were not quite as good as I had hoped, with the OCR transcriptions being quite poor. So, I have some new thoughts as to next steps, and more concerns about feasibility. But, I will continue to push forward, with the hope that I can make some real progress in the coming weeks.

## Detailed Description

### Overview

During the last update I optimized the preprocessing process for the images. This week, I completely restructured this pipeline to be more modular and easier to work with. Thus, my project structure now looks as follows:

README.md
license.txt
requirements.txt
updates/
src/
  - __init__.py
  - modules/
    - __init__.py
    - easy_ocr_processor.py
    - image_preprocessor.py
    - skew_correction.py
  - scripts/
    - __init__.py
    - bounding_box_generation/
    - image_preprocessing/
    - ocr_on_processed/
       - __init__.py
       - process_and_ocr.py

This structure (with some unnecessary files and folders omitted for brevity) allows me to import the modules I have created in the `src/modules` folder into the scripts I have created in the `src/scripts` folder. This will make it easier to test and develop the OCR pipeline in the coming weeks.

Outside of this restructuring, I did some testing on the OCR pipeline with the preprocessed images from the last update. Some of the results are shown below


### Testing

As a refresher: "I used [Otsu's thresholding method](https://ieeexplore.ieee.org/document/4310076) to convert the images to binary. This method is adaptive and should work well with the varying lighting conditions in the scans. I found it to be particularly effective in reducing the noise in the images. However, I have (below) tested offsetting the calculated Otsu's theshhold value by a constant to see if it improves the results.

Finally, I additionally tried using a slight gaussian blur to correct for the harsh lighting conditions in the scans (causing some letters to appear thinner than others, in some cases split into multiple path components)."

Now, with a constant threshold offset (18) and gaussian blur (5x5) applied to the images, I tested the OCR pipeline:

#### Example 1

![Example1_Bounded](../images/Update3/slide_179_image_1.png)
![Example1_Transcription](../images/Update3/slide_179_image_1.png)

#### Example 2

![Example2_Bounded](../images/Update3/slide_179_image_1.png)
![Example2_Transcription](../images/Update3/slide_179_image_1.png)

#### Example 3

![Example3_Bounded](../images/Update3/slide_179_image_1.png)
![Example3_Transcription](../images/Update3/slide_179_image_1.png)

### Next Steps

- Migrate to isolating single bounding boxes, export to image files,

### Challenges

- Skew correction was quite challenging to get right due to the harsh borders in the scans. Results here are acceptable.
- The threshholding and gaussian blur values are still not perfect. I will continue to test these values next week.
- I am not sure how to predict what preprocessing techniques will aid in OCR text recognition past the initial bounding box creation stage. I will need to do more research on this topic.




## References

- [Netra Prasad Neupane's Post](https://netraneupane.medium.com/text-skewness-correction-a51fd3a27157)
- [Nathancy's Post](https://stackoverflow.com/questions/57964634/python-opencv-skew-correction-for-ocr)
- [Sreekiran A R's Post](https://stackoverflow.com/questions/62670920/90-degree-skew-correction-for-ocr-in-opencv-python)
- [Otsu's Thresholding Method](https://ieeexplore.ieee.org/document/4310076)

---

*For more information on the Paul Ricoeur Transcription Project, visit the [Digital Ricoeur Portal](https://www.digitalricoeurportal.org/digital-ricoeur/).*


