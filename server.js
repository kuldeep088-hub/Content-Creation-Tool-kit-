require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const helmet = require('helmet');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const https = require('https');
const http = require('http');
const { URL } = require('url');

const app = express();
let claudeApiKey = '';

// ─── SECURITY & PERFORMANCE MIDDLEWARE ───────────────────────────────────────
app.use(helmet({ contentSecurityPolicy: false }));
app.use(compression());
app.use(cors());
app.use(express.json({ limit: '10mb' }));

const apiLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 60,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please slow down.' }
});
app.use('/api/', apiLimiter);
app.use(express.static(path.join(__dirname, 'public')));

// ─── HTTP HELPERS (works on ALL Node versions) ───────────────────────────────
function httpPost(urlStr, payload, timeoutMs = 35000) {
  return new Promise((resolve, reject) => {
    let settled = false;
    const done = (fn, val) => { if (!settled) { settled = true; fn(val); } };

    const u = new URL(urlStr);
    const lib = u.protocol === 'https:' ? https : http;
    const data = JSON.stringify(payload);
    const req = lib.request({
      hostname: u.hostname,
      port: u.port || (u.protocol === 'https:' ? 443 : 80),
      path: u.pathname + u.search,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) }
    }, res => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        const body = Buffer.concat(chunks).toString();
        done(resolve, {
          ok: res.statusCode >= 200 && res.statusCode < 300,
          status: res.statusCode,
          text: () => body,
          json: () => JSON.parse(body)
        });
      });
      res.on('error', e => done(reject, e));
    });
    req.setTimeout(timeoutMs, () => { req.destroy(); done(reject, new Error('Request timed out after ' + timeoutMs + 'ms')); });
    req.on('error', e => done(reject, e));
    req.write(data);
    req.end();
  });
}

function httpGet(urlStr, timeoutMs = 15000) {
  return new Promise((resolve, reject) => {
    let settled = false;
    const done = (fn, val) => { if (!settled) { settled = true; fn(val); } };

    const u = new URL(urlStr);
    const req = https.get({
      hostname: u.hostname,
      port: u.port || 443,
      path: u.pathname + u.search,
    }, res => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        const body = Buffer.concat(chunks).toString();
        done(resolve, {
          ok: res.statusCode >= 200 && res.statusCode < 300,
          status: res.statusCode,
          json: () => JSON.parse(body)
        });
      });
      res.on('error', e => done(reject, e));
    });
    req.setTimeout(timeoutMs, () => { req.destroy(); done(reject, new Error('Timeout')); });
    req.on('error', e => done(reject, e));
  });
}

function httpPostStream(urlStr, payload, timeoutMs = 60000) {
  return new Promise((resolve, reject) => {
    let settled = false;
    const done = (fn, val) => { if (!settled) { settled = true; fn(val); } };

    const u = new URL(urlStr);
    const data = JSON.stringify(payload);
    const req = https.request({
      hostname: u.hostname,
      port: u.port || 443,
      path: u.pathname + u.search,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) }
    }, res => {
      done(resolve, { ok: res.statusCode >= 200 && res.statusCode < 300, status: res.statusCode, body: res });
    });
    req.setTimeout(timeoutMs, () => { req.destroy(); done(reject, new Error('Stream timeout')); });
    req.on('error', e => done(reject, e));
    req.write(data);
    req.end();
  });
}

// ─── AI — Gemini primary, Pollinations fallback ───────────────────────────────
const GEMINI_ENV_KEY = process.env.GEMINI_API_KEY || '';
const POLLINATIONS_URL = 'https://text.pollinations.ai/openai';

// Always use the user-provided key first, then fall back to env key
function activeGeminiKey() { return claudeApiKey || GEMINI_ENV_KEY; }
function geminiUrl() { return `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${activeGeminiKey()}`; }
function geminiStreamUrl() { return `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:streamGenerateContent?alt=sse&key=${activeGeminiKey()}`; }

function extractJSON(text, type = 'array') {
  try {
    const pattern = type === 'array' ? /\[[\s\S]*\]/ : /\{[\s\S]*\}/;
    const match = text.match(pattern);
    if (match) return JSON.parse(match[0]);
  } catch (_) {}
  return type === 'array' ? [] : {};
}

