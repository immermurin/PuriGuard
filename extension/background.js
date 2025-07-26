chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    if (isSuspiciousUrl(tab.url)) {
      console.warn("Suspicious website detected:", tab.url);
      // Send to Python backend for deeper scan
      fetch('http://localhost:5000/scan_url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: tab.url })
      });
    }
  }
});

function isSuspiciousUrl(url) {
  const suspiciousKeywords = ["porn", "nsfw", "hentai", "xxx", "camgirl", "onlyfans", "bet"];
  return suspiciousKeywords.some(word => url.toLowerCase().includes(word));
}