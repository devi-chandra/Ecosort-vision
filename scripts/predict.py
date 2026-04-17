import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

# Load trained model
model_path = "../models/echosort_model.h5"
model = load_model(model_path)

# Class mapping
class_labels = {
    0: "Organic Waste (O)",
    1: "Recyclable Waste (R)"
}

# Disposal guide
disposal_guide = {
    "Organic Waste (O)": "Dispose in a compost bin. Suitable for natural decomposition.",
    "Recyclable Waste (R)": "Place in the recycling bin. Suitable for reuse or recycling industries."
}

def predict_waste(img_path):
    # Load the image
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Make prediction
    prediction = model.predict(img_array)
    result = 1 if prediction[0][0] > 0.5 else 0
    waste_type = class_labels[result]

    # Print result
    print("\n=========================================")
    print(f"Predicted Waste Type: {waste_type}")
    print(f"Disposal Instruction: {disposal_guide[waste_type]}")
    print("=========================================\n")

# Example test
predict_waste("../data/test/R/R_10000.jpg")


