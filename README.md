# *Optimuz*

This repository contains the code for a *GENAI-based project* featuring a user interface with various accessibility options. The project integrates *PaddleOCR* for Optical Character Recognition (OCR) and the *GEMINI AI chatbot* for enhanced user interaction.

### *Demo of our Website :* 
https://drive.google.com/file/d/14M0tdOSUE9SQSAjlpCKiSHbfJpdtaGyG/view?usp=drivesdk


---

## *Table of Contents*
- [Project Structure](#project-structure)
- [Overview](#overview)
- [PaddleOCR Features](#paddleocr-features)
- [Model Architecture](#model-architecture)
- [Implementation Workflow](#implementation-workflow)
- [Model Fine-tuning for Vertical and Long Text](#model-fine-tuning-for-vertical-and-long-text)
- [JSON Output Example](#json-output-example)
- [Student Results Chatbot Integration](#student-results-chatbot-integration)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Student Results Chatbot with RAG Integration](#student-results-chatbot-with-rag-integration)

---

## *Project Structure*

optimuz/ │ <br>
├── compressed_image/ # Contains compressed images used for testing after resizing.<br>
├── processed_image/ # Stores processed images ready for OCR extraction.<br>
├── processed_json/ # Contains the output JSON files generated from the OCR model.<br>
├── chatbot.ipynb # Jupyter notebook implementing the chatbot logic for data queries. <br>
├── convertor.ipynb # Script to convert various output formats like JSON to CSV/XLS. <br>
├── image4K.ipynb # Notebook to resize and compress large images to 4K resolution. <br>
└── model.ipynb # Main OCR model implementation using PaddleOCR. <br>

web/ │<br>
├── app.py # Main web application script built using Streamlit.<br> 
├── hackathon1.py # Additional backend logic specific to the hackathon requirements. <br>
└── students_results.json # Sample JSON file with student data for testing and demo purposes.<br>


---

## <a id="overview"></a> *Overview*

*PaddleOCR* is an advanced toolkit for optical character recognition that allows users to extract text from images and documents. The toolkit includes multiple pre-trained models for:

- Text Detection
- Text Direction Classification
- Text Recognition

PaddleOCR supports multiple languages such as Latin, Arabic, Traditional Chinese, Korean, and Japanese, making it a versatile tool for global applications.

---

## <a id="paddleocr-features"></a> *PaddleOCR Features*

- 🖼 *Text Detection*: Detects text areas in images and generates bounding boxes around them.
- 🔤 *Text Recognition*: Recognizes and extracts text content within the detected regions.
- 🔄 *Vertical Text Detection*: Detects rotated or vertically aligned text.
- 📏 *Handling Long Text*: Optimized to recognize longer blocks of text.
- ⬆ *Angle Classification*: Automatically detects and corrects the text's orientation.
- 📸 *High-Resolution Text Detection*: Supports high-res input for detecting small and large text accurately.

---

## <a id="model-architecture"></a> *Model Architecture*

*PP-OCRv3*

- *Text Detection* is based on the *Differentiable Binarization (DB)* algorithm, trained with a distillation strategy for high accuracy.
- *Text Recognition* leverages the *Scene Text Recognition with a Single Visual Model (SVTR)*, as outlined by Du et al. (2022).

---

## <a id="implementation-workflow"></a> *Implementation Workflow*

The *Optimuz* project utilizes the *PaddleOCR* model to process images and extract text content. Here's the step-by-step process:

1. *Image Input*: The image is fed into the OCR model.
2. *Text Detection*: Bounding boxes are generated around the detected text areas.
3. *Text Recognition*: Extracts the actual text from the regions inside the bounding boxes (if recognition is enabled).
4. *JSON Output*: The model generates a JSON file containing the detected text, bounding box coordinates, and confidence scores.

---

## <a id="model-fine-tuning-for-vertical-and-long-text"></a> *Model Fine-tuning for Vertical and Long Text*

While PaddleOCR excels at detecting horizontal text, several adjustments were made to enhance performance for vertical and lengthy text:

- **use_angle_cls=True**: Enables detection and correction of rotated or vertically aligned text.
- **det_db_box_thresh=0.2**: Lowers the detection threshold to increase sensitivity for text detection.
- **det_db_unclip_ratio=2.5**: Increases the unclip ratio to capture larger text areas.
- **lang='en'**: Specifies the language to be used (English in this case).
- **rec=False**: Disables the text recognition component (if only detection is required).
- **det_limit_side_len=1536**: Sets a maximum side length for detected text to handle high-resolution images.

---

## <a id="json-output-example"></a> *JSON Output Example*

json
[
    {
        "text": "Hello",
        "confidence": 0.98,
        "position": [[12, 34], [56, 34], [56, 78], [12, 78]]
    },
    {
        "text": "World!",
        "confidence": 0.95,
        "position": [[100, 150], [200, 150], [200, 180], [100, 180]]
    }
]


## *Student Results Chatbot with RAG Integration*

We are expanding the chatbot functionality by integrating *RAG (Retrieval-Augmented Generation)*, enabling the model to provide a structured format of student marklists. This process involves several key steps:

---

### *How It Works:*

#### *1. Data Collection and Processing:*
- We utilize *OCR (Optical Character Recognition)* to extract unstructured data from marklist images.
- Simultaneously, structured data is retrieved from the university’s marks database.

#### *2. Creating a Training Dataset:*
- Since there is no pre-existing, structured dataset for
  ```
  ## *Structured Marklist Integration with RAG Model*

We are integrating a *RAG (Retrieval-Augmented Generation)* model to convert unstructured student marklist images into a structured format. Here's the process:

---

### *1. Dataset Creation:*
- Using *OCR*, unstructured data is extracted from university marklist images.
- Structured data is obtained from the university's marks database.

### *2. Model Training:*
- The *RAG model* is trained on this data to learn the conversion from unstructured to structured format.

### *3. Chatbot Integration:*
- Once trained, the *RAG model* will be integrated into our chatbot, enabling it to provide accurate, structured responses based on user queries.



## *App.js - Prototype Overview*

The *App.js* is the user interface prototype for our project, hosted on *Streamlit*. It allows users to interact with the OCR model and chatbot. Key features include:

- *Image Upload*: Users can upload marklist image files.
- *JSON Preview & Download*: The app generates a JSON file from the image data, previews it, and allows users to download it.
- *Chatbot Interaction*: Users can chat with the bot to ask questions and resolve queries.
- *JSON Conversion*: The app provides options to convert the JSON file to Excel or CSV format.
- *API Key Generation*: Users can generate an API key to access the model programmatically.

- ## *FURTHER UPDATES FOR OUR MODEL*

We are integrating a *RAG (Retrieval-Augmented Generation)* model to convert unstructured student marklist images into a structured format. Here's the process:

---

### *1. Dataset Creation:*
- Using *OCR*, unstructured data is extracted from university marklist images.
- Structured data is obtained from the university's marks database.

### *2. Model Training:*
- The *RAG model* is trained on this data to learn the conversion from unstructured to structured format.

### *3. Chatbot Integration:*
- Once trained, the *RAG model* will be integrated into our chatbot, enabling it to provide accurate, structured responses based on user queries.

---

## *UI Design Overview for OCR Web Application*

This is the *UI design concept* for our OCR model-based web platform, created using *Figma. The platform serves two distinct user types: **Normal Users* and *Organizations*, each with tailored functionalities. Below is a detailed description of the user interface and features for both types of users:
## *Figma Link*
[Access the Figma Design Here](https://www.figma.com/design/Br285x2rsCXaeLzE2XmMOs/OCR_Model?node-id=0-1&t=OZkE2vxdM2a9WogR-1) <!-- Replace with actual link -->

---

### *Normal Users*
*Features:*
- *Upload report card images* and convert them into multiple formats such as *JSON, **CSV, or **XLS*.
- *API Key Access*: After signing in, users can generate their own API key to integrate the OCR model into their own projects or workflows.
- *User-Friendly Interface*: A simple interface designed to ensure ease of use and smooth functionality.

---

### *Organizations*
*Additional Features:*
- Access to all functionalities available to normal users, such as image upload, file conversion, and API key generation.
- *Structured Data Management*: Organized branch-wise and class-wise data views, making it easy for organizations to:
  - Append new data to existing records.
  - Access previous reports quickly.
  - Handle large student datasets efficiently.

This feature is especially useful for institutions like *RGUKT*, where report card management needs to be scalable and structured.

---

### *Design Goal*
The UI design focuses on *simplicity, **efficiency, and **usability* for both individual users and large organizations. With two separate user flows, the platform offers a personalized experience, ensuring that both students and institutions can benefit from the OCR model seamlessly.
