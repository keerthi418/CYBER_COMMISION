# Cyber Commission – Cybercrime Complaint & Detection System

## Project Description
Cyber Commission is a web-based application designed to help users report cybercrime complaints and analyze them using machine learning techniques.

The system allows users to submit cybercrime complaints and predicts the type of cybercrime using a trained machine learning model.

## Features
- User can submit cybercrime complaints
- Machine learning model predicts cybercrime category
- Complaint history stored in database
- Simple web interface for interaction
- Admin can view complaint records

## Technologies Used
Frontend:
- HTML
- CSS

Backend:
- Python
- Flask

Machine Learning:
- Scikit-learn
- NLP Text Vectorization

Database:
- SQLite

## Files in Project
- app.py – Main Flask application
- model.py – ML model logic
- train_model.py – Model training script
- cybercrime_dataset.csv – Dataset used for training
- vectorizer.pkl – NLP vectorizer
- model.pkl – Trained ML model
- complaints.db – Database for storing complaints

## How to Run the Project

1. Install Python dependencies
2. pip install -r requirements.txt
3. 2. Run the Flask app
python app.py3. Open browser and go to
http://127.0.0.1:5000
