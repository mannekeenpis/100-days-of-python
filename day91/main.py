from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import pickle
from collections import Counter

import os
import datetime as dt

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
Bootstrap(app)

#----Get Year (for copyright)----#
now = dt.datetime.now()
year = now.year


#----Create Forms----#
class UploadForm(FlaskForm):
    file = FileField(label='Upload File')
    submit = SubmitField("Submit")

#----Create Routes----#


@app.route("/")
def home():
    return render_template("index.html", year = year)


@app.route("/library")
def library():
    images = os.listdir('static/images')
    hex_files = os.listdir('static/palettes')
    hexes = []
    for hfile in hex_files:
        with open(f'static/palettes/{hfile}', 'rb') as file:
            hexes.append((hfile, pickle.load(file)))
    return render_template("library.html", year = year, images=images, hexes=hexes)


@app.route("/create", methods=['GET', 'POST'])
def create():
    form = UploadForm()
    if form.validate_on_submit():

    #--Save Image--#
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('static/images/' + filename)

    # ---Open Image and Generate Array---#
        img = Image.open(f'static/images/{filename}')
        array = np.array(img)
        d1 = array.shape[0]
        d2 = array.shape[1]

    # ---Pull RGB Values from Array---#
        rgb = []
        for i in range(0, d2):
            for j in range(0, d1):
                colors = img.getpixel((i, j))
                rgb.append(colors)

    # ---Convert RGB Values to HEX (as a list)---#
        hex = []
        for i in rgb:
            hex.append('%02x%02x%02x' % i)

    # ---Identify Most Frequently Used Hex Codes---#
        common_hex = Counter(hex)
        common_hex = common_hex.most_common(100000)
        common_hex = [hex[0] for hex in common_hex[::20000]]

    # --Save Hex Codes to File---#
        with open(f'static/palettes/{filename.strip(".jpg")}', 'wb') as file:
            pickle.dump(common_hex, file)

    # --All Done!---#
        return redirect(url_for('library'))

    return render_template("create.html", year=year, form=form)


@app.route("/delete/<image>", methods = ['GET'])
def delete(image):
    os.remove(f"static/palettes/{image.strip('.jpg')}")
    os.remove(f"static/images/{image}")
    return redirect(url_for('library'))


@app.route("/download/<hex>", methods = ['GET', 'POST'])
def download(hex):
    with open(f'static/palettes/{hex}', 'rb') as file:
            hex_list=pickle.load(file)
    with open(f'static/palettes_text/{hex}.txt', 'w') as file:
        for listitem in hex_list:
            file.write(f'{listitem}\n')
    return send_from_directory ('static/palettes_text', f'{hex}.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
