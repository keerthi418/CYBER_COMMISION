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
http://127.0.0.1:10000/login

## Deployment

### Heroku Deployment

1. **Prerequisites:**
   - Heroku CLI installed
   - Git repository initialized

2. **Environment Setup:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. **Deploy to Heroku:**
   ```bash
   heroku create your-app-name
   heroku config:set SECRET_KEY=your_secret_key
   heroku config:set EMAIL_SENDER=your_email@gmail.com
   heroku config:set EMAIL_PASSWORD=your_app_password
   heroku config:set EMAIL_RECEIVER=admin@cyberguard.com
   git add .
   git commit -m "Prepare for deployment"
   git push heroku main
   ```

4. **Open your app:**
   ```bash
   heroku open
   ```

### Other Platforms

- **Railway:** Connect your GitHub repo, Railway will auto-detect Python
- **Render:** Set build command `pip install -r requirements.txt` and start command `gunicorn app:app`
- **Local Production:** Run `gunicorn --bind 0.0.0.0:8000 app:app`

### Environment Variables Required

- `SECRET_KEY`: Flask secret key for sessions
- `EMAIL_SENDER`: Email address for notifications
- `EMAIL_PASSWORD`: App password for email
- `EMAIL_RECEIVER`: Admin email for notifications

