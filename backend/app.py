from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_video():
    try:
        if 'video' not in request.files:
            return jsonify({"error": "No video file provided"}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Extract pose data from uploaded video
        output_json = "pose_data.json"
        result = subprocess.run(
            ["python", "extract_pose.py", "--input", filepath, "--output", output_json],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return jsonify({"error": f"Pose extraction failed: {result.stderr}"}), 500
        
        return jsonify({"message": "Video uploaded and processed successfully", "filename": filename})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/upload_webcam", methods=["POST"])
def upload_webcam():
    try:
        if 'video' not in request.files:
            return jsonify({"error": "No video file provided"}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save webcam recording
        webcam_filename = "webcam.mp4"
        filepath = os.path.join(UPLOAD_FOLDER, webcam_filename)
        file.save(filepath)
        
        # Extract pose data from webcam video
        output_json = "realtime_pose_data.json"
        result = subprocess.run(
            ["python", "extract_pose.py", "--input", filepath, "--output", output_json],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return jsonify({"error": f"Pose extraction failed: {result.stderr}"}), 500
        
        return jsonify({"message": "Webcam video uploaded and processed successfully"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/compare", methods=["GET"])
def compare():
    try:
        # Check if both pose data files exist
        if not os.path.exists("pose_data.json"):
            return jsonify({"error": "Reference pose data not found. Please upload a dance video first."}), 400
        
        if not os.path.exists("realtime_pose_data.json"):
            return jsonify({"error": "Webcam pose data not found. Please record your dance first."}), 400
        
        # Run comparison
        result = subprocess.run(
            ["python", "compare.py"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return jsonify({"error": f"Comparison failed: {result.stderr}"}), 500
        
        # Parse the output to get the score
        output_lines = result.stdout.strip().split("\n")
        for line in output_lines[::-1]:
            if "Final Average Match Score" in line:
                try:
                    score = float(line.split(":")[-1].replace("%", "").strip())
                    return jsonify({"score": round(score, 2)})
                except ValueError:
                    return jsonify({"error": "Could not parse score from output"}), 500
        
        return jsonify({"error": "No score found in comparison output"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
