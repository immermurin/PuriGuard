// Declare it here
let prankTriggered = false;

const pageText = document.body.innerText;

fetch("http://127.0.0.1:6969/scan-text", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ text: pageText })
})
.then(res => res.json())
.then(data => {
  console.log("🔍 Scan result:", data);

  if ((data.nsfw || (data.flagged_keywords && data.flagged_keywords.length > 0)) && !prankTriggered) {
    prankTriggered = true;
    alert("⚠️ Inappropriate content detected. Activating prank!");

    fetch("http://127.0.0.1:6969/trigger-prank", {
      method: "POST"
    })
    .then(res => res.json())
    .then(result => console.log("🎯 Prank triggered:", result))
    .catch(err => console.error("❌ Prank trigger failed:", err));
  }
})
.catch(err => console.error("❌ Extension Scan Error:", err));

function scanVideoFrame(video) {
  try {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const base64Image = canvas.toDataURL("image/jpeg");

    fetch("http://127.0.0.1:6969/scan-frame", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: base64Image })
    })
    .then(res => res.json())
    .then(data => {
      if (data.nsfw && !prankTriggered) {
        prankTriggered = true;
        alert("⚠️ NSFW video detected!");
        fetch("http://127.0.0.1:6969/trigger-prank", { method: "POST" });
      }
    })
    .catch(err => console.error("Frame scan failed:", err));
  } catch (e) {
    console.error("Capture error:", e);
  }
}

setInterval(() => {
  const videos = document.querySelectorAll("video");
  videos.forEach(video => {
    if (!video.paused && !video.ended) {
      scanVideoFrame(video);
    }
  });
}, 10000); // every 10 seconds
