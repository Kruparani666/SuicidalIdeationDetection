function analyzeTweet() {
  let text = document.getElementById("tweetInput").value.trim();
  let resultDiv = document.getElementById("result");
  let loader = document.getElementById("loader");

  if (!text) {
    resultDiv.innerHTML = "⚠️ Please enter a tweet.";
    return;
  }

  resultDiv.innerHTML = "";
  loader.classList.remove("hidden");

  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: text }),
  })
    .then((response) => response.json())
    .then((data) => {
      loader.classList.add("hidden");
      if (data.error) {
        resultDiv.innerHTML = "⚠️ " + data.error;
      } else {
        resultDiv.innerHTML = `🚀 Prediction: <strong>${data.prediction}</strong>`;
      }
    })
    .catch((error) => {
      loader.classList.add("hidden");
      resultDiv.innerHTML = "❌ Error: Unable to analyze tweet.";
    });
}
