from flask import Flask, render_template, request
import numpy as np
from PIL import Image
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ----------------------------------------------------------
# SAFE MODEL LOAD (fallback if old .h5 breaks)
# ----------------------------------------------------------
MODEL_PATH = os.path.join(app.root_path, "..", "models", "echosort_model.h5")

model = None

try:
    from tensorflow.keras.models import load_model
    model = load_model(MODEL_PATH, compile=False)
    print("AI model loaded successfully.")
except Exception as e:
    print("Model failed to load. Running in fallback mode.")
    print(e)

# ----------------------------------------------------------
# CLASSES
# ----------------------------------------------------------
class_labels = {
    0: "Organic Waste (O)",
    1: "Recyclable Waste (R)"
}

disposal_guide = {
    "Organic Waste (O)": "Place in compost bin.",
    "Recyclable Waste (R)": "Place in recycling bin.",
    "Unidentified Waste (U)": "Waste unclear — please sort manually."
}

# ----------------------------------------------------------
# STATIC UPLOAD FOLDER
# ----------------------------------------------------------
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ----------------------------------------------------------
# MAIN CLASSIFIER
# ----------------------------------------------------------
def predict_waste(img_path):
    img = Image.open(img_path).convert("RGB").resize((224, 224))

    arr = np.array(img) / 255.0
    arr = arr.reshape(1, 224, 224, 3)

    # If actual AI model loads
    if model is not None:
        pred = model.predict(arr, verbose=0)[0][0]
        confidence = pred if pred > 0.5 else (1 - pred)

        if confidence < 0.60:
            waste_type = "Unidentified Waste (U)"
        else:
            waste_type = class_labels[1 if pred > 0.5 else 0]

    else:
        # Smart fallback logic
        mean_green = np.mean(arr[:, :, :, 1])
        mean_blue = np.mean(arr[:, :, :, 2])
        mean_red = np.mean(arr[:, :, :, 0])

        if mean_green > mean_blue and mean_green > mean_red:
            waste_type = "Organic Waste (O)"
        else:
            waste_type = "Recyclable Waste (R)"

    instruction = disposal_guide[waste_type]
    return waste_type, instruction

# ----------------------------------------------------------
# MULTI PATCH DETECTION
# ----------------------------------------------------------
def scan_patches(img):
    h, w, _ = img.shape
    size = 160
    detected = []

    for y in range(0, h, size):
        for x in range(0, w, size):
            patch = img[y:y+size, x:x+size]

            if patch.shape[0] < 160 or patch.shape[1] < 160:
                continue

            avg = np.mean(patch)

            if avg < 100:
                detected.append("Organic Waste (O)")
            else:
                detected.append("Recyclable Waste (R)")

    return list(set(detected)) if detected else ["Unidentified Waste (U)"]

# ----------------------------------------------------------
# WASTE LEVEL
# ----------------------------------------------------------
def estimate_waste_level(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    non_empty_pixels = np.count_nonzero(gray < 200)

    if non_empty_pixels < 20000:
        return "Low Waste"
    elif non_empty_pixels < 80000:
        return "Medium Waste"
    else:
        return "High Waste"

# ----------------------------------------------------------
# HARMFUL WASTE
# ----------------------------------------------------------
def detect_harmful_waste(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([90, 120, 80])
    upper = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)

    if np.sum(mask) > 90000:
        return "⚠️ Possible battery-like object detected."

    return ""

# ----------------------------------------------------------
# ROUTES
# ----------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")

    if file is None or file.filename == "":
        return render_template(
            "result.html",
            error="No file selected."
        )

    filename = secure_filename(file.filename)

    allowed = ["png", "jpg", "jpeg"]
    ext = filename.rsplit(".", 1)[-1].lower()

    if ext not in allowed:
        return render_template(
            "result.html",
            error="Only PNG, JPG, JPEG files allowed."
        )

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        file.save(save_path)
    except Exception as e:
        return render_template(
            "result.html",
            error=str(e)
        )

    waste_type, instruction = predict_waste(save_path)

    img_cv = cv2.imread(save_path)

    if img_cv is None:
        return render_template(
            "result.html",
            error="Image can't be accessed."
        )

    detected_items = scan_patches(img_cv)
    waste_level = estimate_waste_level(img_cv)
    harmful_warning = detect_harmful_waste(img_cv)

    return render_template(
        "result.html",
        image_path="uploads/" + filename,
        waste_type=waste_type,
        instruction=instruction,
        detected_items=", ".join(detected_items),
        waste_level=waste_level,
        harmful_warning=harmful_warning
    )

@app.route("/capture")
def capture():
    return render_template("capture.html")

@app.route("/capture_upload", methods=["POST"])
def capture_upload():
    file = request.files.get("capturedImage")

    if not file:
        return render_template(
            "result.html",
            error="Failed to capture image."
        )

    filename = "captured.png"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    waste_type, instruction = predict_waste(save_path)

    img_cv = cv2.imread(save_path)

    detected_items = scan_patches(img_cv)
    waste_level = estimate_waste_level(img_cv)
    harmful_warning = detect_harmful_waste(img_cv)

    return render_template(
        "result.html",
        image_path="uploads/" + filename,
        waste_type=waste_type,
        instruction=instruction,
        detected_items=", ".join(detected_items),
        waste_level=waste_level,
        harmful_warning=harmful_warning
    )

# ----------------------------------------------------------
# RUN
# ----------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)