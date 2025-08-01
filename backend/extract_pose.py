import cv2
import mediapipe as mp
import json
import os

VIDEO_FILE = "WakkaWakkaCut.mp4"
OUTPUT_FILE = "pose_data.json"

# Initialize MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1)

# Try opening the video
cap = cv2.VideoCapture(VIDEO_FILE)

if not cap.isOpened():
    print(f"❌ Error: Could not open video file '{VIDEO_FILE}'. Make sure the file exists.")
    exit()

print("🎥 Video opened successfully. Starting pose extraction...")

pose_data = []
frame_index = 0
processed_frames = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("✅ Finished reading video.")
        break

    # Convert BGR to RGB for MediaPipe
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(image_rgb)

    # Store keypoints for current frame
    frame_result = {"frame": frame_index, "keypoints": []}

    if result.pose_landmarks:
        for landmark in result.pose_landmarks.landmark:
            frame_result["keypoints"].append([
                round(landmark.x, 5),
                round(landmark.y, 5),
                round(landmark.z, 5),
                round(landmark.visibility, 5)
            ])
    else:
        # If pose not detected, fill with zeros
        frame_result["keypoints"] = [[0, 0, 0, 0] for _ in range(33)]

    pose_data.append(frame_result)
    frame_index += 1
    processed_frames += 1

    if frame_index % 50 == 0:
        print(f"🟢 Processed {frame_index} frames...")

cap.release()
print(f"📦 Total frames processed: {processed_frames}")

# Save to JSON
with open(OUTPUT_FILE, "w") as f:
    json.dump(pose_data, f, indent=2)

print(f"✅ Pose data saved to {OUTPUT_FILE}")
