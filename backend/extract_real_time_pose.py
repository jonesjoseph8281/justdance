import cv2
import mediapipe as mp
import time
import json

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
all_landmarks = []
start_time = time.time()
duration = 16  # seconds
frame_index = 0

print("[INFO] Capturing pose for 16 seconds...")

while time.time() - start_time < duration:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    frame_landmarks = []
    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            frame_landmarks.append({
                "x": round(landmark.x, 5),
                "y": round(landmark.y, 5),
                "z": round(landmark.z, 5),
                "visibility": round(landmark.visibility, 5)
            })
    else:
        frame_landmarks = [{"x": 0, "y": 0, "z": 0, "visibility": 0} for _ in range(33)]

    all_landmarks.append({"frame": frame_index, "keypoints": frame_landmarks})
    frame_index += 1

    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow("Webcam Pose", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pose.close()

with open("realtime_pose_data.json", "w") as f:
    json.dump(all_landmarks, f, indent=2)

print(f"[✅] Saved {len(all_landmarks)} frames to 'realtime_pose_data.json'")
