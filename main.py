from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document
import os
import mimetypes
from GROQ.groq__ import query_pdf_content

app = Flask(__name__)

# Folder to store uploaded files temporarily
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage for file content
uploaded_content = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"detail": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"detail": "No selected file"}), 400

    # Secure the filename and save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        # Detect the file type
        file_type = detect_file_type(file_path)
        
        if file_type == 'pdf':
            text = extract_text_from_pdf(file_path)
        elif file_type == 'word':
            text = extract_text_from_word(file_path)
        else:
            return jsonify({"detail": "Unsupported file type"}), 400

        # Store the extracted text in memory for chat
        uploaded_content['content'] = text

        return jsonify({"message": "File uploaded successfully"}), 200

    except Exception as e:
        return jsonify({"detail": f"Error processing file: {str(e)}"}), 500
    finally:
        # Clean up uploaded file
        os.remove(file_path)

@app.route('/chat', methods=['POST'])
def chat_with_content():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"detail": "No message provided"}), 400

    content = uploaded_content.get('content')
    if not content:
        return jsonify({"detail": "No content available to chat with. Please upload a file first."}), 400
    print(content)
    llm_response = query_pdf_content(content, user_message)
    print(llm_response)
    return jsonify({"response": llm_response}), 200

def detect_file_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        if mime_type == 'application/pdf':
            return 'pdf'
        elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return 'word'
    return None

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_word(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

if __name__ == '__main__':
    app.run(debug=True)
