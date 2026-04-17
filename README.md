# EcoSort Vision ♻️

EcoSort Vision is an AI-assisted waste segregation web application that helps users identify waste as **Organic Waste** or **Recyclable Waste** using image upload or camera capture.

The system is designed to support smarter waste management by combining image classification, waste level estimation, and harmful waste alerts in a clean and user-friendly interface.

---

## 🚀 Features

- 📤 Upload image for waste classification  
- 📷 Capture image using camera  
- 🤖 Predicts:
  - Organic Waste (O)
  - Recyclable Waste (R)
- ⚠️ Detects possible harmful waste objects (battery-like items)
- 📊 Estimates waste level:
  - Low Waste
  - Medium Waste
  - High Waste
- 🎨 Responsive modern UI/UX
- 🌐 Flask-based web application

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### AI / Image Processing
- TensorFlow / Keras
- OpenCV
- NumPy
- Pillow

---

## 📂 Project Structure

```text
EchoSort-vision/
│ README.md
│ requirements.txt
│ .gitignore
│
├── data/
│   ├── train/
│   │   ├── O/
│   │   └── R/
│   └── test/
│       ├── O/
│       └── R/
│
├── models/
│   └── echosort_model.h5
│
├── scripts/
│   ├── train_model.py
│   ├── predict.py
│   └── streamlit_app.py
│
└── webapp/
    ├── app.py
    ├── templates/
    │   ├── index.html
    │   ├── result.html
    │   └── capture.html
    │
    └── static/
        ├── css/
        │   └── style.css
        ├── js/
        │   └── script.js
        └── uploads/

⚙️ Installation & Setup
1️⃣ Clone Repository

 git clone https://github.com/YOUR_USERNAME/EcoSort-Vision.git
 cd EcoSort-Vision

2️⃣ Create Virtual Environment

 python -m venv venv

3️⃣ Activate Virtual Environment

 Windows
  venv\Scripts\activate
 Mac/Linux
  source venv/bin/activate

4️⃣ Install Dependencies

 pip install -r requirements.txt

5️⃣ Run Application

 cd webapp
 python app.py

6️⃣ Open in Browser

http://127.0.0.1:5000

🧠 How It Works
1.User uploads or captures a waste image.
2.Image is preprocessed for classification.
3.AI model predicts waste type.
4.Additional modules analyze:
  >waste level
  >Harmful waste objects
  >Multi-item scan
5.Results displayed instantly.

📌 Notes
 >Includes fallback compatibility mode if legacy model loading fails.
 >Lightweight sample dataset included.
 >Designed as a student innovation project for sustainable waste management.

🔮 Future Enhancements
 >Add more waste categories (plastic, metal, glass, e-waste)
 >Real-time webcam detection
 >Mobile application
 >Cloud deployment
 >Smart dustbin integration using IoT
 >User dashboard with analytics

💼 Use Case

This project can be useful for:

  >Smart cities
  >Educational institutions
  >Waste collection agencies
  >Recycling centers
  >Public awareness campaigns

👨‍💻 Author

J DEVI
Computer Science Engineering (AI & DS)

⭐ Support

If you found this project useful, give it a ⭐.
