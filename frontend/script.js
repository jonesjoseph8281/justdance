const videoUpload = document.getElementById("videoUpload");
const uploadedVideo = document.getElementById("uploadedVideo");
const webcamVideo = document.getElementById("webcamVideo");
const startBtn = document.getElementById("startBtn");
const danceContainer = document.getElementById("danceContainer");
const scoreScreen = document.getElementById("scoreScreen");
const scoreText = document.getElementById("scoreText");

let mediaRecorder;
let recordedChunks = [];
let webcamStream = null;

// When user uploads a video
videoUpload.addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    const url = URL.createObjectURL(file);
    uploadedVideo.src = url;
    startBtn.disabled = false;
  }
});

// Start Dancing
startBtn.addEventListener("click", async function () {
  document.getElementById("landing").classList.add("hidden");
  danceContainer.classList.remove("hidden");

  try {
    // STEP 1: Start webcam stream
    webcamStream = await navigator.mediaDevices.getUserMedia({ video: true });
    webcamVideo.srcObject = webcamStream;

    recordedChunks = [];
    mediaRecorder = new MediaRecorder(webcamStream, { mimeType: "video/webm" });

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) recordedChunks.push(e.data);
    };

    mediaRecorder.onstop = () => {
      const blob = new Blob(recordedChunks, { type: "video/webm" });
      playback.src = URL.createObjectURL(blob);
      playback.controls = true;
      playback.play();
      // Stop webcam after recording
      webcamStream.getTracks().forEach(track => track.stop());
      webcamStream = null;
      webcamVideo.srcObject = null;
    };

    // STEP 2: Get video duration
    await uploadedVideo.play();
    uploadedVideo.pause();
    const duration = uploadedVideo.duration;
    if (!duration || isNaN(duration)) {
      alert("❌ Invalid video duration.");
      return;
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
    alert("Error: " + err.message);
  }
});

function showScore(score) {
  danceContainer.classList.add("hidden");
  scoreScreen.classList.remove("hidden");
  scoreText.textContent = `Accuracy: ${score}%`;
}