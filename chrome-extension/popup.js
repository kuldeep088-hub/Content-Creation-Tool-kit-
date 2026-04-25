let currentTitle = '';
let currentUrl = '';

// Get the active tab's video info
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const tab = tabs[0];
  if (!tab) {
    setStatus('Could not get tab info.');
    return;
  }

  currentUrl = tab.url || '';

  if (!currentUrl.includes('youtube.com/watch')) {
    setStatus('Navigate to a YouTube video to analyze it.');
    document.getElementById('analyzeBtn').disabled = true;
    return;
  }

  // Try to get the title from the content script
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const el = document.querySelector('h1.ytd-video-primary-info-renderer yt-formatted-string') ||
                 document.querySelector('h1.title yt-formatted-string') ||
                 document.querySelector('#title h1 yt-formatted-string') ||
                 document.querySelector('meta[name="title"]');
      if (el && el.textContent) return el.textContent.trim();
      if (el && el.content) return el.content.trim();
      return document.title.replace(' - YouTube', '').trim();
    }
  }, (results) => {
    if (chrome.runtime.lastError || !results || !results[0]) {
      currentTitle = tab.title ? tab.title.replace(' - YouTube', '').trim() : 'Unknown Video';
    } else {
      currentTitle = results[0].result || tab.title.replace(' - YouTube', '').trim();
    }

    setStatus('Ready to analyze:');
    const titleEl = document.getElementById('videoTitle');
    titleEl.textContent = currentTitle;
    titleEl.style.display = 'block';
    document.getElementById('analyzeBtn').disabled = false;
  });
});

function setStatus(msg) {
  document.getElementById('status').textContent = msg;
}

async function analyze() {
  if (!currentTitle) {
    showError('No video title found. Make sure you are on a YouTube video page.');
    return;
  }

  const btn = document.getElementById('analyzeBtn');
  const spinner = document.getElementById('spinner');
  const btnText = document.getElementById('btnText');

  btn.disabled = true;
  spinner.style.display = 'inline-block';
  btnText.textContent = 'Analyzing...';
  setStatus('Connecting to Creator Hub...');
  document.getElementById('error').style.display = 'none';
  document.getElementById('results').style.display = 'none';

  try {
    const response = await fetch('http://localhost:3000/api/analyze-video', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: currentTitle, url: currentUrl })
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const data = await response.json();
    renderResults(data);
    setStatus('Analysis complete!');
  } catch (e) {
    if (e.message.includes('Failed to fetch') || e.message.includes('NetworkError')) {
      showError('Cannot connect to Creator Hub. Make sure the app is running at localhost:3000.');
    } else {
      showError('Error: ' + e.message);
    }
    setStatus('Analysis failed.');
  } finally {
    btn.disabled = false;
    spinner.style.display = 'none';
    btnText.textContent = '✨ Analyze Video';
  }
}

function renderResults(data) {
  const resultsEl = document.getElementById('results');
  resultsEl.style.display = 'block';

  // Shorts
  const shortsEl = document.getElementById('shortsResult');
  shortsEl.innerHTML = '';
  (data.shorts || []).forEach(s => {
    const div = document.createElement('div');
    div.className = 'result-item';
    div.textContent = s;
    div.title = 'Click to copy';
    div.onclick = () => {
      navigator.clipboard.writeText(s).then(() => {
        div.style.borderColor = '#10b981';
        setTimeout(() => div.style.borderColor = '#1c1c30', 1500);
      });
    };
    shortsEl.appendChild(div);
  });

  // Hashtags
  const hashtagsEl = document.getElementById('hashtagsResult');
  hashtagsEl.innerHTML = '';
  (data.hashtags || []).forEach(h => {
    const tag = h.startsWith('#') ? h : '#' + h;
    const span = document.createElement('span');
    span.className = 'hashtag';
    span.textContent = tag;
    span.onclick = () => {
      navigator.clipboard.writeText(tag).then(() => {
        span.style.background = 'rgba(16,185,129,0.2)';
        setTimeout(() => span.style.background = '', 1000);
      });
    };
    hashtagsEl.appendChild(span);
  });

  // Hooks
  const hooksEl = document.getElementById('hooksResult');
  hooksEl.innerHTML = '';
  (data.hooks || []).forEach(h => {
    const div = document.createElement('div');
    div.className = 'result-item';
    div.textContent = h;
    div.title = 'Click to copy';
    div.onclick = () => {
      navigator.clipboard.writeText(h).then(() => {
        div.style.borderColor = '#10b981';
        setTimeout(() => div.style.borderColor = '#1c1c30', 1500);
      });
    };
    hooksEl.appendChild(div);
  });
}

function showError(msg) {
  const el = document.getElementById('error');
  el.textContent = msg;
  el.style.display = 'block';
}

function openHub() {
  chrome.tabs.create({ url: 'http://localhost:3000' });
}
