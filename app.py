import os
import sys
import subprocess
import requests
import ssl
import random
import string
import json

import colorgram

from flask import jsonify
from flask import Flask
from flask import request
import traceback

from app_utils import download
from app_utils import generate_random_filename
from app_utils import clean_me
from app_utils import clean_all
from app_utils import create_directory
from app_utils import get_model_bin
from app_utils import get_multi_model_bin


try:  # Python 3.5+
    from http import HTTPStatus
except ImportError:
    try:  # Python 3
        from http import client as HTTPStatus
    except ImportError:  # Python 2
        import httplib as HTTPStatus


app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/detect", methods=["POST"])
def detect():

    input_path = generate_random_filename(upload_directory,"jpg")

    try:
        if 'file' in request.files:
            file = request.files['file']
            if allowed_file(file.filename):
                file.save(input_path)
            try:
                nb_colors = request.form.getlist('nb_colors')[0]
            except:
                nb_colors = 5
        else:
            url = request.json["url"]
            download(url, input_path)

            nb_colors = request.json["nb_colors"]

       
        results = []

        colors = colorgram.extract(input_path, nb_colors)

        for color in colors:
            results.append({
                'R': color.rgb.r,
                'G': color.rgb.g,
                'B': color.rgb.b,
                'H': color.hsl.h,
                'S': color.hsl.s,
                'L': color.hsl.l,
                'HEX': '#%02x%02x%02x' % (color.rgb.r, color.rgb.g, color.rgb.b)
                })

        return json.dumps(results), 200


    except:
        traceback.print_exc()
        return {'message': 'input error'}, 400


    finally:
        clean_all([
            input_path
        ])


if __name__ == '__main__':
    global upload_directory
    global model, graph
    global img_width, img_height
    global class_names
    global ALLOWED_EXTENSIONS
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    

    upload_directory = '/src/upload/'
    create_directory(upload_directory)

    port = 5000
    host = '0.0.0.0'

    app.run(host=host, port=port, threaded=True)

