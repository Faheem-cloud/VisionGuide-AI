import os
from uuid import uuid4
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from modules.vision import analyze_image

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "Please select or capture an image."}), 400
    image = request.files["image"]
    if not image.filename or not allowed_file(image.filename):
        return jsonify({"error": "Upload a PNG, JPG, JPEG, or WEBP image."}), 400

    safe_name = secure_filename(image.filename)
    filename = f"{uuid4().hex}_{safe_name}"
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(path)
    try:
        result = analyze_image(path)
        return jsonify(result)
    except Exception as exc:
        app.logger.exception("Image analysis failed")
        return jsonify({"error": str(exc)}), 500
    finally:
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
