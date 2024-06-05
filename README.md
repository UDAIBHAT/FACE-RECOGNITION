# Facial Recognition System

This Python script implements a facial recognition system for user registration and authentication using OpenCV, face_recognition, SQLite3, and pyttsx3.

## Features

- **User Registration**: Capture and store face encodings in an SQLite database.
- **User Authentication**: Real-time face recognition and authentication.
- **Audible Feedback**: Provides text-to-speech feedback using pyttsx3.
- **Logging**: Comprehensive logging for debugging and information tracking.
- **Graceful Exit**: Handles interruptions (Ctrl+C) gracefully.

## Technologies Used

- **OpenCV**: For capturing and processing images from the webcam.
- **face_recognition**: For detecting and encoding facial features.
- **SQLite3**: For storing user information and face encodings.
- **pyttsx3**: For text-to-speech capabilities.
- **Threading and Locking**: To manage concurrent tasks and ensure thread safety.
- **Signal Handling**: For handling interruption signals and exiting gracefully.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/UDAIBHAT/FACE-RECOGNITION.git
    ```
2. Navigate to the project directory:
    ```bash
    cd facial-recognition-system
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Register Users**:
    ```bash
    python main.py
    ```
    - Follow the prompts to enter your name and capture your face via the webcam.

2. **Authenticate Users**:
    - The script will automatically attempt to authenticate users in real-time using the webcam.

## Project Structure

- `main.py`: Main script containing the functionality for user registration and authentication.
- `images/`: Directory where captured images are stored.
- `user_database.db`: SQLite database file storing user information and face encodings.

## Functions Overview

- `create_user_table()`: Creates a table to store user information if it doesn't exist.
- `register_user(name, encoding)`: Registers a new user in the database.
- `load_user_encodings()`: Loads user encodings from the database.
- `authenticate_user(encode_face)`: Authenticates a user by comparing face encodings.
- `load_images(image_dir)`: Loads images from a specified directory.
- `find_encodings(images)`: Finds and returns face encodings for a list of images.
- `speak_message(message)`: Uses text-to-speech to speak a given message.
- `perform_post_authentication_tasks(name)`: Executes tasks after successful authentication.
- `register_faces()`: Registers new users by capturing their faces.
- `authenticate_faces()`: Performs real-time face authentication using the webcam.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Maker

This project was created by [UDAI BHAT].

## Contributing

Contributions are welcome! If you have suggestions for improvements, please:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a Pull Request.

## Acknowledgments

- [OpenCV](https://opencv.org/)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [SQLite](https://www.sqlite.org/index.html)
- [pyttsx3](https://pyttsx3.readthedocs.io/)
