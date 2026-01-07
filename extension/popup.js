document.getElementById("summarize").addEventListener("click", async () => {
  document.getElementById("status").innerText = "Request sent";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.tabs.sendMessage(tab.id, { action: "SUMMARIZE" });
});