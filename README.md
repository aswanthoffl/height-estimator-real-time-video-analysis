# Height Estimator: Real-Time Video Analysis

The **Height Estimator: Real-Time Video Analysis** project is a Python-based application that uses computer vision to estimate jump height and air time in real-time using a webcam. It employs the MediaPipe Pose estimation model to track body landmarks, specifically the pelvis, to detect jumps and calculate metrics. The application is served through a Flask web interface, displaying a live video feed with overlaid jump statistics and a results page summarizing all jumps. This project is ideal for fitness tracking, sports analysis, or computer vision experimentation.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Dependencies](#dependencies)
- [Configuration and Customization](#configuration-and-customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features
- **Real-Time Jump Detection**: Detects jumps based on pelvis movement using MediaPipe's Pose estimation.
- **Jump Metrics**: Calculates jump height (in meters) and air time (in seconds).
- **Live Video Overlay**: Displays jump count, last jump height, and air time on the webcam feed.
- **Results Summary**: Provides a detailed summary of all jumps after stopping the session.
- **Web Interface**: Built with Flask for easy access via a browser.
- **Customizable Parameters**: Adjustable thresholds for jump detection sensitivity.

## Prerequisites
To run this project, ensure you have the following:
- **Python**: Version 3.8 or higher.
- **Webcam**: A working webcam connected to your computer.
- **pip**: Python package manager for installing dependencies.
- **Git**: Optional, for cloning the repository.
- **Web Browser**: A modern browser like Chrome, Firefox, or Edge.
- **Operating System**: Windows, macOS, or Linux.

## Installation
Follow these steps to set up the project on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/height-estimator-real-time-video-analysis.git
   cd height-estimator-real-time-video-analysis
   ```
   Replace `<your-username>` with your GitHub username or the appropriate repository owner.

2. **Create a Virtual Environment**:
   Using a virtual environment is recommended to isolate dependencies.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   Install the required Python packages specified in `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Webcam**:
   Ensure your webcam is functional and not in use by other applications. You can test it with a simple OpenCV script:
   ```python
   import cv2
   cap = cv2.VideoCapture(0)
   ret, frame = cap.read()
   if ret:
       cv2.imshow('Webcam Test', frame)
       cv2.waitKey(0)
       cv2.destroyAllWindows()
   cap.release()
   ```

5. **Check Directory Structure**:
   Confirm that the `templates` folder contains `index.html` and the `docs_image` folder contains screenshots. These are required for the web interface and documentation.

## Project Structure
The repository is organized as follows:
```
height-estimator-real-time-video-analysis/
├── templates/
│   └── index.html           # HTML template for rendering the video feed and results
├── docs_image/
│   └── <screenshots>.png   # Screenshots of the application interface
├── app.py                  # Flask application for web routing and serving
├── jump_detector.py        # Core logic for jump detection and video processing
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation (this file)
```

- **templates/index.html**: The HTML template for displaying the live video feed and jump summary.
- **docs_image/**: Contains screenshots of the application, such as the web interface and results page.
- **app.py**: The Flask application that handles routing for the home page, video feed, and results page.
- **jump_detector.py**: Implements jump detection, height and air time calculations, and video overlay using OpenCV and MediaPipe.
- **requirements.txt**: Lists all required Python packages with specific versions.

## Running the Application
1. **Activate the Virtual Environment**:
   If not already activated, run:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Start the Flask Server**:
   Run the Flask application:
   ```bash
   python app.py
   ```
   The server will start in debug mode on `http://127.0.0.1:5000`.

3. **Access the Web Interface**:
   Open a web browser and navigate to `http://127.0.0.1:5000/`. This displays the live webcam feed with overlaid jump statistics.

4. **Stop the Session**:
   To view a summary of all jumps, visit `http://127.0.0.1:5000/stop` in your browser. This renders the results page with details of each jump.

5. **Stop the Server**:
   Press `Ctrl+C` in the terminal to stop the Flask server.

## Usage
1. **Launch the Application**:
   Start the Flask server (`python app.py`) and open `http://127.0.0.1:5000/` in your browser.

2. **Perform Jumps**:
   - Stand in front of the webcam, ensuring your full body is visible.
   - Perform jumps. The application detects jumps by tracking the vertical movement of your pelvis.
   - The video feed displays:
     - **Jump Count**: Total number of valid jumps.
     - **Last Jump Height**: Estimated height of the last jump (in meters).
     - **Last Air Time**: Duration of the last jump (in seconds).

3. **View Jump Summary**:
   Navigate to `http://127.0.0.1:5000/stop` to see a table of all jumps, including count, height, and air time for each.

4. **Best Practices**:
   - Ensure good lighting and minimal background clutter for accurate pose detection.
   - Stand at a distance where your entire body is in the webcam’s frame.
   - Avoid rapid movements that may confuse the pose tracker.

## Screenshots
Screenshots of the application, including the web interface and results page, are available in the `docs_image` folder. These images demonstrate the user interface and functionality of the jump height estimator.

## Dependencies
The project relies on the following Python packages, specified in `requirements.txt`:
- `flask==3.0.0`: Web framework for serving the video feed and results page.
- `opencv-python==4.9.0.80`: Handles webcam capture and image processing.
- `mediapipe==0.10.11`: Provides pose estimation for tracking body landmarks.
- `numpy==1.26.4`: Supports numerical calculations for jump metrics.

Install these dependencies using:
```bash
pip install -r requirements.txt
```

## Configuration and Customization
You can customize the jump detection parameters in `jump_detector.py`:
- **jump_threshold (default: 0.1)**: Minimum vertical pelvis movement (in normalized coordinates) to detect a jump. Increase for stricter detection or decrease for more sensitivity.
- **min_jump_time (default: 0.2)**: Minimum air time (in seconds) for a jump to be counted. Adjust to filter out short movements.
- **pixel_to_meters (default: 0.01)**: Conversion factor from pixel movement to meters. Calibrate based on your setup (e.g., camera distance).
- **min_detection_confidence (default: 0.7)**: Confidence threshold for pose detection. Increase for more reliable detection in complex environments.
- **min_tracking_confidence (default: 0.7)**: Confidence threshold for pose tracking. Adjust for better tracking stability.

To modify these, edit the relevant variables in `jump_detector.py` before running the application.

## Troubleshooting
- **Webcam Not Working**:
  - Ensure the webcam is connected and not used by another application.
  - Check the camera index in `jump_detector.py` (`cv2.VideoCapture(0)`). Try `1` or `2` if `0` fails.
  - Test the webcam with a simple OpenCV script (see [Installation](#installation)).

- **Poor Pose Detection**:
  - Improve lighting and ensure the body is fully visible in the frame.
  - Increase `min_detection_confidence` or `min_tracking_confidence` in `jump_detector.py`.
  - Reduce background distractions or wear contrasting clothing.

- **Flask Server Issues**:
  - Verify all dependencies are installed (`pip install -r requirements.txt`).
  - Check for port conflicts (default: 5000). Change the port in `app.py` using `app.run(debug=True, port=5001)` if needed.

- **Inaccurate Jump Detection**:
  - Adjust `jump_threshold` to make detection more or less sensitive.
  - Modify `min_jump_time` to filter out unintended movements.
  - Calibrate `pixel_to_meters` based on your camera setup and distance.

- **No Video Feed in Browser**:
  - Ensure the Flask server is running and accessible at `http://127.0.0.1:5000/`.
  - Check browser console for errors (right-click > Inspect > Console).
  - Verify that `index.html` is correctly set up in the `templates` folder.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/<feature-name>
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add <feature-name>"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/<feature-name>
   ```
5. Open a pull request on GitHub.

Please include clear descriptions of your changes and ensure code adheres to the project’s style (e.g., PEP 8 for Python).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- **MediaPipe**: For providing robust pose estimation capabilities.
- **OpenCV**: For efficient video processing and webcam handling.
- **Flask**: For the lightweight web framework enabling the user interface.
- **Python Community**: For the extensive libraries and documentation that made this project possible.
