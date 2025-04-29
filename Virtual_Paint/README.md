# Virtual Paint and Draw

A hand gesture-based drawing application that allows users to draw on a digital canvas using their hand movements. The app allow hand tracking with MediaPipe and allows users to choose colors, draw, erase, and create rectangles through hand gestures.

## Features

- **Draw with different colors**: Choose from multiple colors (White, Red, Green, Blue) for drawing.
- **Erase drawings**: Switch to eraser mode to remove any part of the drawing.
- **Rectangle tool**: Draw rectangles by selecting the rectangle mode.
- **Canvas saving**: Save your current drawing as an image file.
- **Canvas clearing**: Clear the entire canvas and start fresh.

## Installation

1. Clone the repository:
   ```bash
    git clone https://github.com/Sub-mist/Virtual_Paint.git
    cd Virtual_Paint
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage:

1. **Launch the application**: Open a terminal and run the following command to start the hand gesture drawing application:
    ```bash
    python main.py
    ```

2. **Control with gestures**:

- **Draw Mode**: Raise two fingers and select a color (White, Red, Green, Blue).
- **Eraser Mode**: Raise one finger to start drawing and use black color to erase.
- **Rectangle Tool**: Select the rectangle tool to draw a rectangle.
- **Clear Canvas**: Press the 'c' key to clear the drawing.
- **Save Canvas**: Press the 's' key to save your drawing as an image file.

**Hand Gesture Mapping**:
- **Selection Mode (2 fingers up)**: Switch between color and tool options.
- **Drawing Mode (1 finger up)**: Start drawing on the canvas.

## File Structure:
```plaintext
hand-gesture-drawing/
│
├── img_folder/              # Folder containing color images for brush selection.
├── main.py                  # Main Python script for running the application.
├── HandTrackingModule.py    # Hand tracking module using MediaPipe.
├── requirements.txt         # List of Python dependencies.
└── README.md                # This README file.

```

## Note:
- There is a default.jpg image inside the img_folder which explain if nothing is selected.
- After cloning the repository:
    1. Create a Virtual Environment:
    ```bash
    python -m venv venv(virtual_environment_name)         
    # try to replace python with python3 in the above command if it does not work.
    ```
    2. Activate the Virtual Environment:
    ```bash
    venv\Scripts\activate                   # For Windows
    source venv/bin/activate                # For macOS
    ```
    Once activated, you should see (venv) before your command prompt, indicating that the virtual environment is active.
    Then install requirements.txt.
- Python version = Python 3.12.8
