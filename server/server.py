from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PIL import Image
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '../')

from judge_fashion import JudgeFashion

judge = JudgeFashion(
    img_size=160,
    model_path='./configs/trained_modelv1.tflite',
    w='./configs/yolov3.weights',
    cfg='./configs/yolo.cfg'
)

UPLOAD_FOLDER = '.\\server\\server_images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    test = request.args.get('test')

    return 'hello ' + str(test)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            with Image.open(path) as img:
                img.show()
            return redirect(url_for('results',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/results', methods=['GET'])
def results():
    filename = request.args.get('filename')
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    im = plt.imread(path)

    res = judge.get_fashion_results(im)

    return str(res)