async function ask(prompt, maxTokens = 2048) {
  const key = activeGeminiKey();
  if (key) {
    try {
      const res = await httpPost(geminiUrl(), {
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { maxOutputTokens: maxTokens, temperature: 0.9 }
      });
      if (res.ok) {
        const data = res.json();
        const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;
        if (text) return text;
      } else {
        console.error('Gemini error', res.status, res.text().slice(0, 200));
      }
    } catch (e) {
      console.error('Gemini request failed:', e.message);
    }
  }
  // Fallback: Pollinations (always free, no key needed)
  const res = await httpPost(POLLINATIONS_URL, {
    messages: [{ role: 'user', content: prompt }],
    model: 'openai',
    private: true,
    seed: Math.floor(Math.random() * 99999)
  }, 60000);
  if (!res.ok) throw new Error('AI service error: ' + res.status);
  const data = res.json();
  return data?.choices?.[0]?.message?.content || res.text();
}

function langSuffix(language) {
  if (!language || language === 'English') return '';
  return `\n\nRespond entirely in ${language}.`;
}

// ─── DEMO DATA ───────────────────────────────────────────────────────────────
const DEMO = {
  ideas: [
    { title: "I Tried Waking Up at 4AM for 30 Days — Here's What Happened", hook: "What if one habit change could double your productivity overnight?", format: "Challenge", why: "30-day challenges get massive watch time because viewers binge the whole series", difficulty: "Medium" },
    { title: "10 Things I Wish I Knew Before Starting My YouTube Channel", hook: "I wasted 8 months doing this wrong — don't make my mistakes.", format: "Listicle", why: "Beginner-targeting titles have 3x higher CTR in the creator niche", difficulty: "Easy" },
    { title: "How I Gained 10,000 Subscribers in 90 Days (Step-by-Step)", hook: "The exact system I used — no clickbait, no luck, just strategy.", format: "Tutorial", why: "Growth case studies perform extremely well — people want proof + process", difficulty: "Easy" },
    { title: "A Day in My Life as a Full-Time Content Creator (Real Numbers)", hook: "I'll show you exactly how much I made this month and how long it took.", format: "Day-in-Life", why: "Transparency about income and time builds massive trust and curiosity", difficulty: "Easy" },
    { title: "Why 99% of YouTubers Quit Before 1,000 Subscribers", hook: "The real reason isn't what you think — and it's completely fixable.", format: "Storytime", why: "Controversy + solution framing drives high comment engagement", difficulty: "Easy" },
    { title: "I Studied the Top 10 YouTube Channels for 30 Days — Here's the Pattern", hook: "Every viral channel does these 3 things. Most new creators skip all of them.", format: "Listicle", why: "Research-backed content gets shared by other creators and in Facebook groups", difficulty: "Hard" },
    { title: "The Exact Script Template I Use for Every Video (Free Download)", hook: "Copy my exact script structure and cut your editing time in half.", format: "Tutorial", why: "Free resource giveaways explode watch time and description clicks", difficulty: "Easy" },
    { title: "Instagram Reels vs YouTube Shorts: Which Grew My Channel Faster?", hook: "I posted on both for 60 days — the data shocked me.", format: "Challenge", why: "Comparison format with real data gets strong search and suggested traffic", difficulty: "Medium" },
    { title: "How I Film Professional Videos in My Bedroom for Under Rs5,000", hook: "You don't need expensive gear — you need this setup.", format: "Tutorial", why: "Budget-specific content targets a huge underserved audience segment", difficulty: "Easy" },
    { title: "The Content Calendar That Got Me to 3 Videos/Week Without Burnout", hook: "I used to hate making content. This system changed everything.", format: "Tutorial", why: "Burnout is a top pain point — solving it with a system = high saves", difficulty: "Medium" }
  ],

  script: `## Hook (0:00 - 0:15)\n\nWhat if I told you that one simple change made me go from 200 views per video to 20,000 in less than 60 days? No paid ads, no viral moment, no luck. Just a system. Stick with me because by the end of this video, you'll have the exact same system in your hands.\n\n---\n\n## Intro (0:15 - 0:45)\n\nWhat's up everyone, welcome back to the channel. Today we're going deep on the framework that changed everything for me. I'm going to break it down step by step.\n\n---\n\n## Section 1: Why Videos Don't Get Recommended\n\nYouTube doesn't care how good your video is. It cares about one thing: does this video keep people on the platform? That's measured through CTR and Average View Duration.\n\n---\n\n## Section 2: The 3-Part Hook Formula\n\nPAS Hook: Problem, Agitate, Solution tease. State the pain point, make it urgent, then tease the solution without giving it away.\n\n---\n\n## Call to Action\n\nIf this helped, smash the like button. Subscribe for weekly content growth tips. See you next week.`,

  shorts: [
    { number: 1, title: "The 4AM Habit That Changed Everything", timestamp: "0:00 - 0:45", hook: "I set my alarm for 4AM and my life changed in 7 days.", script: "I set my alarm for 4AM and I genuinely hated it at first. Day one I hit snooze four times. Day seven I was awake before the alarm. The secret is the evening routine, not the morning routine.", caption: "The 4AM secret nobody talks about #morningroutine #productivity", hashtags: ["morningroutine", "4amclub", "productivity", "contentcreator"], cta: "Follow for more creator hacks" },
    { number: 2, title: "Why Your Videos Have 0 Views", timestamp: "1:30 - 2:15", hook: "Your video has zero views and it's not the algorithm's fault.", script: "Your video has zero views and I'm going to tell you exactly why. It's your thumbnail. Same video, two thumbnails — one got 2% CTR, the other got 11% CTR. That's a 5x difference from ONE change.", caption: "Your views problem is simpler than you think #youtube #youtubetips", hashtags: ["youtubetips", "thumbnails", "growyoutube"], cta: "Save this for when you redesign thumbnails" },
    { number: 3, title: "3 Scripts, 1 Sunday", timestamp: "3:00 - 4:00", hook: "I film an entire week of content in one 4-hour Sunday session.", script: "Sunday is my filming day. Four hours. Three long videos. Done for the week. The trick is momentum — once you're in filming mode, switching topics takes 5 minutes, not starting over.", caption: "Film a whole week in ONE day #contentcreator #batchfilming", hashtags: ["batchfilming", "contentcreator", "productivity"], cta: "Follow to see my full weekly content schedule" }
  ],

  captions: {
    caption: "I used to spend hours on content that got zero traction.\n\nThen I realized the problem wasn't the content — it was the system. I was creating randomly, posting inconsistently, and hoping the algorithm would figure it out.\n\nSpoiler: it didn't.\n\nSo I built a content calendar. Now I create MORE content in LESS time. Save this post and start building your system today.",
    hook: "I used to spend hours on content that got zero traction.",
    hashtags: ["contentcreator", "youtuber", "instagramreels", "creatoreconomy", "contentmarketing", "youtubetips", "instagramtips", "videomarketing", "growyoutube", "growinstagram", "socialmediatips", "contentstrategy", "creatortips", "digitalcreator", "videoediting", "contentcalendar", "batchcontent", "creatorlife", "onlinebusiness", "personalbranding", "youtubegrowth", "reelsviral", "shortsviral", "contentideas", "videocontent", "createeveryday", "creatorhacks", "youtubealgorithm", "instagramalgorithm", "contentplan"],
    cta: "Drop a lightbulb if this helped — and save it for when you need a reset.",
    bestPostTime: "Tuesday–Thursday, 6–9 PM IST"
  },

  seo: {
    titles: [
      { variant: "A", title: "How I Went From 0 to 10K Subscribers in 90 Days (The Exact System)", why: "Specific numbers + time frame + promise of a system = high CTR." },
      { variant: "B", title: "YouTube Growth Strategy 2025: 0 to 10,000 Subscribers Fast", why: "Front-loads the primary keyword for search traffic." },
      { variant: "C", title: "I Was Stuck at 0 Subscribers for Months — Until I Did This", why: "Emotional storytelling hook. Strong for suggested/browse traffic." }
    ],
    description: "How I grew my YouTube channel from 0 to 10,000 subscribers in 90 days — complete breakdown of the strategy, tools, and mindset that made it possible.\n\nIn this video you'll learn:\n- The exact content calendar I follow\n- How to batch film an entire week in one session\n- The thumbnail formula that gets 8–12% CTR consistently\n- Why most new creators plateau at 500 subscribers\n\nTimestamps:\n0:00 — Why most channels fail in the first 90 days\n1:30 — The content calendar breakdown\n3:45 — My thumbnail design process\n6:00 — SEO research in under 10 minutes",
    tags: ["youtube growth", "how to grow on youtube", "youtube tips 2025", "get more subscribers", "youtube algorithm", "content creator tips"],
    chapters: [
      { time: "0:00", title: "Why most channels fail in 90 days" },
      { time: "1:30", title: "The content calendar breakdown" },
      { time: "3:45", title: "Thumbnail design process" },
      { time: "6:00", title: "SEO research in 10 minutes" }
    ],
    thumbnailTip: "Use a split design: your face on the left showing a surprised/excited expression, bold white text on the right with ONE specific number, and a bright yellow or red background."
  },

  improve: "## What's Working\n\n- Your most-viewed videos are tutorial/how-to formats — the algorithm is rewarding educational content\n- Your like-to-view ratio on top performers is above 4%, which is excellent\n\n## Top Issues to Fix\n\n1. **CTR below 4% on recent uploads** — Your thumbnails need a refresh. Test adding a face with strong emotion + one bold number.\n2. **Watch time drop-off before 2 minutes** — Your intros are too long. Cut them to under 30 seconds.\n3. **Inconsistent posting** — The algorithm rewards channels that post on a predictable schedule.\n\n## Growth Strategy\n\n1. **Double down on your top 3 videos** — Create sequels or updated versions of your best performers.\n2. **Add chapters/timestamps to every video** — This improves AVD.\n3. **Post one Short per day for 30 days** — Shorts are your fastest path to new subscribers right now.",

  hooks: [
    { text: "I quit my 9-5 job with zero savings and built a 6-figure business in 12 months. Here's every mistake I made.", scores: { curiosity: 9, clarity: 8, emotion: 9, novelty: 7 }, total: 33, feedback: "Strong emotional stakes + specific timeframe. 'Every mistake' creates open loop." },
    { text: "Most creators spend 80% of their time on the wrong 20% of tasks. I'll show you what actually moves the needle.", scores: { curiosity: 8, clarity: 9, emotion: 6, novelty: 6 }, total: 29, feedback: "Good clarity and the 80/20 frame is recognizable. Low novelty — this pattern is overused." },
    { text: "What if the reason you're not growing has nothing to do with your content?", scores: { curiosity: 10, clarity: 7, emotion: 7, novelty: 8 }, total: 32, feedback: "Excellent curiosity trigger — disrupts assumptions. Works best as a hook for a video with a surprising reveal." }
  ],

  newsletter: {
    subject: "The content system that 10x'd my output (without burning out)",
    preview: "I filmed 3 videos on Sunday. Here's exactly how.",
    html: "<h2>This week's big idea</h2><p>Most creators think consistency means willpower. It doesn't. It means systems.</p><p>I used to stare at a blank page every Monday wondering what to film. Now I have a queue of 12 ideas ready before I open my camera bag.</p><h2>What changed</h2><p>I stopped creating content and started <strong>engineering</strong> it. Every Sunday I batch-film 3 long videos. Each one gets repurposed into 5 Shorts, 2 Instagram Reels, and 1 email newsletter.</p><h2>Your action step</h2><p>This Sunday, film just <em>two</em> videos instead of one. Notice how much easier the second one feels once you're already in the zone. That's momentum. That's the system.</p>",
    plain: "THIS WEEK'S BIG IDEA\n\nMost creators think consistency means willpower. It doesn't. It means systems.\n\nWHAT CHANGED\n\nI stopped creating content and started engineering it. Every Sunday I batch-film 3 long videos.\n\nYOUR ACTION STEP\n\nThis Sunday, film just two videos instead of one.\n\nReply and tell me how it goes."
  },

  competitor: {
    channel: "@mkbhd",
    postingFrequency: "2–3 videos per week on YouTube, daily on Shorts/Reels.",
    topFormats: ["First Look / Unboxing with cinematic production quality", "Comparison reviews (Phone A vs Phone B)", "Annual 'Best of' listicles", "Behind-the-scenes studio/workflow vlogs"],
    avoidedTopics: ["Budget or entry-level devices", "Software-only reviews", "Creator business and monetization advice", "Mid-tier creator gear for beginners"],
    opportunities: ["Create a 'best budget tech for creators under $200' series", "Make 'how I edit my videos' tutorials", "Review productivity and creator software", "Start a 'tech for beginners' series", "Cover tech from an Indian market perspective"]
  },

  youtubeStats: {
    channelTitle: "Creator Hub Demo Channel",
    subscriberCount: "24,500",
    videos: [
      { title: "How I Got 10K Subscribers in 90 Days", views: 48200, likes: 2100, publishedAt: "2025-03-15" },
      { title: "My Complete Video Setup Under Rs20,000", views: 31500, likes: 1400, publishedAt: "2025-03-22" },
      { title: "Why Your Thumbnails Are Killing Your CTR", views: 27800, likes: 980, publishedAt: "2025-03-29" },
      { title: "I Batch Filmed 30 Videos in One Weekend", views: 19200, likes: 870, publishedAt: "2025-04-05" },
      { title: "The Hook Formula That 5x'd My Views", views: 44600, likes: 2300, publishedAt: "2025-04-08" }
    ]
  }
};

