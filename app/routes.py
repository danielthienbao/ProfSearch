from flask import Blueprint, render_template, request
from app.utils import extract_text_with_pdfplumber, search_by_class
import os

routes = Blueprint("routes", __name__)
UPLOAD_FOLDER = "uploads"

@routes.route("/", methods=["GET", "POST"])
def index():
    result_table = None
    if request.method == "POST":
        uploaded_file = request.files['file']
        class_name = request.form['class_name'].strip().upper()
        if uploaded_file:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)
            full_text = extract_text_with_pdfplumber(file_path)
            result_table = search_by_class(full_text, class_name)
    return render_template("index.html", result_table=result_table)
