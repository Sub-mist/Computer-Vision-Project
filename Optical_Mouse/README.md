# Hand Gesture Recognition for Mouse and System Control

This project uses hand gestures to control system functionalities such as mouse movement, clicks, volume control, brightness control, and taking screenshots. It leverages computer vision with the help of OpenCV, MediaPipe, and other Python libraries to track hand landmarks and detect gestures.

## Features

- **Mouse Control**: Move the mouse based on index finger movement.
- **Mouse Click**: Perform left and right clicks based on hand gestures.
- **Double Click**: Perform a double click with specific hand gestures.
- **Volume Control**: Adjust the system volume up or down.
- **Brightness Control**: Increase or decrease the screen brightness.
- **Screenshot**: Capture and save screenshots based on hand gestures.

### Installation:
1. Create Virtual Environment and activate it.

2. Install Dependencies:
To install the required Python packages, run the following command:

```bash
pip install -r requirements.txt
```

## Usage:

1. Run the main.py script.
    ```bash
    python main.py
    ```

2. A webcam window will open. Use the following hand gestures for the respective actions:

- **Move Mouse**: keeping the thumb close to the index base (thumb and index distance < 50).
- **Left Click**: Curve your index finger (sharp angle) and thumb away from the index (distance > 50).
- **Right Click**: Curve your middle finger and thumb away.
- **Double Click**: Curve both index and middle fingers, with the thumb away from the index.
- **Volume Up**: Keep your thumb and pinky far apart (100–130 distance) and ensure the index and middle fingers are close.
- **Volume Down**: Bring thumb and pinky very close (< 50) while index and middle fingers are still close.
- **Brightness Up**: Keep thumb and ring finger moderately apart (100–140), with index and middle fingers close.
- **Brightness Down**: Bring thumb and ring finger very close (< 40), with index and middle fingers close.
- **Screenshot**: Form a fist with your thumb and index finger together.

3. Press 'q' to exit the webcam window.

## Note:

- Python Version = Python 3.11.9
- If you are having trouble understanding the indexes for the finger refer to the fig 2.21
in https://mediapipe.readthedocs.io/en/latest/solutions/hands.html 
(readthedocs.io)

