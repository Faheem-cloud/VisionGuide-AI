const input = document.getElementById("imageInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const speakBtn = document.getElementById("speakBtn");
const statusEl = document.getElementById("status");
let speechText = "";

analyzeBtn.addEventListener("click", async () => {
  if (!input.files.length) {
    statusEl.textContent = "Please choose or capture an image first.";
    return;
  }
  const form = new FormData();
  form.append("image", input.files[0]);
  analyzeBtn.disabled = true;
  statusEl.textContent = "Analyzing image. The first run may take longer while the AI model downloads.";
  try {
    const response = await fetch("/analyze", { method: "POST", body: form });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Analysis failed.");
    document.getElementById("scene").textContent = data.scene_description;
    document.getElementById("ocr").textContent = data.recognized_text;
    const list = document.getElementById("objects");
    list.innerHTML = "";
    if (!data.objects.length) {
      list.innerHTML = "<li>No objects confidently detected.</li>";
    } else {
      data.objects.forEach(item => {
        const li = document.createElement("li");
        li.textContent = `${item.label} (${Math.round(item.confidence * 100)}% confidence)`;
        list.appendChild(li);
      });
    }
    speechText = `${data.scene_description} Text detected: ${data.recognized_text}`;
    speakBtn.disabled = false;
    statusEl.textContent = "Analysis complete.";
  } catch (error) {
    statusEl.textContent = error.message;
  } finally {
    analyzeBtn.disabled = false;
  }
});

speakBtn.addEventListener("click", () => {
  if (!speechText || !("speechSynthesis" in window)) {
    statusEl.textContent = "Speech output is not supported in this browser.";
    return;
  }
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(new SpeechSynthesisUtterance(speechText));
});
