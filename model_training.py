"""
Facial Emotion Recognition Model Training Script
This script trains a CNN model on the FER2013-like dataset structure
(train/ and test/ folders with emotion subfolders)
"""

import os
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from pathlib import Path

# Define emotion categories
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
IMG_SIZE = 48
BATCH_SIZE = 64

def load_dataset(data_dir, emotions=EMOTIONS):
    """
    Load images from directory structure: data_dir/emotion_name/*.jpg
    Returns normalized images and labels
    """
    images = []
    labels = []
    
    for emotion_idx, emotion in enumerate(emotions):
        emotion_dir = os.path.join(data_dir, emotion)
        
        if not os.path.exists(emotion_dir):
            print(f"Warning: {emotion_dir} does not exist")
            continue
        
        print(f"Loading {emotion} images from {emotion_dir}...")
        
        for img_file in os.listdir(emotion_dir):
            if img_file.endswith(('.jpg', '.jpeg', '.png')):
                try:
                    img_path = os.path.join(emotion_dir, img_file)
                    # Load image as grayscale (emotions are grayscale in FER2013)
                    img = load_img(img_path, color_mode='grayscale', target_size=(IMG_SIZE, IMG_SIZE))
                    img_array = img_to_array(img) / 255.0  # Normalize to 0-1
                    
                    images.append(img_array)
                    labels.append(emotion_idx)
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")
                    continue
    
    return np.array(images), np.array(labels)

def create_model():
    """
    Create a CNN model for emotion classification
    Architecture: Conv2D -> MaxPool -> Conv2D -> MaxPool -> Dense layers
    """
    model = Sequential([
        # First Convolutional Block
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
        BatchNormalization(),
        Conv2D(32, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        
        # Second Convolutional Block
        Conv2D(64, (3, 3), activation='relu'),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        
        # Third Convolutional Block
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        
        # Flatten and Dense layers
        Flatten(),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(len(EMOTIONS), activation='softmax')  # Output layer for 7 emotions
    ])
    
    return model

def main():
    """
    Main training pipeline
    """
    print("=" * 60)
    print("FACIAL EMOTION RECOGNITION - MODEL TRAINING")
    print("=" * 60)
    
    # Get parent directory (where train/ and test/ folders are)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)  # Go up from FACE_DETECTION/
    
    train_dir = os.path.join(parent_dir, 'train')
    test_dir = os.path.join(parent_dir, 'test')
    
    print(f"\nLooking for training data in: {train_dir}")
    print(f"Looking for test data in: {test_dir}")
    
    # Load datasets
    print("\n[1/5] Loading training data...")
    X_train, y_train = load_dataset(train_dir)
    print(f"Training data shape: {X_train.shape}, Labels shape: {y_train.shape}")
    
    print("\n[2/5] Loading test data...")
    X_test, y_test = load_dataset(test_dir)
    print(f"Test data shape: {X_test.shape}, Labels shape: {y_test.shape}")
    
    if X_train.size == 0 or X_test.size == 0:
        print("ERROR: Could not load training or test data!")
        print("Make sure train/ and test/ folders exist with emotion subfolders")
        return
    
    # Convert labels to one-hot encoding
    y_train = keras.utils.to_categorical(y_train, len(EMOTIONS))
    y_test = keras.utils.to_categorical(y_test, len(EMOTIONS))
    
    print(f"\nProcessed y_train shape: {y_train.shape}")
    print(f"Processed y_test shape: {y_test.shape}")
    
    # Create model
    print("\n[3/5] Creating CNN model...")
    model = create_model()
    model.summary()
    
    # Compile model
    print("\n[4/5] Compiling model...")
    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Data augmentation for better generalization
    train_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2
    )
    
    # Train model
    print("\n[5/5] Training model (this may take a few minutes)...")
    history = model.fit(
        train_datagen.flow(X_train, y_train, batch_size=BATCH_SIZE),
        epochs=50,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    # Evaluate model
    print("\nEvaluating model on test data...")
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Accuracy: {test_accuracy * 100:.2f}%")
    print(f"Test Loss: {test_loss:.4f}")
    
    # Save model
    model_path = os.path.join(script_dir, 'face_emotionModel.h5')
    print(f"\nSaving model to {model_path}...")
    model.save(model_path)
    print("✓ Model saved successfully!")
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    main()
