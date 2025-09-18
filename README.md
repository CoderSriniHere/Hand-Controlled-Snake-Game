🐍 Hand Gesture Controlled Snake Game

This project is a modern twist on the classic Snake Game 🎮, where the snake is controlled not by a keyboard but through hand gestures tracked via webcam using MediaPipe and OpenCV. The game is built with Pygame and integrates real-time gesture recognition for an interactive gaming experience.

🚀 Features

Hand Gesture Controls: Control the snake’s movement (up, down, left, right) with simple hand gestures.

Boundary Wrapping: Snake doesn’t die at screen borders; it appears on the opposite side, making gameplay continuous.

Score Tracking: Snake grows and score increases upon eating food.

Real-Time Processing: Efficient hand tracking using MediaPipe.

Engaging UI: Smooth gameplay with modernized snake design.

🛠️ Tech Stack

Python 3.10+

Pygame – for game logic & rendering

OpenCV – for real-time video capture

MediaPipe – for hand tracking & gesture recognition

NumPy – for calculations and snake mechanics

🎯 How It Works

The webcam captures your hand movements.

MediaPipe processes the video feed to detect hand landmarks.

Gestures are mapped to snake directions (up, down, left, right).

Snake follows the gesture input while collecting food and avoiding self-collision.

📂 Project Structure
snake_hand_control.py   # Main game file
requirements.txt        # Required Python libraries
README.md               # Project documentation

snake_hand_control.py   # Main game file
requirements.txt        # Required Python libraries
README.md               # Project documentation
