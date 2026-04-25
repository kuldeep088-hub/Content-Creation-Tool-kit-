import os

f = open(r'C:\Users\HP\Desktop\Content Creaction\public\index.html', 'a', encoding='utf-8')

def w(s):
    f.write(s)

# IDs confirmed from HTML:
# scriptOutput (not scriptStreamOut)
# shortsInput (not shortsScript), no shortsCount in HTML
# hookInput1/2/3 (not hook1/2/3)
# captionHashtags (not hashtagsWrap), captionTopic, captionPlatform (no captionTone in HTML)
# seoInput (not seoTopic)
# trackTitle, trackViews, trackLikes, trackCtr (not vtTitle etc)
# voiceText, voiceSpeed, voicePitch, voiceSpeedVal, voicePitchVal (not voText/voRate etc)
# competitorInput (not competitorChannel), no competitorNiche in HTML
# newsletterInput (not newsletterTopic), no newsletterAudience/newsletterTone in HTML
# thumbTextColor (not thumbText)
# notionPreview (not notionOut)
# viewsChart, likesChart, ctrChart, rateChart (not chartViews/chartEng)
# statsRow (no individual stat IDs)
# abResultsWrap (not abResultsTable), abTableBody exists
# abTitle does NOT exist in HTML - need to check what fields AB log form uses
# abDate, abCtrA, abCtrB exist; no abViewsA/abViewsB, no abTitle

