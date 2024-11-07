# Update 2: Preprocessing: Normalization, Skew Correction, and Threshholding

**Date**: November 7, 2024  
**Author**: Daniel Grant  
**Institution**: Bowdoin College  

## Summary

This week, I focused on improving OCR text segmentation for Paul Ricoeur’s handwritten notes by enhancing image preprocessing techniques. EasyOCR’s bounding box creation had previously shown mixed results, so I built a preprocessing pipeline to help it better identify text. My pipeline includes steps like normalization, greyscale conversion, shadow reduction, Gaussian blurring, thresholding, and skew correction. Skew correction was particularly challenging due to the strong borders in the scans, but with guidance from various resources, I managed to get satisfactory results. Testing emphasized Otsu’s thresholding with different offsets and Gaussian blur to tackle lighting inconsistencies and thin, fragmented text. So far, an offset around 20 seems most promising, though I’ll keep refining these values. Next steps include testing the impact of this preprocessing on EasyOCR’s segmentation accuracy and exploring methods to match bounding boxes with expert-created transcriptions.

## Detailed Description

### Overview

Despite reasonable results from EasyOCR last week regarding the creation of bounding boxes for Ricoeur's scanned handwritten notes, there were still some issues with the quality of the text segmentation. Thus, rather than moving directly into trying to match bounding boxes with expert-created transcriptions, I decided to concentrate my efforts on preprocessing the images to (hopefully) help EasyOCR better identify the text. 

Given the nature of the scanned images, I created a simplified preprocessing pipeline that included normalization, conversion to greyscale, shadow reduction, , blurring, thresholding, and skew correction. I tried a number of different methods for each of these steps, drawing inspiration from a large variety of sources. I found skew correction to be particularly challenging, as the scans had harsh borders which affected the accuracy of the skew correction. The following posts helped me to develop my pipeline:

- [Netra Prasad Neupane's Post](https://netraneupane.medium.com/text-skewness-correction-a51fd3a27157)
- [Nathancy's Post](https://stackoverflow.com/questions/57964634/python-opencv-skew-correction-for-ocr)
- [Sreekiran A R's Post](https://stackoverflow.com/questions/62670920/90-degree-skew-correction-for-ocr-in-opencv-python)

I will additionally add resources used for the other steps in the pipeline in the references section. 


### Testing

As it is important to my testing for the week, I have included some details about my implementation below:

I used [Otsu's thresholding method](https://ieeexplore.ieee.org/document/4310076) to convert the images to binary. This method is adaptive and should work well with the varying lighting conditions in the scans. I found it to be particularly effective in reducing the noise in the images. However, I have (below) tested offsetting the calculated Otsu's theshhold value by a constant to see if it improves the results.

Finally, I additionally tried using a slight gaussian blur to correct for the harsh lighting conditions in the scans (causing some letters to appear thinner than others, in some cases split into multiple path components).

The results of this testing are shown below.



### Threshhold + Gaussian Testing

I have included two images of differing complexity below to show the results of  my thresholding and gaussian blur testing.

#### Example 1

Here is the original Image:

![Image1_Original](../images/Update2/slide_179_image_1.png)

Now, here is the image after thresholding and gaussian blur:

![Image1_Threshold_1](../images/Update2/processed_slide_179_image_40.png)

![Image1_Threshold_1_gaussian](../images/Update2/processed_slide_179_image_40_gaussian.png)

The best results seemed to be around a threshhold offset of 20. Thus, a smaller range of offsets was tested below around this value.

![Image1_Threshold_2](../images/Update2/processed_slide_179_image_30.png)

![Image1_Threshold_2_gaussian](../images/Update2/processed_slide_179_image_30_gaussian.png)


#### Example 2

Here is the original Image:

![Image2_Original](../images/Update2/slide_7_image_1.png)

Now, here is the image after thresholding and gaussian blur:

![Image2_Threshold_1](../images/Update2/processed_slide_7_image_40.png)

![Image2_Threshold_1_gaussian](../images/Update2/processed_slide_7_image_40_gaussian.png)

![Image2_Threshold_2](../images/Update2/processed_slide_7_image_30.png)

![Image2_Threshold_2_gaussian](../images/Update2/processed_slide_7_image_30_gaussian.png)


### Skew Correction Testing

I have included three examples (picked at random) of skew correction below.

#### Example 1
![Image1_Original](../images/Update2/original_slide_114_image_1.png)
![Image1_Skew_Corrected](../images/Update2/skew_corrected_slide_114_image_1.png)

#### Example 2
![Image2_Original](../images/Update2/original_slide_352_image_1.png)
![Image2_Skew_Corrected](../images/Update2/skew_corrected_slide_352_image_1.png)

#### Example 3
![Image3_Original](../images/Update2/original_slide_446_image_1.png)
![Image3_Skew_Corrected](../images/Update2/skew_corrected_slide_446_image_1.png)


Pretty happy with the skew correction results. Might continue to play around with threshhold offsets and gaussian blur values for next week, testing in conjunction with EasyOCR's bounding box creation.


### Next Steps

- Compare newly preprocessed images against to unprocessed images with EasyOCR to see if the preprocessing has improved the text segmentation.
- Test different threshhold offsets and gaussian blur values to see if they improve the results.
- Begin thinking about methods for matching bounding boxes with expert-created transcriptions.

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


