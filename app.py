import os
import json
import joblib

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file
)

from werkzeug.utils import secure_filename

from pdfminer.high_level import extract_text as extract_pdf_text

from docx import Document

from resume_parser import parse_resume


# =========================================================
# FLASK CONFIGURATION
# =========================================================

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# LOAD TRAINED MODEL
# =========================================================

classifier = joblib.load(
    "resume_classifier.pkl"
)

tfidf = joblib.load(
    "tfidf_vectorizer.pkl"
)

model_info = joblib.load(
    "model_info.pkl"
)


# =========================================================
# FILE VALIDATION
# =========================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# EXTRACT TEXT FROM PDF
# =========================================================

def extract_pdf(filepath):

    try:

        text = extract_pdf_text(filepath)

        return text

    except Exception as e:

        print("PDF extraction error:", e)

        return ""


# =========================================================
# EXTRACT TEXT FROM DOCX
# =========================================================

def extract_docx(filepath):

    try:

        document = Document(filepath)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
        ]

        return "\n".join(paragraphs)

    except Exception as e:

        print("DOCX extraction error:", e)

        return ""


# =========================================================
# EXTRACT TEXT FROM TXT
# =========================================================

def extract_txt(filepath):

    try:

        with open(
            filepath,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            return file.read()

    except Exception as e:

        print("TXT extraction error:", e)

        return ""


# =========================================================
# GENERAL TEXT EXTRACTION
# =========================================================

def extract_resume_text(filepath):

    extension = filepath.rsplit(
        ".",
        1
    )[1].lower()

    if extension == "pdf":

        return extract_pdf(filepath)

    elif extension == "docx":

        return extract_docx(filepath)

    elif extension == "txt":

        return extract_txt(filepath)

    return ""


# =========================================================
# CLEAN TEXT FOR CLASSIFIER
# =========================================================

def clean_text(text):

    import re
    import string

    text = str(text)

    text = text.lower()

    text = re.sub(
        r"http\S+|www\S+|https\S+",
        " ",
        text
    )

    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        " ",
        text
    )

    text = re.sub(
        r"<.*?>",
        " ",
        text
    )

    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )

    text = re.sub(
        r"\d+",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================================
# RESUME PARSING
# =========================================================

@app.route(
    "/parse",
    methods=["POST"]
)
def parse():

    if "resume" not in request.files:

        return jsonify({
            "error": "No resume file uploaded."
        }), 400

    file = request.files["resume"]

    if file.filename == "":

        return jsonify({
            "error": "Please select a file."
        }), 400

    if not allowed_file(file.filename):

        return jsonify({
            "error": "Only PDF, DOCX and TXT files are supported."
        }), 400

    filename = secure_filename(
        file.filename
    )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    # Extract raw resume text
    resume_text = extract_resume_text(
        filepath
    )

    if not resume_text.strip():

        return jsonify({
            "error": "Could not extract text from the resume."
        }), 400

    # -----------------------------------------
    # NLP INFORMATION EXTRACTION
    # -----------------------------------------

    parsed_data = parse_resume(
        resume_text
    )

    # -----------------------------------------
    # CATEGORY PREDICTION
    # -----------------------------------------

    cleaned_resume = clean_text(
        resume_text
    )

    vectorized_resume = tfidf.transform(
        [cleaned_resume]
    )

    predicted_category = classifier.predict(
        vectorized_resume
    )[0]

    parsed_data["category"] = predicted_category

    # -----------------------------------------
    # Save JSON
    # -----------------------------------------

    json_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "parsed_resume.json"
    )

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as json_file:

        json.dump(
            parsed_data,
            json_file,
            indent=4,
            ensure_ascii=False
        )

    return render_template(
        "index.html",
        result=parsed_data
    )


# =========================================================
# DOWNLOAD JSON
# =========================================================

@app.route(
    "/download-json"
)
def download_json():

    json_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "parsed_resume.json"
    )

    if not os.path.exists(json_path):

        return "No parsed resume available.", 404

    return send_file(
        json_path,
        as_attachment=True,
        download_name="parsed_resume.json",
        mimetype="application/json"
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )