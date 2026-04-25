import os

out = open(r'C:\Users\HP\Desktop\Content Creaction\public\index.html', 'w', encoding='utf-8')

def w(s):
    out.write(s)

# ── HEAD ──────────────────────────────────────────────────────────────────────
w('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CreatorOS v2.0 — Content Command Center</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
:root {
  --bg: #08090f; --surface: #0d0e1c; --card: #111220; --card2: #151627;
  --border: #1c1d30; --border2: #252640;
  --purple: #8b5cf6; --purple2: #7c3aed; --blue: #3b82f6; --cyan: #06b6d4;
  --green: #10b981; --amber: #f59e0b; --red: #ef4444;
  --grad: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
  --grad2: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%);
  --text: #eaecf4; --text2: #8892b0; --text3: #4a5270;
  --sidebar: 240px; --radius: 14px; --radius-sm: 8px;
  --shadow: 0 4px 24px rgba(0,0,0,0.4); --shadow-lg: 0 12px 48px rgba(0,0,0,0.5);
  --glow: 0 0 20px rgba(139,92,246,0.2);
}
*{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{font-family:"Plus Jakarta Sans",sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--surface);}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px;}
::-webkit-scrollbar-thumb:hover{background:var(--purple);}

/* MODAL */
#apiModal{position:fixed;inset:0;z-index:1000;background:rgba(8,9,15,0.96);display:flex;align-items:center;justify-content:center;backdrop-filter:blur(10px);}
#apiModal.hidden{display:none;}
.modal-box{background:var(--card);border:1px solid var(--border2);border-radius:20px;padding:48px;width:480px;max-width:95vw;text-align:center;box-shadow:0 40px 80px rgba(139,92,246,0.2);}
.modal-logo{font-family:"Bricolage Grotesque",sans-serif;font-size:2rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;}
.modal-sub{color:var(--text2);font-size:0.9rem;margin-bottom:32px;line-height:1.6;}
.modal-box input{width:100%;background:var(--surface);border:1px solid var(--border2);border-radius:var(--radius-sm);padding:14px 16px;color:var(--text);font-family:"Fira Code",monospace;font-size:0.85rem;outline:none;margin-bottom:16px;transition:border-color 0.2s,box-shadow 0.2s;}
.modal-box input:focus{border-color:var(--purple);box-shadow:0 0 0 3px rgba(139,92,246,0.15);}
.modal-box input::placeholder{color:var(--text3);}
.btn-primary{display:inline-flex;align-items:center;gap:8px;background:var(--grad);color:#fff;border:none;border-radius:var(--radius-sm);padding:13px 28px;font-family:"Plus Jakarta Sans",sans-serif;font-size:0.95rem;font-weight:600;cursor:pointer;transition:all 0.2s;width:100%;justify-content:center;box-shadow:0 4px 20px rgba(139,92,246,0.3);}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 6px 24px rgba(139,92,246,0.4);}
.btn-primary:active{transform:translateY(0);}
.btn-primary:disabled{opacity:0.5;cursor:not-allowed;transform:none;}
.modal-hint{color:var(--text3);font-size:0.78rem;margin-top:12px;}
.modal-hint a{color:var(--purple);text-decoration:none;}

/* LAYOUT */
.app{display:flex;min-height:100vh;}

/* SIDEBAR */
.sidebar{width:var(--sidebar);background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;position:fixed;top:0;left:0;bottom:0;z-index:100;overflow-y:auto;transition:width 0.2s;}
.sidebar-logo{padding:22px 18px 18px;border-bottom:1px solid var(--border);}
.logo-wrap{display:flex;align-items:center;gap:10px;}
.logo-icon{width:32px;height:32px;background:var(--grad);border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.logo-text{font-family:"Bricolage Grotesque",sans-serif;font-size:1.15rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;display:block;}
.logo-sub{font-size:0.68rem;color:var(--text3);margin-top:1px;}
.nav-section{padding:10px 10px;flex:1;}
.nav-label{font-size:0.6rem;font-weight:700;color:var(--text3);letter-spacing:0.12em;text-transform:uppercase;padding:0 10px;margin:12px 0 5px;}
.nav-label:first-child{margin-top:4px;}
.nav-item{display:flex;align-items:center;gap:9px;padding:8px 10px;border-radius:var(--radius-sm);cursor:pointer;transition:all 0.15s;margin-bottom:1px;color:var(--text2);font-size:0.82rem;font-weight:500;border-left:2px solid transparent;}
.nav-item:hover{background:rgba(255,255,255,0.04);color:var(--text);}
.nav-item.active{background:rgba(139,92,246,0.1);color:var(--purple);border-left-color:var(--purple);}
.nav-item .icon{font-size:0.9rem;width:18px;text-align:center;flex-shrink:0;}
.nav-arrow{margin-left:auto;opacity:0;font-size:0.65rem;transition:opacity 0.15s;}
.nav-item:hover .nav-arrow{opacity:0.5;}
.nav-item.active .nav-arrow{opacity:1;color:var(--purple);}
.sidebar-footer{padding:12px 14px;border-top:1px solid var(--border);}
.api-badge{display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:var(--radius-sm);background:var(--card);border:1px solid var(--border);font-size:0.74rem;cursor:pointer;transition:border-color 0.2s;margin-bottom:8px;}
.api-badge:hover{border-color:var(--border2);}
.api-dot{width:7px;height:7px;border-radius:50%;background:var(--text3);flex-shrink:0;}
.api-dot.ok{background:var(--green);box-shadow:0 0 6px var(--green);}
.api-badge-text{color:var(--text2);flex:1;}
.lang-pill{display:inline-flex;align-items:center;background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.3);border-radius:20px;padding:2px 8px;font-size:0.65rem;font-weight:700;color:var(--purple);}
.lang-select-wrap label{font-size:0.65rem;color:var(--text3);display:block;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.08em;}
.version-tag{font-size:0.62rem;color:var(--text3);text-align:center;margin-top:8px;opacity:0.6;}

/* MAIN */
.main{margin-left:var(--sidebar);flex:1;min-height:100vh;}
.section{display:none;padding:32px 36px;max-width:1060px;animation:sectionIn 0.3s ease;}
.section.active{display:block;}
@keyframes sectionIn{from{opacity:0;transform:translateY(12px);}to{opacity:1;transform:translateY(0);}}
.section-header{margin-bottom:28px;}
.section-title{font-family:"Bricolage Grotesque",sans-serif;font-size:1.9rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:6px;line-height:1.2;}
.section-desc{color:var(--text2);font-size:0.88rem;line-height:1.6;}

/* DEMO BANNER */
#demoBanner{display:none;align-items:center;justify-content:space-between;background:rgba(245,158,11,0.07);border-bottom:1px solid rgba(245,158,11,0.2);padding:10px 36px;font-size:0.82rem;color:var(--amber);gap:12px;flex-wrap:wrap;}
#demoBanner a{color:var(--amber);font-weight:600;cursor:pointer;text-decoration:underline;}

/* TOAST */
#toastContainer{position:fixed;bottom:24px;right:24px;z-index:9999;display:flex;flex-direction:column;gap:8px;pointer-events:none;}
.toast-item{background:var(--card2);border:1px solid var(--border2);border-radius:var(--radius-sm);padding:12px 16px;font-size:0.83rem;color:var(--text);box-shadow:var(--shadow-lg);display:flex;align-items:center;gap:10px;animation:toastIn 0.25s ease;min-width:240px;pointer-events:all;}
.toast-out{animation:toastOut 0.3s ease forwards;}
@keyframes toastIn{from{opacity:0;transform:translateX(20px);}to{opacity:1;transform:translateX(0);}}
@keyframes toastOut{from{opacity:1;}to{opacity:0;transform:translateX(20px);}}

/* CARDS */
.card{background:var(--card);border:1px solid var(--border);border-top:1px solid rgba(139,92,246,0.12);border-radius:var(--radius);padding:24px;margin-bottom:20px;transition:border-color 0.2s,box-shadow 0.2s;}
.card:hover{border-color:var(--border2);box-shadow:var(--shadow);}
.card-title{font-family:"Bricolage Grotesque",sans-serif;font-size:0.82rem;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:0.09em;margin-bottom:16px;}

/* INPUTS */
.input-row{display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap;}
.input-group{flex:1;min-width:180px;}
.input-group label{display:block;font-size:0.78rem;font-weight:600;color:var(--text2);margin-bottom:6px;}
input[type=text],input[type=number],input[type=url],input[type=email],input[type=password],textarea,select{width:100%;background:var(--surface);border:1px solid var(--border2);border-radius:var(--radius-sm);padding:10px 13px;color:var(--text);font-family:"Plus Jakarta Sans",sans-serif;font-size:0.86rem;outline:none;transition:border-color 0.2s,box-shadow 0.2s;appearance:none;}
input:focus,textarea:focus,select:focus{border-color:var(--purple);box-shadow:0 0 0 3px rgba(139,92,246,0.1);}
input::placeholder,textarea::placeholder{color:var(--text3);}
textarea{resize:vertical;min-height:80px;line-height:1.6;}
select{cursor:pointer;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%234a5270' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 12px center;padding-right:36px;}
input[type=range]{width:100%;accent-color:var(--purple);cursor:pointer;padding:0;}
input[type=color]{width:100%;height:40px;border-radius:var(--radius-sm);border:1px solid var(--border2);background:var(--surface);cursor:pointer;padding:3px;}
input[type=file]{padding:10px;cursor:pointer;}

/* BUTTONS */
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 20px;border-radius:var(--radius-sm);font-family:"Plus Jakarta Sans",sans-serif;font-size:0.86rem;font-weight:600;cursor:pointer;transition:all 0.15s;border:none;}
.btn-grad{background:var(--grad);color:#fff;box-shadow:0 4px 16px rgba(139,92,246,0.3);}
.btn-grad:hover{opacity:0.92;transform:translateY(-1px);box-shadow:0 6px 22px rgba(139,92,246,0.4);}
.btn-grad:active{transform:translateY(0);}
.btn-ghost{background:transparent;color:var(--text2);border:1px solid var(--border2);}
.btn-ghost:hover{background:rgba(255,255,255,0.04);color:var(--text);}
.btn-green{background:linear-gradient(135deg,#10b981,#059669);color:#fff;}
.btn-green:hover{opacity:0.9;transform:translateY(-1px);}
.btn-sm{padding:6px 13px;font-size:0.78rem;}
.btn:disabled{opacity:0.45;cursor:not-allowed;transform:none!important;}
.spinner{display:inline-block;width:15px;height:15px;border:2px solid rgba(255,255,255,0.2);border-top-color:#fff;border-radius:50%;animation:spin 0.7s linear infinite;}
@keyframes spin{to{transform:rotate(360deg);}}

.result-area{margin-top:20px;display:none;}
.result-area.show{display:block;}
.result-title{font-family:"Bricolage Grotesque",sans-serif;font-size:0.8rem;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:var(--text3);margin-bottom:12px;display:flex;align-items:center;gap:8px;}
.result-count{background:rgba(139,92,246,0.15);color:var(--purple);padding:2px 8px;border-radius:10px;font-size:0.68rem;}
.progress-bar{height:3px;background:var(--border);border-radius:2px;overflow:hidden;margin-bottom:14px;}
.progress-fill{height:100%;background:var(--grad);border-radius:2px;animation:progressPulse 1.4s ease-in-out infinite;}
@keyframes progressPulse{0%,100%{opacity:1}50%{opacity:0.5}}
.divider{height:1px;background:var(--border);margin:22px 0;}
.empty-state{text-align:center;padding:46px 22px;color:var(--text3);}
.empty-state .icon{font-size:2.4rem;margin-bottom:11px;}
.empty-state p{font-size:0.86rem;}

/* STREAM OUTPUT */
.stream-output{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px;font-family:"Fira Code",monospace;font-size:0.83rem;line-height:1.9;color:var(--text);max-height:580px;overflow-y:auto;position:relative;}
.stream-output h1,.stream-output h2{font-family:"Bricolage Grotesque",sans-serif;font-size:1.05rem;font-weight:700;color:var(--purple);margin:20px 0 8px;padding-bottom:6px;border-bottom:1px solid var(--border);}
.stream-output h1:first-child,.stream-output h2:first-child{margin-top:0;}
.stream-output h3{font-family:"Bricolage Grotesque",sans-serif;font-size:0.9rem;font-weight:700;color:var(--text);margin:14px 0 6px;}
.stream-output p{margin-bottom:10px;color:var(--text2);font-family:"Plus Jakarta Sans",sans-serif;font-size:0.86rem;}
.stream-output strong{color:var(--text);}
.stream-output ul,.stream-output ol{padding-left:20px;margin-bottom:10px;}
.stream-output li{color:var(--text2);margin-bottom:4px;font-family:"Plus Jakarta Sans",sans-serif;font-size:0.86rem;}
.stream-output hr{border:none;border-top:1px solid var(--border);margin:16px 0;}
.stream-cursor{display:inline-block;width:2px;height:1.1em;background:var(--purple);margin-left:2px;vertical-align:text-bottom;animation:blink 0.8s step-end infinite;}
@keyframes blink{50%{opacity:0;}}
.output-wrap{position:relative;}
.copy-float{position:absolute;top:12px;right:12px;opacity:0;transition:opacity 0.2s;z-index:2;}
.output-wrap:hover .copy-float{opacity:1;}

/* IDEAS */
.ideas-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px;margin-top:4px;}
.idea-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;transition:all 0.2s;}
.idea-card:hover{border-color:rgba(139,92,246,0.35);transform:translateY(-2px);box-shadow:0 8px 28px rgba(8,9,15,0.5);}
.idea-format{display:inline-flex;align-items:center;padding:3px 10px;border-radius:20px;font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;}
.fmt-Tutorial{background:rgba(59,130,246,0.15);color:#60a5fa;border:1px solid rgba(59,130,246,0.25);}
.fmt-Challenge{background:rgba(245,158,11,0.15);color:#fbbf24;border:1px solid rgba(245,158,11,0.25);}
.fmt-Storytime{background:rgba(139,92,246,0.15);color:#a78bfa;border:1px solid rgba(139,92,246,0.25);}
.fmt-Listicle{background:rgba(6,182,212,0.15);color:#22d3ee;border:1px solid rgba(6,182,212,0.25);}
.fmt-Vlog,.fmt-default{background:rgba(16,185,129,0.15);color:#34d399;border:1px solid rgba(16,185,129,0.25);}
.fmt-Reaction{background:rgba(239,68,68,0.15);color:#f87171;border:1px solid rgba(239,68,68,0.25);}
.idea-title{font-family:"Bricolage Grotesque",sans-serif;font-size:0.93rem;font-weight:700;color:var(--text);margin-bottom:8px;line-height:1.4;}
.idea-hook{font-size:0.8rem;color:var(--text2);margin-bottom:8px;font-style:italic;line-height:1.5;}
.idea-why{font-size:0.76rem;color:var(--text3);line-height:1.5;}

/* SHORTS */
.short-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:10px;overflow:hidden;}
.short-header{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;cursor:pointer;transition:background 0.15s;}
.short-header:hover{background:rgba(255,255,255,0.02);}
.short-num{width:28px;height:28px;background:var(--grad);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.76rem;font-weight:800;color:#fff;flex-shrink:0;}
.short-title-wrap{flex:1;margin:0 14px;}
.short-title-text{font-weight:600;font-size:0.88rem;color:var(--text);}
.short-ts{font-size:0.72rem;color:var(--text3);margin-top:2px;}
.short-chevron{color:var(--text3);font-size:0.75rem;transition:transform 0.2s;}
.short-card.open .short-chevron{transform:rotate(180deg);}
.short-body{display:none;padding:0 18px 18px;}
.short-card.open .short-body{display:block;}
.short-field{margin-bottom:12px;}
.short-field-label{font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:var(--text3);margin-bottom:5px;}
.short-field-value{background:var(--card);border:1px solid var(--border);border-radius:var(--radius-sm);padding:11px 13px;font-size:0.83rem;color:var(--text2);line-height:1.6;white-space:pre-wrap;}
.short-tags{display:flex;flex-wrap:wrap;gap:5px;}
.short-tag{padding:3px 9px;background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);border-radius:20px;font-size:0.73rem;color:var(--blue);}

/* THUMBNAIL */
.thumb-tabs{display:flex;margin-bottom:20px;border:1px solid var(--border2);border-radius:var(--radius-sm);overflow:hidden;width:fit-content;}
.thumb-tab{padding:9px 20px;font-size:0.83rem;font-weight:600;cursor:pointer;background:transparent;color:var(--text2);border:none;font-family:"Plus Jakarta Sans",sans-serif;transition:all 0.15s;}
.thumb-tab.active{background:var(--grad);color:#fff;}
.thumb-tab:hover:not(.active){background:rgba(255,255,255,0.04);color:var(--text);}
.thumb-tab-content{display:none;}
.thumb-tab-content.active{display:block;}
.thumb-layout{display:flex;gap:22px;flex-wrap:wrap;}
.thumb-canvas-wrap{flex-shrink:0;}
#thumbCanvas{display:block;border-radius:var(--radius);border:1px solid var(--border2);cursor:crosshair;max-width:100%;}
.thumb-controls{flex:1;min-width:260px;}
.thumb-templates{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:14px;}
.tpl-btn{padding:6px 13px;border-radius:var(--radius-sm);border:1px solid var(--border2);background:var(--surface);color:var(--text2);font-size:0.78rem;cursor:pointer;font-family:"Plus Jakarta Sans",sans-serif;transition:all 0.15s;}
.tpl-btn.active{background:rgba(139,92,246,0.15);border-color:var(--purple);color:var(--purple);}
.color-row{display:flex;gap:10px;align-items:flex-end;}
.color-field{flex:1;}
#aiThumbImg{width:100%;border-radius:var(--radius);border:1px solid var(--border2);display:none;margin-top:16px;}
.style-presets{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:14px;}
.preset-btn{padding:5px 13px;border-radius:20px;border:1px solid var(--border2);background:var(--surface);color:var(--text2);font-size:0.76rem;cursor:pointer;font-family:"Plus Jakarta Sans",sans-serif;transition:all 0.15s;}
.preset-btn.active{background:rgba(139,92,246,0.15);border-color:var(--purple);color:var(--purple);}

/* CAPTIONS */
.caption-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px;font-size:0.86rem;line-height:1.7;color:var(--text2);white-space:pre-wrap;word-break:break-word;}
.hashtags-wrap{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;}
.hashtag{padding:4px 11px;background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.2);border-radius:20px;font-size:0.76rem;color:var(--purple);cursor:pointer;transition:background 0.15s;}
.hashtag:hover{background:rgba(139,92,246,0.22);}
.copy-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;}
.copy-label{font-size:0.76rem;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:0.07em;}

/* SEO */
.title-variants{display:grid;gap:11px;margin-bottom:18px;}
.title-variant{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:15px 18px;display:flex;gap:14px;align-items:flex-start;transition:border-color 0.2s;}
.title-variant:hover{border-color:var(--border2);}
.variant-badge{width:30px;height:30px;background:var(--grad);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.78rem;font-weight:800;color:#fff;flex-shrink:0;margin-top:2px;}
.variant-title{font-weight:600;font-size:0.93rem;color:var(--text);margin-bottom:4px;line-height:1.4;}
.variant-why{font-size:0.78rem;color:var(--text3);}
.seo-desc-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;font-size:0.82rem;line-height:1.7;color:var(--text2);white-space:pre-wrap;max-height:280px;overflow-y:auto;font-family:"Fira Code",monospace;}
.tags-wrap{display:flex;flex-wrap:wrap;gap:6px;}
.seo-tag{padding:4px 11px;background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);border-radius:20px;font-size:0.76rem;color:var(--blue);}
.chapters-list{display:grid;gap:7px;}
.chapter-item{display:flex;gap:11px;align-items:center;padding:7px 11px;background:var(--surface);border-radius:var(--radius-sm);border:1px solid var(--border);}
.chapter-time{font-family:"Fira Code",monospace;font-size:0.76rem;color:var(--purple);font-weight:600;min-width:40px;}
.chapter-title{font-size:0.83rem;color:var(--text2);}

/* TRACKER */
.tracker-add{display:grid;grid-template-columns:2fr 1fr 1fr 1fr auto;gap:10px;align-items:end;margin-bottom:18px;}
@media(max-width:800px){.tracker-add{grid-template-columns:1fr 1fr;}}
.videos-table{width:100%;border-collapse:collapse;font-size:0.83rem;margin-bottom:24px;}
.videos-table th{text-align:left;padding:10px 13px;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:var(--text3);border-bottom:1px solid var(--border);}
.videos-table td{padding:11px 13px;border-bottom:1px solid var(--border);color:var(--text2);}
.videos-table tr:last-child td{border-bottom:none;}
.videos-table tr:hover td{background:rgba(255,255,255,0.015);}
.td-title{color:var(--text);font-weight:500;}
.td-del{color:var(--red);cursor:pointer;opacity:0.5;font-size:0.78rem;}
.td-del:hover{opacity:1;}
.charts-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-bottom:22px;}
@media(max-width:700px){.charts-grid{grid-template-columns:1fr;}}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:18px;}
.chart-card-title{font-family:"Bricolage Grotesque",sans-serif;font-size:0.8rem;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:0.07em;margin-bottom:13px;}
.suggestions-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:22px;font-size:0.86rem;line-height:1.85;color:var(--text2);}
.suggestions-box h2{font-family:"Bricolage Grotesque",sans-serif;font-size:0.98rem;font-weight:700;color:var(--purple);margin:16px 0 8px;}
.suggestions-box h2:first-child{margin-top:0;}
.suggestions-box ul{padding-left:18px;}
.suggestions-box li{margin-bottom:5px;}
.suggestions-box strong{color:var(--text);}
.stat-row{display:flex;gap:12px;margin-bottom:18px;flex-wrap:wrap;}
.stat-box{flex:1;min-width:100px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:18px;text-align:center;}
.stat-val{font-family:"Bricolage Grotesque",sans-serif;font-size:1.8rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.stat-lbl{font-size:0.72rem;color:var(--text3);margin-top:4px;text-transform:uppercase;letter-spacing:0.07em;}

/* HOOKS */
.hook-input-grid{display:grid;gap:14px;margin-bottom:18px;}
.hook-input-wrap{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px;}
.hook-label{font-size:0.76rem;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:0.09em;margin-bottom:8px;}
.hook-results-grid{display:grid;gap:14px;}
.hook-result-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;transition:border-color 0.2s;}
.hook-result-card.winner{border-color:var(--green);background:rgba(16,185,129,0.04);box-shadow:0 0 20px rgba(16,185,129,0.08);}
.hook-winner-badge{display:inline-flex;align-items:center;gap:6px;background:linear-gradient(135deg,#10b981,#059669);color:#fff;border-radius:20px;padding:3px 12px;font-size:0.7rem;font-weight:700;margin-bottom:12px;}
.hook-score-bars{display:grid;gap:9px;margin:13px 0;}
.hook-score-row{display:flex;align-items:center;gap:9px;}
.hook-score-label{font-size:0.73rem;color:var(--text3);min-width:68px;text-transform:capitalize;}
.hook-score-bar-track{flex:1;height:5px;background:var(--border);border-radius:3px;overflow:hidden;}
.hook-score-bar-fill{height:100%;border-radius:3px;background:var(--grad);transition:width 0.8s cubic-bezier(0.4,0,0.2,1);width:0;}
.hook-score-num{font-size:0.76rem;font-weight:700;color:var(--purple);min-width:22px;text-align:right;}
.hook-total{font-family:"Bricolage Grotesque",sans-serif;font-size:1.4rem;font-weight:800;color:var(--text);margin-bottom:4px;}
.hook-feedback{font-size:0.8rem;color:var(--text2);line-height:1.6;}

/* VOICEOVER */
.voice-controls{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px;}
.slider-group{margin-bottom:12px;}
.slider-group label{display:flex;justify-content:space-between;font-size:0.78rem;color:var(--text2);margin-bottom:6px;}
.slider-group label span{color:var(--purple);font-weight:600;}
.vo-play-row{display:flex;gap:9px;flex-wrap:wrap;align-items:center;}
.premium-box{background:rgba(245,158,11,0.05);border:1px solid rgba(245,158,11,0.18);border-radius:var(--radius);padding:18px;margin-top:14px;}
.premium-title{font-family:"Bricolage Grotesque",sans-serif;font-size:0.84rem;font-weight:700;color:var(--amber);margin-bottom:10px;display:flex;align-items:center;gap:7px;}

/* CALENDAR */
.cal-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;}
.cal-month-title{font-family:"Bricolage Grotesque",sans-serif;font-size:1.15rem;font-weight:700;color:var(--text);}
.cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;}
.cal-dow{text-align:center;font-size:0.68rem;font-weight:700;color:var(--text3);text-transform:uppercase;padding:6px 0;}
.cal-day{min-height:76px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:7px;cursor:pointer;transition:all 0.15s;position:relative;}
.cal-day:hover{border-color:rgba(139,92,246,0.35);background:rgba(139,92,246,0.03);}
.cal-day.other-month{opacity:0.3;}
.cal-day.today{border-color:var(--purple);background:rgba(139,92,246,0.05);}
.cal-day-num{font-size:0.76rem;font-weight:600;color:var(--text2);margin-bottom:3px;}
.cal-day.today .cal-day-num{color:var(--purple);}
.cal-item-badge{display:inline-block;width:100%;padding:2px 5px;border-radius:3px;font-size:0.62rem;font-weight:600;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cal-item-badge.yt-long{background:rgba(239,68,68,0.18);color:#f87171;}
.cal-item-badge.yt-short{background:rgba(245,158,11,0.18);color:#fbbf24;}
.cal-item-badge.ig-post{background:rgba(139,92,246,0.18);color:#a78bfa;}
.cal-item-badge.ig-reel{background:rgba(59,130,246,0.18);color:#60a5fa;}
.cal-day-count{position:absolute;top:5px;right:5px;background:var(--purple);color:#fff;border-radius:50%;width:14px;height:14px;font-size:0.58rem;font-weight:700;display:flex;align-items:center;justify-content:center;}
.cal-legend{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:14px;}
.cal-legend-item{display:flex;align-items:center;gap:5px;font-size:0.73rem;color:var(--text2);}
.cal-legend-dot{width:9px;height:9px;border-radius:2px;}
#calModal{position:fixed;inset:0;z-index:500;background:rgba(8,9,15,0.85);display:none;align-items:center;justify-content:center;backdrop-filter:blur(4px);}
#calModal.open{display:flex;}
.cal-modal-box{background:var(--card);border:1px solid var(--border2);border-radius:var(--radius);padding:26px;width:420px;max-width:95vw;}
.cal-modal-title{font-family:"Bricolage Grotesque",sans-serif;font-size:1rem;font-weight:700;color:var(--text);margin-bottom:18px;}
.cal-type-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:14px;}
.cal-type-btn{padding:9px;border-radius:var(--radius-sm);border:2px solid var(--border2);background:var(--surface);color:var(--text2);font-size:0.8rem;font-weight:600;cursor:pointer;font-family:"Plus Jakarta Sans",sans-serif;transition:all 0.15s;text-align:center;}
.cal-type-btn.selected.yt-long{border-color:#ef4444;color:#ef4444;background:rgba(239,68,68,0.08);}
.cal-type-btn.selected.yt-short{border-color:#f59e0b;color:#f59e0b;background:rgba(245,158,11,0.08);}
.cal-type-btn.selected.ig-post{border-color:#a78bfa;color:#a78bfa;background:rgba(139,92,246,0.08);}
.cal-type-btn.selected.ig-reel{border-color:#60a5fa;color:#60a5fa;background:rgba(59,130,246,0.08);}
.cal-items-list{margin-bottom:14px;}
.cal-existing-item{display:flex;align-items:center;justify-content:space-between;padding:7px 11px;background:var(--surface);border-radius:var(--radius-sm);margin-bottom:5px;border:1px solid var(--border);}
.cal-existing-item .remove-btn{color:var(--red);cursor:pointer;font-size:0.78rem;opacity:0.6;background:none;border:none;}

/* AB TRACKER */
.ab-upload-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:18px;}
.ab-preview-box{background:var(--surface);border:2px dashed var(--border2);border-radius:var(--radius);padding:18px;text-align:center;transition:border-color 0.2s;cursor:pointer;}
.ab-preview-box:hover{border-color:var(--purple);}
.ab-preview-box img{width:100%;border-radius:var(--radius-sm);margin-top:10px;display:none;}
.ab-preview-label{font-size:0.78rem;color:var(--text3);margin-top:7px;}
.ab-log-form{display:grid;grid-template-columns:auto 1fr 1fr auto;gap:10px;align-items:end;margin-bottom:18px;}
@media(max-width:700px){.ab-log-form{grid-template-columns:1fr 1fr;}}
.ab-table{width:100%;border-collapse:collapse;font-size:0.83rem;}
.ab-table th{text-align:left;padding:9px 13px;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:var(--text3);border-bottom:1px solid var(--border);}
.ab-table td{padding:9px 13px;border-bottom:1px solid var(--border);color:var(--text2);}
.winner-pill{background:var(--grad);color:#fff;border-radius:20px;padding:2px 9px;font-size:0.7rem;font-weight:700;}

/* COMPETITOR */
.competitor-section{margin-bottom:18px;}
.competitor-section-title{font-family:"Bricolage Grotesque",sans-serif;font-size:0.82rem;font-weight:700;color:var(--purple);text-transform:uppercase;letter-spacing:0.09em;margin-bottom:10px;display:flex;align-items:center;gap:7px;}
.competitor-list{list-style:none;}
.competitor-list li{padding:9px 13px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);margin-bottom:7px;font-size:0.83rem;color:var(--text2);line-height:1.5;display:flex;gap:9px;}
.competitor-list li::before{content:"→";color:var(--purple);flex-shrink:0;}
.opportunity-list li{border-left:2px solid var(--purple);}
.opportunity-list li::before{content:"★";}
.freq-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px;font-size:0.86rem;color:var(--text2);line-height:1.6;}

/* NEWSLETTER */
.newsletter-preview{background:#fff;border-radius:var(--radius);padding:28px;color:#111;font-family:Georgia,serif;font-size:0.9rem;line-height:1.8;max-height:480px;overflow-y:auto;}
.newsletter-preview h2{font-size:1.05rem;font-weight:700;color:#111;margin:18px 0 9px;padding-bottom:5px;border-bottom:1px solid #e5e5e5;}
.newsletter-preview h2:first-child{margin-top:0;}
.newsletter-preview p{margin-bottom:11px;color:#333;}
.newsletter-preview ul{padding-left:18px;margin-bottom:11px;}
.newsletter-preview li{margin-bottom:5px;color:#333;}
.newsletter-preview strong{color:#111;}

/* EXPORT */
.export-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;}
.export-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;display:flex;flex-direction:column;gap:11px;transition:all 0.2s;}
.export-card:hover{border-color:var(--border2);transform:translateY(-1px);box-shadow:var(--shadow);}
.export-icon{font-size:1.7rem;}
.export-title{font-family:"Bricolage Grotesque",sans-serif;font-size:0.88rem;font-weight:700;color:var(--text);}
.export-desc{font-size:0.76rem;color:var(--text3);line-height:1.5;flex:1;}
.notion-export-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;font-family:"Fira Code",monospace;font-size:0.78rem;color:var(--text2);white-space:pre-wrap;max-height:280px;overflow-y:auto;line-height:1.6;}
.sheets-instructions{background:rgba(16,185,129,0.05);border:1px solid rgba(16,185,129,0.18);border-radius:var(--radius);padding:18px;}
.sheets-instructions ol{padding-left:18px;color:var(--text2);font-size:0.83rem;line-height:1.8;}

/* EXTENSION */
.ext-step{display:flex;gap:14px;padding:14px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:10px;align-items:flex-start;}
.ext-step-num{width:30px;height:30px;background:var(--grad);border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.82rem;color:#fff;flex-shrink:0;}
.ext-step-text{flex:1;}
.ext-step-title{font-weight:600;font-size:0.88rem;color:var(--text);margin-bottom:3px;}
.ext-step-desc{font-size:0.8rem;color:var(--text2);line-height:1.5;}
.ext-file-list{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px;}
.ext-file{display:flex;align-items:center;gap:9px;padding:7px 0;border-bottom:1px solid var(--border);}
.ext-file:last-child{border-bottom:none;}
.ext-file-name{font-family:"Fira Code",monospace;font-size:0.8rem;color:var(--purple);flex:1;}
.ext-file-desc{font-size:0.76rem;color:var(--text3);}
.ext-preview{background:var(--card);border:1px solid var(--border);border-radius:var(--radius-sm);padding:11px 14px;margin-top:7px;font-size:0.8rem;color:var(--text2);line-height:1.6;font-style:italic;}
.yt-connect-box{background:rgba(239,68,68,0.05);border:1px solid rgba(239,68,68,0.18);border-radius:var(--radius);padding:18px;margin-bottom:18px;}
.yt-connect-title{font-family:"Bricolage Grotesque",sans-serif;font-size:0.88rem;font-weight:700;color:#f87171;margin-bottom:13px;display:flex;align-items:center;gap:7px;}
.info-box{background:rgba(59,130,246,0.06);border:1px solid rgba(59,130,246,0.18);border-radius:var(--radius-sm);padding:11px 14px;font-size:0.8rem;color:#93c5fd;margin-bottom:14px;display:flex;gap:9px;align-items:flex-start;}
.info-box .info-icon{flex-shrink:0;}

@media(max-width:768px){
  :root{--sidebar:48px;}
  .nav-item>span:not(.icon){display:none;}
  .nav-arrow,.nav-label,.sidebar-footer .api-badge-text,.lang-select-wrap,.version-tag{display:none!important;}
  .lang-pill{display:none!important;}
  .section{padding:20px 16px;}
  .section-title{font-size:1.5rem;}
  .charts-grid{grid-template-columns:1fr;}
  .tracker-add{grid-template-columns:1fr 1fr;}
  .ab-upload-grid{grid-template-columns:1fr;}
  .voice-controls{grid-template-columns:1fr;}
}
</style>
</head>
<body>
''')

# ── MODALS & OVERLAYS ─────────────────────────────────────────────────────────
w('''
<div id="apiModal" class="hidden">
  <div class="modal-box">
    <div class="modal-logo">CreatorOS</div>
    <p class="modal-sub">Add your Anthropic API key for live AI generation.<br>Or continue in Demo Mode — all tools work instantly.</p>
    <input type="password" id="apiKeyInput" placeholder="sk-ant-api03-..." autocomplete="off">
    <button class="btn-primary" onclick="saveApiKey()"><span>Save API Key</span><span>&#8594;</span></button>
    <button class="btn-primary" onclick="closeModal()" style="background:transparent;border:1px solid var(--border2);color:var(--text2);margin-top:8px;box-shadow:none">Continue in Demo Mode</button>
    <p class="modal-hint">Get a free key at <a href="https://console.anthropic.com" target="_blank" rel="noopener">console.anthropic.com</a> &mdash; stored locally, never shared</p>
  </div>
</div>

<div id="calModal">
  <div class="cal-modal-box">
    <div class="cal-modal-title" id="calModalTitle">Add content</div>
    <div class="cal-items-list" id="calModalItems"></div>
    <div style="margin-bottom:12px">
      <label style="font-size:0.8rem;color:var(--text2);display:block;margin-bottom:8px">Content Type</label>
      <div class="cal-type-grid">
        <button class="cal-type-btn yt-long" onclick="selectCalType('yt-long',this)">&#128308; YouTube Long</button>
        <button class="cal-type-btn yt-short" onclick="selectCalType('yt-short',this)">&#128993; YouTube Short</button>
        <button class="cal-type-btn ig-post" onclick="selectCalType('ig-post',this)">&#128995; Instagram Post</button>
        <button class="cal-type-btn ig-reel" onclick="selectCalType('ig-reel',this)">&#128309; Instagram Reel</button>
      </div>
    </div>
    <div class="input-group" style="margin-bottom:16px">
      <label>Title (optional)</label>
      <input type="text" id="calItemTitle" placeholder="e.g. My morning routine video">
    </div>
    <div style="display:flex;gap:10px">
      <button class="btn btn-grad" style="flex:1" onclick="addCalItem()">+ Add Item</button>
      <button class="btn btn-ghost" onclick="closeCalModal()">Done</button>
    </div>
  </div>
</div>

<div id="toastContainer"></div>

<div id="demoBanner">
  <span>&#9889; Running in <strong>Demo Mode</strong> &mdash; results are realistic examples. <a onclick="document.getElementById('apiModal').classList.remove('hidden')">Add an API key</a> for live AI generation.</span>
  <span style="opacity:0.5;font-size:0.75rem">All 16 tools fully functional in demo mode</span>
</div>
''')

# ── APP SHELL ─────────────────────────────────────────────────────────────────
w('''
<div class="app">
<aside class="sidebar">
  <div class="sidebar-logo">
    <div class="logo-wrap">
      <div class="logo-icon">
        <svg viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 2L11.5 7H16.5L12.5 10.5L14 16L9 13L4 16L5.5 10.5L1.5 7H6.5L9 2Z" fill="white" opacity="0.9"/>
        </svg>
      </div>
      <div>
        <span class="logo-text">CreatorOS</span>
        <span class="logo-sub">Content Command Center</span>
      </div>
    </div>
  </div>
  <nav class="nav-section">
    <div class="nav-label">Creation</div>
    <div class="nav-item active" onclick="showSection('ideas',this)"><span class="icon">&#128161;</span><span>Idea Generator</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-item" onclick="showSection('script',this)"><span class="icon">&#128221;</span><span>Script Writer</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-item" onclick="showSection('shorts',this)"><span class="icon">&#127909;</span><span>Shorts Repurposer</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-item" onclick="showSection('captions',this)"><span class="icon">&#9999;&#65039;</span><span>Caption Generator</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-item" onclick="showSection('hooks',this)"><span class="icon">&#127908;</span><span>Hook Tester</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-item" onclick="showSection('voiceover',this)"><span class="icon">&#127897;&#65039;</span><span>Voiceover</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-label">Visuals</div>
    <div class="nav-item" onclick="showSection('thumbnail',this)"><span class="icon">&#128444;&#65039;</span><span>Thumbnail Studio</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-item" onclick="showSection('abthumb',this)"><span class="icon">&#127374;</span><span>A/B Thumbnail</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-label">Publishing</div>
    <div class="nav-item" onclick="showSection('calendar',this)"><span class="icon">&#128197;</span><span>Content Calendar</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-item" onclick="showSection('seo',this)"><span class="icon">&#128269;</span><span>SEO Optimizer</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-item" onclick="showSection('newsletter',this)"><span class="icon">&#128231;</span><span>Newsletter</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-label">Analytics</div>
    <div class="nav-item" onclick="showSection('tracker',this)"><span class="icon">&#128202;</span><span>Performance Tracker</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-item" onclick="showSection('competitor',this)"><span class="icon">&#128373;&#65039;</span><span>Competitor Analysis</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-label">Tools</div>
    <div class="nav-item" onclick="showSection('export',this)"><span class="icon">&#128228;</span><span>Export Center</span><span class="nav-arrow">&#8250;</span></div>
    <div class="nav-item" onclick="showSection('extension',this)"><span class="icon">&#129513;</span><span>Chrome Extension</span><span class="nav-arrow">&#8250;</span></div>
  </nav>
  <div class="sidebar-footer">
    <div class="api-badge" onclick="document.getElementById('apiModal').classList.remove('hidden')">
      <div class="api-dot" id="apiDot"></div>
      <span class="api-badge-text" id="apiBadgeText">Demo Mode</span>
      <span class="lang-pill" id="langPill" style="display:none">EN</span>
    </div>
    <div class="lang-select-wrap">
      <label>Language</label>
      <select id="globalLang" onchange="setLanguage(this.value)">
        <option value="English">English</option>
        <option value="Hindi">Hindi</option>
        <option value="Spanish">Spanish</option>
        <option value="Portuguese">Portuguese</option>
        <option value="French">French</option>
        <option value="Arabic">Arabic</option>
        <option value="German">German</option>
        <option value="Japanese">Japanese</option>
      </select>
    </div>
    <div class="version-tag">v2.0 &mdash; CreatorOS</div>
  </div>
</aside>
<main class="main">
''')

# ── SECTION 1: IDEAS ──────────────────────────────────────────────────────────
w('''
<section class="section active" id="sec-ideas">
  <div class="section-header">
    <div class="section-title">&#128161; Idea Generator</div>
    <p class="section-desc">Generate viral content ideas tailored to your niche and platform</p>
  </div>
  <div class="card">
    <div class="input-row">
      <div class="input-group" style="flex:2">
        <label>Your Niche</label>
        <input type="text" id="ideasNiche" placeholder="e.g. Personal Finance, Fitness, Tech Reviews, Travel...">
      </div>
      <div class="input-group">
        <label>Platform</label>
        <select id="ideasPlatform">
          <option>YouTube</option>
          <option>Instagram</option>
          <option>Both YouTube &amp; Instagram</option>
        </select>
      </div>
      <div class="input-group" style="flex:0;min-width:110px">
        <label>Count</label>
        <select id="ideasCount">
          <option value="5">5 ideas</option>
          <option value="10" selected>10 ideas</option>
          <option value="15">15 ideas</option>
        </select>
      </div>
    </div>
    <button class="btn btn-grad" id="ideasBtn" onclick="generateIdeas()">
      <span class="spinner" id="ideasSpinner" style="display:none"></span>
      <span>&#10024; Generate Ideas</span>
    </button>
  </div>
  <div class="result-area" id="ideasResult">
    <div class="progress-bar" id="ideasProgress" style="display:none"><div class="progress-fill"></div></div>
    <div class="result-title">Generated Ideas <span class="result-count" id="ideasCountBadge">0</span></div>
    <div class="ideas-grid" id="ideasGrid"></div>
  </div>
</section>
''')

# ── SECTION 2: SCRIPT ─────────────────────────────────────────────────────────
w('''
<section class="section" id="sec-script">
  <div class="section-header">
    <div class="section-title">&#128221; Script Writer</div>
    <p class="section-desc">Get a complete, structured script with hooks, sections, and a strong CTA &mdash; streamed live</p>
  </div>
  <div class="card">
    <div class="input-group" style="margin-bottom:14px">
      <label>Video Topic</label>
      <textarea id="scriptTopic" rows="3" placeholder="e.g. How I went from 0 to 10K subscribers in 90 days &mdash; step by step breakdown"></textarea>
    </div>
    <div class="input-row">
      <div class="input-group">
        <label>Target Duration</label>
        <select id="scriptDuration">
          <option>5 minutes</option>
          <option selected>10 minutes</option>
          <option>15 minutes</option>
          <option>20 minutes</option>
          <option>30 minutes</option>
        </select>
      </div>
      <div class="input-group">
        <label>Style</label>
        <select id="scriptStyle">
          <option value="conversational">Conversational</option>
          <option value="educational">Educational</option>
          <option value="storytelling">Storytelling</option>
          <option value="motivational">Motivational</option>
        </select>
      </div>
    </div>
    <button class="btn btn-grad" id="scriptBtn" onclick="generateScript()">
      <span class="spinner" id="scriptSpinner" style="display:none"></span>
      <span>&#9998;&#65039; Write Full Script</span>
    </button>
  </div>
  <div class="result-area" id="scriptResult">
    <div class="output-wrap">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
        <div class="result-title" style="margin:0">Generated Script</div>
        <div style="display:flex;gap:8px">
          <span id="scriptWordCount" style="font-size:0.75rem;color:var(--text3);align-self:center"></span>
          <button class="btn btn-ghost btn-sm" onclick="copyEl('scriptOutput')">&#128203; Copy</button>
        </div>
      </div>
      <div class="stream-output" id="scriptOutput"></div>
    </div>
  </div>
</section>
''')

# ── SECTION 3: SHORTS ─────────────────────────────────────────────────────────
w('''
<section class="section" id="sec-shorts">
  <div class="section-header">
    <div class="section-title">&#127909; Shorts Repurposer</div>
    <p class="section-desc">Paste a YouTube URL or video title &mdash; get 7 ready-to-shoot Shorts scripts</p>
  </div>
  <div class="card">
    <div class="input-group" style="margin-bottom:16px">
      <label>YouTube URL or Video Title/Topic</label>
      <input type="text" id="shortsInput" placeholder="https://youtube.com/watch?v=... or just paste your video title">
    </div>
    <button class="btn btn-grad" id="shortsBtn" onclick="generateShorts()">
      <span class="spinner" id="shortsSpinner" style="display:none"></span>
      <span>&#9986;&#65039; Generate 7 Shorts</span>
    </button>
  </div>
  <div class="result-area" id="shortsResult">
    <div class="progress-bar" id="shortsProgress" style="display:none"><div class="progress-fill"></div></div>
    <div class="result-title">Shorts Breakdown</div>
    <div id="shortsGrid"></div>
  </div>
</section>
''')

# ── SECTION 4: THUMBNAIL ──────────────────────────────────────────────────────
w('''
<section class="section" id="sec-thumbnail">
  <div class="section-header">
    <div class="section-title">&#128444;&#65039; Thumbnail Studio</div>
    <p class="section-desc">Design thumbnails manually or generate with AI &mdash; completely free</p>
  </div>
  <div class="thumb-tabs">
    <button class="thumb-tab active" onclick="switchThumbTab('manual',this)">&#9999;&#65039; Manual Design</button>
    <button class="thumb-tab" onclick="switchThumbTab('ai',this)">&#129302; AI Generate</button>
  </div>
  <div class="thumb-tab-content active" id="thumbTabManual">
    <div class="card">
      <div class="thumb-layout">
        <div class="thumb-canvas-wrap">
          <canvas id="thumbCanvas" width="640" height="360"></canvas>
          <div style="margin-top:12px;display:flex;gap:8px">
            <button class="btn btn-grad" onclick="downloadThumb()">&#11015;&#65039; Download PNG</button>
            <button class="btn btn-ghost btn-sm" onclick="drawThumb()">&#128260; Refresh</button>
          </div>
        </div>
        <div class="thumb-controls">
          <div class="card-title">Templates</div>
          <div class="thumb-templates" id="tplBtns">
            <button class="tpl-btn active" data-tpl="gradient" onclick="setTemplate(this,'gradient')">Gradient</button>
            <button class="tpl-btn" data-tpl="split" onclick="setTemplate(this,'split')">Split</button>
            <button class="tpl-btn" data-tpl="dark" onclick="setTemplate(this,'dark')">Dark</button>
            <button class="tpl-btn" data-tpl="bold" onclick="setTemplate(this,'bold')">Bold</button>
            <button class="tpl-btn" data-tpl="minimal" onclick="setTemplate(this,'minimal')">Minimal</button>
          </div>
          <div class="divider"></div>
          <div style="margin-bottom:12px"><label style="font-size:0.8rem;color:var(--text2);display:block;margin-bottom:6px">Main Title</label><input type="text" id="thumbTitle" value="YOUR TITLE HERE" oninput="drawThumb()"></div>
          <div style="margin-bottom:12px"><label style="font-size:0.8rem;color:var(--text2);display:block;margin-bottom:6px">Subtitle / Number</label><input type="text" id="thumbSub" value="5 SECRETS" oninput="drawThumb()"></div>
          <div style="margin-bottom:12px"><label style="font-size:0.8rem;color:var(--text2);display:block;margin-bottom:6px">Emoji / Icon</label><input type="text" id="thumbEmoji" value="&#128293;" oninput="drawThumb()" maxlength="4"></div>
          <div class="divider"></div>
          <div class="color-row" style="margin-bottom:12px">
            <div class="color-field"><label style="font-size:0.8rem;color:var(--text2);display:block;margin-bottom:6px">BG Color 1</label><input type="color" id="thumbBg1" value="#7c3aed" oninput="drawThumb()"></div>
            <div class="color-field"><label style="font-size:0.8rem;color:var(--text2);display:block;margin-bottom:6px">BG Color 2</label><input type="color" id="thumbBg2" value="#2563eb" oninput="drawThumb()"></div>
            <div class="color-field"><label style="font-size:0.8rem;color:var(--text2);display:block;margin-bottom:6px">Text Color</label><input type="color" id="thumbTextColor" value="#ffffff" oninput="drawThumb()"></div>
          </div>
          <div style="margin-bottom:12px">
            <label style="font-size:0.8rem;color:var(--text2);display:block;margin-bottom:6px">Title Size: <span id="thumbSizeVal">52</span>px</label>
            <input type="range" id="thumbSize" min="24" max="90" value="52" oninput="document.getElementById('thumbSizeVal').textContent=this.value;drawThumb()">
          </div>
          <div><label style="font-size:0.8rem;color:var(--text2);display:block;margin-bottom:6px">Format</label>
            <select id="thumbFormat" onchange="updateCanvasSize()">
              <option value="yt">YouTube (1280x720)</option>
              <option value="shorts">Shorts / Reels (1080x1920)</option>
              <option value="square">Square Post (1080x1080)</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="thumb-tab-content" id="thumbTabAi">
    <div class="card">
      <div class="info-box"><span class="info-icon">&#8505;&#65039;</span><span>Powered by <strong>Pollinations.ai</strong> &mdash; completely free, no API key needed.</span></div>
      <div class="input-group" style="margin-bottom:14px"><label>Describe your thumbnail</label><textarea id="aiThumbPrompt" rows="3" placeholder="e.g. A shocked creator at a desk with glowing computer screen, bold text overlay, cinematic lighting"></textarea></div>
      <div style="margin-bottom:16px">
        <label style="font-size:0.8rem;color:var(--text2);display:block;margin-bottom:8px">Style Preset</label>
        <div class="style-presets" id="stylePresets">
          <button class="preset-btn active" onclick="selectPreset(this,'Cinematic dramatic lighting, professional photography')">Cinematic</button>
          <button class="preset-btn" onclick="selectPreset(this,'Bold oversized text, high contrast colors, eye-catching')">Bold Text</button>
          <button class="preset-btn" onclick="selectPreset(this,'Clean minimalist design, simple background, elegant')">Minimalist</button>
          <button class="preset-btn" onclick="selectPreset(this,'Viral YouTube thumbnail style, bright colors, shocked face')">Viral</button>
          <button class="preset-btn" onclick="selectPreset(this,'Dark dramatic atmosphere, moody lighting, deep shadows')">Dark Drama</button>
        </div>
      </div>
      <button class="btn btn-grad" id="aiThumbBtn" onclick="generateAIThumb()">
        <span class="spinner" id="aiThumbSpinner" style="display:none"></span>
        <span>&#127912; Generate Thumbnail</span>
      </button>
      <img id="aiThumbImg" alt="AI Generated Thumbnail" onload="document.getElementById('aiThumbDownloadWrap').style.display='block'">
      <div style="margin-top:12px;display:none" id="aiThumbDownloadWrap">
        <a id="aiThumbDownloadBtn" class="btn btn-ghost" style="display:inline-flex" download="ai-thumbnail.jpg">&#11015;&#65039; Download</a>
      </div>
    </div>
  </div>
</section>
''')

# ── SECTION 5: CAPTIONS ───────────────────────────────────────────────────────
w('''
<section class="section" id="sec-captions">
  <div class="section-header">
    <div class="section-title">&#9999;&#65039; Caption Generator</div>
    <p class="section-desc">Generate platform-optimized captions and targeted hashtag sets</p>
  </div>
  <div class="card">
    <div class="input-row">
      <div class="input-group" style="flex:2"><label>Video Topic / Description</label><input type="text" id="captionTopic" placeholder="e.g. Morning routine that changed my life, 5AM habits for success"></div>
      <div class="input-group"><label>Platform</label>
        <select id="captionPlatform">
          <option>YouTube</option><option>Instagram</option><option>YouTube Shorts</option><option>Instagram Reels</option>
        </select>
      </div>
    </div>
    <button class="btn btn-grad" id="captionBtn" onclick="generateCaption()">
      <span class="spinner" id="captionSpinner" style="display:none"></span>
      <span>&#10024; Generate Caption</span>
    </button>
  </div>
  <div class="result-area" id="captionResult">
    <div class="progress-bar" id="captionProgress" style="display:none"><div class="progress-fill"></div></div>
    <div class="card"><div class="copy-row"><div class="copy-label">&#127908; Hook</div><button class="btn btn-ghost btn-sm" onclick="copyEl('captionHook')">&#128203; Copy</button></div><div class="caption-box" id="captionHook"></div></div>
    <div class="card"><div class="copy-row"><div class="copy-label">&#128221; Full Caption</div><button class="btn btn-ghost btn-sm" onclick="copyEl('captionBody')">&#128203; Copy</button></div><div class="caption-box" id="captionBody"></div></div>
    <div class="card"><div class="copy-row"><div class="copy-label">&#127991;&#65039; Hashtags</div><button class="btn btn-ghost btn-sm" onclick="copyHashtags()">&#128203; Copy All</button></div><div class="hashtags-wrap" id="captionHashtags"></div></div>
    <div class="card">
      <div class="copy-label" style="margin-bottom:8px">&#127919; Call to Action</div>
      <div class="caption-box" id="captionCta"></div>
      <div style="margin-top:10px;font-size:0.8rem;color:var(--text3)">&#9200; Best post time: <span id="captionBestTime" style="color:var(--purple)"></span></div>
    </div>
  </div>
</section>
''')

# ── SECTION 6: SEO ────────────────────────────────────────────────────────────
w('''
<section class="section" id="sec-seo">
  <div class="section-header">
    <div class="section-title">&#128269; SEO Optimizer</div>
    <p class="section-desc">A/B test titles, generate optimized descriptions, tags, and chapters</p>
  </div>
  <div class="card">
    <div class="input-group" style="margin-bottom:16px"><label>YouTube URL or Video Topic</label><input type="text" id="seoInput" placeholder="https://youtube.com/watch?v=... or describe your video topic"></div>
    <button class="btn btn-grad" id="seoBtn" onclick="generateSEO()">
      <span class="spinner" id="seoSpinner" style="display:none"></span>
      <span>&#128269; Optimize for SEO</span>
    </button>
  </div>
  <div class="result-area" id="seoResult">
    <div class="progress-bar" id="seoProgress" style="display:none"><div class="progress-fill"></div></div>
    <div class="result-title">A/B Title Variants</div>
    <div class="title-variants" id="seoTitles"></div>
    <div class="divider"></div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
      <div class="result-title" style="margin:0">Optimized Description</div>
      <button class="btn btn-ghost btn-sm" onclick="copyEl('seoDesc')">&#128203; Copy</button>
    </div>
    <div class="seo-desc-box" id="seoDesc"></div>
    <div class="divider"></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
      <div><div class="result-title" style="margin-bottom:10px">Tags</div><div class="tags-wrap" id="seoTags"></div></div>
      <div><div class="result-title" style="margin-bottom:10px">Chapters</div><div class="chapters-list" id="seoChapters"></div></div>
    </div>
    <div style="margin-top:16px;padding:13px;background:rgba(139,92,246,0.07);border:1px solid rgba(139,92,246,0.18);border-radius:var(--radius-sm);font-size:0.83rem">
      <strong style="color:var(--purple)">&#128161; Thumbnail Tip:</strong> <span id="seoThumbTip" style="color:var(--text2)"></span>
    </div>
  </div>
</section>
''')

# ── SECTION 7: TRACKER ────────────────────────────────────────────────────────
w('''
<section class="section" id="sec-tracker">
  <div class="section-header">
    <div class="section-title">&#128202; Performance Tracker</div>
    <p class="section-desc">Track views, likes, CTR &mdash; and get AI-powered improvement suggestions streamed live</p>
  </div>
  <div class="yt-connect-box">
    <div class="yt-connect-title">&#9654;&#65039; Connect YouTube Analytics (Optional)</div>
    <div class="input-row">
      <div class="input-group"><label>Google API Key</label><input type="text" id="ytApiKey" placeholder="AIzaSy..."></div>
      <div class="input-group"><label>Channel ID</label><input type="text" id="ytChannelId" placeholder="UCxxxxxxxxxxxxxxx"></div>
      <div class="input-group" style="flex:0;min-width:130px"><label>&nbsp;</label><button class="btn btn-grad" id="ytFetchBtn" onclick="fetchYTStats()"><span class="spinner" id="ytFetchSpinner" style="display:none"></span><span>Fetch Stats</span></button></div>
    </div>
    <div style="font-size:0.74rem;color:var(--text3);margin-top:4px">Leave blank to use demo data or enter manually below.</div>
    <div id="ytChannelInfo" style="display:none;margin-top:12px;padding:10px 14px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);border-radius:var(--radius-sm);font-size:0.83rem;color:#f87171"></div>
  </div>
  <div class="card">
    <div class="card-title">Add Video Performance</div>
    <div class="tracker-add">
      <div class="input-group"><label>Video Title</label><input type="text" id="trackTitle" placeholder="Video title..."></div>
      <div class="input-group"><label>Views</label><input type="number" id="trackViews" placeholder="10000"></div>
      <div class="input-group"><label>Likes</label><input type="number" id="trackLikes" placeholder="500"></div>
      <div class="input-group"><label>CTR %</label><input type="number" id="trackCtr" placeholder="4.2" step="0.1"></div>
      <div class="input-group" style="min-width:auto"><label>&nbsp;</label><button class="btn btn-grad" onclick="addVideo()" style="white-space:nowrap">+ Add</button></div>
    </div>
  </div>
  <div id="trackerData" style="display:none">
    <div class="stat-row" id="statsRow"></div>
    <div class="card" style="padding:0;overflow:hidden">
      <table class="videos-table" id="videosTable">
        <thead><tr><th>Video</th><th>Views</th><th>Likes</th><th>CTR</th><th>Like Rate</th><th></th></tr></thead>
        <tbody id="videosBody"></tbody>
      </table>
    </div>
    <div class="charts-grid">
      <div class="chart-card"><div class="chart-card-title">&#128200; Views per Video</div><canvas id="viewsChart" height="180"></canvas></div>
      <div class="chart-card"><div class="chart-card-title">&#128077; Likes per Video</div><canvas id="likesChart" height="180"></canvas></div>
      <div class="chart-card"><div class="chart-card-title">&#127919; CTR % per Video</div><canvas id="ctrChart" height="180"></canvas></div>
      <div class="chart-card"><div class="chart-card-title">&#10084;&#65039; Like Rate %</div><canvas id="rateChart" height="180"></canvas></div>
    </div>
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
        <div class="card-title" style="margin:0">AI Improvement Suggestions</div>
        <button class="btn btn-grad btn-sm" id="improveBtn" onclick="getImprovement()"><span class="spinner" id="improveSpinner" style="display:none"></span><span>&#129302; Analyze &amp; Suggest</span></button>
      </div>
      <div id="improveSuggestions" class="stream-output" style="display:none"></div>
      <div id="improveEmpty" class="empty-state"><div class="icon">&#129302;</div><p>Click "Analyze &amp; Suggest" to get AI recommendations based on your data</p></div>
    </div>
  </div>
  <div id="trackerEmpty" class="empty-state"><div class="icon">&#128202;</div><p>Add your first video above to start tracking performance</p></div>
</section>
''')

# ── SECTION 8: HOOKS ──────────────────────────────────────────────────────────
w('''
<section class="section" id="sec-hooks">
  <div class="section-header">
    <div class="section-title">&#127908; Hook Tester</div>
    <p class="section-desc">Score 3 hooks on Curiosity, Clarity, Emotion, and Novelty. Declare the winner.</p>
  </div>
  <div class="card">
    <div class="hook-input-grid">
      <div class="hook-input-wrap"><div class="hook-label">Hook 1</div><textarea id="hookInput1" rows="2" placeholder="I quit my 9-5 job with zero savings and built a 6-figure business in 12 months..."></textarea></div>
      <div class="hook-input-wrap"><div class="hook-label">Hook 2</div><textarea id="hookInput2" rows="2" placeholder="Most creators spend 80% of their time on the wrong 20% of tasks..."></textarea></div>
      <div class="hook-input-wrap"><div class="hook-label">Hook 3</div><textarea id="hookInput3" rows="2" placeholder="What if the reason you're not growing has nothing to do with your content?"></textarea></div>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <button class="btn btn-grad" id="hooksBtn" onclick="testHooks()"><span class="spinner" id="hooksSpinner" style="display:none"></span><span>&#127919; Score All Hooks</span></button>
      <button class="btn btn-ghost btn-sm" onclick="fillDemoHooks()">Load Demo Hooks</button>
    </div>
  </div>
  <div class="result-area" id="hooksResult">
    <div class="progress-bar" id="hooksProgress" style="display:none"><div class="progress-fill"></div></div>
    <div class="hook-results-grid" id="hooksGrid"></div>
  </div>
</section>
''')

# ── SECTION 9: VOICEOVER ──────────────────────────────────────────────────────
w('''
<section class="section" id="sec-voiceover">
  <div class="section-header">
    <div class="section-title">&#127897;&#65039; Voiceover Generator</div>
    <p class="section-desc">Free browser-based text-to-speech. No API key needed.</p>
  </div>
  <div class="card">
    <div class="info-box"><span class="info-icon">&#127358;</span><span>Uses your browser's built-in Web Speech API &mdash; completely free, works offline.</span></div>
    <div class="input-group" style="margin-bottom:14px">
      <label style="display:flex;justify-content:space-between">
        <span>Script Text</span>
        <button class="btn btn-ghost btn-sm" onclick="fillFromLastScript()" style="padding:2px 10px;font-size:0.75rem">&#128221; Fill from Last Script</button>
      </label>
      <textarea id="voiceText" rows="6" placeholder="Paste your script here...">What if I told you that one simple change made me go from 200 views per video to 20,000 in less than 60 days? No paid ads, no viral moment, no luck. Just a system.</textarea>
    </div>
    <div class="voice-controls">
      <div class="input-group"><label>Voice</label><select id="voiceSelect"></select></div>
      <div>
        <div class="slider-group"><label>Speed <span id="voiceSpeedVal">1.0</span>x</label><input type="range" id="voiceSpeed" min="0.5" max="2" step="0.1" value="1" oninput="document.getElementById('voiceSpeedVal').textContent=parseFloat(this.value).toFixed(1)"></div>
        <div class="slider-group"><label>Pitch <span id="voicePitchVal">1.0</span></label><input type="range" id="voicePitch" min="0.5" max="2" step="0.1" value="1" oninput="document.getElementById('voicePitchVal').textContent=parseFloat(this.value).toFixed(1)"></div>
      </div>
    </div>
    <div class="vo-play-row">
      <button class="btn btn-grad" onclick="playVoiceover()">&#9654;&#65039; Play</button>
      <button class="btn btn-ghost" onclick="stopVoiceover()">&#9209; Stop</button>
      <button class="btn btn-ghost btn-sm" onclick="pauseVoiceover()">&#9208; Pause</button>
      <span id="voiceStatus" style="font-size:0.8rem;color:var(--text3);margin-left:8px"></span>
    </div>
  </div>
  <div class="premium-box">
    <div class="premium-title">&#11088; ElevenLabs Premium Voices</div>
    <p style="font-size:0.82rem;color:var(--text2);margin-bottom:14px">For ultra-realistic AI voices, use ElevenLabs. Free tier: 10,000 chars/month at elevenlabs.io</p>
    <div class="input-row">
      <div class="input-group"><label>ElevenLabs API Key</label><input type="password" id="elevenLabsKey" placeholder="sk_..."></div>
      <div class="input-group"><label>Voice ID</label><input type="text" id="elevenVoiceId" placeholder="21m00Tcm4TlvDq8ikWAM (Rachel)"></div>
    </div>
    <button class="btn btn-ghost btn-sm" onclick="generateElevenLabs()">Generate with ElevenLabs</button>
    <audio id="elevenAudio" controls style="margin-top:12px;display:none;width:100%"></audio>
  </div>
</section>
''')

# ── SECTION 10: CALENDAR ──────────────────────────────────────────────────────
w('''
<section class="section" id="sec-calendar">
  <div class="section-header">
    <div class="section-title">&#128197; Content Calendar</div>
    <p class="section-desc">Plan your content month by month. Click any day to add items.</p>
  </div>
  <div class="card">
    <div class="cal-legend">
      <div class="cal-legend-item"><div class="cal-legend-dot" style="background:#ef4444"></div>YouTube Long</div>
      <div class="cal-legend-item"><div class="cal-legend-dot" style="background:#f59e0b"></div>YouTube Short</div>
      <div class="cal-legend-item"><div class="cal-legend-dot" style="background:#a78bfa"></div>Instagram Post</div>
      <div class="cal-legend-item"><div class="cal-legend-dot" style="background:#60a5fa"></div>Instagram Reel</div>
    </div>
    <div class="cal-header">
      <button class="btn btn-ghost btn-sm" onclick="calNav(-1)">&#8592; Prev</button>
      <div class="cal-month-title" id="calMonthTitle"></div>
      <button class="btn btn-ghost btn-sm" onclick="calNav(1)">Next &#8594;</button>
    </div>
    <div class="cal-grid" id="calGrid"></div>
  </div>
  <div class="card">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
      <div class="card-title" style="margin:0">Monthly Summary</div>
      <button class="btn btn-ghost btn-sm" onclick="clearCalMonth()">Clear Month</button>
    </div>
    <div id="calSummary" class="stat-row"></div>
  </div>
</section>
''')

# ── SECTION 11: AB THUMB ──────────────────────────────────────────────────────
w('''
<section class="section" id="sec-abthumb">
  <div class="section-header">
    <div class="section-title">&#127374; A/B Thumbnail Tracker</div>
    <p class="section-desc">Upload two thumbnails, log CTR tests, and find the winner</p>
  </div>
  <div class="card">
    <div class="card-title">Upload Thumbnails</div>
    <div class="ab-upload-grid">
      <div>
        <div class="ab-preview-box" id="abPreviewA" onclick="document.getElementById('abFileA').click()">
          <div style="font-size:1.5rem">&#128444;&#65039;</div>
          <div class="ab-preview-label">Click to upload Variant A</div>
          <img id="abImgA" alt="Variant A">
        </div>
        <input type="file" id="abFileA" accept="image/*" style="display:none" onchange="previewAB('A',this)">
        <div style="margin-top:8px"><input type="text" id="abNameA" placeholder="Variant A name (e.g. Red Background)"></div>
      </div>
      <div>
        <div class="ab-preview-box" id="abPreviewB" onclick="document.getElementById('abFileB').click()">
          <div style="font-size:1.5rem">&#128444;&#65039;</div>
          <div class="ab-preview-label">Click to upload Variant B</div>
          <img id="abImgB" alt="Variant B">
        </div>
        <input type="file" id="abFileB" accept="image/*" style="display:none" onchange="previewAB('B',this)">
        <div style="margin-top:8px"><input type="text" id="abNameB" placeholder="Variant B name (e.g. Blue Background)"></div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">Log CTR Test</div>
    <div class="ab-log-form">
      <div class="input-group"><label>Date</label><input type="date" id="abDate"></div>
      <div class="input-group"><label>CTR A %</label><input type="number" id="abCtrA" placeholder="4.2" step="0.1" min="0" max="100"></div>
      <div class="input-group"><label>CTR B %</label><input type="number" id="abCtrB" placeholder="6.8" step="0.1" min="0" max="100"></div>
      <div class="input-group" style="min-width:auto"><label>&nbsp;</label><button class="btn btn-grad" onclick="logABTest()">+ Log</button></div>
    </div>
  </div>
  <div id="abResultsWrap" style="display:none">
    <div class="card" style="padding:0;overflow:hidden">
      <table class="ab-table"><thead><tr><th>Date</th><th>CTR A %</th><th>CTR B %</th><th>Winner</th></tr></thead><tbody id="abTableBody"></tbody></table>
    </div>
    <div id="abWinnerBox" class="card" style="margin-top:0"></div>
    <div class="card"><div class="chart-card-title">&#128200; CTR Over Time</div><canvas id="abChart" height="180"></canvas></div>
  </div>
</section>
''')

# ── SECTION 12: COMPETITOR ────────────────────────────────────────────────────
w('''
<section class="section" id="sec-competitor">
  <div class="section-header">
    <div class="section-title">&#128373;&#65039; Competitor Analysis</div>
    <p class="section-desc">Analyze any YouTube channel &mdash; AI-powered, no API key needed</p>
  </div>
  <div class="card">
    <div class="info-box"><span class="info-icon">&#8505;&#65039;</span><span>No YouTube Data API required. The AI analyzes based on its knowledge of public YouTube content.</span></div>
    <div class="input-group" style="margin-bottom:16px"><label>Channel Handle or URL</label><input type="text" id="competitorInput" placeholder="@mkbhd or https://youtube.com/@mkbhd"></div>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <button class="btn btn-grad" id="competitorBtn" onclick="analyzeCompetitor()"><span class="spinner" id="competitorSpinner" style="display:none"></span><span>&#128269; Analyze Channel</span></button>
      <button class="btn btn-ghost btn-sm" onclick="loadDemoCompetitor()">Load Demo</button>
    </div>
  </div>
  <div class="result-area" id="competitorResult">
    <div class="progress-bar" id="competitorProgress" style="display:none"><div class="progress-fill"></div></div>
    <div class="card">
      <div id="competitorStreamOut" class="stream-output" style="display:none"></div>
      <div id="competitorStructured">
        <div class="competitor-section"><div class="competitor-section-title">&#128197; Posting Frequency</div><div class="freq-box" id="compFreq"></div></div>
        <div class="divider"></div>
        <div class="competitor-section"><div class="competitor-section-title">&#127919; Top Content Formats</div><ul class="competitor-list" id="compFormats"></ul></div>
        <div class="divider"></div>
        <div class="competitor-section"><div class="competitor-section-title">&#128683; Topics They Avoid</div><ul class="competitor-list" id="compGaps"></ul></div>
        <div class="divider"></div>
        <div class="competitor-section"><div class="competitor-section-title">&#11088; Your 5 Opportunities</div><ul class="competitor-list opportunity-list" id="compOpps"></ul></div>
      </div>
    </div>
  </div>
</section>
''')

# ── SECTION 13: NEWSLETTER ────────────────────────────────────────────────────
w('''
<section class="section" id="sec-newsletter">
  <div class="section-header">
    <div class="section-title">&#128231; Newsletter Generator</div>
    <p class="section-desc">Turn a script or topic into a full email newsletter &mdash; streamed live</p>
  </div>
  <div class="card">
    <div class="input-group" style="margin-bottom:16px"><label>Paste Video Script or Topic</label><textarea id="newsletterInput" rows="5" placeholder="Paste your video script here, or describe the topic you want to turn into a newsletter..."></textarea></div>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <button class="btn btn-grad" id="newsletterBtn" onclick="generateNewsletter()"><span class="spinner" id="newsletterSpinner" style="display:none"></span><span>&#128231; Generate Newsletter</span></button>
      <button class="btn btn-ghost btn-sm" onclick="loadDemoNewsletter()">Load Demo</button>
    </div>
  </div>
  <div class="result-area" id="newsletterResult">
    <div class="progress-bar" id="newsletterProgress" style="display:none"><div class="progress-fill"></div></div>
    <div class="card">
      <div style="display:flex;gap:20px;flex-wrap:wrap;margin-bottom:16px">
        <div style="flex:1;min-width:200px"><div class="copy-label" style="margin-bottom:6px">Subject Line</div><div class="caption-box" id="newsletterSubject" style="padding:10px 14px;font-size:0.9rem;font-weight:600;color:var(--text)"></div></div>
        <div style="flex:1;min-width:200px"><div class="copy-label" style="margin-bottom:6px">Preview Text</div><div class="caption-box" id="newsletterPreview" style="padding:10px 14px;font-size:0.85rem"></div></div>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
        <div class="copy-label">HTML Preview</div>
        <div style="display:flex;gap:8px">
          <button class="btn btn-ghost btn-sm" onclick="copyNewsletterHTML()">&#128203; Copy HTML</button>
          <button class="btn btn-ghost btn-sm" onclick="copyNewsletterPlain()">&#128196; Copy Plain Text</button>
        </div>
      </div>
      <div id="newsletterStreamOut" class="stream-output" style="display:none;margin-bottom:16px"></div>
      <div class="newsletter-preview" id="newsletterBody"></div>
    </div>
  </div>
</section>
''')

# ── SECTION 14: EXPORT ────────────────────────────────────────────────────────
w('''
<section class="section" id="sec-export">
  <div class="section-header">
    <div class="section-title">&#128228; Export Center</div>
    <p class="section-desc">Export your data as CSV, JSON, or Notion-ready markdown. All client-side.</p>
  </div>
  <div class="card">
    <div class="card-title">Export Data</div>
    <div class="export-grid">
      <div class="export-card"><div class="export-icon">&#128161;</div><div class="export-title">Ideas &#8594; CSV</div><div class="export-desc">Export all generated ideas with title, hook, format, and why columns</div><button class="btn btn-ghost btn-sm" onclick="exportIdeasCSV()">&#11015;&#65039; Download CSV</button></div>
      <div class="export-card"><div class="export-icon">&#128202;</div><div class="export-title">Performance Data &#8594; CSV</div><div class="export-desc">Export all tracked videos with views, likes, CTR, and like rate</div><button class="btn btn-ghost btn-sm" onclick="exportPerformanceCSV()">&#11015;&#65039; Download CSV</button></div>
      <div class="export-card"><div class="export-icon">&#128197;</div><div class="export-title">Content Calendar &#8594; JSON</div><div class="export-desc">Export your full content calendar with all items and dates</div><button class="btn btn-ghost btn-sm" onclick="exportCalendarJSON()">&#11015;&#65039; Download JSON</button></div>
      <div class="export-card"><div class="export-icon">&#127374;</div><div class="export-title">A/B Test History &#8594; CSV</div><div class="export-desc">Export all A/B thumbnail test results with dates and CTR data</div><button class="btn btn-ghost btn-sm" onclick="exportABCSV()">&#11015;&#65039; Download CSV</button></div>
      <div class="export-card"><div class="export-icon">&#128190;</div><div class="export-title">Full Backup &#8594; JSON</div><div class="export-desc">Download everything in localStorage as a single JSON backup file</div><button class="btn btn-grad btn-sm" onclick="exportFullBackup()">&#11015;&#65039; Download Backup</button></div>
      <div class="export-card"><div class="export-icon">&#128229;</div><div class="export-title">Import Backup</div><div class="export-desc">Restore data from a previously exported backup JSON file</div><input type="file" id="importFile" accept=".json" style="display:none" onchange="importBackup(this)"><button class="btn btn-ghost btn-sm" onclick="document.getElementById('importFile').click()">&#128194; Choose File</button></div>
    </div>
  </div>
  <div class="divider"></div>
  <div class="card">
    <div class="card-title">Notion Export</div>
    <p style="font-size:0.85rem;color:var(--text2);margin-bottom:16px">Generate a formatted Markdown document ready to paste directly into Notion.</p>
    <button class="btn btn-grad" onclick="exportNotion()">&#128203; Copy Notion Markdown</button>
    <div id="notionPreview" class="notion-export-box" style="margin-top:16px;display:none"></div>
  </div>
  <div class="card">
    <div class="card-title">Google Sheets</div>
    <p style="font-size:0.85rem;color:var(--text2);margin-bottom:16px">Export performance data as a CSV you can import directly into Google Sheets.</p>
    <button class="btn btn-ghost" onclick="exportSheetsCSV()">&#11015;&#65039; Download Sheets CSV</button>
    <div class="sheets-instructions" style="margin-top:16px">
      <div style="font-family:'Bricolage Grotesque',sans-serif;font-size:0.85rem;font-weight:700;color:#34d399;margin-bottom:10px">How to import into Google Sheets</div>
      <ol><li>Click "Download Sheets CSV" above</li><li>Open <strong>sheets.google.com</strong> and create a new spreadsheet</li><li>Go to <strong>File &#8594; Import</strong></li><li>Click <strong>Upload</strong> and select the CSV</li><li>Click <strong>Import data</strong></li></ol>
    </div>
  </div>
</section>
''')

# ── SECTION 15: EXTENSION ─────────────────────────────────────────────────────
w('''
<section class="section" id="sec-extension">
  <div class="section-header">
    <div class="section-title">&#129513; Chrome Extension</div>
    <p class="section-desc">Analyze any YouTube video from your browser and get instant content ideas</p>
  </div>
  <div class="card">
    <div class="card-title">What the Extension Does</div>
    <p style="font-size:0.86rem;color:var(--text2);line-height:1.7;margin-bottom:16px">When you're on any YouTube video page, the extension adds a floating <strong style="color:var(--purple)">"Analyze"</strong> button. Click it and get instant Shorts scripts, hashtags, and hook ideas.</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-bottom:16px">
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px;text-align:center"><div style="font-size:1.4rem;margin-bottom:6px">&#128220;</div><div style="font-size:0.82rem;font-weight:600;color:var(--text)">Short Scripts</div><div style="font-size:0.74rem;color:var(--text3);margin-top:4px">3 ready-to-film short-form ideas</div></div>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px;text-align:center"><div style="font-size:1.4rem;margin-bottom:6px">&#127991;&#65039;</div><div style="font-size:0.82rem;font-weight:600;color:var(--text)">Hashtags</div><div style="font-size:0.74rem;color:var(--text3);margin-top:4px">10 relevant hashtags</div></div>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px;text-align:center"><div style="font-size:1.4rem;margin-bottom:6px">&#127908;</div><div style="font-size:0.82rem;font-weight:600;color:var(--text)">Hook Ideas</div><div style="font-size:0.74rem;color:var(--text3);margin-top:4px">3 hook variations</div></div>
    </div>
    <div class="ext-preview">Requires Creator Hub server running at localhost:3000.</div>
  </div>
  <div class="card">
    <div class="card-title">Installation Instructions</div>
    <div class="ext-step"><div class="ext-step-num">1</div><div class="ext-step-text"><div class="ext-step-title">Find the extension files</div><div class="ext-step-desc">The extension files are in your Creator Hub folder at: <code style="font-family:'Fira Code',monospace;color:var(--purple);font-size:0.8rem">chrome-extension/</code></div></div></div>
    <div class="ext-step"><div class="ext-step-num">2</div><div class="ext-step-text"><div class="ext-step-title">Open Chrome Extensions</div><div class="ext-step-desc">Navigate to <code style="font-family:'Fira Code',monospace;color:var(--purple);font-size:0.8rem">chrome://extensions</code></div></div></div>
    <div class="ext-step"><div class="ext-step-num">3</div><div class="ext-step-text"><div class="ext-step-title">Enable Developer Mode</div><div class="ext-step-desc">Toggle <strong>"Developer mode"</strong> in the top-right corner</div></div></div>
    <div class="ext-step"><div class="ext-step-num">4</div><div class="ext-step-text"><div class="ext-step-title">Load Unpacked</div><div class="ext-step-desc">Click <strong>"Load unpacked"</strong> and select the <code style="font-family:'Fira Code',monospace;color:var(--purple);font-size:0.8rem">chrome-extension/</code> folder</div></div></div>
    <div class="ext-step"><div class="ext-step-num">5</div><div class="ext-step-text"><div class="ext-step-title">Use it on YouTube</div><div class="ext-step-desc">Go to any YouTube video page. You'll see a purple <strong>"Analyze"</strong> button floating at the bottom-right.</div></div></div>
  </div>
  <div class="card">
    <div class="card-title">Extension Files</div>
    <div class="ext-file-list">
      <div class="ext-file"><div class="ext-file-name">manifest.json</div><div class="ext-file-desc">Extension configuration, permissions, and metadata</div></div>
      <div class="ext-file"><div class="ext-file-name">popup.html</div><div class="ext-file-desc">The popup UI shown when clicking the extension icon</div></div>
      <div class="ext-file"><div class="ext-file-name">popup.js</div><div class="ext-file-desc">Handles popup logic and communication with content script</div></div>
      <div class="ext-file"><div class="ext-file-name">content.js</div><div class="ext-file-desc">Injected into YouTube pages &mdash; reads video title, shows floating button</div></div>
    </div>
  </div>
</section>
</main>
</div>
''')

out.close()
print('HTML structure done, size:', os.path.getsize(r'C:\Users\HP\Desktop\Content Creaction\public\index.html'))
