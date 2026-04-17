const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const snap = document.getElementById("snap");
const uploadForm = document.getElementById("uploadForm");
const capturedImage = document.getElementById("capturedImage");
const submitBtn = document.getElementById("submitBtn");

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    });

snap.addEventListener("click", () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    canvas.getContext("2d").drawImage(video, 0, 0);

    canvas.toBlob(blob => {
        const file = new File([blob], "captured.png", { type: "image/png" });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);

        capturedImage.files = dataTransfer.files;
        submitBtn.style.display = "block";
    });
});
