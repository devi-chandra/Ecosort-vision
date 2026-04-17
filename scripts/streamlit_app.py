import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# ===== Load Model =====
model = load_model("../models/echosort_model.h5")

# ===== Class Labels =====
class_labels = {
    0: "Organic Waste (O)",
    1: "Recyclable Waste (R)"
}

# ===== Disposal Guide =====
disposal_guide = {
    "Organic Waste (O)": "Dispose in a compost bin. Suitable for natural decomposition.",
    "Recyclable Waste (R)": "Place in the recycling bin. Suitable for reuse or recycling industries."
}

# ===== Prediction Function =====
def predict_waste(img):
    img = img.resize((224, 224))
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    pred = model.predict(arr)
    result = 1 if pred[0][0] > 0.5 else 0

    return class_labels[result], disposal_guide[class_labels[result]]

# ==========================
#       Website UI
# ==========================

st.set_page_config(page_title="EchoSort Vision", page_icon="♻️", layout="centered")

# ===== Custom CSS for Beautiful UI =====
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
.title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    color: #2c3e50;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #7f8c8d;
}
.upload-box {
    padding: 20px;
    border-radius: 12px;
    background: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.result-box {
    padding: 20px;
    border-radius: 12px;
    background: #e8f5e9;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===== Title =====
st.markdown('<div class="title">EchoSort Vision ♻️</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Classify waste as Organic or Recyclable — Upload or Click a Photo</div>', unsafe_allow_html=True)
st.write("")

# ===== UI Section =====
with st.container():
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)

    st.subheader("📸 Take a Photo Using Camera")
    camera_input = st.camera_input("Click a picture")

    st.subheader("📁 Or Upload an Image")
    uploaded_img = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    st.markdown("</div>", unsafe_allow_html=True)

# ===== If user provides a photo =====
final_image = None

if camera_input is not None:
    final_image = Image.open(camera_input)

elif uploaded_img is not None:
    final_image = Image.open(uploaded_img)

# ===== Prediction Section =====
if final_image:
    st.image(final_image, caption="Input Image", use_column_width=True)

    if st.button("🔍 Classify Waste"):
        waste_type, instruction = predict_waste(final_image)

        st.markdown("""
        <div class="result-box">
            <h3>🟢 Prediction Result</h3>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"**Waste Type:** {waste_type}")
        st.info(f"**Disposal Instruction:** {instruction}")
