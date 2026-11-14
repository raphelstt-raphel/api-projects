import os
import time
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from utils.text_extractor import extract_text
from utils.question_generator import generate_questions
from utils.pdf_maker import create_pdf

app = Flask(__name__)
app.secret_key = "supersecretkey" # Change this for production
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB limit

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'pptx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'documents' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    files = request.files.getlist('documents')
    
    if not files or files[0].filename == '':
        flash('No selected file')
        return redirect(request.url)

    if len(files) > 5:
        flash('You can only upload a maximum of 5 files.')
        return redirect(request.url)
        
    combined_text = ""
    valid_files = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                text = extract_text(filepath)
                if text.strip():
                     combined_text += text + "\n\n"
                     valid_files = True
            except Exception as e:
                print(f"Error extracting text from {filename}: {e}")
                # Continue with other files

    if not valid_files or not combined_text.strip():
        flash('Could not extract text from the documents.')
        return redirect(url_for('index'))
        
    # Get selected question types
    question_types = request.form.getlist('question_types')
    if not question_types:
        flash('Please select at least one question type')
        return redirect(url_for('index'))

    try:
        # Generate Questions
        questions = generate_questions(combined_text, question_types)
        
        if not any(questions.values()):
            flash('No questions could be generated from this text.')
            return redirect(url_for('index'))

        # Store questions in session for download
        session['questions'] = questions
        
        return render_template('preview.html', questions=questions)

    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('index'))

@app.route('/download_pdf')
def download_pdf():
    questions = session.get('questions')
    if not questions:
        flash("No questions found to download. Please generate them first.")
        return redirect(url_for('index'))
        
    try:
        timestamp = int(time.time())
        output_filename = f"questions_{timestamp}.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        create_pdf(questions, output_path)
        
        return send_file(output_path, as_attachment=True)
        
    except Exception as e:
        flash(f"Error creating PDF: {str(e)}")
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
