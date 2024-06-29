# rock_paper-scisors
This repository contains a Rock-Paper-Scissors game implemented using OpenCV and MediaPipe. The game detects hand gestures through the webcam and plays against the computer.

Features:
Hand gesture detection using MediaPipe 
Real-time webcam input with OpenCV
Random computer opponent
Interactive UI with visual feedback

How to Use:
1) Clone the repository.
2) Ensure you have the necessary dependencies installed:
---pip install opencv-python
---pip install mediapipe
3) Use your webcam to show the Rock, Paper, or Scissors gesture.
4) Click the "Play" button to play against the computer.

Code Explanation:
The script uses OpenCV for capturing webcam input and MediaPipe for detecting hand landmarks. It recognizes the Rock, Paper, and Scissors gestures based on the positions of the hand landmarks and compares them against the computer's random choice.

tutorial that help me build this:
https://www.youtube.com/watch?v=WYYFgCjgdKA
