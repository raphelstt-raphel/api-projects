**Document-Based Question Generator**

A lightweight Flask web app that reads PDF and PPTX documents and generates questions from their text. The questions are exported as a PDF.

**Features**
- Upload PDF or PPTX files
- Extracts text from the documents
- Generates questions using lightweight NLP models
- Exports the questions as a PDF
- Works completely offline, with no internet needed
- Light enough to run on a normal laptop

**Tech Stack**
Python, Flask, NLP models

**How to Run**
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start the app: `python app.py`
4. Open `http://127.0.0.1:5000` in your browser
5. Upload a document and download the generated questions