w('''
<script>
// ── STATE ─────────────────────────────────────────────────────────────────────
let videos = JSON.parse(localStorage.getItem('cos_videos') || '[]');
let calData = JSON.parse(localStorage.getItem('cos_calendar') || '{}');
let abTests = JSON.parse(localStorage.getItem('cos_ab') || '[]');
let calYear = new Date().getFullYear();
let calMonth = new Date().getMonth();
let calSelDate = null;
let calTypeSelected = 'yt-long';
let charts = {};
let lastScript = '';
let synth = window.speechSynthesis;
let voiceUtter = null;
let voices = [];
const DEMO_KEY = '__demo__';

// ── INIT ─────────────────────────────────────────────────────────────────────
window.onload = () => {
  const stored = localStorage.getItem('cos_apikey');
  const storedLang = localStorage.getItem('cos_lang') || 'English';
  document.getElementById('globalLang').value = storedLang;
  updateLangPill(storedLang);
  if (!stored) {
    document.getElementById('apiModal').classList.remove('hidden');
  } else {
    checkDemoMode(stored);
  }
  if (synth) synth.onvoiceschanged = loadVoices;
  loadVoices();
  renderCalendar();
  renderTracker();
  renderABResults();
  const c = document.getElementById('thumbCanvas');
  if (c) { c.width = 640; c.height = 360; drawThumb(); }
};

// ── TOAST ─────────────────────────────────────────────────────────────────────
function showToast(msg, type, dur) {
  type = type || 'info'; dur = dur || 3200;
  const c = document.getElementById('toastContainer');
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  const colors = { success: 'var(--green)', error: 'var(--red)', info: 'var(--blue)', warning: 'var(--amber)' };
  const t = document.createElement('div');
  t.className = 'toast-item';
  t.style.cssText = 'border-left:3px solid ' + (colors[type]||colors.info);
  t.innerHTML = '<span style="font-size:1rem">' + (icons[type]||icons.info) + '</span><span style="flex:1">' + msg + '</span><span onclick="this.parentElement.remove()" style="cursor:pointer;opacity:0.5;padding-left:8px">×</span>';
  c.appendChild(t);
  setTimeout(function(){ t.classList.add('toast-out'); setTimeout(function(){ t.remove(); }, 320); }, dur);
}

// ── API KEY & DEMO MODE ───────────────────────────────────────────────────────
function saveApiKey() {
  const val = document.getElementById('apiKeyInput').value.trim();
  if (!val) { showToast('Please enter an API key', 'warning'); return; }
  localStorage.setItem('cos_apikey', val);
  setKeyOnServer(val);
  closeModal();
}

async function setKeyOnServer(key) {
  try {
    const r = await fetch('/api/set-key', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({key:key}) });
    const d = await r.json();
    if (d.ok) { checkDemoMode(key); showToast('API key saved — live AI mode active', 'success'); }
    else showToast('Key saved locally', 'info');
  } catch(e) { showToast('Server not reachable', 'error'); }
}

function checkDemoMode(key) {
  const isDemo = !key || key === DEMO_KEY;
  document.getElementById('demoBanner').style.display = isDemo ? 'flex' : 'none';
  const dot = document.getElementById('apiDot');
  const txt = document.getElementById('apiBadgeText');
  dot.className = 'api-dot' + (isDemo ? '' : ' ok');
  txt.textContent = isDemo ? 'Demo Mode' : 'API Key Set';
}

function closeModal() {
  document.getElementById('apiModal').classList.add('hidden');
  if (!localStorage.getItem('cos_apikey')) localStorage.setItem('cos_apikey', DEMO_KEY);
  checkDemoMode(localStorage.getItem('cos_apikey'));
}

function setLanguage(lang) {
  localStorage.setItem('cos_lang', lang);
  updateLangPill(lang);
  showToast('Language set to ' + lang, 'info');
}

function updateLangPill(lang) {
  var pill = document.getElementById('langPill');
  var codes = { English:'EN', Hindi:'HI', Spanish:'ES', Portuguese:'PT', French:'FR', Arabic:'AR', German:'DE', Japanese:'JA' };
  pill.textContent = codes[lang] || lang.slice(0,2).toUpperCase();
  pill.style.display = 'inline-flex';
}

function getLang() { return localStorage.getItem('cos_lang') || 'English'; }

// ── NAVIGATION ────────────────────────────────────────────────────────────────
function showSection(id, el) {
  document.querySelectorAll('.section').forEach(function(s){ s.classList.remove('active'); });
  document.querySelectorAll('.nav-item').forEach(function(n){ n.classList.remove('active'); });
  var sec = document.getElementById('sec-' + id);
  if (sec) sec.classList.add('active');
  if (el) el.classList.add('active');
  if (id === 'tracker') { destroyCharts(); setTimeout(renderTracker, 50); }
  if (id === 'calendar') renderCalendar();
  if (id === 'abthumb') renderABResults();
}

// ── HELPERS ───────────────────────────────────────────────────────────────────
function setLoading(btnId, spinnerId, loading) {
  var btn = document.getElementById(btnId);
  var sp = document.getElementById(spinnerId);
  if (btn) btn.disabled = loading;
  if (sp) sp.style.display = loading ? 'inline-block' : 'none';
}

function showProgress(id, show) {
  var el = document.getElementById(id);
  if (el) el.style.display = show ? 'block' : 'none';
}

function showResult(id) {
  var el = document.getElementById(id);
  if (el) { el.classList.add('show'); el.style.display = 'block'; }
}

async function apiFetch(endpoint, body) {
  const r = await fetch(endpoint, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body) });
  if (!r.ok) throw new Error('API error ' + r.status);
  return r.json();
}

function copyEl(id) {
  var el = document.getElementById(id);
  if (!el) return;
  navigator.clipboard.writeText(el.innerText || el.textContent).then(function(){ showToast('Copied!', 'success'); });
}

function copyText(text) {
  navigator.clipboard.writeText(text).then(function(){ showToast('Copied!', 'success'); });
}

function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function fmtNum(n) { return Number(n).toLocaleString(); }

function downloadBlob(content, filename, mime) {
  mime = mime || 'text/plain';
  var a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([content], {type: mime}));
  a.download = filename;
  a.click();
}

// ── STREAMING CLIENT ──────────────────────────────────────────────────────────
async function streamToEl(endpoint, body, elId, onDone) {
  var el = document.getElementById(elId);
  if (!el) return;
  el.innerHTML = '<span class="stream-cursor"></span>';
  el.scrollTop = 0;
  var raw = '';
  try {
    const res = await fetch(endpoint, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body) });
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    var buf = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      const lines = buf.split('\\n');
      buf = lines.pop();
      for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        if (!line.startsWith('data: ')) continue;
        var payload = line.slice(6).trim();
        if (payload === '[DONE]') break;
        try {
          var obj = JSON.parse(payload);
          if (obj.text) raw += obj.text;
        } catch(e) {}
      }
      el.innerHTML = (typeof marked !== 'undefined' ? marked.parse(raw) : raw) + '<span class="stream-cursor"></span>';
      el.scrollTop = el.scrollHeight;
    }
    el.innerHTML = typeof marked !== 'undefined' ? marked.parse(raw) : raw;
    if (onDone) onDone(raw);
  } catch(e) {
    el.innerHTML = '<span style="color:var(--red)">Stream error: ' + esc(e.message) + '</span>';
  }
}

// ── IDEAS ─────────────────────────────────────────────────────────────────────
async function generateIdeas() {
  var niche = document.getElementById('ideasNiche').value.trim();
  if (!niche) { showToast('Please enter your niche', 'warning'); return; }
  setLoading('ideasBtn','ideasSpinner',true);
  showProgress('ideasProgress',true);
  showResult('ideasResult');
  document.getElementById('ideasGrid').innerHTML = '<div class="empty-state"><div class="icon">⏳</div><p>Generating ideas...</p></div>';
  try {
    const d = await apiFetch('/api/ideas', { niche: niche, platform: document.getElementById('ideasPlatform').value, count: document.getElementById('ideasCount').value, language: getLang() });
    var ideas = d.ideas || [];
    document.getElementById('ideasCountBadge').textContent = ideas.length;
    document.getElementById('ideasGrid').innerHTML = ideas.map(function(idea){
      var fmt = (idea.format||'default').replace(/\\s/g,'');
      return '<div class="idea-card">' +
        '<span class="idea-format fmt-' + fmt + ' fmt-default">' + esc(idea.format||'Video') + '</span>' +
        '<div class="idea-title">' + esc(idea.title) + '</div>' +
        '<div class="idea-hook">"' + esc(idea.hook||'') + '"</div>' +
        '<div class="idea-why">' + esc(idea.why||'') + '</div>' +
        '<div style="margin-top:10px;display:flex;gap:7px;flex-wrap:wrap">' +
          '<button class="btn btn-ghost btn-sm" onclick="copyText(' + JSON.stringify(idea.title) + ')">Copy</button>' +
          '<button class="btn btn-ghost btn-sm" onclick="document.getElementById(\'scriptTopic\').value=' + JSON.stringify(idea.title) + ';showSection(\'script\',null)">→ Script</button>' +
        '</div></div>';
    }).join('');
    showToast(ideas.length + ' ideas generated', 'success');
  } catch(e) {
    document.getElementById('ideasGrid').innerHTML = '<div class="empty-state"><p>Error: ' + esc(e.message) + '</p></div>';
    showToast('Error generating ideas', 'error');
  }
  setLoading('ideasBtn','ideasSpinner',false);
  showProgress('ideasProgress',false);
}

// ── SCRIPT WRITER (streaming) ─────────────────────────────────────────────────
async function generateScript() {
  var topic = document.getElementById('scriptTopic').value.trim();
  if (!topic) { showToast('Please enter a topic', 'warning'); return; }
  setLoading('scriptBtn','scriptSpinner',true);
  showResult('scriptResult');
  var out = document.getElementById('scriptOutput');
  out.style.display = 'block';
  await streamToEl('/api/stream/script', {
    topic: topic,
    duration: document.getElementById('scriptDuration').value,
    style: document.getElementById('scriptStyle').value,
    language: getLang()
  }, 'scriptOutput', function(raw) {
    lastScript = raw;
    showToast('Script complete', 'success');
    setLoading('scriptBtn','scriptSpinner',false);
  });
  setLoading('scriptBtn','scriptSpinner',false);
}

// ── SHORTS REPURPOSER ─────────────────────────────────────────────────────────
async function generateShorts() {
  var script = document.getElementById('shortsInput').value.trim();
  if (!script) { showToast('Enter a URL or topic', 'warning'); return; }
  setLoading('shortsBtn','shortsSpinner',true);
  showProgress('shortsProgress',true);
  showResult('shortsResult');
  document.getElementById('shortsGrid').innerHTML = '<div class="empty-state"><div class="icon">⏳</div><p>Extracting shorts...</p></div>';
  try {
    const d = await apiFetch('/api/shorts', { script: script, count: 7, language: getLang() });
    var shorts = d.shorts || [];
    document.getElementById('shortsGrid').innerHTML = shorts.map(function(s,i){
      return '<div class="short-card" id="sc' + i + '">' +
        '<div class="short-header" onclick="this.parentElement.classList.toggle(\'open\')">' +
          '<div class="short-num">' + (i+1) + '</div>' +
          '<div class="short-title-wrap"><div class="short-title-text">' + esc(s.title||s.hook||'Short '+(i+1)) + '</div><div class="short-ts">' + esc(s.duration||'~60s') + '</div></div>' +
          '<span class="short-chevron">▾</span>' +
        '</div>' +
        '<div class="short-body">' +
          '<div class="short-field"><div class="short-field-label">Hook</div><div class="short-field-value">' + esc(s.hook||'') + '</div></div>' +
          '<div class="short-field"><div class="short-field-label">Script</div><div class="short-field-value">' + esc(s.script||s.content||'') + '</div></div>' +
          '<div class="short-field"><div class="short-field-label">CTA</div><div class="short-field-value">' + esc(s.cta||'') + '</div></div>' +
          '<div class="short-tags">' + (s.hashtags||[]).map(function(h){ return '<span class="short-tag">' + esc(h) + '</span>'; }).join('') + '</div>' +
          '<div style="margin-top:12px"><button class="btn btn-ghost btn-sm" onclick="copyText(' + JSON.stringify((s.hook||'')+' '+(s.script||s.content||'')+' '+(s.cta||'')) + ')">Copy Script</button></div>' +
        '</div></div>';
    }).join('');
    showToast(shorts.length + ' shorts created', 'success');
  } catch(e) {
    document.getElementById('shortsGrid').innerHTML = '<div class="empty-state"><p>Error: ' + esc(e.message) + '</p></div>';
    showToast('Error', 'error');
  }
  setLoading('shortsBtn','shortsSpinner',false);
  showProgress('shortsProgress',false);
}

// ── THUMBNAIL STUDIO ──────────────────────────────────────────────────────────
var thumbTemplate = 'gradient';
var thumbPreset = 'YouTube 16:9';
var presets = { 'YouTube 16:9':[1280,720], 'YouTube Shorts':[1080,1920], 'Instagram Post':[1080,1080] };

function switchThumbTab(tab, btn) {
  document.querySelectorAll('.thumb-tab').forEach(function(t){ t.classList.remove('active'); });
  document.querySelectorAll('.thumb-tab-content').forEach(function(c){ c.classList.remove('active'); });
  if (btn) btn.classList.add('active');
  var tc = document.getElementById('thumbTab' + tab.charAt(0).toUpperCase() + tab.slice(1));
  if (!tc) tc = document.getElementById('thumbTab' + tab);
  if (tc) tc.classList.add('active');
}

function setTemplate(btn, tpl) {
  thumbTemplate = tpl;
  document.querySelectorAll('.tpl-btn').forEach(function(b){ b.classList.remove('active'); });
  if (btn) btn.classList.add('active');
  drawThumb();
}

function selectPreset(btn, style) {
  document.querySelectorAll('.preset-btn').forEach(function(b){ b.classList.remove('active'); });
  if (btn) btn.classList.add('active');
}

function updateCanvasSize() {
  var c = document.getElementById('thumbCanvas');
  var fmt = document.getElementById('thumbFormat').value;
  if (fmt === 'shorts') { c.width = 360; c.height = 640; }
  else if (fmt === 'square') { c.width = 360; c.height = 360; }
  else { c.width = 640; c.height = 360; }
  drawThumb();
}

function drawThumb() {
  var c = document.getElementById('thumbCanvas');
  if (!c) return;
  var ctx = c.getContext('2d');
  var W = c.width, H = c.height;
  var titleEl = document.getElementById('thumbTitle');
  var subEl = document.getElementById('thumbSub');
  var bg1El = document.getElementById('thumbBg1');
  var bg2El = document.getElementById('thumbBg2');
  var txtEl = document.getElementById('thumbTextColor');
  var title = titleEl ? titleEl.value : 'Your Title Here';
  var sub = subEl ? subEl.value : '';
  var bg1 = bg1El ? bg1El.value : '#7c3aed';
  var bg2 = bg2El ? bg2El.value : '#2563eb';
  var textColor = txtEl ? txtEl.value : '#ffffff';
  ctx.clearRect(0,0,W,H);
  var grad = ctx.createLinearGradient(0,0,W,H);
  if (thumbTemplate === 'dark') {
    ctx.fillStyle = '#0a0a0f'; ctx.fillRect(0,0,W,H);
    grad.addColorStop(0, bg1+'44'); grad.addColorStop(1, bg2+'22');
    ctx.fillStyle = grad; ctx.fillRect(0,0,W,H);
    ctx.strokeStyle = bg1; ctx.lineWidth = 3; ctx.strokeRect(8,8,W-16,H-16);
  } else if (thumbTemplate === 'split') {
    ctx.fillStyle = bg1; ctx.fillRect(0,0,W/2,H);
    ctx.fillStyle = bg2; ctx.fillRect(W/2,0,W/2,H);
    ctx.fillStyle = 'rgba(0,0,0,0.25)'; ctx.fillRect(0,0,W,H);
  } else if (thumbTemplate === 'minimal') {
    ctx.fillStyle = '#111'; ctx.fillRect(0,0,W,H);
    ctx.fillStyle = bg1; ctx.fillRect(0,H-6,W,6);
  } else if (thumbTemplate === 'bold') {
    grad.addColorStop(0, bg1); grad.addColorStop(1, bg2);
    ctx.fillStyle = grad; ctx.fillRect(0,0,W,H);
    ctx.fillStyle = 'rgba(0,0,0,0.15)'; ctx.fillRect(0,H*0.6,W,H*0.4);
  } else {
    // gradient (default)
    grad.addColorStop(0, bg1); grad.addColorStop(1, bg2);
    ctx.fillStyle = grad; ctx.fillRect(0,0,W,H);
  }
  var fs = Math.max(20, Math.min(W * 0.068, 80));
  var sizeEl = document.getElementById('thumbSize');
  if (sizeEl) fs = Math.max(20, Math.min(parseInt(sizeEl.value)||52, 90));
  ctx.fillStyle = textColor;
  ctx.font = '900 ' + fs + 'px "Arial Black", Arial, sans-serif';
  ctx.textAlign = 'center';
  var words = title.split(' ');
  var lines = []; var cur = '';
  for (var wi = 0; wi < words.length; wi++) {
    var test = cur ? cur + ' ' + words[wi] : words[wi];
    if (ctx.measureText(test).width > W * 0.88 && cur) { lines.push(cur); cur = words[wi]; }
    else cur = test;
  }
  if (cur) lines.push(cur);
  var lh = fs * 1.2;
  var startY = H/2 - (lines.length - 1) * lh/2;
  ctx.shadowColor = 'rgba(0,0,0,0.7)'; ctx.shadowBlur = 6; ctx.shadowOffsetY = 2;
  for (var li = 0; li < lines.length; li++) ctx.fillText(lines[li], W/2, startY + li*lh);
  ctx.shadowBlur = 0; ctx.shadowOffsetY = 0;
  if (sub) {
    ctx.font = '600 ' + Math.round(fs*0.38) + 'px Arial, sans-serif';
    ctx.fillStyle = textColor + 'bb';
    ctx.fillText(sub, W/2, startY + lines.length*lh + fs*0.3);
  }
}

function downloadThumb() {
  var c = document.getElementById('thumbCanvas');
  var a = document.createElement('a');
  a.download = 'thumbnail.png';
  a.href = c.toDataURL('image/png');
  a.click();
  showToast('Thumbnail downloaded', 'success');
}

async function generateAIThumb() {
  var title = document.getElementById('aiThumbPrompt').value.trim();
  if (!title) { showToast('Enter a prompt first', 'warning'); return; }
  var btn = document.getElementById('aiThumbBtn');
  btn.disabled = true;
  var img = document.getElementById('aiThumbImg');
  var url = 'https://image.pollinations.ai/prompt/' + encodeURIComponent(title + ', youtube thumbnail, professional, vibrant, 16:9') + '?width=1280&height=720&nologo=true';
  img.style.display = 'block';
  img.src = url;
  img.onload = function() {
    btn.disabled = false;
    var dl = document.getElementById('aiThumbDownloadWrap');
    var dlBtn = document.getElementById('aiThumbDownloadBtn');
    if (dl) dl.style.display = 'block';
    if (dlBtn) { dlBtn.href = url; dlBtn.download = 'ai-thumbnail.jpg'; }
    showToast('AI thumbnail ready', 'success');
  };
  img.onerror = function() { btn.disabled = false; showToast('Generation failed', 'error'); };
}

// ── CAPTIONS ──────────────────────────────────────────────────────────────────
async function generateCaption() {
  var topic = document.getElementById('captionTopic').value.trim();
  if (!topic) { showToast('Enter a topic', 'warning'); return; }
  setLoading('captionBtn','captionSpinner',true);
  showProgress('captionProgress',true);
  showResult('captionResult');
  try {
    const d = await apiFetch('/api/captions', { topic: topic, platform: document.getElementById('captionPlatform').value, language: getLang() });
    var captionHook = document.getElementById('captionHook');
    var captionBody = document.getElementById('captionBody');
    var captionCta = document.getElementById('captionCta');
    var captionBestTime = document.getElementById('captionBestTime');
    if (captionHook) captionHook.textContent = d.hook || d.caption?.split('\\n')[0] || '';
    if (captionBody) captionBody.textContent = d.caption || d.body || '';
    if (captionCta) captionCta.textContent = d.cta || '';
    if (captionBestTime) captionBestTime.textContent = d.best_time || '9AM–11AM';
    var tags = d.hashtags || [];
    var hashEl = document.getElementById('captionHashtags');
    if (hashEl) hashEl.innerHTML = tags.map(function(h){ return '<span class="hashtag" onclick="copyText(' + JSON.stringify(h) + ')">' + esc(h) + '</span>'; }).join('');
    showToast('Caption ready', 'success');
  } catch(e) { showToast(e.message, 'error'); }
  setLoading('captionBtn','captionSpinner',false);
  showProgress('captionProgress',false);
}

function copyHashtags() {
  var el = document.getElementById('captionHashtags');
  if (!el) return;
  var text = Array.from(el.querySelectorAll('.hashtag')).map(function(h){ return h.textContent; }).join(' ');
  copyText(text);
}

// ── SEO ───────────────────────────────────────────────────────────────────────
async function generateSEO() {
  var topic = document.getElementById('seoInput').value.trim();
  if (!topic) { showToast('Enter a topic or URL', 'warning'); return; }
  setLoading('seoBtn','seoSpinner',true);
  showProgress('seoProgress',true);
  showResult('seoResult');
  try {
    const d = await apiFetch('/api/seo', { topic: topic, language: getLang() });
    var titles = d.titles || [];
    document.getElementById('seoTitles').innerHTML = titles.map(function(t,i){
      return '<div class="title-variant"><div class="variant-badge">' + (i+1) + '</div><div>' +
        '<div class="variant-title">' + esc(t.title||t) + '</div>' +
        '<div class="variant-why">' + esc(t.why||'') + '</div>' +
        '<button class="btn btn-ghost btn-sm" style="margin-top:7px" onclick="copyText(' + JSON.stringify(t.title||t) + ')">Copy</button>' +
        '</div></div>';
    }).join('');
    var descEl = document.getElementById('seoDesc');
    if (descEl) descEl.textContent = d.description || '';
    var tags = d.tags || d.keywords || [];
    document.getElementById('seoTags').innerHTML = tags.map(function(t){ return '<span class="seo-tag">' + esc(t) + '</span>'; }).join('');
    var chaps = d.chapters || [];
    var chapEl = document.getElementById('seoChapters');
    if (chapEl) chapEl.innerHTML = chaps.length ? chaps.map(function(c){ return '<div class="chapter-item"><span class="chapter-time">' + esc(c.time||'0:00') + '</span><span class="chapter-title">' + esc(c.title||c) + '</span></div>'; }).join('') : '<span style="color:var(--text3);font-size:0.83rem">No chapters generated</span>';
    var tipEl = document.getElementById('seoThumbTip');
    if (tipEl) tipEl.textContent = d.thumbnail_tip || d.tip || 'Use high contrast and a readable font at small sizes.';
    showToast('SEO package ready', 'success');
  } catch(e) { showToast(e.message, 'error'); }
  setLoading('seoBtn','seoSpinner',false);
  showProgress('seoProgress',false);
}

// ── PERFORMANCE TRACKER ───────────────────────────────────────────────────────
function addVideo() {
  var title = document.getElementById('trackTitle').value.trim();
  if (!title) { showToast('Enter a video title', 'warning'); return; }
  videos.push({
    id: Date.now(),
    title: title,
    views: parseInt(document.getElementById('trackViews').value) || 0,
    likes: parseInt(document.getElementById('trackLikes').value) || 0,
    ctr: parseFloat(document.getElementById('trackCtr').value) || 0,
    date: new Date().toISOString().slice(0,10)
  });
  localStorage.setItem('cos_videos', JSON.stringify(videos));
  ['trackTitle','trackViews','trackLikes','trackCtr'].forEach(function(id){ document.getElementById(id).value = ''; });
  renderTracker();
  showToast('Video added', 'success');
}

function deleteVideo(id) {
  videos = videos.filter(function(v){ return v.id !== id; });
  localStorage.setItem('cos_videos', JSON.stringify(videos));
  destroyCharts();
  renderTracker();
  showToast('Video removed', 'info');
}

function destroyCharts() {
  Object.keys(charts).forEach(function(k){ if (charts[k]) charts[k].destroy(); });
  charts = {};
}

function renderTracker() {
  var tbody = document.getElementById('videosBody');
  var trackerData = document.getElementById('trackerData');
  var trackerEmpty = document.getElementById('trackerEmpty');
  if (!tbody) return;

  if (trackerData) trackerData.style.display = videos.length ? 'block' : 'none';
  if (trackerEmpty) trackerEmpty.style.display = videos.length ? 'none' : 'block';

  if (!videos.length) { tbody.innerHTML = ''; return; }

  tbody.innerHTML = videos.map(function(v){
    var likeRate = v.views ? Math.round(v.likes / v.views * 100) : 0;
    return '<tr>' +
      '<td class="td-title">' + esc(v.title) + '</td>' +
      '<td>' + fmtNum(v.views) + '</td>' +
      '<td>' + fmtNum(v.likes) + '</td>' +
      '<td>' + (v.ctr||0) + '%</td>' +
      '<td>' + likeRate + '%</td>' +
      '<td><span class="td-del" onclick="deleteVideo(' + v.id + ')">✕</span></td>' +
    '</tr>';
  }).join('');

  // Stats row
  var totalViews = videos.reduce(function(a,v){ return a+v.views; }, 0);
  var totalLikes = videos.reduce(function(a,v){ return a+v.likes; }, 0);
  var avgCtr = videos.length ? (videos.reduce(function(a,v){ return a+v.ctr; }, 0) / videos.length).toFixed(1) : 0;
  var avgEng = totalViews ? Math.round(totalLikes / totalViews * 100) : 0;
  var statsRow = document.getElementById('statsRow');
  if (statsRow) {
    statsRow.innerHTML =
      '<div class="stat-box"><div class="stat-val">' + fmtNum(totalViews) + '</div><div class="stat-lbl">Total Views</div></div>' +
      '<div class="stat-box"><div class="stat-val">' + fmtNum(totalLikes) + '</div><div class="stat-lbl">Total Likes</div></div>' +
      '<div class="stat-box"><div class="stat-val">' + avgCtr + '%</div><div class="stat-lbl">Avg CTR</div></div>' +
      '<div class="stat-box"><div class="stat-val">' + avgEng + '%</div><div class="stat-lbl">Engagement</div></div>';
  }

  destroyCharts();
  var labels = videos.map(function(v){ return v.title.length > 16 ? v.title.slice(0,16)+'…' : v.title; });
  var chartCfg = { responsive:true, plugins:{legend:{display:false}}, scales:{x:{ticks:{color:'#8892b0',font:{size:10}}},y:{ticks:{color:'#8892b0'}}} };
  var cViews = document.getElementById('viewsChart');
  var cLikes = document.getElementById('likesChart');
  var cCtr = document.getElementById('ctrChart');
  var cRate = document.getElementById('rateChart');
  if (cViews) charts.views = new Chart(cViews, { type:'bar', data:{ labels:labels, datasets:[{ data:videos.map(function(v){ return v.views; }), backgroundColor:'rgba(139,92,246,0.6)', borderColor:'#8b5cf6', borderWidth:1, borderRadius:4 }] }, options:chartCfg });
  if (cLikes) charts.likes = new Chart(cLikes, { type:'bar', data:{ labels:labels, datasets:[{ data:videos.map(function(v){ return v.likes; }), backgroundColor:'rgba(59,130,246,0.6)', borderColor:'#3b82f6', borderWidth:1, borderRadius:4 }] }, options:chartCfg });
  if (cCtr) charts.ctr = new Chart(cCtr, { type:'bar', data:{ labels:labels, datasets:[{ data:videos.map(function(v){ return v.ctr||0; }), backgroundColor:'rgba(16,185,129,0.6)', borderColor:'#10b981', borderWidth:1, borderRadius:4 }] }, options:chartCfg });
  if (cRate) charts.rate = new Chart(cRate, { type:'bar', data:{ labels:labels, datasets:[{ data:videos.map(function(v){ return v.views?Math.round(v.likes/v.views*100):0; }), backgroundColor:'rgba(245,158,11,0.6)', borderColor:'#f59e0b', borderWidth:1, borderRadius:4 }] }, options:chartCfg });
}

// ── IMPROVE (streaming) ───────────────────────────────────────────────────────
async function getImprovement() {
  if (!videos.length) { showToast('Add videos first', 'warning'); return; }
  setLoading('improveBtn','improveSpinner',true);
  var result = document.getElementById('improveResult');
  if (result) result.style.display = 'block';
  var suggestions = document.getElementById('improveSuggestions');
  var empty = document.getElementById('improveEmpty');
  if (suggestions) suggestions.style.display = 'block';
  if (empty) empty.style.display = 'none';
  var top3 = videos.slice().sort(function(a,b){ return b.views-a.views; }).slice(0,3);
  await streamToEl('/api/stream/improve', { videos: top3, language: getLang() }, 'improveSuggestions', function() {
    setLoading('improveBtn','improveSpinner',false);
    showToast('Analysis complete', 'success');
  });
  setLoading('improveBtn','improveSpinner',false);
}

// ── YOUTUBE STATS ─────────────────────────────────────────────────────────────
async function fetchYTStats() {
  var key = document.getElementById('ytApiKey').value.trim();
  var channelId = document.getElementById('ytChannelId').value.trim();
  if (!channelId) { showToast('Enter a Channel ID', 'warning'); return; }
  setLoading('ytFetchBtn','ytFetchSpinner',true);
  var infoEl = document.getElementById('ytChannelInfo');
  if (infoEl) { infoEl.style.display = 'block'; infoEl.textContent = 'Fetching...'; }
  try {
    const d = await apiFetch('/api/youtube-stats', { channelId: channelId, apiKey: key });
    if (infoEl) infoEl.innerHTML = '<pre style="white-space:pre-wrap;font-size:0.78rem">' + esc(JSON.stringify(d,null,2)) + '</pre>';
    showToast('Stats fetched', 'success');
  } catch(e) {
    if (infoEl) infoEl.textContent = e.message;
    showToast(e.message,'error');
  }
  setLoading('ytFetchBtn','ytFetchSpinner',false);
}

// ── HOOK TESTER ───────────────────────────────────────────────────────────────
async function testHooks() {
  var h1 = document.getElementById('hookInput1').value.trim();
  var h2 = document.getElementById('hookInput2').value.trim();
  var h3 = document.getElementById('hookInput3').value.trim();
  if (!h1) { showToast('Enter at least Hook 1', 'warning'); return; }
  setLoading('hooksBtn','hooksSpinner',true);
  showProgress('hooksProgress',true);
  showResult('hooksResult');
  try {
    const d = await apiFetch('/api/hooks', { hooks: [h1,h2,h3].filter(Boolean), language: getLang() });
    var hooks = d.hooks || d.results || [];
    var maxScore = Math.max.apply(null, hooks.map(function(h){ return h.total||h.score||0; }));
    document.getElementById('hooksGrid').innerHTML = hooks.map(function(h){
      var isWinner = (h.total||h.score||0) === maxScore;
      var scores = h.scores || {};
      return '<div class="hook-result-card' + (isWinner?' winner':'') + '">' +
        (isWinner ? '<div class="hook-winner-badge">🏆 Best Hook</div>' : '') +
        '<div style="font-size:0.92rem;font-weight:600;color:var(--text);margin-bottom:10px">"' + esc(h.hook||h.text||'') + '"</div>' +
        '<div class="hook-total">' + (h.total||h.score||0) + '/100</div>' +
        '<div class="hook-score-bars">' +
          Object.entries(scores).map(function(e){
            return '<div class="hook-score-row"><span class="hook-score-label">' + esc(e[0]) + '</span>' +
              '<div class="hook-score-bar-track"><div class="hook-score-bar-fill" style="width:' + e[1] + '%"></div></div>' +
              '<span class="hook-score-num">' + e[1] + '</span></div>';
          }).join('') +
        '</div>' +
        '<div class="hook-feedback">' + esc(h.feedback||h.reasoning||'') + '</div>' +
        '<button class="btn btn-ghost btn-sm" style="margin-top:10px" onclick="copyText(' + JSON.stringify(h.hook||h.text||'') + ')">Copy Hook</button>' +
      '</div>';
    }).join('');
    showToast('Hook analysis complete', 'success');
  } catch(e) { showToast(e.message,'error'); }
  setLoading('hooksBtn','hooksSpinner',false);
  showProgress('hooksProgress',false);
}

function fillDemoHooks() {
  document.getElementById('hookInput1').value = "Wait — you've been brushing your teeth wrong your entire life";
  document.getElementById('hookInput2').value = "The morning habit that made me $10K in 30 days";
  document.getElementById('hookInput3').value = "Stop doing this if you want to grow on YouTube";
}

// ── VOICEOVER ─────────────────────────────────────────────────────────────────
function loadVoices() {
  if (!synth) return;
  voices = synth.getVoices();
  var sel = document.getElementById('voiceSelect');
  if (!sel) return;
  sel.innerHTML = '';
  var enVoices = voices.filter(function(v){ return v.lang.startsWith('en'); });
  var toShow = enVoices.length ? enVoices : voices.slice(0,20);
  toShow.forEach(function(v,i){
    var opt = document.createElement('option');
    opt.value = i; opt.textContent = v.name + (v.default?' (default)':'');
    sel.appendChild(opt);
  });
}

function fillFromLastScript() {
  if (!lastScript) { showToast('Generate a script first', 'warning'); return; }
  var plain = lastScript.replace(/[#*_`]/g,'').replace(/\n+/g,' ').trim().slice(0,1500);
  document.getElementById('voiceText').value = plain;
  showToast('Script loaded into voiceover', 'success');
}

function playVoiceover() {
  if (!synth) { showToast('Speech synthesis not supported', 'error'); return; }
  var text = document.getElementById('voiceText').value.trim();
  if (!text) { showToast('Enter text first', 'warning'); return; }
  synth.cancel();
  voiceUtter = new SpeechSynthesisUtterance(text);
  var selIdx = parseInt(document.getElementById('voiceSelect').value) || 0;
  var enVoices = voices.filter(function(v){ return v.lang.startsWith('en'); });
  var toUse = enVoices.length ? enVoices : voices;
  if (toUse[selIdx]) voiceUtter.voice = toUse[selIdx];
  var speedEl = document.getElementById('voiceSpeed');
  var pitchEl = document.getElementById('voicePitch');
  voiceUtter.rate = speedEl ? parseFloat(speedEl.value)||1 : 1;
  voiceUtter.pitch = pitchEl ? parseFloat(pitchEl.value)||1 : 1;
  voiceUtter.onend = function(){ showToast('Voiceover complete', 'success'); };
  synth.speak(voiceUtter);
  showToast('Playing voiceover...', 'info');
}

function pauseVoiceover() {
  if (synth) { if (synth.paused) synth.resume(); else synth.pause(); }
}

function stopVoiceover() {
  if (synth) synth.cancel();
}

function generateElevenLabs() {
  showToast('ElevenLabs: add your XI API key in server.js to enable', 'info', 5000);
}

// ── CONTENT CALENDAR ──────────────────────────────────────────────────────────
function calKey(y,m,d) { return y + '-' + String(m+1).padStart(2,'0') + '-' + String(d).padStart(2,'0'); }
function saveCalendar() { localStorage.setItem('cos_calendar', JSON.stringify(calData)); }

function calNav(dir) {
  calMonth += dir;
  if (calMonth > 11) { calMonth = 0; calYear++; }
  if (calMonth < 0) { calMonth = 11; calYear--; }
  renderCalendar();
}

function renderCalendar() {
  var el = document.getElementById('calGrid');
  var titleEl = document.getElementById('calMonthTitle');
  if (!el) return;
  var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  if (titleEl) titleEl.textContent = months[calMonth] + ' ' + calYear;
  var first = new Date(calYear, calMonth, 1).getDay();
  var days = new Date(calYear, calMonth+1, 0).getDate();
  var prevDays = new Date(calYear, calMonth, 0).getDate();
  var today = new Date();
  var html = '';
  var dow = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  dow.forEach(function(d){ html += '<div class="cal-dow">' + d + '</div>'; });
  for (var i = 0; i < first; i++) {
    var pd = prevDays - first + 1 + i;
    html += '<div class="cal-day other-month"><div class="cal-day-num">' + pd + '</div></div>';
  }
  for (var d = 1; d <= days; d++) {
    var key = calKey(calYear, calMonth, d);
    var isToday = d===today.getDate()&&calMonth===today.getMonth()&&calYear===today.getFullYear();
    var items = calData[key] || [];
    var show = items.slice(0,2);
    var more = items.length - 2;
    html += '<div class="cal-day' + (isToday?' today':'') + '" onclick="openCalModal(\'' + key + '\')">' +
      '<div class="cal-day-num">' + d + '</div>' +
      show.map(function(it){ return '<div class="cal-item-badge ' + it.type + '">' + esc(it.title||it.type) + '</div>'; }).join('') +
      (more>0?'<div class="cal-day-count">+' + more + '</div>':'') +
    '</div>';
  }
  var cells = first + days;
  var rem = cells % 7 ? 7 - (cells%7) : 0;
  for (var i2=1;i2<=rem;i2++) html += '<div class="cal-day other-month"><div class="cal-day-num">' + i2 + '</div></div>';
  el.innerHTML = html;
  var sumEl = document.getElementById('calSummary');
  if (sumEl) renderCalSummary(sumEl);
}

function renderCalSummary(el) {
  var allItems = Object.values(calData).reduce(function(a,b){ return a.concat(b); }, []);
  var counts = {};
  allItems.forEach(function(it){ counts[it.type] = (counts[it.type]||0) + 1; });
  var labels = {'yt-long':'YouTube Long','yt-short':'YouTube Short','ig-post':'Instagram Post','ig-reel':'Instagram Reel'};
  var colors = {'yt-long':'#ef4444','yt-short':'#f59e0b','ig-post':'#a78bfa','ig-reel':'#60a5fa'};
  el.innerHTML = Object.keys(counts).map(function(k){
    return '<div class="cal-legend-item"><div class="cal-legend-dot" style="background:' + (colors[k]||'#8892b0') + '"></div><span>' + (labels[k]||k) + ': ' + counts[k] + '</span></div>';
  }).join('') || '<span style="color:var(--text3);font-size:0.8rem">No content scheduled yet</span>';
}

function openCalModal(dateKey) {
  calSelDate = dateKey;
  calTypeSelected = 'yt-long';
  var titleEl = document.getElementById('calModalTitle');
  var itemEl = document.getElementById('calItemTitle');
  if (titleEl) titleEl.textContent = 'Content for ' + dateKey;
  if (itemEl) itemEl.value = '';
  renderCalModalItems();
  document.getElementById('calModal').classList.add('open');
}

function renderCalModalItems() {
  var items = calData[calSelDate] || [];
  var el = document.getElementById('calModalItems');
  if (!el) return;
  el.innerHTML = items.length ? items.map(function(it,i){
    return '<div class="cal-existing-item">' +
      '<span class="cal-item-badge ' + it.type + '" style="width:auto;margin:0">' + it.type + '</span>' +
      '<span style="flex:1;font-size:0.83rem;color:var(--text2);margin-left:8px">' + esc(it.title||'') + '</span>' +
      '<button class="remove-btn" onclick="removeCalItem(' + i + ')">✕</button>' +
    '</div>';
  }).join('') : '<p style="color:var(--text3);font-size:0.8rem;margin-bottom:8px">No content scheduled</p>';
}

function selectCalType(type, el) {
  calTypeSelected = type;
  document.querySelectorAll('.cal-type-btn').forEach(function(b){ b.classList.remove('selected'); });
  if (el) el.classList.add('selected');
}

function addCalItem() {
  if (!calSelDate) return;
  if (!calData[calSelDate]) calData[calSelDate] = [];
  var titleEl = document.getElementById('calItemTitle');
  calData[calSelDate].push({ type: calTypeSelected, title: titleEl ? titleEl.value.trim() : '' });
  saveCalendar();
  if (titleEl) titleEl.value = '';
  renderCalModalItems();
  renderCalendar();
  showToast('Added to calendar', 'success');
}

function removeCalItem(idx) {
  if (calData[calSelDate]) {
    calData[calSelDate].splice(idx, 1);
    saveCalendar(); renderCalModalItems(); renderCalendar();
  }
}

function closeCalModal() { document.getElementById('calModal').classList.remove('open'); }

function clearCalMonth() {
  var prefix = calYear + '-' + String(calMonth+1).padStart(2,'0');
  Object.keys(calData).filter(function(k){ return k.startsWith(prefix); }).forEach(function(k){ delete calData[k]; });
  saveCalendar(); renderCalendar();
  showToast('Month cleared', 'info');
}

// ── A/B THUMBNAIL TRACKER ─────────────────────────────────────────────────────
function previewAB(ab, input) {
  var file = input.files[0];
  if (!file) return;
  var img = document.getElementById('abImg' + ab);
  if (img) { img.src = URL.createObjectURL(file); img.style.display = 'block'; }
}

function saveABTests() { localStorage.setItem('cos_ab', JSON.stringify(abTests)); }

function logABTest() {
  var ctrA = parseFloat(document.getElementById('abCtrA').value)||0;
  var ctrB = parseFloat(document.getElementById('abCtrB').value)||0;
  var date = document.getElementById('abDate').value || new Date().toISOString().slice(0,10);
  var nameA = document.getElementById('abNameA') ? document.getElementById('abNameA').value.trim()||'Variant A' : 'Variant A';
  var nameB = document.getElementById('abNameB') ? document.getElementById('abNameB').value.trim()||'Variant B' : 'Variant B';
  abTests.push({ nameA:nameA, nameB:nameB, ctrA:ctrA, ctrB:ctrB, date:date });
  saveABTests(); renderABResults();
  ['abCtrA','abCtrB'].forEach(function(id){ document.getElementById(id).value=''; });
  showToast('A/B test logged', 'success');
}

function renderABResults() {
  var wrap = document.getElementById('abResultsWrap');
  var tbody = document.getElementById('abTableBody');
  var winnerBox = document.getElementById('abWinnerBox');
  if (!tbody) return;
  if (!abTests.length) { if (wrap) wrap.style.display='none'; return; }
  if (wrap) wrap.style.display='block';
  tbody.innerHTML = abTests.map(function(t){
    var winner = t.ctrA>=t.ctrB ? t.nameA : t.nameB;
    return '<tr><td>' + esc(t.date) + '</td><td>' + t.ctrA + '%</td><td>' + t.ctrB + '%</td><td><span class="winner-pill">' + esc(winner) + '</span></td></tr>';
  }).join('');
  if (winnerBox) {
    var last = abTests[abTests.length-1];
    var w = last.ctrA>=last.ctrB ? last.nameA : last.nameB;
    var improvement = Math.abs(last.ctrA-last.ctrB).toFixed(1);
    winnerBox.innerHTML = '<div style="font-family:\'Bricolage Grotesque\',sans-serif;font-size:0.9rem;font-weight:700;color:var(--green);margin-bottom:6px">🏆 Latest Winner: ' + esc(w) + '</div><div style="font-size:0.8rem;color:var(--text2)">CTR advantage: +' + improvement + '% over the losing variant</div>';
  }
  var chartEl = document.getElementById('abChart');
  if (chartEl && typeof Chart !== 'undefined') {
    if (charts.ab) { charts.ab.destroy(); }
    charts.ab = new Chart(chartEl, {
      type: 'line',
      data: {
        labels: abTests.map(function(t){ return t.date; }),
        datasets: [
          { label:'CTR A', data:abTests.map(function(t){ return t.ctrA; }), borderColor:'#8b5cf6', backgroundColor:'rgba(139,92,246,0.1)', tension:0.3 },
          { label:'CTR B', data:abTests.map(function(t){ return t.ctrB; }), borderColor:'#3b82f6', backgroundColor:'rgba(59,130,246,0.1)', tension:0.3 }
        ]
      },
      options: { responsive:true, plugins:{legend:{labels:{color:'#8892b0'}}}, scales:{x:{ticks:{color:'#8892b0'}},y:{ticks:{color:'#8892b0'}}} }
    });
  }
}

function clearABTests() { abTests=[]; saveABTests(); renderABResults(); showToast('Tests cleared','info'); }

// ── COMPETITOR ANALYSIS (streaming) ──────────────────────────────────────────
async function analyzeCompetitor() {
  var channel = document.getElementById('competitorInput').value.trim();
  if (!channel) { showToast('Enter a channel handle or URL', 'warning'); return; }
  setLoading('competitorBtn','competitorSpinner',true);
  showResult('competitorResult');
  var streamOut = document.getElementById('competitorStreamOut');
  var structured = document.getElementById('competitorStructured');
  if (streamOut) streamOut.style.display = 'block';
  if (structured) structured.style.display = 'none';
  await streamToEl('/api/stream/competitor', { channel: channel, language: getLang() }, 'competitorStreamOut', function() {
    setLoading('competitorBtn','competitorSpinner',false);
    showToast('Analysis complete', 'success');
  });
  setLoading('competitorBtn','competitorSpinner',false);
}

function loadDemoCompetitor() {
  document.getElementById('competitorInput').value = '@mkbhd';
  showToast('Demo channel loaded', 'info');
}

// ── NEWSLETTER (streaming) ─────────────────────────────────────────────────────
async function generateNewsletter() {
  var topic = document.getElementById('newsletterInput').value.trim();
  if (!topic) { showToast('Enter a script or topic', 'warning'); return; }
  setLoading('newsletterBtn','newsletterSpinner',true);
  showResult('newsletterResult');
  var streamOut = document.getElementById('newsletterStreamOut');
  var bodyEl = document.getElementById('newsletterBody');
  if (streamOut) streamOut.style.display = 'block';
  if (bodyEl) bodyEl.innerHTML = '';
  await streamToEl('/api/stream/newsletter', { topic: topic, language: getLang() }, 'newsletterStreamOut', function(raw) {
    if (bodyEl) bodyEl.innerHTML = typeof marked !== 'undefined' ? marked.parse(raw) : raw;
    setLoading('newsletterBtn','newsletterSpinner',false);
    showToast('Newsletter ready', 'success');
  });
  setLoading('newsletterBtn','newsletterSpinner',false);
}

function loadDemoNewsletter() {
  document.getElementById('newsletterInput').value = 'How I grew my YouTube channel from 0 to 10,000 subscribers in 6 months without spending money on ads';
  showToast('Demo topic loaded', 'info');
}

function copyNewsletterHTML() {
  var el = document.getElementById('newsletterBody');
  if (el) navigator.clipboard.writeText(el.innerHTML).then(function(){ showToast('HTML copied','success'); });
}

function copyNewsletterPlain() {
  var el = document.getElementById('newsletterStreamOut');
  if (el) navigator.clipboard.writeText(el.innerText).then(function(){ showToast('Plain text copied','success'); });
}

// ── EXPORT CENTER ─────────────────────────────────────────────────────────────
function exportIdeasCSV() {
  var grid = document.getElementById('ideasGrid');
  if (!grid || !grid.children.length || grid.children[0].className === 'empty-state') { showToast('Generate ideas first','warning'); return; }
  var rows = [['Format','Title','Hook','Why']];
  grid.querySelectorAll('.idea-card').forEach(function(c){
    rows.push([
      c.querySelector('.idea-format') ? c.querySelector('.idea-format').textContent.trim() : '',
      c.querySelector('.idea-title') ? c.querySelector('.idea-title').textContent.trim() : '',
      c.querySelector('.idea-hook') ? c.querySelector('.idea-hook').textContent.trim() : '',
      c.querySelector('.idea-why') ? c.querySelector('.idea-why').textContent.trim() : ''
    ].map(function(v){ return '"' + v.replace(/"/g,'""') + '"'; }));
  });
  downloadBlob(rows.map(function(r){ return r.join(','); }).join('\n'), 'ideas.csv', 'text/csv');
  showToast('Ideas exported','success');
}

function exportPerformanceCSV() {
  if (!videos.length) { showToast('No videos to export','warning'); return; }
  var rows = [['Title','Views','Likes','CTR','Date']].concat(videos.map(function(v){ return [v.title,v.views,v.likes,v.ctr||0,v.date]; }));
  downloadBlob(rows.map(function(r){ return r.join(','); }).join('\n'), 'performance.csv', 'text/csv');
  showToast('Performance data exported','success');
}

function exportCalendarJSON() {
  downloadBlob(JSON.stringify(calData,null,2), 'calendar.json', 'application/json');
  showToast('Calendar exported','success');
}

function exportABCSV() {
  if (!abTests.length) { showToast('No A/B tests to export','warning'); return; }
  var rows = [['Date','Name A','CTR A %','Name B','CTR B %','Winner']].concat(abTests.map(function(t){
    return [t.date, t.nameA||'A', t.ctrA, t.nameB||'B', t.ctrB, t.ctrA>=t.ctrB?'A':'B'];
  }));
  downloadBlob(rows.map(function(r){ return r.join(','); }).join('\n'), 'ab_tests.csv', 'text/csv');
  showToast('A/B data exported','success');
}

function exportFullBackup() {
  var data = { videos:videos, calData:calData, abTests:abTests, language:getLang(), exported:new Date().toISOString() };
  downloadBlob(JSON.stringify(data,null,2), 'creatoros_backup.json', 'application/json');
  showToast('Full backup exported','success');
}

function importBackup(input) {
  var file = input.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function(e) {
    try {
      var data = JSON.parse(e.target.result);
      if (data.videos) { videos = data.videos; localStorage.setItem('cos_videos', JSON.stringify(videos)); }
      if (data.calData) { calData = data.calData; localStorage.setItem('cos_calendar', JSON.stringify(calData)); }
      if (data.abTests) { abTests = data.abTests; localStorage.setItem('cos_ab', JSON.stringify(abTests)); }
      renderTracker(); renderCalendar(); renderABResults();
      showToast('Backup restored','success');
    } catch(err) { showToast('Invalid backup file','error'); }
  };
  reader.readAsText(file);
}

function exportNotion() {
  if (!videos.length) { showToast('No data to export','warning'); return; }
  var lines = ['# Video Performance','','| Title | Views | Likes | CTR | Date |','|-------|-------|-------|-----|------|'].concat(
    videos.map(function(v){ return '| ' + v.title + ' | ' + fmtNum(v.views) + ' | ' + fmtNum(v.likes) + ' | ' + (v.ctr||0) + '% | ' + v.date + ' |'; })
  );
  var el = document.getElementById('notionPreview');
  if (el) { el.textContent = lines.join('\n'); el.style.display = 'block'; }
  showToast('Notion markdown ready — copy from box above','success');
}

function exportSheetsCSV() {
  exportPerformanceCSV();
}

// ── SLIDERS LIVE LABELS ───────────────────────────────────────────────────────
document.addEventListener('input', function(e) {
  if (e.target.id === 'voiceSpeed') {
    var el = document.getElementById('voiceSpeedVal');
    if (el) el.textContent = parseFloat(e.target.value).toFixed(1) + 'x';
  }
  if (e.target.id === 'voicePitch') {
    var el2 = document.getElementById('voicePitchVal');
    if (el2) el2.textContent = parseFloat(e.target.value).toFixed(1);
  }
  if (e.target.id === 'thumbSize') {
    var sv = document.getElementById('thumbSizeVal');
    if (sv) sv.textContent = e.target.value;
    drawThumb();
  }
  if (['thumbTitle','thumbSub','thumbBg1','thumbBg2','thumbTextColor'].indexOf(e.target.id) !== -1) {
    drawThumb();
  }
});

// ── KEYBOARD SHORTCUTS ────────────────────────────────────────────────────────
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeModal();
    closeCalModal();
  }
  if ((e.ctrlKey||e.metaKey) && e.key === 'Enter') {
    var active = document.querySelector('.section.active');
    if (!active) return;
    var id = active.id.replace('sec-','');
    var map = { ideas:generateIdeas, script:generateScript, shorts:generateShorts, captions:generateCaption, seo:generateSEO, newsletter:generateNewsletter };
    if (map[id]) { e.preventDefault(); map[id](); }
  }
});
</script>
</body>
</html>
''')

f.close()
print("JS appended, final size:", os.path.getsize(r'C:\Users\HP\Desktop\Content Creaction\public\index.html'))
