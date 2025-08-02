import cv2
import mediapipe as mp
import json
import argparse
import sys

def extract_pose_from_video(video_file, output_file):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, model_complexity=1)
    cap = cv2.VideoCapture(video_file)

    if not cap.isOpened():
        print(f"❌ Error: Could not open video file '{video_file}'.")
        return False

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

    with open(output_file, "w") as f:
        json.dump(pose_data, f, indent=2)

    print(f"✅ Pose data saved to '{output_file}' with {frame_index} frames.")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract pose data from video")
    parser.add_argument("--input", required=True, help="Input video file")
    parser.add_argument("--output", required=True, help="Output JSON file")
    
    args = parser.parse_args()
    
    success = extract_pose_from_video(args.input, args.output)
    if not success:
        sys.exit(1)
