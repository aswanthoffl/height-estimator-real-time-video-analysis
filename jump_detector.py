import cv2
import mediapipe as mp
import time

# Shared data for live overlay
jump_data = {
    "jump_count": 0,
    "last_height": 0.0,
    "last_air_time": 0.0,
    "all_jumps": []
}

def gen_frames():
    global jump_data

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    jump_start_y = None
    is_jumping = False
    jump_start_time = 0
    jump_threshold = 0.1
    min_jump_time = 0.2
    pixel_to_meters = 0.01

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
            pelvis_y = (left_hip.y + right_hip.y) / 2

            if jump_start_y is None:
                jump_start_y = pelvis_y

            current_time = time.time()

            if not is_jumping and pelvis_y < jump_start_y - jump_threshold:
                is_jumping = True
                jump_start_y = pelvis_y
                jump_start_time = current_time

            elif is_jumping and pelvis_y > jump_start_y + jump_threshold * 0.5:
                is_jumping = False
                air_time = current_time - jump_start_time
                if air_time >= min_jump_time:
                    jump_data["jump_count"] += 1
                    jump_height = abs(pelvis_y - jump_start_y) * frame.shape[0] * pixel_to_meters
                    jump_data["last_height"] = round(jump_height, 2)
                    jump_data["last_air_time"] = round(air_time, 2)
                    jump_data["all_jumps"].append({
                        "count": jump_data["jump_count"],
                        "height": jump_data["last_height"],
                        "air_time": jump_data["last_air_time"]
                    })

            if not is_jumping:
                jump_start_y = pelvis_y

        # Overlay values on the frame
        cv2.putText(frame, f"Jumps: {jump_data['jump_count']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(frame, f"Height: {jump_data['last_height']:.2f}m", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(frame, f"Air Time: {jump_data['last_air_time']:.2f}s", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    pose.close()
