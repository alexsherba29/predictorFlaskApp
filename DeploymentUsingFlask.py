from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os
from pathlib import Path

try:
    Path("uploaded/image").mkdir(parents=True, exist_ok=True)
    print()
except:
    pass

model = tf.keras.models.load_model('saved_models/alex_model.h5')
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploaded/image'


@app.route('/')
def upload_f():
    return render_template('upload.html')


def finds():
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    vals = ['Cat', 'Dog']  # change this according to what you've trained your model to do
    test_dir = 'uploaded'
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(180, 180),
        color_mode="rgb",
        shuffle=False,
        class_mode='categorical',
        batch_size=1)

    pred = model.predict(test_generator)
    print(pred)
    return str(vals[np.argmax(pred)])


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        val = finds()
        return render_template('pred.html', ss=val)


if __name__ == '__main__':
    app.run()
