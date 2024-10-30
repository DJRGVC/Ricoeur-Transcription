# Paul Ricoeur Transcription Project (Digital Ricoeur)

**Author**: Daniel Grant  

**Date Begun**: October 17, 2024  

**Institution**: Bowdoin College  

**Advisor**: Fernando Nascimento  

**Contact**: [dgrant2@bowdoin.edu](mailto:dgrant2@bowdoin.edu)  

**Advisor's Email**: [fnasc@bowdoin.edu](mailto:fnasc@bowdoin.edu)


## Project Overview

This project aims to transcribe the notes and lecture materials of French philosopher Paul Ricoeur using AI-powered handwriting and text recognition technology. The goal is to develop an efficient, scalable solution for digitizing and preserving these important philosophical documents, making them more accessible to scholars and the public.

## Recent Updates

- [Update 1: Initial Approach, Text Segmentation, and Towards OCR Training](updates/reports/October30_2024.md)


## Objectives

1. **Handwriting Recognition**: Utilize advanced OCR tools to transcribe handwritten notes.
2. **Text Processing**: Refine transcribed text for accuracy and readability.
3. **Digitization**: Organize and format the transcriptions for academic use.
4. **Analysis**: Explore methods for analyzing the transcribed data to reveal Ricoeur's thought processes and lecture methodologies.

## Roadmap

[x] Expert-verified transcription of 400+ pages of handwritten Ricoeur Notes
[x] Convert into labelled dataset with image + transcription pairs
[x] Complete text segmentation to create OCR training pipeline friendly dataset
[] Match bounding boxes with ground-truth data
[] Train OCR model(s), compare efficacy by testing with ground-truth data

## Tools and Technologies

- OCR tools for text segmentation and transciption (e.g., EasyOCR, PaddleOCR, Tesseract, Keras_OCR,... )
- Version control: GitHub

## Workflow

1. **Data Collection**: Gather Ricoeur’s notes and lecture materials in digital format. (Note: this step is already completed--500 training examples have been annotated prior to my involvement.)
2. **Model Training and Fine-tuning**: Train and fine-tune the AI models on the annotated data (beginning with tools such as Transcribus, but potentially moving to other models as needed).
3. **Transcription**: Run the AI models on the notes to generate text.
4. **Verification**: Manually verify produced texts for accuracy and completeness.
5. **Final Output**: Compile the verified texts for Digital Ricoeur project.

## Website

For more information on related work and additional resources, visit the [Digital Ricoeur Portal](https://www.digitalricoeurportal.org/digital-ricoeur/).


## Contribution Guidelines

- This project is currently in the research and development phase and is open to collaboration. Feel free to reach out via email if you would like to contribute.

## Acknowledgments

This research is being conducted under the guidance of Professor Fernando Nascimento at Bowdoin College. Special thanks to the Digital and Computational Studies Department for their support.


