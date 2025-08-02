const videoUpload = document.getElementById("videoUpload");
const uploadedVideo = document.getElementById("uploadedVideo");
const webcamVideo = document.getElementById("webcamVideo");
const playback = document.getElementById("playback");
const playbackBox = document.getElementById("playbackBox");
const startBtn = document.getElementById("startBtn");
const danceContainer = document.getElementById("danceContainer");
const scoreScreen = document.getElementById("scoreScreen");
const scoreText = document.getElementById("scoreText");
const scoreFill = document.getElementById("scoreFill");
const loadingScreen = document.getElementById("loadingScreen");

let mediaRecorder;
let recordedChunks = [];
let webcamStream = null;
let uploadedVideoFile = null;

const API_BASE = "http://localhost:5000";

// Show loading screen
function showLoading() {
  loadingScreen.classList.remove("hidden");
}

// Hide loading screen
function hideLoading() {
  loadingScreen.classList.add("hidden");
}

// Show error message
function showError(message) {
  alert(`❌ Error: ${message}`);
  hideLoading();
}

// When user uploads a video
videoUpload.addEventListener("change", async function () {
  const file = this.files[0];
  if (file) {
    uploadedVideoFile = file;
    const url = URL.createObjectURL(file);
    uploadedVideo.src = url;
    startBtn.disabled = false;
    
    // Upload video to backend
    showLoading();
    try {
      const formData = new FormData();
      formData.append("video", file);
      
      const response = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData
      });
      
      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.error || "Failed to upload video");
      }
      
      console.log("✅ Video uploaded successfully:", result.message);
    } catch (error) {
      showError(error.message);
      return;
    } finally {
      hideLoading();
    }
  }
});

// Start Dancing
startBtn.addEventListener("click", async function () {
  document.getElementById("landing").classList.add("hidden");
  danceContainer.classList.remove("hidden");

  try {
    // STEP 1: Start webcam stream
    webcamStream = await navigator.mediaDevices.getUserMedia({ 
      video: { 
        width: { ideal: 1280 },
        height: { ideal: 720 }
      } 
    });
    webcamVideo.srcObject = webcamStream;

    recordedChunks = [];
    mediaRecorder = new MediaRecorder(webcamStream, { 
      mimeType: "video/webm;codecs=vp9" 
    });

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) recordedChunks.push(e.data);
    };

    mediaRecorder.onstop = async () => {
      const blob = new Blob(recordedChunks, { type: "video/webm" });
      playback.src = URL.createObjectURL(blob);
      playbackBox.classList.remove("hidden");
      
      // Stop webcam
      webcamStream.getTracks().forEach(track => track.stop());
      webcamStream = null;
      webcamVideo.srcObject = null;
      
      // Upload webcam recording to backend
      await uploadWebcamRecording(blob);
    };

    // STEP 2: Get video duration
    await uploadedVideo.play();
    uploadedVideo.pause();
    const duration = uploadedVideo.duration;
    if (!duration || isNaN(duration)) {
      throw new Error("Invalid video duration");
    }

    // STEP 3: Start recording & play video
    mediaRecorder.start();
    await uploadedVideo.play();

    // STEP 4: Stop recording after video ends
    setTimeout(() => {
      mediaRecorder.stop();
      uploadedVideo.pause();
    }, duration * 1000);

  } catch (err) {
    console.error("❌ Error during dancing:", err);
    showError(err.message);
  }
});

// Upload webcam recording to backend
async function uploadWebcamRecording(blob) {
  showLoading();
  try {
    const formData = new FormData();
    formData.append("video", blob, "webcam.webm");
    
    const response = await fetch(`${API_BASE}/upload_webcam`, {
      method: "POST",
      body: formData
    });
    
    const result = await response.json();
    
    if (!response.ok) {
      throw new Error(result.error || "Failed to upload webcam recording");
    }
    
    console.log("✅ Webcam recording uploaded successfully");
    
    // Calculate score
    await calculateScore();
    
  } catch (error) {
    showError(error.message);
  } finally {
    hideLoading();
  }
}

// Calculate dance score
async function calculateScore() {
  showLoading();
  try {
    const response = await fetch(`${API_BASE}/compare`);
    const result = await response.json();
    
    if (!response.ok) {
      throw new Error(result.error || "Failed to calculate score");
    }
    
    const score = result.score;
    showScore(score);
    
  } catch (error) {
    showError(error.message);
  } finally {
    hideLoading();
  }
}

// Display score with animation
function showScore(score) {
  danceContainer.classList.add("hidden");
  scoreScreen.classList.remove("hidden");
  
  // Animate score
  let currentScore = 0;
  const targetScore = score;
  const duration = 2000; // 2 seconds
  const interval = 50; // Update every 50ms
  const steps = duration / interval;
  const increment = targetScore / steps;
  
  const scoreInterval = setInterval(() => {
    currentScore += increment;
    if (currentScore >= targetScore) {
      currentScore = targetScore;
      clearInterval(scoreInterval);
    }
    
    scoreText.textContent = `Accuracy: ${Math.round(currentScore)}%`;
    scoreFill.style.width = `${currentScore}%`;
    
    // Color coding
    if (currentScore >= 80) {
      scoreFill.style.backgroundColor = "#4CAF50"; // Green
    } else if (currentScore >= 60) {
      scoreFill.style.backgroundColor = "#FF9800"; // Orange
    } else {
      scoreFill.style.backgroundColor = "#F44336"; // Red
    }
  }, interval);
}