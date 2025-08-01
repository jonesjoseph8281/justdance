from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 Add this import
import subprocess

app = Flask(__name__)
CORS(app)  # 👈 Enable CORS for all routes

@app.route("/upload", methods=["POST"])
def upload_video():
    file = request.files["video"]
    filename = request.form.get("filename", "WakkaWakkaCut.mp4")
    output_json = request.form.get("output_json", "pose_data.json")
    file.save(filename)
    subprocess.run(["python", "extract_pose.py", "--input", filename, "--output", output_json])
    return jsonify({"message": "Video uploaded and processed."})

@app.route("/compare", methods=["GET"])
def compare():
    result = subprocess.run(["python", "compare.py"], capture_output=True, text=True)
    output_lines = result.stdout.strip().split("\n")
    for line in output_lines[::-1]:
        if "Final Average Match Score" in line:
            score = float(line.split(":")[-1].replace("%", "").strip())
            return jsonify({"score": round(score)})
    return jsonify({"error": "Comparison failed."})

@app.route("/upload_webcam", methods=["POST"])
def upload_webcam():
    file = request.files["video"]
    file.save("webcam.mp4")
    subprocess.run(["python", "extract_pose.py", "--input", "webcam.mp4", "--output", "realtime_pose_data.json"])
    return jsonify({"message": "Webcam video uploaded and processed."})

if __name__ == "__main__":
    app.run(debug=True)
