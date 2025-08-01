const videoUpload = document.getElementById("videoUpload");
const uploadedVideo = document.getElementById("uploadedVideo");
const webcamVideo = document.getElementById("webcamVideo");
const startBtn = document.getElementById("startBtn");
const danceContainer = document.getElementById("danceContainer");
const scoreScreen = document.getElementById("scoreScreen");
const scoreText = document.getElementById("scoreText");

let webcamStream = null;

videoUpload.addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    const url = URL.createObjectURL(file);
    uploadedVideo.src = url;
    startBtn.disabled = false;
  }
});

startBtn.addEventListener("click", async function () {
  document.getElementById("landing").classList.add("hidden");
  danceContainer.classList.remove("hidden");

  uploadedVideo.play();

  try {
    webcamStream = await navigator.mediaDevices.getUserMedia({ video: true });
    webcamVideo.srcObject = webcamStream;
  } catch (err) {
    alert("Could not access webcam: " + err.message);
  }

  uploadedVideo.onended = () => {
    stopWebcam();
    showScore();
  };
});

function stopWebcam() {
  if (webcamStream) {
    webcamStream.getTracks().forEach(track => track.stop());
  }
}

function showScore() {
  danceContainer.classList.add("hidden");
  scoreScreen.classList.remove("hidden");

  const score = Math.floor(Math.random() * 50 + 50); // Random accuracy
  scoreText.textContent = `Accuracy: ${score}%`;
}
