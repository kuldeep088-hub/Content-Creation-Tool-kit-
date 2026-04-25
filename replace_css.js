const fs = require('fs');
let html = fs.readFileSync('public/index.html', 'utf8');

// Find markers
const start = html.indexOf('/* MODAL */');
const styleClose = html.indexOf('</style>');

if (start === -1 || styleClose === -1) {
  console.error('Markers not found. start:', start, 'styleClose:', styleClose);
  process.exit(1);
}

const newCSS = `/* keyframes */
@keyframes spin{to{transform:rotate(360deg);}}
@keyframes blink{50%{opacity:0;}}
@keyframes progressPulse{0%,100%{opacity:1}50%{opacity:0.5}}
@keyframes toastIn{from{opacity:0;transform:translateX(20px);}to{opacity:1;transform:translateX(0);}}
@keyframes toastOut{from{opacity:1;}to{opacity:0;transform:translateX(20px);}}
@keyframes sectionIn{from{opacity:0;transform:translateY(16px);}to{opacity:1;transform:translateY(0);}}
@keyframes blobDrift{0%,100%{transform:translate(0,0) scale(1);}30%{transform:translate(-40px,30px) scale(1.08);}60%{transform:translate(25px,-35px) scale(0.93);}80%{transform:translate(-15px,10px) scale(1.03);}}
@keyframes fadeSlideUp{from{opacity:0;transform:translateY(28px);}to{opacity:1;transform:translateY(0);}}
@keyframes glitchShift{0%,85%,100%{text-shadow:none;transform:none;}86%{text-shadow:-3px 0 #06ceff,3px 0 #f72585;transform:skewX(-1deg);}88%{text-shadow:3px 0 #06ceff,-3px 0 #f72585;transform:skewX(1deg);}90%{text-shadow:none;transform:none;}}
@keyframes pulseDot{0%,100%{box-shadow:0 0 0 0 rgba(12,187,135,0.6);}50%{box-shadow:0 0 0 6px rgba(12,187,135,0);}}

/* modal */
#apiModal{position:fixed;inset:0;z-index:1000;background:rgba(4,4,12,0.96);display:flex;align-items:center;justify-content:center;backdrop-filter:blur(12px);}
#apiModal.hidden{display:none;}
.modal-box{background:var(--card);border:1px solid var(--border2);border-radius:20px;padding:48px;width:480px;max-width:95vw;text-align:center;box-shadow:0 40px 80px rgba(168,85,247,0.2);}
.modal-logo{font-family:"Syne",sans-serif;font-size:2rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;}
.modal-sub{color:var(--text2);font-size:0.9rem;margin-bottom:32px;line-height:1.6;}
.modal-box input{width:100%;background:var(--surface);border:1px solid var(--border2);border-radius:var(--radius-sm);padding:14px 16px;color:var(--text);font-family:"JetBrains Mono",monospace;font-size:0.85rem;outline:none;margin-bottom:16px;transition:border-color 0.2s,box-shadow 0.2s;}
.modal-box input:focus{border-color:var(--purple);box-shadow:0 0 0 3px rgba(168,85,247,0.15);}
.modal-hint{color:var(--text3);font-size:0.78rem;margin-top:12px;}
.modal-hint a{color:var(--purple);text-decoration:none;}

/* layout */
.app{display:flex;min-height:100vh;}

/* sidebar */
.sidebar{width:var(--sidebar);background:linear-gradient(180deg,#07071e 0%,#04040c 100%);border-right:1px solid rgba(168,85,247,0.12);display:flex;flex-direction:column;position:fixed;top:0;left:0;bottom:0;z-index:100;overflow-y:auto;}
.sidebar-logo{padding:20px 16px;border-bottom:1px solid rgba(168,85,247,0.1);}
.logo-wrap{display:flex;align-items:center;gap:12px;}
.logo-icon{width:36px;height:36px;background:var(--grad);border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 0 20px rgba(168,85,247,0.4);}
.logo-text{font-family:"Syne",sans-serif;font-size:1.2rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;display:block;animation:glitchShift 9s ease-in-out infinite;}
.logo-sub{font-size:0.64rem;color:var(--text3);margin-top:1px;letter-spacing:0.04em;}
.nav-section{padding:8px 8px;flex:1;}
.nav-label{font-size:0.58rem;font-weight:700;color:var(--text3);letter-spacing:0.14em;text-transform:uppercase;padding:0 10px;margin:14px 0 4px;}
.nav-label:first-child{margin-top:6px;}
.nav-item{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:var(--radius-sm);cursor:pointer;transition:all 0.18s;margin-bottom:1px;color:var(--text2);font-size:0.82rem;font-weight:500;position:relative;overflow:hidden;}
.nav-item::before{content:'';position:absolute;left:0;top:0;bottom:0;width:0;background:var(--grad);border-radius:0 2px 2px 0;transition:width 0.18s;}
.nav-item:hover{background:rgba(168,85,247,0.07);color:var(--text);padding-left:14px;}
.nav-item.active{background:rgba(168,85,247,0.13);color:var(--purple);}
.nav-item.active::before{width:3px;}
.nav-item .icon{font-size:0.92rem;width:18px;text-align:center;flex-shrink:0;}
.nav-arrow{margin-left:auto;opacity:0;font-size:0.62rem;transition:opacity 0.15s;color:var(--purple);}
.nav-item:hover .nav-arrow,.nav-item.active .nav-arrow{opacity:1;}
.sidebar-footer{padding:12px 12px 14px;border-top:1px solid rgba(168,85,247,0.1);}
.api-badge{display:flex;align-items:center;gap:8px;padding:9px 11px;border-radius:var(--radius-sm);background:rgba(168,85,247,0.05);border:1px solid rgba(168,85,247,0.15);font-size:0.74rem;cursor:pointer;transition:all 0.2s;margin-bottom:10px;}
.api-badge:hover{background:rgba(168,85,247,0.1);border-color:rgba(168,85,247,0.3);}
.api-dot{width:7px;height:7px;border-radius:50%;background:var(--text3);flex-shrink:0;}
.api-dot.ok{background:var(--green);animation:pulseDot 2s infinite;}
.api-badge-text{color:var(--text2);flex:1;}
.lang-pill{display:inline-flex;align-items:center;background:rgba(168,85,247,0.15);border:1px solid rgba(168,85,247,0.3);border-radius:20px;padding:2px 8px;font-size:0.65rem;font-weight:700;color:var(--purple);}
.lang-select-wrap label{font-size:0.62rem;color:var(--text3);display:block;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.08em;}
.version-tag{font-size:0.6rem;color:var(--text3);text-align:center;margin-top:8px;opacity:0.5;font-family:"JetBrains Mono",monospace;}

/* main */
.main{margin-left:var(--sidebar);flex:1;min-height:100vh;}
.section{display:none;padding:32px 36px;max-width:1080px;animation:sectionIn 0.35s cubic-bezier(0.16,1,0.3,1);}
.section.active{display:block;}
.section-header{margin-bottom:28px;}
.section-title{font-family:"Syne",sans-serif;font-size:1.9rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:6px;line-height:1.2;}
.section-desc{color:var(--text2);font-size:0.88rem;line-height:1.6;}

/* home section */
#sec-home{padding:0;max-width:none;position:relative;min-height:100vh;overflow:hidden;}
.home-bg{position:absolute;inset:0;pointer-events:none;overflow:hidden;}
.home-blob{position:absolute;border-radius:50%;filter:blur(80px);opacity:0.18;}
.home-blob-1{width:600px;height:600px;background:radial-gradient(circle,#a855f7,transparent);top:-10%;left:-5%;animation:blobDrift 18s ease-in-out infinite;}
.home-blob-2{width:500px;height:500px;background:radial-gradient(circle,#06ceff,transparent);bottom:-5%;right:-5%;animation:blobDrift 22s ease-in-out infinite reverse;}
.home-blob-3{width:400px;height:400px;background:radial-gradient(circle,#f72585,transparent);top:40%;left:35%;animation:blobDrift 15s ease-in-out infinite 3s;}
.home-grid-bg{position:absolute;inset:0;background-image:linear-gradient(rgba(168,85,247,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(168,85,247,0.04) 1px,transparent 1px);background-size:56px 56px;}
.home-content{position:relative;z-index:2;padding:60px 52px 40px;}
.home-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.3);border-radius:100px;padding:6px 16px;font-size:0.76rem;font-weight:600;color:var(--purple);margin-bottom:28px;animation:fadeSlideUp 0.6s ease both;}
.home-badge-dot{width:6px;height:6px;background:var(--green);border-radius:50%;animation:pulseDot 2s infinite;}
.home-title{font-family:"Syne",sans-serif;font-size:clamp(2.4rem,5vw,4rem);font-weight:800;line-height:1.08;margin-bottom:20px;animation:fadeSlideUp 0.6s ease 0.1s both;}
.home-title-line1{display:block;color:var(--text);}
.home-title-line2{display:block;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-size:200% auto;animation:fadeSlideUp 0.6s ease 0.15s both, glitchShift 10s ease-in-out 2s infinite;}
.home-sub{font-size:1.05rem;color:var(--text2);max-width:520px;line-height:1.7;margin-bottom:36px;animation:fadeSlideUp 0.6s ease 0.2s both;font-weight:300;}
.home-stats{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:52px;animation:fadeSlideUp 0.6s ease 0.3s both;}
.home-stat-pill{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,0.04);border:1px solid var(--border2);border-radius:100px;padding:8px 18px;font-size:0.82rem;font-weight:600;color:var(--text2);transition:all 0.2s;}
.home-stat-pill:hover{border-color:rgba(168,85,247,0.4);color:var(--text);background:rgba(168,85,247,0.07);}
.home-stat-pill .sp-icon{font-size:1rem;}
.tools-label{font-family:"Syne",sans-serif;font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.14em;color:var(--text3);margin-bottom:18px;animation:fadeSlideUp 0.6s ease 0.35s both;}
.tools-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;animation:fadeSlideUp 0.7s ease 0.4s both;}
@media(max-width:1100px){.tools-grid{grid-template-columns:repeat(3,1fr);}}
@media(max-width:750px){.tools-grid{grid-template-columns:repeat(2,1fr);}}
.tool-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px 18px;cursor:pointer;transition:all 0.25s;display:flex;flex-direction:column;gap:10px;position:relative;overflow:hidden;}
.tool-card::before{content:'';position:absolute;inset:0;opacity:0;transition:opacity 0.25s;border-radius:inherit;}
.tool-card:hover{transform:translateY(-4px);border-color:rgba(168,85,247,0.4);box-shadow:0 16px 40px rgba(4,4,12,0.7),var(--glow);}
.tool-card:hover::before{opacity:1;background:linear-gradient(135deg,rgba(168,85,247,0.04),rgba(6,206,255,0.02));}
.tool-card:nth-child(3n+1):hover{box-shadow:0 16px 40px rgba(4,4,12,0.7),0 0 30px rgba(168,85,247,0.2);}
.tool-card:nth-child(3n+2):hover{box-shadow:0 16px 40px rgba(4,4,12,0.7),0 0 30px rgba(6,206,255,0.15);}
.tool-card:nth-child(3n):hover{box-shadow:0 16px 40px rgba(4,4,12,0.7),0 0 30px rgba(247,37,133,0.15);}
.tool-icon-wrap{width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;flex-shrink:0;}
.tc-purple .tool-icon-wrap{background:rgba(168,85,247,0.15);}
.tc-cyan .tool-icon-wrap{background:rgba(6,206,255,0.12);}
.tc-pink .tool-icon-wrap{background:rgba(247,37,133,0.12);}
.tc-green .tool-icon-wrap{background:rgba(12,187,135,0.12);}
.tc-amber .tool-icon-wrap{background:rgba(245,158,11,0.12);}
.tc-blue .tool-icon-wrap{background:rgba(59,130,246,0.12);}
.tool-name{font-family:"Syne",sans-serif;font-size:0.9rem;font-weight:700;color:var(--text);line-height:1.3;}
.tool-desc{font-size:0.74rem;color:var(--text3);line-height:1.4;}
.tool-arrow{position:absolute;top:16px;right:16px;color:var(--text3);font-size:0.7rem;opacity:0;transition:all 0.2s;transform:translateX(-4px);}
.tool-card:hover .tool-arrow{opacity:1;transform:translateX(0);color:var(--purple);}

/* demo banner */
#demoBanner{display:none;align-items:center;justify-content:space-between;background:rgba(245,158,11,0.07);border-bottom:1px solid rgba(245,158,11,0.18);padding:10px 36px;font-size:0.82rem;color:var(--amber);gap:12px;flex-wrap:wrap;}
#demoBanner a{color:var(--amber);font-weight:600;cursor:pointer;text-decoration:underline;}

/* toast */
#toastContainer{position:fixed;bottom:24px;right:24px;z-index:9999;display:flex;flex-direction:column;gap:8px;pointer-events:none;}
.toast-item{background:var(--card2);border:1px solid var(--border2);border-radius:var(--radius-sm);padding:12px 16px;font-size:0.83rem;color:var(--text);box-shadow:var(--shadow-lg);display:flex;align-items:center;gap:10px;animation:toastIn 0.25s ease;min-width:240px;pointer-events:all;}
.toast-out{animation:toastOut 0.3s ease forwards;}

/* cards */
.card{background:var(--card);border:1px solid var(--border);border-top:1px solid rgba(168,85,247,0.15);border-radius:var(--radius);padding:24px;margin-bottom:20px;transition:border-color 0.25s,box-shadow 0.25s;}
.card:hover{border-color:rgba(168,85,247,0.3);box-shadow:var(--shadow),var(--glow);}
.card-title{font-family:"Syne",sans-serif;font-size:0.78rem;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;}

/* inputs */
.input-row{display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap;}
.input-group{flex:1;min-width:180px;}
.input-group label{display:block;font-size:0.76rem;font-weight:600;color:var(--text2);margin-bottom:6px;}
input[type=text],input[type=number],input[type=url],input[type=email],input[type=password],textarea,select{width:100%;background:var(--surface);border:1px solid var(--border2);border-radius:var(--radius-sm);padding:10px 13px;color:var(--text);font-family:"Outfit",sans-serif;font-size:0.87rem;outline:none;transition:border-color 0.2s,box-shadow 0.2s;appearance:none;}
input:focus,textarea:focus,select:focus{border-color:var(--purple);box-shadow:0 0 0 3px rgba(168,85,247,0.12);}
input::placeholder,textarea::placeholder{color:var(--text3);}
textarea{resize:vertical;min-height:80px;line-height:1.6;}
select{cursor:pointer;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%23363b68' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 12px center;padding-right:36px;}
input[type=range]{width:100%;accent-color:var(--purple);cursor:pointer;padding:0;}
input[type=color]{width:100%;height:40px;border-radius:var(--radius-sm);border:1px solid var(--border2);background:var(--surface);cursor:pointer;padding:3px;}
input[type=file]{padding:10px;cursor:pointer;}

/* buttons */
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 20px;border-radius:var(--radius-sm);font-family:"Outfit",sans-serif;font-size:0.87rem;font-weight:600;cursor:pointer;transition:all 0.2s;border:none;}
.btn-grad{background:var(--grad);color:#fff;box-shadow:0 4px 20px rgba(168,85,247,0.35);}
.btn-grad:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(168,85,247,0.5);}
.btn-grad:active{transform:translateY(0);}
.btn-ghost{background:transparent;color:var(--text2);border:1px solid var(--border2);}
.btn-ghost:hover{background:rgba(255,255,255,0.04);color:var(--text);}
.btn-green{background:linear-gradient(135deg,#0cbb87,#06ceff);color:#fff;}
.btn-green:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(6,206,255,0.3);}
.btn-primary{display:inline-flex;align-items:center;gap:8px;background:var(--grad);color:#fff;border:none;border-radius:var(--radius-sm);padding:13px 28px;font-family:"Outfit",sans-serif;font-size:0.95rem;font-weight:600;cursor:pointer;transition:all 0.2s;width:100%;justify-content:center;box-shadow:0 4px 20px rgba(168,85,247,0.3);}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(168,85,247,0.45);}
.btn-sm{padding:6px 13px;font-size:0.78rem;}
.btn:disabled{opacity:0.4;cursor:not-allowed;transform:none!important;}
.spinner{display:inline-block;width:15px;height:15px;border:2px solid rgba(255,255,255,0.2);border-top-color:#fff;border-radius:50%;animation:spin 0.7s linear infinite;}

/* result areas */
.result-area{margin-top:20px;display:none;}
.result-area.show{display:block;}
.result-title{font-family:"Syne",sans-serif;font-size:0.76rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:12px;display:flex;align-items:center;gap:8px;}
.result-count{background:rgba(168,85,247,0.15);color:var(--purple);padding:2px 8px;border-radius:10px;font-size:0.68rem;}
.progress-bar{height:2px;background:var(--border);border-radius:2px;overflow:hidden;margin-bottom:14px;}
.progress-fill{height:100%;background:var(--grad);border-radius:2px;animation:progressPulse 1.4s ease-in-out infinite;}
.divider{height:1px;background:var(--border);margin:22px 0;}
.empty-state{text-align:center;padding:46px 22px;color:var(--text3);}
.empty-state .icon{font-size:2.4rem;margin-bottom:11px;}
.empty-state p{font-size:0.86rem;}

/* stream output */
.stream-output{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px;font-family:"JetBrains Mono",monospace;font-size:0.82rem;line-height:1.9;color:var(--text);max-height:580px;overflow-y:auto;position:relative;}
.stream-output h1,.stream-output h2{font-family:"Syne",sans-serif;font-size:1.05rem;font-weight:700;color:var(--purple);margin:20px 0 8px;padding-bottom:6px;border-bottom:1px solid var(--border);}
.stream-output h1:first-child,.stream-output h2:first-child{margin-top:0;}
.stream-output h3{font-family:"Syne",sans-serif;font-size:0.92rem;font-weight:700;color:var(--text);margin:14px 0 6px;}
.stream-output p{margin-bottom:10px;color:var(--text2);font-family:"Outfit",sans-serif;font-size:0.86rem;}
.stream-output strong{color:var(--text);}
.stream-output ul,.stream-output ol{padding-left:20px;margin-bottom:10px;}
.stream-output li{color:var(--text2);margin-bottom:4px;font-family:"Outfit",sans-serif;font-size:0.86rem;}
.stream-output hr{border:none;border-top:1px solid var(--border);margin:16px 0;}
.stream-cursor{display:inline-block;width:2px;height:1.1em;background:var(--purple);margin-left:2px;vertical-align:text-bottom;animation:blink 0.8s step-end infinite;}
.output-wrap{position:relative;}
.copy-float{position:absolute;top:12px;right:12px;opacity:0;transition:opacity 0.2s;z-index:2;}
.output-wrap:hover .copy-float{opacity:1;}

/* ideas */
.ideas-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px;margin-top:4px;}
.idea-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;transition:all 0.25s;}
.idea-card:hover{border-color:rgba(168,85,247,0.4);transform:translateY(-3px);box-shadow:0 12px 36px rgba(4,4,12,0.6),var(--glow);}
.idea-format{display:inline-flex;align-items:center;padding:3px 10px;border-radius:20px;font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;}
.fmt-Tutorial{background:rgba(59,130,246,0.15);color:#60a5fa;border:1px solid rgba(59,130,246,0.25);}
.fmt-Challenge{background:rgba(245,158,11,0.15);color:#fbbf24;border:1px solid rgba(245,158,11,0.25);}
.fmt-Storytime{background:rgba(168,85,247,0.15);color:#c084fc;border:1px solid rgba(168,85,247,0.25);}
.fmt-Listicle{background:rgba(6,206,255,0.15);color:#22d3ee;border:1px solid rgba(6,206,255,0.25);}
.fmt-Vlog,.fmt-default{background:rgba(12,187,135,0.15);color:#34d399;border:1px solid rgba(12,187,135,0.25);}
.fmt-Reaction{background:rgba(247,37,133,0.15);color:#f472b6;border:1px solid rgba(247,37,133,0.25);}
.idea-title{font-family:"Syne",sans-serif;font-size:0.9rem;font-weight:700;color:var(--text);margin-bottom:8px;line-height:1.4;}
.idea-hook{font-size:0.8rem;color:var(--text2);margin-bottom:8px;font-style:italic;line-height:1.5;}
.idea-why{font-size:0.75rem;color:var(--text3);line-height:1.5;}

/* shorts */
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

/* thumbnail */
.thumb-tabs{display:flex;margin-bottom:20px;border:1px solid var(--border2);border-radius:var(--radius-sm);overflow:hidden;width:fit-content;}
.thumb-tab{padding:9px 20px;font-size:0.83rem;font-weight:600;cursor:pointer;background:transparent;color:var(--text2);border:none;font-family:"Outfit",sans-serif;transition:all 0.15s;}
.thumb-tab.active{background:var(--grad);color:#fff;}
.thumb-tab:hover:not(.active){background:rgba(255,255,255,0.04);color:var(--text);}
.thumb-tab-content{display:none;}
.thumb-tab-content.active{display:block;}
.thumb-layout{display:flex;gap:22px;flex-wrap:wrap;}
.thumb-canvas-wrap{flex-shrink:0;}`;

// Keep everything from first </style> onward
const after = html.slice(styleClose);
html = html.slice(0, start) + newCSS + '\n' + after;
fs.writeFileSync('public/index.html', html);
console.log('Done. Length:', html.length);
