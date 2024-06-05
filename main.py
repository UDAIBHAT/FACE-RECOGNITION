import sqlite3
import cv2
import numpy as np
import face_recognition
import os
import pyttsx3
import threading
import logging
import signal
import sys

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
IMAGE_DIR = 'images'
CONFIDENCE_THRESHOLD = 0.6
TEXT_TO_SPEECH_VOICE = 0  # Index of the desired voice

# Initialize text-to-speech engine
speaker = pyttsx3.init()
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[TEXT_TO_SPEECH_VOICE].id)
tts_lock = threading.Lock()  # Lock to ensure TTS thread safety

# Database Constants
DATABASE_NAME = 'user_database.db'

# Initialize database connection
conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

def create_user_table():
    """Create a table to store user information if it doesn't exist."""
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY, name TEXT, encoding BLOB)''')
    conn.commit()

def register_user(name, encoding):
    """Register a new user in the database."""
    cursor.execute("INSERT INTO users (name, encoding) VALUES (?, ?)", (name, encoding))
    conn.commit()
    print(f"User '{name}' registered successfully.")

def load_user_encodings():
    """Load user encodings from the database."""
    cursor.execute("SELECT name, encoding FROM users")
    rows = cursor.fetchall()
    return rows

def authenticate_user(encode_face):
    """Authenticate the user by comparing their face encoding with the encodings in the database."""
    users = load_user_encodings()
    for user_name, user_encoding in users:
        user_encoding = np.frombuffer(user_encoding, dtype=np.float64)
        match = face_recognition.compare_faces([user_encoding], encode_face, tolerance=CONFIDENCE_THRESHOLD)[0]
        if match:
            return user_name
    return None

def signal_handler(sig, frame):
    logger.info('You pressed Ctrl+C! Exiting gracefully.')
    sys.exit(0)

def load_images(image_dir):
    """Load images from the specified directory and extract class names."""
    images = []
    class_names = []
    try:
        image_files = os.listdir(image_dir)
        logger.info("Image files found: %s", image_files)
        for file in image_files:
            img_path = os.path.join(image_dir, file)
            current_img = cv2.imread(img_path)
            if current_img is not None:
                images.append(current_img)
                class_names.append(os.path.splitext(file)[0])
            else:
                logger.warning("Could not read image %s", img_path)
        logger.info("Class names: %s", class_names)
    except Exception as e:
        logger.error("Error loading images: %s", e)
    return images, class_names

def find_encodings(images):
    """Find and return face encodings for a list of images."""
    encoding_list = []
    for img in images:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img_rgb)
        if encodes:  # Check if face encodings were found
            encoding_list.append(encodes[0])
        else:
            logger.warning("No face encodings found for an image.")
    return encoding_list

def speak_message(message):
    """Use text-to-speech to speak a given message."""
    try:
        with tts_lock:
            speaker.say(message)
            speaker.runAndWait()
    except Exception as e:
        logger.error("Error speaking message: %s", e)

def perform_post_authentication_tasks(name):
    """Perform tasks after successful authentication."""
    logger.info(f"Performing post-authentication tasks for {name}")
    # Add your tasks here
    # For example:
    print(f"Welcome {name}! You have been authenticated.")
    # more tasks.

def register_faces():
    """Register new users by capturing their faces."""
    try:
        create_user_table()
        while True:
            name = input("Enter your name or 'q' to quit: ")
            if name.lower() == 'q':
                break
            print("Please look at the camera and press 'r' to take a picture.")
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                cv2.imshow('Registration', frame)
                if cv2.waitKey(1) & 0xFF == ord('r'):
                    cv2.imwrite(f'images/{name}.jpg', frame)
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    encoding = face_recognition.face_encodings(img)[0]
                    register_user(name, encoding.tobytes())
                    break
            cap.release()
            cv2.destroyAllWindows()
    except Exception as e:
        logger.error("Error in user registration: %s", e)

def authenticate_faces():
    """Perform real-time face authentication using the webcam."""
    try:
        images, _ = load_images(IMAGE_DIR)
        encode_list_known = find_encodings(images)
        logger.info('Encodings Done')
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.error("Error opening webcam.")
            return
        authenticated = False
        while not authenticated:
            success, img = cap.read()
            if not success:
                logger.error("Failed to capture frame from webcam.")
                break
            img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)
            faces_curr_frame = face_recognition.face_locations(img_s)
            encodes_curr_frame = face_recognition.face_encodings(img_s, faces_curr_frame)
            for encode_face, face_loc in zip(encodes_curr_frame, faces_curr_frame):
                name = authenticate_user(encode_face)
                if name:
                    logger.info("Authenticated: %s", name)
                    threading.Thread(target=speak_message, args=(f"Welcome {name}",)).start()
                    authenticated = True
                    y1, x2, y2, x1 = face_loc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    break
            if not authenticated:
                logger.info("Authentication failed")
                threading.Thread(target=speak_message, args=("Authentication failed",)).start()
            cv2.imshow('Webcam', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        if authenticated:
            perform_post_authentication_tasks(name)
    except Exception as e:
        logger.error("Error in face authentication: %s", e)
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    register_faces()  # Register new users
    authenticate_faces()  # Authenticate users            
