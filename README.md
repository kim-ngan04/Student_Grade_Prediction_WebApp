# BKLG – AI-Powered Student Grade Prediction Application

BKLG is a web application that leverages Artificial Intelligence (AI) to support teachers and students in predicting academic performance. The primary goal of the application is to provide early insights into student outcomes, enabling timely adjustments in both teaching and learning processes.

## Application Objectives
- Grade Prediction: Utilize Machine Learning models to generate accurate predictions of student grades.
- Early Insights: Provide estimated scores before examinations to assist both teachers and students.
- Support for Teachers and Students: Facilitate efficient and effective monitoring of student progress.

## Key Features
- Manual data entry or CSV file import.
- Modern user interface built on Material Design standards.
- Smooth animations with intuitive usability.
- Integrated AI models for grade prediction.

## Frontend
- Flutter/Dart: Primary framework for cross-platform UI development.
- Material Design: Optimized UI/UX design for improved user experience.
- HTTP Package: Enables communication with backend APIs.

## Backend
- Python 3.8+: Core backend programming language.
- Flask: Lightweight and customizable web framework.
- Scikit-learn: Robust machine learning library.
- Pandas and NumPy: Data processing and analytical computing libraries.
- Joblib: Model serialization and deserialization tool.

## System Requirements

### Frontend
- Flutter SDK: Install the latest version from [Flutter Official](https://flutter.dev/docs/get-started/install).
- Dart SDK: Integrated with Flutter.
- IDE: Visual Studio Code or Android Studio.
- Git: Version control system.

### Backend
- Python 3.8+: Download from [Python Official](https://www.python.org/downloads/).
- pip: Python package manager.
- Required Libraries:
  - flask
  - pandas
  - scikit-learn
  - joblib
  - numpy

## Installation Guide

# ===== Backend Setup =====
# Step 1: Create virtual environment
python -m venv venv

# Step 2: Activate virtual environment
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Step 3: Install dependencies
pip install flask pandas scikit-learn joblib numpy

# Step 4: Start the server
cd backend
python app.py

# ===== Frontend Setup =====
# Step 1: Install Flutter SDK and Dart SDK as per the official guide:
# https://flutter.dev/docs/get-started/install

# Step 2: Clone the repository
git clone https://github.com/BaoHust2004/IntroAI20242

# Step 3: Navigate to frontend
cd frontend

# Step 4: Get dependencies
flutter pub get

# Step 5: Run the app
flutter run
