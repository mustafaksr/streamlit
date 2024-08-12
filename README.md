
# Streamlit Apps Repo

## Document Question Answering App

This application allows you to upload a document image and ask questions about its content. 
It uses a pre-trained NLP model to analyze the document and provide answers based on the text within the image.

### Instructions:
1. **Upload a Document**: Click on the "Upload a document image" button to select and upload an image file (PNG, JPG, or JPEG) of the document you want to query.
2. **Enter Your Question**: Type your question in the text input field.
3. **Get Results**: Once both the document and the question are provided, the model will process the document and display the answer.

**Note**: Ensure that the document is clear and legible for accurate results.
[Document Question Answering App in Repo](document/)

## Table Question Answering App:

This application allows you to upload a CSV file containing tabular data and ask questions about its content.
It uses a pre-trained NLP model to analyze the table and provide answers based on the data within the table.

### Instructions:
1. **Upload a CSV File**: Click on the "Choose a CSV file for data" button to select and upload a CSV file of the table you want to query.
2. **Enter Your Question**: Type your question in the text input field.
3. **Get Results**: Once both the CSV file and the question are provided, the model will process the table and display the answer.

**Note**: Ensure that the table is clear and properly formatted for accurate results.

[Document Question Answering App in Repo](table/)

## repo structure:
```
.
├── chatbot
│   ├── backend
│   ├── docker-compose.yml
│   └── ui
├── document
│   ├── app.py
│   ├── cloudbuild.yaml
│   ├── Dockerfile
│   ├── models--impira--layoutlm-document-qa
│   ├── readme.md
│   └── requirements.txt
├── shipwrecks
│   ├── app.py
│   └── Dockerfile
├── streamlit_app0
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── table
    ├── app.py
    ├── cloudbuild.yaml
    ├── Dockerfile
    ├── models--microsoft--tapex-large-finetuned-wtq
    └── requirements.txt
```