// ─── API ROUTES ───────────────────────────────────────────────────────────────

app.post('/api/set-key', (req, res) => {
  claudeApiKey = (req.body.key || '').trim();
  res.json({ ok: !!claudeApiKey });
});

app.get('/api/key-status', (req, res) => {
  res.json({ set: !!activeGeminiKey() });
});

app.get('/api/history', (req, res) => {
  res.json({ history: [] });
});

app.post('/api/ideas', async (req, res) => {
  const { niche, platform, count = 10, language } = req.body;
  if (!niche) return res.json({ ideas: DEMO.ideas.slice(0, Number(count)) });
  try {
    const result = await ask(
      `You are a viral content strategist. Generate ${count} high-performing content ideas for a ${niche} creator on ${platform}.\n\nReturn ONLY a valid JSON array:\n[\n  {\n    "title": "Compelling video title",\n    "hook": "Opening hook sentence",\n    "format": "Tutorial|Vlog|Storytime|Listicle|Challenge|Reaction|Day-in-Life",\n    "why": "One sentence: why this will get views",\n    "difficulty": "Easy|Medium|Hard"\n  }\n]\n\nMake all ${count} ideas specific to ${niche} on ${platform}.` + langSuffix(language), 2000
    );
    res.json({ ideas: extractJSON(result, 'array') });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/script', async (req, res) => {
  const { topic, duration = '10 minutes', style = 'conversational', language } = req.body;
  if (!topic) return res.json({ script: DEMO.script });
  try {
    const result = await ask(
      `Write a complete YouTube video script for: "${topic}"\nTarget duration: ${duration} | Style: ${style}\n\n## Hook (0:00 - 0:15)\n[Powerful opening]\n\n## Intro (0:15 - 0:45)\n[Brief intro + preview]\n\n## Section 1: [Title]\n[Content with [PAUSE] markers and **BOLD** emphasis]\n\n## Section 2: [Title]\n[Content]\n\n## Section 3: [Title]\n[Content]\n\n## Key Takeaway\n[Main insight]\n\n## Call to Action\n[Like, subscribe, next video CTA]` + langSuffix(language), 3500
    );
    res.json({ script: result });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/shorts', async (req, res) => {
  const { input, language } = req.body;
  if (!input) return res.json({ shorts: DEMO.shorts });
  try {
    const result = await ask(
      `YouTube Shorts expert. Based on: "${input}"\n\nGenerate 7 short-form video ideas (under 60 seconds). Return ONLY valid JSON:\n[\n  {\n    "number": 1,\n    "title": "Short title under 50 chars",\n    "timestamp": "0:00 - 1:30",\n    "hook": "First 3 seconds hook",\n    "script": "Full 60-second word-for-word script with [PAUSE] markers",\n    "caption": "Caption with emojis",\n    "hashtags": ["tag1","tag2","tag3"],\n    "cta": "End screen CTA"\n  }\n]` + langSuffix(language), 3000
    );
    res.json({ shorts: extractJSON(result, 'array') });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/captions', async (req, res) => {
  const { topic, platform, language } = req.body;
  if (!topic) return res.json(DEMO.captions);
  try {
    const result = await ask(
      `Write optimized social media content for: "${topic}"\nPlatform: ${platform}\n\nReturn ONLY valid JSON:\n{\n  "caption": "Full caption with emojis and line breaks",\n  "hook": "First line hook",\n  "hashtags": ["tag1","tag2"],\n  "cta": "Call to action",\n  "bestPostTime": "Best time to post"\n}\n\n${platform && platform.includes('Instagram') ? '30 hashtags, mix of large/medium/small' : '5-8 relevant hashtags'}` + langSuffix(language), 1500
    );
    res.json(extractJSON(result, 'object'));
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/seo', async (req, res) => {
  const { input, language } = req.body;
  if (!input) return res.json(DEMO.seo);
  try {
    const result = await ask(
      `YouTube SEO expert. Optimize: "${input}"\n\nReturn ONLY valid JSON:\n{\n  "titles": [\n    {"variant":"A","title":"...","why":"..."},\n    {"variant":"B","title":"...","why":"..."},\n    {"variant":"C","title":"...","why":"..."}\n  ],\n  "description": "Full 400+ word description with timestamps, links, hashtags",\n  "tags": ["tag1","tag2"],\n  "chapters": [{"time":"0:00","title":"..."}],\n  "thumbnailTip": "Specific CTR tip"\n}` + langSuffix(language), 2500
    );
    res.json(extractJSON(result, 'object'));
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/improve', async (req, res) => {
  const { videos, language } = req.body;
  if (!videos || !videos.length) return res.status(400).json({ error: 'No video data' });
  try {
    const stats = videos.map(v => `"${v.title}": ${v.views} views | ${v.likes} likes | ${v.ctr}% CTR`).join('\n');
    const result = await ask(
      `Analyze YouTube channel performance:\n\n${stats}\n\n## What's Working\n## Top Issues to Fix\n## Growth Strategy\n## Thumbnail & Title Wins\n## Posting Strategy\n\nBe specific. Reference actual video titles.` + langSuffix(language), 1500
    );
    res.json({ suggestions: result });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/hooks', async (req, res) => {
  const { hooks, language } = req.body;
  if (!hooks || !Array.isArray(hooks) || hooks.length === 0) {
    return res.json({ results: DEMO.hooks, winner: 0 });
  }
  try {
    const hookList = hooks.map((h, i) => `Hook ${i + 1}: "${h}"`).join('\n');
    const result = await ask(
      `You are a world-class YouTube hook analyzer. Score each hook on 4 dimensions (1-10 each).\n\n${hookList}\n\nReturn ONLY valid JSON array:\n[\n  {\n    "text": "original hook text",\n    "scores": { "curiosity": 8, "clarity": 7, "emotion": 9, "novelty": 6 },\n    "total": 30,\n    "feedback": "2-3 sentence specific analysis"\n  }\n]\n\nBe harsh and specific. Total = sum of all 4 scores.` + langSuffix(language), 1500
    );
    const results = extractJSON(result, 'array');
    if (results.length > 0) {
      const winnerIdx = results.reduce((best, cur, idx) => cur.total > results[best].total ? idx : best, 0);
      res.json({ results, winner: winnerIdx });
    } else {
      res.json({ results: DEMO.hooks.slice(0, hooks.length), winner: 0, demo: true });
    }
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/newsletter', async (req, res) => {
  const { content, language } = req.body;
  if (!content || !content.trim()) return res.json(DEMO.newsletter);
  try {
    const result = await ask(
      `You are an expert email newsletter writer for content creators. Based on this script/topic:\n\n"${content}"\n\nGenerate a complete newsletter. Return ONLY valid JSON:\n{\n  "subject": "Compelling email subject line (max 60 chars)",\n  "preview": "Preview text shown in inbox (max 90 chars)",\n  "html": "Full HTML email body with <h2>, <p>, <ul>, <li>, <strong> tags — 4 sections minimum",\n  "plain": "Plain text version with section headers in ALL CAPS"\n}` + langSuffix(language), 2500
    );
    const data = extractJSON(result, 'object');
    res.json(data.subject ? data : { ...DEMO.newsletter, demo: true });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/competitor', async (req, res) => {
  const { channel, language } = req.body;
  if (!channel || !channel.trim()) return res.json(DEMO.competitor);
  try {
    const result = await ask(
      `You are a YouTube competitive intelligence analyst. Analyze this channel: "${channel}"\n\nReturn ONLY valid JSON:\n{\n  "channel": "${channel}",\n  "postingFrequency": "Detailed posting pattern description",\n  "topFormats": ["format1", "format2", "format3", "format4"],\n  "avoidedTopics": ["gap1", "gap2", "gap3", "gap4"],\n  "opportunities": ["specific opportunity 1", "specific opportunity 2", "specific opportunity 3", "specific opportunity 4", "specific opportunity 5"]\n}` + langSuffix(language), 2000
    );
    const data = extractJSON(result, 'object');
    res.json(data.channel ? data : { ...DEMO.competitor, channel, demo: true });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/youtube-stats', async (req, res) => {
  const { apiKey, channelId } = req.body;
  if (!apiKey || !channelId) {
    return res.json({ ...DEMO.youtubeStats, demo: true });
  }
  try {
    const channelResp = await httpGet(`https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id=${channelId}&key=${apiKey}`);
    const channelData = channelResp.json();
    if (channelData.error) return res.json({ ...DEMO.youtubeStats, demo: true, apiError: channelData.error.message });

    const channelInfo = channelData.items && channelData.items[0];
    const channelTitle = channelInfo?.snippet?.title || 'Your Channel';
    const subscriberCount = channelInfo?.statistics?.subscriberCount || '0';

    const searchResp = await httpGet(`https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=${channelId}&maxResults=10&order=date&type=video&key=${apiKey}`);
    const searchData = searchResp.json();
    if (searchData.error) return res.json({ ...DEMO.youtubeStats, demo: true, apiError: searchData.error.message });

    const videoIds = (searchData.items || []).map(item => item.id.videoId).join(',');
    if (!videoIds) return res.json({ ...DEMO.youtubeStats, demo: true });

    const statsResp = await httpGet(`https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=${videoIds}&key=${apiKey}`);
    const statsData = statsResp.json();

    const videos = (statsData.items || []).map(item => ({
      title: item.snippet.title,
      views: parseInt(item.statistics.viewCount || 0),
      likes: parseInt(item.statistics.likeCount || 0),
      publishedAt: item.snippet.publishedAt ? item.snippet.publishedAt.slice(0, 10) : ''
    }));

    const subCount = parseInt(subscriberCount);
    const displaySubs = subCount >= 1000000 ? (subCount / 1000000).toFixed(1) + 'M' :
                        subCount >= 1000 ? (subCount / 1000).toFixed(1) + 'K' :
                        subscriberCount;
    res.json({ channelTitle, subscriberCount: displaySubs, videos });
  } catch (e) {
    res.json({ ...DEMO.youtubeStats, demo: true, apiError: e.message });
  }
});

app.post('/api/analyze-video', async (req, res) => {
  const { title, url, language } = req.body;
  if (!title) return res.status(400).json({ error: 'No title provided' });
  try {
    const result = await ask(
      `YouTube content strategist. A creator is watching a video titled: "${title}"\nURL: ${url || 'N/A'}\n\nGenerate repurposing ideas. Return ONLY valid JSON:\n{\n  "shorts": ["3 short-form script ideas (60 seconds each)"],\n  "hashtags": ["10 relevant hashtags without #"],\n  "hooks": ["3 hook variations for this topic"]\n}` + langSuffix(language), 1500
    );
    const data = extractJSON(result, 'object');
    res.json(data.shorts ? data : { shorts: [], hashtags: [], hooks: [], demo: true });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// ─── STREAMING ENDPOINTS ─────────────────────────────────────────────────────

function sseHeaders(res) {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');
}

async function streamDemo(res, text) {
  const words = text.split(' ');
  for (const word of words) {
    res.write('data: ' + JSON.stringify({ text: word + ' ' }) + '\n\n');
    await new Promise(r => setTimeout(r, 30));
  }
  res.write('data: [DONE]\n\n');
  res.end();
}

async function streamAI(res, prompt) {
  if (activeGeminiKey()) {
    try {
      const aiRes = await httpPostStream(geminiStreamUrl(), {
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { maxOutputTokens: 3000, temperature: 0.9 }
      });
      if (aiRes.ok) {
        let buf = '';
        for await (const chunk of aiRes.body) {
          buf += chunk.toString();
          const lines = buf.split('\n');
          buf = lines.pop() || '';
          for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            const raw = line.slice(6).trim();
            if (!raw || raw === '[DONE]') continue;
            try {
              const json = JSON.parse(raw);
              const text = json?.candidates?.[0]?.content?.parts?.[0]?.text;
              if (text) res.write('data: ' + JSON.stringify({ text }) + '\n\n');
            } catch (_) {}
          }
        }
        res.write('data: [DONE]\n\n');
        res.end();
        return;
      }
    } catch (e) {
      console.error('Gemini stream error:', e.message);
    }
  }
  // Fallback: Pollinations
  try {
    const aiRes = await httpPost(POLLINATIONS_URL, {
      messages: [{ role: 'user', content: prompt }],
      model: 'openai',
      private: true,
      seed: Math.floor(Math.random() * 99999)
    }, 60000);
    if (!aiRes.ok) throw new Error('AI error ' + aiRes.status);
    const pData = aiRes.json();
    const text = pData?.choices?.[0]?.message?.content || aiRes.text();
    const words = text.split(' ');
    for (const word of words) {
      res.write('data: ' + JSON.stringify({ text: word + ' ' }) + '\n\n');
      await new Promise(r => setTimeout(r, 20));
    }
  } catch (e) {
    res.write('data: ' + JSON.stringify({ text: '\n\n**Error:** ' + e.message }) + '\n\n');
  }
  res.write('data: [DONE]\n\n');
  res.end();
}

app.post('/api/stream/script', async (req, res) => {
  const { topic, duration = '10 minutes', style = 'conversational', language } = req.body;
  sseHeaders(res);
  if (!topic || !topic.trim()) return streamDemo(res, DEMO.script);
  const prompt = `Write a complete YouTube video script for: "${topic}"
Target duration: ${duration} | Style: ${style}

## Hook (0:00 - 0:15)
[Powerful opening that stops the scroll]

## Intro (0:15 - 0:45)
[Brief intro + preview of what they'll learn]

## Section 1: [Title]
[Detailed content with [PAUSE] markers and **BOLD** emphasis]

## Section 2: [Title]
[Content]

## Section 3: [Title]
[Content]

## Key Takeaway
[Main insight summary]

## Call to Action
[Like, subscribe, comment CTA]

Write conversationally with energy. Include specific examples.` + langSuffix(language);
  await streamAI(res, prompt);
});

app.post('/api/stream/newsletter', async (req, res) => {
  const { content, language } = req.body;
  sseHeaders(res);
  if (!content || !content.trim()) return streamDemo(res, `Subject: ${DEMO.newsletter.subject}\n\n${DEMO.newsletter.plain}`);
  const prompt = `You are an expert email newsletter writer for content creators. Based on this script/topic:

"${content}"

Write a complete newsletter in Markdown:

# Subject: [compelling subject line]

**Preview text:** [one sentence hook]

---

## [Opening Hook Section]
[Engaging intro]

## [Main Value Section]
[Core content from the topic]

## [Actionable Takeaway]
[What they can do today]

## This Week's Challenge
[One specific action to take]

*Hit reply and tell me how it goes!*` + langSuffix(language);
  await streamAI(res, prompt);
});

app.post('/api/stream/competitor', async (req, res) => {
  const { channel, language } = req.body;
  sseHeaders(res);
  if (!channel || !channel.trim()) {
    const c = DEMO.competitor;
    return streamDemo(res, `# Competitor Analysis\n\n## Posting Frequency\n${c.postingFrequency}\n\n## Top Formats\n${c.topFormats.map(f => '- ' + f).join('\n')}\n\n## Gaps You Can Own\n${c.avoidedTopics.map(f => '- ' + f).join('\n')}\n\n## Your 5 Opportunities\n${c.opportunities.map(f => '- ' + f).join('\n')}`);
  }
  const prompt = `You are a YouTube competitive intelligence analyst. Analyze this channel: "${channel}"

Write a comprehensive Markdown analysis:

# Competitor Analysis: ${channel}

## Posting Frequency & Schedule
[Their posting patterns and cadence]

## Top Content Formats
[Bullet list of their best-performing content types with examples]

## Topics They Avoid (Your Gaps)
[Bullet list of content gaps you can exploit]

## Your 5 Opportunities
1. [Specific opportunity]
2. [Specific opportunity]
3. [Specific opportunity]
4. [Specific opportunity]
5. [Specific opportunity]

## Key Strategic Takeaway
[One paragraph summary]` + langSuffix(language);
  await streamAI(res, prompt);
});

app.post('/api/stream/improve', async (req, res) => {
  const { videos, language } = req.body;
  sseHeaders(res);
  if (!videos || !videos.length) return streamDemo(res, DEMO.improve);
  const stats = videos.map(v => `"${v.title}": ${v.views} views | ${v.likes} likes | ${v.ctr}% CTR`).join('\n');
  const prompt = `Analyze these YouTube video performances and give specific actionable advice:

${stats}

## What's Working
[2-3 specific things performing well based on the numbers]

## Top 3 Issues to Fix
[Specific, actionable fixes referencing actual video titles]

## Growth Strategy
[3 data-backed recommendations]

## Thumbnail & Title Wins
[Specific CTR improvement tips based on underperformers]

## Optimal Posting Strategy
[Based on patterns in this data]

Be direct. Reference actual video titles from the data.` + langSuffix(language);
  await streamAI(res, prompt);
});

// ─── GLOBAL ERROR HANDLER ────────────────────────────────────────────────────
process.on('unhandledRejection', (reason) => {
  console.error('Unhandled rejection:', reason);
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught exception:', err.message);
});

// ─── START ────────────────────────────────────────────────────────────────────
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`\nCreatorOS v2.0 is live!`);
  console.log(`Open: http://localhost:${PORT}`);
  if (GEMINI_ENV_KEY || claudeApiKey) {
    console.log(`Google Gemini AI active`);
  } else {
    console.log(`Pollinations.ai active (free)`);
  }
});
