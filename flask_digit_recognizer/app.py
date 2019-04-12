import os, sys
from flask import Flask, request, redirect, url_for,send_from_directory, render_template
from werkzeug import secure_filename
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import pickle
import cv2


model = pickle.load(open('model/model.pkl','rb'))

UPLOAD_FOLDER = 'static/data/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('predict', filename=filename))
    return render_template('home.html')

@app.route('/pred/<filename>', methods=['GET', 'POST'])
def predict(filename):
    img = cv2.imread("static/data/{}".format(filename), 0)

    img = img.astype('float32')
    img = img.astype('float32')
    print(img.shape)
    img /= 255
    img = img.reshape(1,784)
    print(img.shape)
    model._make_predict_function()
    predicted_number = model.predict_classes(img)[0]
    return render_template('image.html', image=filename, number=predicted_number)




if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5001)
