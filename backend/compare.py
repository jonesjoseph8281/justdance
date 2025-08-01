import json
import math

# --------- ANGLE CALCULATION ---------
def get_angle(a, b, c):
    ba = [a[i] - b[i] for i in range(2)]
    bc = [c[i] - b[i] for i in range(2)]

    dot_product = ba[0]*bc[0] + ba[1]*bc[1]
    magnitude_ba = math.sqrt(ba[0]**2 + ba[1]**2)
    magnitude_bc = math.sqrt(bc[0]**2 + bc[1]**2)

    if magnitude_ba * magnitude_bc == 0:
        return 0.0

    angle_rad = math.acos(dot_product / (magnitude_ba * magnitude_bc))
    return math.degrees(angle_rad)

# --------- JOINTS TO USE FOR ANGLES ---------
ANGLE_JOINTS = [
    (11, 13, 15),  # Left Elbow
    (12, 14, 16),  # Right Elbow
    (13, 11, 23),  # Left Shoulder
    (14, 12, 24),  # Right Shoulder
    (23, 25, 27),  # Left Knee
    (24, 26, 28),  # Right Knee
    (11, 23, 25),  # Left Hip
    (12, 24, 26),  # Right Hip
]

# --------- EXTRACT ANGLES FROM A FRAME ---------
def extract_angles(frame):
    angles = []
    try:
        for j1, j2, j3 in ANGLE_JOINTS:
            a = frame[j1]
            b = frame[j2]
            c = frame[j3]
            angle = get_angle((a["x"], a["y"]), (b["x"], b["y"]), (c["x"], c["y"]))
            angles.append(angle)
    except Exception as e:
        print(f"[Error extracting angles]: {e}")
        return None
    return angles

# --------- COMPARE ALL FRAMES ---------
def compare_angles(file1="pose_data.json", file2="realtime_pose_data.json", window=2):
    with open(file1) as f:
        video_data = json.load(f)
    with open(file2) as f:
        live_data = json.load(f)

    scores = []
    print("🎯 Frame-by-frame ANGLE match scores (with sliding window):")

    for i in range(len(video_data)):
        video_angles = extract_angles(video_data[i]["keypoints"])
        if video_angles is None:
            continue

        best_score = 0
        for offset in range(-window, window + 1):
            j = i + offset
            if j < 0 or j >= len(live_data):
                continue
            live_angles = extract_angles(live_data[j]["keypoints"])
            if live_angles is None:
                continue

            total_diff = sum(abs(a - b) for a, b in zip(video_angles, live_angles)) / len(video_angles)
            score = max(0, 100 - total_diff)
            best_score = max(best_score, score)

        scores.append(best_score)
        print(f"Frame {i+1}: Best match = {best_score:.2f}%")

    if scores:
        avg = sum(scores) / len(scores)
        print(f"\n✅ Final Average Match Score: {avg:.2f}%")
    else:
        print("❌ No valid frames matched.")

if __name__ == "__main__":
    compare_angles()
