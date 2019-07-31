# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


html = '''
    <!DOCTYPE html>
    <title>test</title>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file >
         <input type=submit value=上傳>
    </form>
    '''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/audiovideo', methods=['GET', 'POST'])
def audiovideo():
    if request.method == 'POST':
        file = request.files['file']
        filename = "myaudiovideo.webm"
        filename = secure_filename(filename)
        file.save(os.path.join('.', 'uploads', filename))
    return html
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
