import cv2
import mediapipe as mp
import numpy as np
import time
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize video capture (webcam)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    logging.error("Failed to open webcam. Check camera connection.")
    exit()

# Set lower resolution for better performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Variables for jump detection
jump_count = 0
is_jumping = False
jump_start_y = None
jump_start_time = 0
jump_threshold = 0.1  # Vertical displacement threshold (normalized coordinates)
min_jump_time = 0.2  # Minimum air time for a jump (seconds)
jump_heights = []
air_times = []
pixel_to_meters = 0.01  # Calibration factor (adjust after testing)
fps = 30  # Approximate FPS

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        logging.error("Failed to capture frame. Exiting.")
        break

    # Convert frame to RGB for MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    # Draw pose landmarks
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get pelvis keypoint (average of left and right hip)
        left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        pelvis_y = (left_hip.y + right_hip.y) / 2

        # Initialize jump_start_y on first detection
        if jump_start_y is None:
            jump_start_y = pelvis_y
            logging.info(f"Initialized jump_start_y: {jump_start_y}")

        # Detect jump
        current_time = time.time()
        try:
            if not is_jumping and pelvis_y < jump_start_y - jump_threshold:
                # Jump starts (upward movement)
                is_jumping = True
                jump_start_y = pelvis_y
                jump_start_time = current_time
                logging.info(f"Jump started at y={pelvis_y}, time={current_time}")
            elif is_jumping and pelvis_y > jump_start_y + jump_threshold * 0.5:
                # Jump ends (downward movement)
                is_jumping = False
                air_time = current_time - jump_start_time
                if air_time >= min_jump_time:
                    jump_count += 1
                    # Calculate jump height (pixel displacement to meters)
                    jump_height = abs(pelvis_y - jump_start_y) * frame.shape[0] * pixel_to_meters
                    jump_heights.append(jump_height)
                    air_times.append(air_time)
                    logging.info(f"Jump {jump_count}: Height={jump_height:.2f}m, Air Time={air_time:.2f}s")
                else:
                    logging.warning(f"Jump too short: {air_time:.2f}s")
            # Update jump_start_y for next detection
            if not is_jumping:
                jump_start_y = pelvis_y
        except Exception as e:
            logging.error(f"Error in jump detection: {e}")

        # Display metrics on frame
        cv2.putText(frame, f"Jumps: {jump_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if jump_heights:
            cv2.putText(frame, f"Last Height: {jump_heights[-1]:.2f}m", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if air_times:
            cv2.putText(frame, f"Last Air Time: {air_times[-1]:.2f}s", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    else:
        logging.warning("No pose landmarks detected in frame.")
        cv2.putText(frame, "No Pose Detected", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show frame
    cv2.imshow("Jump Detection", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# Print last jump metrics
if jump_heights and air_times:
    logging.info(f"Last Jump Summary --> Height: {jump_heights[-1]:.2f} meters, Air Time: {air_times[-1]:.2f} seconds")
else:
    logging.info("No jumps detected.")

pose.close()
logging.info("Program terminated.")

