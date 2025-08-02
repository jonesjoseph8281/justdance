# 🎵 Just Dance Clone

A web-based dance game that compares your dance moves with a reference video using pose estimation and provides accuracy scores.

## 🚀 Features

- Upload any dance video as reference
- Real-time webcam recording during dance
- Pose estimation using MediaPipe
- Frame-by-frame dance accuracy comparison
- Beautiful animated score display
- Responsive web interface

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Modern web browser with webcam support
- Webcam for recording your dance moves

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd justdance
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend server**
   ```bash
   cd backend
   python app.py
   ```
   The server will start on `http://localhost:5000`

4. **Open the frontend**
   - Open `frontend/index.html` in your web browser
   - Or serve it using a local server:
     ```bash
     cd frontend
     python -m http.server 8000
     ```
     Then visit `http://localhost:8000`

## 🎮 How to Use

1. **Upload a Dance Video**
   - Click "📁 Choose Dance Video" to select a reference dance video
   - The video will be processed to extract pose data

2. **Start Dancing**
   - Click "🕺 Start Dancing" to begin
   - Allow webcam access when prompted
   - The reference video will play while recording your dance

3. **Get Your Score**
   - After the recording completes, your dance will be compared
   - View your accuracy score with animated display
   - Try again to improve your score!

## 📁 Project Structure

```
justdance/
├── backend/
│   ├── app.py              # Flask server
│   ├── extract_pose.py     # Pose extraction script
│   ├── compare.py          # Dance comparison algorithm
│   └── *.mp4              # Sample videos
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── script.js           # Frontend JavaScript
│   └── style.css           # Styling
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Technical Details

### Backend
- **Flask**: Web server and API endpoints
- **MediaPipe**: Pose estimation from video frames
- **OpenCV**: Video processing
- **JSON**: Pose data storage

### Frontend
- **HTML5**: Video recording and playback
- **JavaScript**: Webcam access and API communication
- **CSS3**: Responsive design and animations

### Pose Comparison Algorithm
- Extracts key body joint angles from both videos
- Uses sliding window comparison for timing flexibility
- Calculates average match score across all frames

## 🐛 Troubleshooting

### Common Issues

1. **Webcam not working**
   - Ensure your browser supports getUserMedia API
   - Check camera permissions in browser settings
   - Try refreshing the page

2. **Video upload fails**
   - Check file format (supported: mp4, avi, mov, webm)
   - Ensure file size is reasonable (< 100MB)
   - Check browser console for error messages

3. **Backend server issues**
   - Verify Python dependencies are installed
   - Check if port 5000 is available
   - Look for error messages in terminal

4. **Pose extraction fails**
   - Ensure video contains clear human figures
   - Check video quality and lighting
   - Verify MediaPipe installation

### Browser Compatibility
- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License. 