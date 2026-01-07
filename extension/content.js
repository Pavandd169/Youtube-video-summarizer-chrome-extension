// 1. Helper: Extract Video ID from URL
function getVideoId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('v');
}

// 2. Helper: Call your FastAPI Backend
async function fetchSummary(videoId) {
    // ⚠️ Ensure this URL matches your running uvicorn port
    const response = await fetch('http://127.0.0.1:8000/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_id: videoId })
    });

    if (!response.ok) {
        throw new Error('Failed to fetch summary');
    }

    const data = await response.json();
    return data.summary;
}

// 3. Main Logic: Inject Button and Handle Click
function injectSummarizer() {
    // A. Check if we are on a video page and if button already exists
    const targetSection = document.querySelector('#secondary'); // The right sidebar
    if (!targetSection || document.getElementById('ai-summarizer-btn')) return;

    // B. Create the Button
    const btn = document.createElement('button');
    btn.id = 'ai-summarizer-btn';
    btn.className = 'ai-summary-btn';
    btn.innerText = '✨ Summarize this Video';
    
    // C. Add Click Event
    btn.addEventListener('click', async () => {
        const videoId = getVideoId();
        if (!videoId) return alert("No video ID found.");

        const existingBox = document.getElementById('ai-summary-content');
        if (existingBox) existingBox.remove(); // Clear old summary

        btn.innerText = "Summarizing... (Please wait)";
        btn.disabled = true;

        try {
            const summaryText = await fetchSummary(videoId);
            
            // Create Summary Box
            const summaryBox = document.createElement('div');
            summaryBox.id = 'ai-summary-content';
            summaryBox.className = 'ai-summary-box';
            summaryBox.innerText = summaryText;

            // Append after the button
            btn.parentNode.insertBefore(summaryBox, btn.nextSibling);

        } catch (error) {
            console.error(error);
            alert("Error generating summary. Make sure your API is running!");
        } finally {
            btn.innerText = '✨ Summarize this Video';
            btn.disabled = false;
        }
    });

    // D. Insert button at the top of the sidebar
    targetSection.prepend(btn);
}

// 4. Run the injector repeatedly
// YouTube is a "Single Page App" (SPA), so the page doesn't reload when you click a new video.
// We use setInterval to keep checking if the button needs to be added.
setInterval(injectSummarizer, 2000);