import os
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from .utils import classify_image

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/classify/<disease>', methods=['GET', 'POST'])
def classify(disease):
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            static_filepath = os.path.join('app/static/images', filename)
            file.save(filepath)
            file.save(static_filepath)  # Save to static folder
            result = classify_image(filepath, disease)
            return render_template('classify.html', disease=disease, result=result, filepath=static_filepath)
    return render_template('classify.html', disease=disease)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}
