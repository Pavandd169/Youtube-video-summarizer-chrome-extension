// 1. Extract Video ID
function getVideoId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('v');
}

// 2. Call API
async function fetchSummary(videoId) {
    const response = await fetch('http://127.0.0.1:8000/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_id: videoId })
    });

    if (!response.ok) {
        let errorMessage = `Server Error (${response.status})`;
        try {
            const errorData = await response.json();
            if (errorData.detail) errorMessage = errorData.detail;
        } catch (e) {}
        throw new Error(errorMessage);
    }

    const data = await response.json();
    return data.summary;
}

function injectSummarizer() {
    const targetSection = document.querySelector('#secondary');
    if (!targetSection || document.getElementById('ai-summarizer-btn')) return;

    const btn = document.createElement('button');
    btn.id = 'ai-summarizer-btn';
    btn.className = 'ai-summary-btn';
    btn.innerText = '✨ Summarize this Video';
    
    btn.addEventListener('click', async () => {
        const videoId = getVideoId();
        if (!videoId) return alert("No video ID found.");

        const existingBox = document.getElementById('ai-summary-content');
        if (existingBox) existingBox.remove();

        btn.innerText = "Summarizing...";
        btn.disabled = true;

        try {
            const summaryText = await fetchSummary(videoId);
            
            const summaryBox = document.createElement('div');
            summaryBox.id = 'ai-summary-content';
            summaryBox.className = 'ai-summary-box';

            // ⚠️ KEY CHANGE: Parse Markdown to HTML
            // 'marked.parse' comes from the library we added
            summaryBox.innerHTML = marked.parse(summaryText);

            btn.parentNode.insertBefore(summaryBox, btn.nextSibling);

        } catch (error) {
            console.error(error);
            alert(error.message); 
        } finally {
            btn.innerText = '✨ Summarize this Video';
            btn.disabled = false;
        }
    });

    targetSection.prepend(btn);
}

setInterval(injectSummarizer, 2000);