import cv2
import mediapipe as mp
import json

VIDEO_FILE = "WakkaWakkaCut.mp4"
OUTPUT_FILE = "pose_data.json"

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1)
cap = cv2.VideoCapture(VIDEO_FILE)

if not cap.isOpened():
    print(f"❌ Error: Could not open video file '{VIDEO_FILE}'.")
    exit()

pose_data = []
frame_index = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(image_rgb)

    keypoints = []
    if result.pose_landmarks:
        for landmark in result.pose_landmarks.landmark:
            keypoints.append({
                "x": round(landmark.x, 5),
                "y": round(landmark.y, 5),
                "z": round(landmark.z, 5),
                "visibility": round(landmark.visibility, 5)
            })
    else:
        keypoints = [{"x": 0, "y": 0, "z": 0, "visibility": 0} for _ in range(33)]

    pose_data.append({"frame": frame_index, "keypoints": keypoints})
    frame_index += 1

cap.release()
pose.close()

with open(OUTPUT_FILE, "w") as f:
    json.dump(pose_data, f, indent=2)

print(f"✅ Pose data saved to '{OUTPUT_FILE}' with {frame_index} frames.")
