"""
Flask Web Application for Facial Emotion Recognition
Handles form submission, image processing, emotion detection, and database storage
"""

import os
import sqlite3
from datetime import datetime
import numpy as np
from io import BytesIO
from PIL import Image
import cv2

from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Emotion labels (must match training order)
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# Emotion feedback messages
EMOTION_MESSAGES = {
    'angry': "You look angry. Everything okay?",
    'disgust': "You seem disgusted. Is something wrong?",
    'fear': "You appear fearful. Don't worry, you're safe!",
    'happy': "You're smiling! Great to see you happy!",
    'neutral': "You have a neutral expression. What's on your mind?",
    'sad': "You look sad. Why are you sad?",
    'surprise': "You look surprised! What's the news?"
}

# Cascade classifier for face detection
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    """Initialize database if not exists"""
    db_path = 'database.db'
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                detected_emotion TEXT NOT NULL,
                emotion_confidence REAL,
                image_data BLOB NOT NULL,
                submission_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                feedback_message TEXT
            )
        ''')
        conn.commit()
        conn.close()

def save_to_database(name, emotion, confidence, image_bytes, feedback_message):
    """Save user submission to database"""
    try:
        db_path = 'database.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users_submissions 
            (name, detected_emotion, emotion_confidence, image_data, feedback_message)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, emotion, confidence, image_bytes, feedback_message))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False

def preprocess_image(image_path):
    """
    Load and preprocess image for model prediction
    Returns: preprocessed image array and original image
    """
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            return None, None
        
        # Detect faces
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None, None
        
        # Use the largest face detected
        (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
        
        # Crop face region
        face_roi = gray[y:y+h, x:x+w]
        
        # Resize to model input size (48x48)
        face_roi = cv2.resize(face_roi, (48, 48))
        
        # Normalize
        face_roi = face_roi.astype('float32') / 255.0
        
        # Reshape for model (add batch and channel dimensions)
        face_roi = np.expand_dims(face_roi, axis=0)  # Add batch dimension
        face_roi = np.expand_dims(face_roi, axis=-1)  # Add channel dimension
        
        return face_roi, img
    
    except Exception as e:
        print(f"Image preprocessing error: {e}")
        return None, None

def predict_emotion(model, image_array):
    """
    Predict emotion from preprocessed image
    Returns: emotion label and confidence score
    """
    try:
        predictions = model.predict(image_array, verbose=0)
        emotion_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][emotion_idx])
        
        emotion = EMOTIONS[emotion_idx]
        return emotion, confidence
    
    except Exception as e:
        print(f"Prediction error: {e}")
        return None, 0.0

def get_image_bytes(image_path):
    """Read image file and return as bytes"""
    try:
        with open(image_path, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading image: {e}")
        return None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle image upload and emotion prediction
    Expected: form data with 'name' and 'image' file
    Returns: JSON with emotion prediction and feedback
    """
    try:
        # Check if form has required fields
        if 'name' not in request.form or 'image' not in request.files:
            return jsonify({'error': 'Name and image are required'}), 400
        
        name = request.form.get('name', '').strip()
        image_file = request.files['image']
        
        # Validate name
        if not name or len(name) < 2:
            return jsonify({'error': 'Please enter a valid name'}), 400
        
        # Validate file
        if image_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(image_file.filename):
            return jsonify({'error': 'Invalid file type. Use JPG, PNG, GIF, or BMP'}), 400
        
        if image_file.content_length > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large. Maximum 5MB'}), 400
        
        # Save uploaded file temporarily
        temp_path = os.path.join(UPLOAD_FOLDER, f'temp_{datetime.now().timestamp()}.jpg')
        image_file.save(temp_path)
        
        # Load trained model
        model_path = 'face_emotionModel.h5'
        if not os.path.exists(model_path):
            return jsonify({'error': 'Model not found. Please train the model first'}), 500
        
        model = load_model(model_path)
        
        # Preprocess image
        processed_image, original_image = preprocess_image(temp_path)
        
        if processed_image is None:
            os.remove(temp_path)
            return jsonify({'error': 'No face detected in image. Please upload a clear face image'}), 400
        
        # Predict emotion
        emotion, confidence = predict_emotion(model, processed_image)
        
        if emotion is None:
            os.remove(temp_path)
            return jsonify({'error': 'Emotion prediction failed'}), 500
        
        # Generate feedback message
        feedback_message = EMOTION_MESSAGES.get(emotion, f"You look {emotion}")
        
        # Get image bytes for database
        image_bytes = get_image_bytes(temp_path)
        
        # Save to database
        save_to_database(name, emotion, confidence, image_bytes, feedback_message)
        
        # Clean up temp file
        os.remove(temp_path)
        
        # Return response
        return jsonify({
            'success': True,
            'name': name,
            'emotion': emotion,
            'confidence': round(confidence * 100, 2),
            'message': feedback_message
        }), 200
    
    except Exception as e:
        print(f"Error in /predict route: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/submissions', methods=['GET'])
def get_submissions():
    """
    Retrieve all submissions from database
    Returns: JSON list of submissions
    """
    try:
        db_path = 'database.db'
        if not os.path.exists(db_path):
            return jsonify({'submissions': []}), 200
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, detected_emotion, emotion_confidence, 
                   submission_timestamp, feedback_message
            FROM users_submissions
            ORDER BY submission_timestamp DESC
            LIMIT 100
        ''')
        
        submissions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'submissions': submissions}), 200
    
    except Exception as e:
        print(f"Error fetching submissions: {e}")
        return jsonify({'error': 'Failed to fetch submissions'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for deployment monitoring"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run Flask app
    # For development: debug=True, host='localhost', port=5000
    # For production (Render): use host='0.0.0.0' and port from environment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
