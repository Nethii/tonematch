## ToneMatch 

ToneMatch is a web app I built for my final year project — it looks at a photo of your face, works out your skin tone and undertone, and then suggests makeup, clothing and hair colours that actually suit you.



# Features

AI-powered skin tone detection - using MediaPipe facial landmark detection
Colour space analysis - in RGB, HSV and LAB colour spaces using OpenCV
Skin tone classification into 5 categories — Fair, Light, Medium, Tan, Deep
Undertone detection — Warm, Cool or Neutral
Personalised recommendations - for makeup, clothing and hair colours
User authentication — register, login, logout
Result history — all analyses saved to database and viewable anytime
Profile management — update name, email and password
Responsive design — works on desktop and mobile browsers



# Tech Stack

Language - Python 3.10+ 
Web Framework - Flask 3.0.0 
Face Detection - MediaPipe Face Landmarker 
Image Processing - OpenCV (cv2) 
Database ORM - Flask-SQLAlchemy 
Database - MySQL 
Authentication - Flask-Login 
Frontend - HTML, CSS, JavaScript 
Fonts - DM Sans, DM Serif Display 



# System Architecture


User uploads image
       ↓
Face Detection (MediaPipe)
       ↓
Skin Region Extraction (OpenCV)
       ↓
Colour Space Analysis (LAB, HSV, RGB)
       ↓
Skin Tone Classification
       ↓
Recommendation Engine
       ↓
Results saved to MySQL database
       ↓
Results displayed to user



# Database Structure

Three tables:

- users — stores user accounts (id, name, email, password, created_at)
- results — stores each analysis (id, user_id, skin_tone, undertone, hex_colour, image_path, created_at)
- recommendations — stores individual colour recommendations (id, result_id, category, subcategory, colour_name)



# Project Structure


skin-tone-app/
├── app.py                      # Flask application factory
├── wsgi.py                     # WSGI entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
│
├── modules/
│   ├── face_detector.py        # MediaPipe face detection
│   ├── skin_extractor.py       # OpenCV skin region extraction
│   ├── skin_classifier.py      # LAB colour space classification
│   └── recommender.py          # Colour recommendation engine
│
├── database/
│   └── models.py               # SQLAlchemy database models
│
├── routes/
│   ├── auth.py                 # Login, register, logout routes
│   └── main.py                 # Main application routes
│
├── templates/
│   ├── landing.html            # Public landing page
│   ├── login.html              # Login page
│   ├── register.html           # Register page
│   ├── index.html              # Analyse page
│   ├── results.html            # Results page
│   ├── history.html            # History page
│   └── profile.html            # Profile page
│
└── static/
    ├── css/                    # Stylesheets
    ├── js/                     # JavaScript
    └── uploads/                # Uploaded images (not in repo)



# Installation and Setup

 Prerequisites

- Python 3.10 or above
- MySQL 8.0 or above
- pip

 Steps

1. Clone the repository
```bash
git clone https://github.com/Nethii/tonematch.git
cd tonematch
```

2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create the database

Open MySQL Workbench and run:
```bash
CREATE DATABASE tonematch;
```

5. Create a `.env` file

Create a file called `.env` in the project root:
```bash
SECRET_KEY=your_secret_key_here
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=tonematch
```

6. Run the application
```bash
python app.py
```

7. Open in browser

http://127.0.0.1:5000

The database tables will be created automatically on first run.



# Usage

1. Go to `http://127.0.0.1:5000`
2. Register a new account or sign in
3. Click "Analyse" in the navigation
4. Upload a clear, front-facing portrait photo
5. Click "Analyse my skin tone"
6. View your personalised colour recommendations
7. Find all past results in "History"


# Photo Guidelines

For best results:
- Use a clear, front-facing photo
- Natural lighting works best
- No filters or heavy editing
- Face should be clearly visible
- JPG or PNG format, max 10MB


# Limitations

- It needs a clear, front-facing shot — side profiles don't really work
- Accuracy depends on image quality and lighting conditions
- The system uses a rule-based recommendation engine rather than a trained ML model
- Recommendations are based on established colour theory principles


# Author

Nethmi Bandusena
BSc (Hons) Computer Science
University of Bedfordshire
2026