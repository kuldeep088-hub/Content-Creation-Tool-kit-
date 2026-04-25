// Creator Hub Analyzer — Content Script
// Injected into youtube.com pages. Adds a floating "Analyze" button.

(function () {
  'use strict';

  // Avoid duplicate injection
  if (document.getElementById('ch-analyze-btn')) return;

  // Only run on video watch pages
  if (!window.location.pathname.startsWith('/watch')) {
    // Watch for navigation (YouTube is a SPA)
    observeNavigation();
    return;
  }

  injectButton();
  observeNavigation();

  function injectButton() {
    // Remove existing button if any
    const existing = document.getElementById('ch-analyze-btn');
    if (existing) existing.remove();

    if (!window.location.pathname.startsWith('/watch')) return;

    const btn = document.createElement('div');
    btn.id = 'ch-analyze-btn';
    btn.innerHTML = `
      <button id="ch-analyze-inner">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M12 2L2 7l10 5 10-5-10-5z"/>
          <path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>
        </svg>
        <span>Analyze</span>
      </button>
      <div id="ch-panel" style="display:none">
        <div id="ch-panel-title"></div>
        <div id="ch-panel-content"></div>
      </div>
    `;

    const style = document.createElement('style');
    style.textContent = `
      #ch-analyze-btn {
        position: fixed;
        bottom: 80px;
        right: 20px;
        z-index: 9999;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      }
      #ch-analyze-inner {
        display: flex;
        align-items: center;
        gap: 7px;
        padding: 10px 18px;
        background: linear-gradient(135deg, #8b5cf6, #3b82f6);
        color: #fff;
        border: none;
        border-radius: 24px;
        font-size: 13px;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(139,92,246,0.4);
        transition: all 0.2s;
      }
      #ch-analyze-inner:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(139,92,246,0.5);
      }
      #ch-analyze-inner:active { transform: translateY(0); }
      #ch-panel {
        position: absolute;
        bottom: 52px;
        right: 0;
        width: 320px;
        background: #07070f;
        border: 1px solid #252540;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 16px 48px rgba(0,0,0,0.6);
        max-height: 400px;
        overflow-y: auto;
      }
      #ch-panel::-webkit-scrollbar { width: 4px; }
      #ch-panel::-webkit-scrollbar-thumb { background: #252540; border-radius: 2px; }
      #ch-panel-title {
        font-size: 0.78rem;
        font-weight: 700;
        color: #8b5cf6;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }
      .ch-section { margin-bottom: 14px; }
      .ch-section-label {
        font-size: 0.68rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
      }
      .ch-item {
        background: #10101e;
        border: 1px solid #1c1c30;
        border-radius: 6px;
        padding: 8px 10px;
        font-size: 0.78rem;
        color: #94a3b8;
        line-height: 1.5;
        margin-bottom: 5px;
        cursor: pointer;
        transition: border-color 0.15s;
      }
      .ch-item:hover { border-color: #8b5cf6; color: #e2e8f0; }
      .ch-tags { display: flex; flex-wrap: wrap; gap: 4px; }
      .ch-tag {
        padding: 2px 8px;
        background: rgba(139,92,246,0.15);
        border: 1px solid rgba(139,92,246,0.3);
        border-radius: 12px;
        font-size: 0.7rem;
        color: #a78bfa;
        cursor: pointer;
      }
      .ch-tag:hover { background: rgba(139,92,246,0.25); }
      .ch-loading { text-align: center; padding: 20px; color: #64748b; font-size: 0.82rem; }
      .ch-error { color: #ef4444; font-size: 0.78rem; padding: 8px; background: rgba(239,68,68,0.1); border-radius: 6px; }
      .ch-close {
        float: right;
        background: none;
        border: none;
        color: #64748b;
        cursor: pointer;
        font-size: 1rem;
        line-height: 1;
        padding: 0;
        margin-top: -2px;
      }
      .ch-close:hover { color: #e2e8f0; }
    `;

    document.head.appendChild(style);
    document.body.appendChild(btn);

    document.getElementById('ch-analyze-inner').addEventListener('click', handleAnalyzeClick);
  }

  function getVideoTitle() {
    const selectors = [
      'h1.ytd-video-primary-info-renderer yt-formatted-string',
      'h1.title yt-formatted-string',
      '#title h1 yt-formatted-string',
      'h1.ytd-watch-metadata yt-formatted-string'
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el && el.textContent.trim()) return el.textContent.trim();
    }
    return document.title.replace(' - YouTube', '').trim();
  }

  async function handleAnalyzeClick() {
    const panel = document.getElementById('ch-panel');
    const content = document.getElementById('ch-panel-content');
    const titleEl = document.getElementById('ch-panel-title');

    // Toggle panel
    if (panel.style.display !== 'none') {
      panel.style.display = 'none';
      return;
    }
    panel.style.display = 'block';

    const title = getVideoTitle();
    titleEl.innerHTML = `<button class="ch-close" onclick="document.getElementById('ch-panel').style.display='none'">✕</button><span>${escapeHtml(title.slice(0, 60))}${title.length > 60 ? '...' : ''}</span>`;
    content.innerHTML = '<div class="ch-loading">✨ Analyzing with Creator Hub...</div>';

    try {
      const resp = await fetch('http://localhost:3000/api/analyze-video', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, url: window.location.href })
      });

      if (!resp.ok) throw new Error('Server error ' + resp.status);
      const data = await resp.json();
      renderPanel(content, data);
    } catch (e) {
      if (e.message.includes('Failed to fetch') || e.message.includes('NetworkError')) {
        content.innerHTML = '<div class="ch-error">Cannot connect to Creator Hub. Make sure it\'s running at <strong>localhost:3000</strong>.</div>';
      } else {
        content.innerHTML = `<div class="ch-error">${escapeHtml(e.message)}</div>`;
      }
    }
  }

  function renderPanel(container, data) {
    let html = '';

    if (data.shorts && data.shorts.length) {
      html += '<div class="ch-section"><div class="ch-section-label">📜 Short Script Ideas</div>';
      data.shorts.forEach(s => {
        html += `<div class="ch-item" onclick="copyToClipboard('${escapeAttr(s)}')" title="Click to copy">${escapeHtml(s.slice(0, 120))}${s.length > 120 ? '...' : ''}</div>`;
      });
      html += '</div>';
    }

    if (data.hashtags && data.hashtags.length) {
      html += '<div class="ch-section"><div class="ch-section-label">🏷️ Hashtags</div><div class="ch-tags">';
      data.hashtags.forEach(h => {
        const tag = h.startsWith('#') ? h : '#' + h;
        html += `<span class="ch-tag" onclick="copyToClipboard('${escapeAttr(tag)}')" title="Copy">${escapeHtml(tag)}</span>`;
      });
      html += '</div></div>';
    }

    if (data.hooks && data.hooks.length) {
      html += '<div class="ch-section"><div class="ch-section-label">🎣 Hook Ideas</div>';
      data.hooks.forEach(h => {
        html += `<div class="ch-item" onclick="copyToClipboard('${escapeAttr(h)}')" title="Click to copy">${escapeHtml(h)}</div>`;
      });
      html += '</div>';
    }

    html += '<div style="font-size:0.68rem;color:#64748b;text-align:center;padding-top:8px">Click any item to copy</div>';
    container.innerHTML = html;
  }

  // Inject copy helper into page scope
  const script = document.createElement('script');
  script.textContent = `
    window.copyToClipboard = function(text) {
      navigator.clipboard.writeText(text).then(() => {
        const toast = document.createElement('div');
        toast.textContent = 'Copied!';
        toast.style.cssText = 'position:fixed;bottom:140px;right:20px;background:#10b981;color:#fff;padding:6px 14px;border-radius:20px;font-size:12px;font-weight:700;z-index:99999;transition:opacity 0.3s;font-family:sans-serif';
        document.body.appendChild(toast);
        setTimeout(() => { toast.style.opacity='0'; setTimeout(() => toast.remove(), 300); }, 1500);
      });
    };
  `;
  document.head.appendChild(script);

  function escapeHtml(str) {
    return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
  function escapeAttr(str) {
    return String(str).replace(/\\/g,'\\\\').replace(/'/g,"\\'").replace(/\n/g,' ');
  }

  function observeNavigation() {
    // YouTube is a SPA — watch for URL changes
    let lastUrl = location.href;
    const observer = new MutationObserver(() => {
      if (location.href !== lastUrl) {
        lastUrl = location.href;
        setTimeout(() => {
          if (window.location.pathname.startsWith('/watch')) {
            injectButton();
          } else {
            const btn = document.getElementById('ch-analyze-btn');
            if (btn) btn.remove();
          }
        }, 1500);
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }
})();
