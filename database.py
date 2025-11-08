"""
Database initialization script for Facial Emotion Recognition project
Creates SQLite database schema for storing user submissions and images
"""

import sqlite3
import os

def init_database(db_path):
    """
    Initialize the SQLite database with required tables
    """
    # Create database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users_submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            detected_emotion TEXT NOT NULL,
            emotion_confidence REAL,
            image_data BLOB NOT NULL,
            submission_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            feedback_message TEXT
        )
    ''')
    
    conn.commit()
    print(f"✓ Database initialized at: {db_path}")
    print("✓ Table 'users_submissions' created successfully")
    
    # Verify the table was created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"✓ Tables in database: {[table[0] for table in tables]}")
    
    conn.close()

if __name__ == '__main__':
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'database.db')
    
    if os.path.exists(db_path):
        print(f"Database already exists at {db_path}")
        print("Skipping initialization (database will be updated if needed)")
    else:
        print("Creating new database...")
        init_database(db_path)
