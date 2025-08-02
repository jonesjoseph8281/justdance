import json
import math
import os

# --------- ANGLE CALCULATION ---------
def get_angle(a, b, c):
    """Calculate angle between three points a, b, c where b is the vertex."""
    try:
        ba = [a["x"] - b["x"], a["y"] - b["y"]]
        bc = [c["x"] - b["x"], c["y"] - b["y"]]

        dot_product = ba[0]*bc[0] + ba[1]*bc[1]
        magnitude_ba = math.sqrt(ba[0]**2 + ba[1]**2)
        magnitude_bc = math.sqrt(bc[0]**2 + bc[1]**2)

        if magnitude_ba * magnitude_bc == 0:
            return 0.0

        cos_angle = dot_product / (magnitude_ba * magnitude_bc)
        # Clamp cos_angle to [-1, 1] to avoid math domain error
        cos_angle = max(-1.0, min(1.0, cos_angle))
        angle_rad = math.acos(cos_angle)
        return math.degrees(angle_rad)
    except Exception as e:
        print(f"[Error calculating angle]: {e}")
        return 0.0

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
    """Extract joint angles from a frame of pose data."""
    angles = []
    try:
        for j1, j2, j3 in ANGLE_JOINTS:
            if j1 < len(frame) and j2 < len(frame) and j3 < len(frame):
                a = frame[j1]
                b = frame[j2]
                c = frame[j3]
                
                # Check if points are visible enough
                if (a["visibility"] > 0.5 and b["visibility"] > 0.5 and c["visibility"] > 0.5):
                    angle = get_angle(a, b, c)
                    angles.append(angle)
                else:
                    angles.append(0.0)  # Use 0 for invisible joints
            else:
                angles.append(0.0)
    except Exception as e:
        print(f"[Error extracting angles]: {e}")
        return None
    return angles

# --------- NORMALIZE ANGLES ---------
def normalize_angles(angles):
    """Normalize angles to handle different body orientations."""
    if not angles:
        return angles
    
    # Find the dominant angle (usually the most active joint)
    max_angle = max(angles)
    if max_angle > 0:
        return [angle / max_angle * 180 for angle in angles]
    return angles

# --------- COMPARE TWO ANGLE SETS ---------
def compare_angle_sets(angles1, angles2):
    """Compare two sets of angles and return a similarity score."""
    if not angles1 or not angles2:
        return 0.0
    
    if len(angles1) != len(angles2):
        return 0.0
    
    total_diff = 0
    valid_angles = 0
    
    for a1, a2 in zip(angles1, angles2):
        if a1 > 0 or a2 > 0:  # Only compare non-zero angles
            diff = abs(a1 - a2)
            total_diff += diff
            valid_angles += 1
    
    if valid_angles == 0:
        return 0.0
    
    avg_diff = total_diff / valid_angles
    # Convert to percentage (0-100)
    score = max(0, 100 - avg_diff)
    return score

# --------- COMPARE ALL FRAMES ---------
def compare_angles(file1="pose_data.json", file2="realtime_pose_data.json", window=3):
    """Compare pose data from two videos using sliding window approach."""
    
    # Check if files exist
    if not os.path.exists(file1):
        print(f"❌ Error: {file1} not found")
        return False
    
    if not os.path.exists(file2):
        print(f"❌ Error: {file2} not found")
        return False
    
    try:
        with open(file1) as f:
            video_data = json.load(f)
        with open(file2) as f:
            live_data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading pose data files: {e}")
        return False

    if not video_data or not live_data:
        print("❌ Error: Empty pose data files")
        return False

    scores = []
    print("🎯 Frame-by-frame ANGLE match scores (with sliding window):")

    for i in range(len(video_data)):
        video_angles = extract_angles(video_data[i]["keypoints"])
        if video_angles is None:
            continue

        best_score = 0
        best_offset = 0
        
        # Try different time offsets within the window
        for offset in range(-window, window + 1):
            j = i + offset
            if j < 0 or j >= len(live_data):
                continue
                
            live_angles = extract_angles(live_data[j]["keypoints"])
            if live_angles is None:
                continue

            # Normalize angles for better comparison
            norm_video = normalize_angles(video_angles)
            norm_live = normalize_angles(live_angles)
            
            score = compare_angle_sets(norm_video, norm_live)
            
            if score > best_score:
                best_score = score
                best_offset = offset

        scores.append(best_score)
        print(f"Frame {i+1}: Best match = {best_score:.2f}% (offset: {best_offset})")

    if scores:
        avg = sum(scores) / len(scores)
        print(f"\n✅ Final Average Match Score: {avg:.2f}%")
        return True
    else:
        print("❌ No valid frames matched.")
        return False

if __name__ == "__main__":
    success = compare_angles()
    if not success:
        exit(1)
