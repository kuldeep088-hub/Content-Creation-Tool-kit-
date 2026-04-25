# CreatorOS v2.0 — AI Content Creator Hub

A single-page web app with 16 AI-powered tools for YouTube and Instagram creators. Runs on **Google Gemini AI** with a free **Pollinations.ai** fallback — no API key required to use.

---

## Features

| Tool | What it does |
|------|-------------|
| Idea Generator | 10 viral content ideas tailored to your niche + platform |
| Script Writer | Full video script with Hook, Intro, Body sections, and CTA |
| Shorts Repurposer | 7 Shorts scripts with hooks, CTAs, and hashtags |
| Thumbnail Studio | Canvas-based thumbnail designer — download as PNG |
| Caption Generator | Platform-optimized captions + 30 hashtags |
| Hook Tester | Scores 3 hooks on Curiosity, Clarity, Emotion, Novelty |
| SEO Optimizer | 3 title A/B variants + full optimized description |
| Voiceover | Browser TTS to read back your script |
| Content Calendar | Visual monthly calendar to plan your upload schedule |
| A/B Thumbnail Tracker | Track which thumbnails win by CTR |
| Competitor Analysis | AI breakdown of any channel's strategy and gaps |
| Newsletter Generator | Turn any script into a ready-to-send email newsletter |
| Performance Tracker | Log views/likes/CTR + AI improvement suggestions |
| Export Center | Export data as CSV, JSON, or Notion markdown |
| Chrome Extension Guide | Files + instructions to build your own YouTube sidebar tool |
| Multi-Language | Generate all content in 8+ languages |

---

## Getting Started

### Prerequisites

- Node.js 18+
- A free [Google Gemini API key](https://aistudio.google.com/app/apikey) (optional — app works without one via Pollinations.ai)

### Install

```bash
git clone https://github.com/kuldeep088-hub/Content-Creation-Tool-kit-.git
cd Content-Creation-Tool-kit-
npm install
```

### Configure

```bash
cp .env.example .env
```

Open `.env` and add your Gemini key:

```
GEMINI_API_KEY=your_key_here
PORT=3000
```

### Run

```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000)

---

## Deploy

### Railway (recommended — free tier)

1. Push to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select this repo
4. Add environment variable: `GEMINI_API_KEY`
5. Live in ~2 minutes

### Render

1. New Web Service → connect this repo
2. Build command: `npm install`
3. Start command: `npm start`
4. Add `GEMINI_API_KEY` in environment variables

### Heroku

```bash
heroku create
heroku config:set GEMINI_API_KEY=your_key_here
git push heroku main
```

---

## Tech Stack

- **Backend** — Node.js + Express
- **AI** — Google Gemini 2.0 Flash (primary) / Pollinations.ai (free fallback)
- **Frontend** — Vanilla JS, HTML/CSS (single file SPA)
- **Charts** — Chart.js
- **Markdown** — marked.js
- **Security** — helmet, express-rate-limit, compression

---

## Project Structure

```
├── server.js          # Express server + all AI API endpoints
├── public/
│   └── index.html     # Full SPA frontend (all 16 tools)
├── chrome-extension/  # Chrome extension starter files
├── .env.example       # Environment variable template
├── Procfile           # Heroku/Railway deployment config
└── package.json
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ideas` | Generate content ideas |
| POST | `/api/script` | Generate video script |
| POST | `/api/shorts` | Generate Shorts breakdown |
| POST | `/api/captions` | Generate captions + hashtags |
| POST | `/api/seo` | Generate SEO titles + description |
| POST | `/api/hooks` | Score and rank hooks |
| POST | `/api/newsletter` | Generate email newsletter |
| POST | `/api/competitor` | Analyze competitor channel |
| POST | `/api/improve` | AI performance suggestions |
| POST | `/api/stream/script` | Streaming script generation (SSE) |
| POST | `/api/stream/newsletter` | Streaming newsletter (SSE) |
| POST | `/api/stream/competitor` | Streaming competitor analysis (SSE) |
| POST | `/api/stream/improve` | Streaming improvement suggestions (SSE) |

---

## License

MIT
