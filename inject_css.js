const fs = require('fs');
let html = fs.readFileSync('public/index.html', 'utf8');
const tag = '</style>';
const idx = html.indexOf(tag);

const missing = `
#thumbCanvas{display:block;border-radius:var(--radius);border:1px solid var(--border2);cursor:crosshair;max-width:100%;}
.thumb-controls{flex:1;min-width:260px;}
.thumb-templates{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:14px;}
.tpl-btn{padding:6px 13px;border-radius:var(--radius-sm);border:1px solid var(--border2);background:var(--surface);color:var(--text2);font-size:0.78rem;cursor:pointer;font-family:'Outfit',sans-serif;transition:all 0.15s;}
.tpl-btn.active{background:rgba(168,85,247,0.15);border-color:var(--purple);color:var(--purple);}
.color-row{display:flex;gap:10px;align-items:flex-end;}
.color-field{flex:1;}
#aiThumbImg{width:100%;border-radius:var(--radius);border:1px solid var(--border2);display:none;margin-top:16px;}
.style-presets{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:14px;}
.preset-btn{padding:5px 13px;border-radius:20px;border:1px solid var(--border2);background:var(--surface);color:var(--text2);font-size:0.76rem;cursor:pointer;transition:all 0.15s;}
.preset-btn.active{background:rgba(168,85,247,0.15);border-color:var(--purple);color:var(--purple);}
.caption-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px;font-size:0.86rem;line-height:1.7;color:var(--text2);white-space:pre-wrap;word-break:break-word;}
.hashtags-wrap{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;}
.hashtag{padding:4px 11px;background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.2);border-radius:20px;font-size:0.76rem;color:var(--purple);cursor:pointer;transition:background 0.15s;}
.hashtag:hover{background:rgba(168,85,247,0.22);}
.copy-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;}
.copy-label{font-size:0.76rem;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:0.07em;}
.title-variants{display:grid;gap:11px;margin-bottom:18px;}
.title-variant{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:15px 18px;display:flex;gap:14px;align-items:flex-start;transition:border-color 0.2s;}
.title-variant:hover{border-color:var(--border2);}
.variant-badge{width:30px;height:30px;background:var(--grad);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.78rem;font-weight:800;color:#fff;flex-shrink:0;margin-top:2px;}
.variant-title{font-weight:600;font-size:0.93rem;color:var(--text);margin-bottom:4px;line-height:1.4;}
.variant-why{font-size:0.78rem;color:var(--text3);}
.seo-desc-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;font-size:0.82rem;line-height:1.7;color:var(--text2);white-space:pre-wrap;max-height:280px;overflow-y:auto;font-family:"JetBrains Mono",monospace;}
.tags-wrap{display:flex;flex-wrap:wrap;gap:6px;}
.seo-tag{padding:4px 11px;background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);border-radius:20px;font-size:0.76rem;color:var(--blue);}
.chapters-list{display:grid;gap:7px;}
.chapter-item{display:flex;gap:11px;align-items:center;padding:7px 11px;background:var(--surface);border-radius:var(--radius-sm);border:1px solid var(--border);}
.chapter-time{font-family:"JetBrains Mono",monospace;font-size:0.76rem;color:var(--purple);font-weight:600;min-width:40px;}
.chapter-title{font-size:0.83rem;color:var(--text2);}
.tracker-add{display:grid;grid-template-columns:2fr 1fr 1fr 1fr auto;gap:10px;align-items:end;margin-bottom:18px;}
.videos-table{width:100%;border-collapse:collapse;font-size:0.83rem;margin-bottom:24px;}
.videos-table th{text-align:left;padding:10px 13px;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:var(--text3);border-bottom:1px solid var(--border);}
.videos-table td{padding:11px 13px;border-bottom:1px solid var(--border);color:var(--text2);}
.videos-table tr:last-child td{border-bottom:none;}
.videos-table tr:hover td{background:rgba(255,255,255,0.015);}
.td-title{color:var(--text);font-weight:500;}
.td-del{color:var(--red);cursor:pointer;opacity:0.5;font-size:0.78rem;}
.td-del:hover{opacity:1;}
.charts-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-bottom:22px;}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:18px;}
.chart-card-title{font-family:"Syne",sans-serif;font-size:0.8rem;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:0.07em;margin-bottom:13px;}
.suggestions-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:22px;font-size:0.86rem;line-height:1.85;color:var(--text2);}
.suggestions-box h2{font-family:"Syne",sans-serif;font-size:0.98rem;font-weight:700;color:var(--purple);margin:16px 0 8px;}
.suggestions-box h2:first-child{margin-top:0;}
.suggestions-box ul{padding-left:18px;}
.suggestions-box li{margin-bottom:5px;}
.suggestions-box strong{color:var(--text);}
.stat-row{display:flex;gap:12px;margin-bottom:18px;flex-wrap:wrap;}
.stat-box{flex:1;min-width:100px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:18px;text-align:center;}
.stat-val{font-family:"Syne",sans-serif;font-size:1.8rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.stat-lbl{font-size:0.72rem;color:var(--text3);margin-top:4px;text-transform:uppercase;letter-spacing:0.07em;}
.hook-input-grid{display:grid;gap:14px;margin-bottom:18px;}
.hook-input-wrap{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px;}
.hook-label{font-size:0.76rem;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:0.09em;margin-bottom:8px;}
.hook-results-grid{display:grid;gap:14px;}
.hook-result-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;transition:border-color 0.2s;}
.hook-result-card.winner{border-color:var(--green);background:rgba(12,187,135,0.04);box-shadow:0 0 20px rgba(12,187,135,0.08);}
.hook-winner-badge{display:inline-flex;align-items:center;gap:6px;background:linear-gradient(135deg,#0cbb87,#059669);color:#fff;border-radius:20px;padding:3px 12px;font-size:0.7rem;font-weight:700;margin-bottom:12px;}
.hook-score-bars{display:grid;gap:9px;margin:13px 0;}
.hook-score-row{display:flex;align-items:center;gap:9px;}
.hook-score-label{font-size:0.73rem;color:var(--text3);min-width:68px;text-transform:capitalize;}
.hook-score-bar-track{flex:1;height:5px;background:var(--border);border-radius:3px;overflow:hidden;}
.hook-score-bar-fill{height:100%;border-radius:3px;background:var(--grad);transition:width 0.8s cubic-bezier(0.4,0,0.2,1);width:0;}
.hook-score-num{font-size:0.76rem;font-weight:700;color:var(--purple);min-width:22px;text-align:right;}
.hook-total{font-family:"Syne",sans-serif;font-size:1.4rem;font-weight:800;color:var(--text);margin-bottom:4px;}
.hook-feedback{font-size:0.8rem;color:var(--text2);line-height:1.6;}
.voice-controls{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px;}
.slider-group{margin-bottom:12px;}
.slider-group label{display:flex;justify-content:space-between;font-size:0.78rem;color:var(--text2);margin-bottom:6px;}
.slider-group label span{color:var(--purple);font-weight:600;}
.vo-play-row{display:flex;gap:9px;flex-wrap:wrap;align-items:center;}
.premium-box{background:rgba(245,158,11,0.05);border:1px solid rgba(245,158,11,0.18);border-radius:var(--radius);padding:18px;margin-top:14px;}
.premium-title{font-family:"Syne",sans-serif;font-size:0.84rem;font-weight:700;color:var(--amber);margin-bottom:10px;display:flex;align-items:center;gap:7px;}
.cal-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;}
.cal-month-title{font-family:"Syne",sans-serif;font-size:1.15rem;font-weight:700;color:var(--text);}
.cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;}
.cal-dow{text-align:center;font-size:0.68rem;font-weight:700;color:var(--text3);text-transform:uppercase;padding:6px 0;}
.cal-day{min-height:76px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:7px;cursor:pointer;transition:all 0.15s;position:relative;}
.cal-day:hover{border-color:rgba(168,85,247,0.35);background:rgba(168,85,247,0.03);}
.cal-day.other-month{opacity:0.3;}
.cal-day.today{border-color:var(--purple);background:rgba(168,85,247,0.05);}
.cal-day-num{font-size:0.76rem;font-weight:600;color:var(--text2);margin-bottom:3px;}
.cal-day.today .cal-day-num{color:var(--purple);}
.cal-item-badge{display:inline-block;width:100%;padding:2px 5px;border-radius:3px;font-size:0.62rem;font-weight:600;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cal-item-badge.yt-long{background:rgba(239,68,68,0.18);color:#f87171;}
.cal-item-badge.yt-short{background:rgba(245,158,11,0.18);color:#fbbf24;}
.cal-item-badge.ig-post{background:rgba(168,85,247,0.18);color:#c084fc;}
.cal-item-badge.ig-reel{background:rgba(59,130,246,0.18);color:#60a5fa;}
.cal-day-count{position:absolute;top:5px;right:5px;background:var(--purple);color:#fff;border-radius:50%;width:14px;height:14px;font-size:0.58rem;font-weight:700;display:flex;align-items:center;justify-content:center;}
.cal-legend{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:14px;}
.cal-legend-item{display:flex;align-items:center;gap:5px;font-size:0.73rem;color:var(--text2);}
.cal-legend-dot{width:9px;height:9px;border-radius:2px;}
#calModal{position:fixed;inset:0;z-index:500;background:rgba(4,4,12,0.85);display:none;align-items:center;justify-content:center;backdrop-filter:blur(4px);}
#calModal.open{display:flex;}
.cal-modal-box{background:var(--card);border:1px solid var(--border2);border-radius:var(--radius);padding:26px;width:420px;max-width:95vw;}
.cal-modal-title{font-family:"Syne",sans-serif;font-size:1rem;font-weight:700;color:var(--text);margin-bottom:18px;}
.cal-type-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:14px;}
.cal-type-btn{padding:9px;border-radius:var(--radius-sm);border:2px solid var(--border2);background:var(--surface);color:var(--text2);font-size:0.8rem;font-weight:600;cursor:pointer;font-family:"Outfit",sans-serif;transition:all 0.15s;text-align:center;}
.cal-type-btn.selected.yt-long{border-color:#ef4444;color:#ef4444;background:rgba(239,68,68,0.08);}
.cal-type-btn.selected.yt-short{border-color:#f59e0b;color:#f59e0b;background:rgba(245,158,11,0.08);}
.cal-type-btn.selected.ig-post{border-color:#c084fc;color:#c084fc;background:rgba(168,85,247,0.08);}
.cal-type-btn.selected.ig-reel{border-color:#60a5fa;color:#60a5fa;background:rgba(59,130,246,0.08);}
.cal-items-list{margin-bottom:14px;}
.cal-existing-item{display:flex;align-items:center;justify-content:space-between;padding:7px 11px;background:var(--surface);border-radius:var(--radius-sm);margin-bottom:5px;border:1px solid var(--border);}
.cal-existing-item .remove-btn{color:var(--red);cursor:pointer;font-size:0.78rem;opacity:0.6;background:none;border:none;}
.ab-upload-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:18px;}
.ab-preview-box{background:var(--surface);border:2px dashed var(--border2);border-radius:var(--radius);padding:18px;text-align:center;transition:border-color 0.2s;cursor:pointer;}
.ab-preview-box:hover{border-color:var(--purple);}
.ab-preview-box img{width:100%;border-radius:var(--radius-sm);margin-top:10px;display:none;}
.ab-preview-label{font-size:0.78rem;color:var(--text3);margin-top:7px;}
.ab-log-form{display:grid;grid-template-columns:auto 1fr 1fr auto;gap:10px;align-items:end;margin-bottom:18px;}
.ab-table{width:100%;border-collapse:collapse;font-size:0.83rem;}
.ab-table th{text-align:left;padding:9px 13px;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:var(--text3);border-bottom:1px solid var(--border);}
.ab-table td{padding:9px 13px;border-bottom:1px solid var(--border);color:var(--text2);}
.winner-pill{background:var(--grad);color:#fff;border-radius:20px;padding:2px 9px;font-size:0.7rem;font-weight:700;}
.competitor-section{margin-bottom:18px;}
.competitor-section-title{font-family:"Syne",sans-serif;font-size:0.82rem;font-weight:700;color:var(--purple);text-transform:uppercase;letter-spacing:0.09em;margin-bottom:10px;display:flex;align-items:center;gap:7px;}
.competitor-list{list-style:none;}
.competitor-list li{padding:9px 13px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);margin-bottom:7px;font-size:0.83rem;color:var(--text2);line-height:1.5;display:flex;gap:9px;}
.competitor-list li::before{content:"→";color:var(--purple);flex-shrink:0;}
.opportunity-list li{border-left:2px solid var(--purple);}
.opportunity-list li::before{content:"★";}
.freq-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px;font-size:0.86rem;color:var(--text2);line-height:1.6;}
.newsletter-preview{background:#fff;border-radius:var(--radius);padding:28px;color:#111;font-family:Georgia,serif;font-size:0.9rem;line-height:1.8;max-height:480px;overflow-y:auto;}
.newsletter-preview h2{font-size:1.05rem;font-weight:700;color:#111;margin:18px 0 9px;padding-bottom:5px;border-bottom:1px solid #e5e5e5;}
.newsletter-preview h2:first-child{margin-top:0;}
.newsletter-preview p{margin-bottom:11px;color:#333;}
.newsletter-preview ul{padding-left:18px;margin-bottom:11px;}
.newsletter-preview li{margin-bottom:5px;color:#333;}
.newsletter-preview strong{color:#111;}
.export-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;}
.export-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;display:flex;flex-direction:column;gap:11px;transition:all 0.2s;}
.export-card:hover{border-color:var(--border2);transform:translateY(-1px);box-shadow:var(--shadow);}
.export-icon{font-size:1.7rem;}
.export-title{font-family:"Syne",sans-serif;font-size:0.88rem;font-weight:700;color:var(--text);}
.export-desc{font-size:0.76rem;color:var(--text3);line-height:1.5;flex:1;}
.notion-export-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;font-family:"JetBrains Mono",monospace;font-size:0.78rem;color:var(--text2);white-space:pre-wrap;max-height:280px;overflow-y:auto;line-height:1.6;}
.sheets-instructions{background:rgba(12,187,135,0.05);border:1px solid rgba(12,187,135,0.18);border-radius:var(--radius);padding:18px;}
.sheets-instructions ol{padding-left:18px;color:var(--text2);font-size:0.83rem;line-height:1.8;}
.ext-step{display:flex;gap:14px;padding:14px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:10px;align-items:flex-start;}
.ext-step-num{width:30px;height:30px;background:var(--grad);border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.82rem;color:#fff;flex-shrink:0;}
.ext-step-text{flex:1;}
.ext-step-title{font-weight:600;font-size:0.88rem;color:var(--text);margin-bottom:3px;}
.ext-step-desc{font-size:0.8rem;color:var(--text2);line-height:1.5;}
.ext-file-list{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px;}
.ext-file{display:flex;align-items:center;gap:9px;padding:7px 0;border-bottom:1px solid var(--border);}
.ext-file:last-child{border-bottom:none;}
.ext-file-name{font-family:"JetBrains Mono",monospace;font-size:0.8rem;color:var(--purple);flex:1;}
.ext-file-desc{font-size:0.76rem;color:var(--text3);}
.ext-preview{background:var(--card);border:1px solid var(--border);border-radius:var(--radius-sm);padding:11px 14px;margin-top:7px;font-size:0.8rem;color:var(--text2);line-height:1.6;font-style:italic;}
.yt-connect-box{background:rgba(239,68,68,0.05);border:1px solid rgba(239,68,68,0.18);border-radius:var(--radius);padding:18px;margin-bottom:18px;}
.yt-connect-title{font-family:"Syne",sans-serif;font-size:0.88rem;font-weight:700;color:#f87171;margin-bottom:13px;display:flex;align-items:center;gap:7px;}
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
  .home-content{padding:30px 20px 30px;}
  .home-title{font-size:2rem;}
  .tools-grid{grid-template-columns:repeat(2,1fr);}
}`;

html = html.slice(0, idx) + missing + '\n' + html.slice(idx);
fs.writeFileSync('public/index.html', html);
console.log('Done. Length:', html.length);
