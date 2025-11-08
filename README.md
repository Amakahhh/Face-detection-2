# Facial Emotion Recognition - Web Application

A machine learning-based web application that detects emotions from facial images and saves user submissions to a database.

## 📋 Project Structure

```
FACE_DETECTION/
├── app.py                    # Flask web application
├── model_training.py         # CNN model training script
├── database.py               # Database initialization
├── requirements.txt          # Python dependencies
├── face_emotionModel.h5      # Trained emotion detection model
├── database.db               # SQLite database (auto-created)
├── link_web_app.txt          # Render deployment link
├── .gitignore                # Git ignore rules
├── templates/
│   └── index.html            # Web interface
└── uploads/                  # Temporary image uploads (auto-created)
```

## 🎯 Features

- **Facial Emotion Detection**: Recognizes 7 emotions (angry, disgust, fear, happy, neutral, sad, surprise)
- **Simple Web Interface**: HTML form with name input and image upload
- **Real-time Feedback**: Personalized messages based on detected emotion
- **Database Storage**: Saves submissions with name, emotion, confidence, and image
- **Submissions History**: View all submitted entries with timestamps
- **Mobile Responsive**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model (One-time setup)
```bash
python model_training.py
```
**Note**: This requires training data in `../train/` folder with emotion subfolders.
Training takes 5-10 minutes depending on your hardware.

### 3. Run the Flask App
```bash
python app.py
```
The app will start at `http://localhost:5000`

## 📖 Usage

1. Open the web application
2. Enter your name
3. Upload a clear photo of your face
4. Click "Detect Emotion"
5. View your emotion prediction and feedback message
6. See all submissions in the "Recent Submissions" section

## 🧠 How It Works

1. **Image Upload**: User uploads an image via the web form
2. **Face Detection**: OpenCV detects face(s) in the image
3. **Preprocessing**: Face is cropped, resized to 48x48, and normalized
4. **Emotion Prediction**: CNN model predicts emotion (0-1 confidence for each class)
5. **Database Storage**: Result and image stored in SQLite database
6. **Feedback**: User receives personalized message based on emotion

## 🔧 Model Architecture

```
Input (48x48x1 grayscale image)
    ↓
Conv2D(32) → BatchNorm → ReLU → Conv2D(32) → BatchNorm → MaxPool → Dropout
    ↓
Conv2D(64) → BatchNorm → ReLU → Conv2D(64) → BatchNorm → MaxPool → Dropout
    ↓
Conv2D(128) → BatchNorm → ReLU → Conv2D(128) → BatchNorm → MaxPool → Dropout
    ↓
Flatten
    ↓
Dense(256) → BatchNorm → ReLU → Dropout
    ↓
Dense(128) → BatchNorm → ReLU → Dropout
    ↓
Dense(7) → Softmax (Output: emotion probabilities)
```

## 📊 Supported Emotions

1. **Angry** - Detected from furrowed brows, tight lips
2. **Disgust** - Detected from wrinkled nose, raised upper lip
3. **Fear** - Detected from wide eyes, raised eyebrows
4. **Happy** - Detected from raised cheeks, smile
5. **Neutral** - Detected from relaxed facial features
6. **Sad** - Detected from lowered eyebrows, downturned mouth
7. **Surprise** - Detected from raised eyebrows, open mouth

## 🗄️ Database Schema

**users_submissions table:**
- `id`: INTEGER PRIMARY KEY (auto-increment)
- `name`: TEXT (student name)
- `detected_emotion`: TEXT (emotion category)
- `emotion_confidence`: REAL (0-1 confidence score)
- `image_data`: BLOB (stored image file)
- `submission_timestamp`: DATETIME (submission time)
- `feedback_message`: TEXT (personalized response)

## 🐛 Troubleshooting

### Model not found error
**Solution**: Run `python model_training.py` first to train the model

### No face detected error
**Solution**: Ensure the image shows a clear, frontal face

### Port already in use
**Solution**: Run on a different port:
```bash
python -c "from app import app; app.run(host='0.0.0.0', port=5001)"
```

### Database locked error
**Solution**: Close any existing Flask instances and try again

## 📝 API Endpoints

- `GET /` - Serves the main web interface
- `POST /predict` - Process image and predict emotion
  - **Input**: Form data with `name` and `image` file
  - **Output**: JSON with emotion, confidence, and message
- `GET /submissions` - Retrieve all submissions
  - **Output**: JSON array of all submissions
- `GET /health` - Health check endpoint
  - **Output**: JSON with status and timestamp

## 🌐 Deployment (Render)

1. Push code to GitHub repository
2. Connect Render to GitHub
3. Create new Web Service on Render
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python app.py`
6. Add environment variable: `PORT=10000`
7. Deploy and copy the deployment link to `link_web_app.txt`

## ⚠️ Important Notes

- **Training Data**: Ensure `../train/` and `../test/` folders exist with emotion subfolders
- **Face Detection**: Works best with clear, frontal face images
- **Image Size Limit**: Maximum 5MB per image
- **Supported Formats**: JPG, PNG, GIF, BMP
- **Database**: Created automatically on first run as `database.db`

## 🔒 Security Features

- File type validation (only image formats allowed)
- File size limit enforcement (5MB max)
- HTML escaping for XSS prevention
- CSRF protection ready (add if needed)
- Secure model loading
- Safe database operations with parameterized queries

## 📈 Future Improvements

- Model accuracy optimization
- Real-time video stream support
- Multiple face detection and analysis
- Emotion statistics and trends
- User authentication and profiles
- Model confidence threshold tuning
- Batch image upload
- Export results as CSV/PDF

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Created as an AI assignment for CSC 415.

## 📞 Support

For issues or questions, refer to the code comments and error messages provided by the application.
