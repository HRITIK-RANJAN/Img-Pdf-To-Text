# app.py
import os , shutil
from flask import Flask, render_template, request
import pytesseract
import cv2
import fitz
import time
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = [ 'png', 'jpg', 'jpeg']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST', 'GET'])
def process_data():
    if request.method == 'POST':
        # For POST requests, retrieve form data
        name = request.form['name']
        dateTime = request.form['futureDateTime']
        file=request.files['file']
        file_extension=file.filename.split('.')[-1]
        date=dateTime.split('T')[0]
        times=dateTime.split('T')[1]
        dateTime=str(date)+" "+str(times)
        given_time = datetime.strptime(dateTime, "%Y-%m-%d %H:%M")
        current_time = datetime.now()
        time_difference = given_time - current_time

        if time_difference.total_seconds() > 0:
            time.sleep(time_difference.total_seconds())


        if file_extension in ALLOWED_EXTENSIONS :
            file.save("./uploads/image.png")
            image = cv2.imread('./uploads/image.png')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            
        elif file_extension=='pdf':
            file.save("./uploads/converted.pdf")
            convert_pdf_to_text()
            with open("./uploads/convert.txt","r") as reader:
                text=reader.read()
            
        else:
            text='Given File type is not supported !'
        
        formData={
            'name':name,
            'Submission time':given_time,
            'Current time':current_time,
            'text':text
        }
        # Return a JSON response for the POST request
        return render_template('mark.html', formData=formData)
           
    elif request.method == 'GET':
        # For GET requests, retrieve data from query parameters in the URL
        formData = request.args.get('formData')
        print("FormData:", formData)
        return render_template('mark.html', formData=formData)

def convert_pdf_to_text():
    text=""
    doc = fitz.open('./uploads/converted.pdf')
    for page in doc: 
        text += page.get_text() 
    with open('./uploads/convert.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    return



if __name__ == '__main__':
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
