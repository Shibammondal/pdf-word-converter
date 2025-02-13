from flask import Flask, request, render_template, send_file
import os
from pdf2docx import Converter
from fpdf import FPDF

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def pdf_to_word(pdf_path, docx_path):
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()

def word_to_pdf(word_path, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    with open(word_path, "r", encoding="utf-8") as file:
        for line in file:
            pdf.cell(200, 10, txt=line, ln=True)
    pdf.output(pdf_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file uploaded"
    
    file = request.files['file']
    convert_type = request.form['convert_type']
    
    if file.filename == '':
        return "No selected file"
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    if convert_type == 'pdf_to_word':
        output_file = filepath.replace(".pdf", ".docx")
        pdf_to_word(filepath, output_file)
    elif convert_type == 'word_to_pdf':
        output_file = filepath.replace(".txt", ".pdf")
        word_to_pdf(filepath, output_file)
    else:
        return "Invalid conversion type"
    
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
