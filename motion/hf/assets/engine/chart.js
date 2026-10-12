/* chart.js — cảnh riêng kênh "Biểu Đồ Biết Nói" (theme "chart") cho engine video dài casewide.js.
   Nạp TRƯỚC casewide.js; casewide gọi window.chartScenes({...}). Chỉ đổi cảnh khi C.theme === "chart" -> kênh khác
   không bị ảnh hưởng. Tất định, mọi tween trên timeline tạm dừng (tua được).

   brand : nhận diện kênh ~3 s — bong bóng thoại vàng tự vẽ, 5 cây nến mọc lên + cột khối lượng, đường MA vẽ dần,
           chấm vàng bật sáng; rồi logo lùi sang trái, tên kênh 2 dòng hiện bên phải, dòng phụ gõ chữ.
           Mốc (giây, tính từ t0) khớp sfx_long.py (nhánh brand/chart): BUB 0.0 · CANDLE 0.45+0.12k · MA 0.95 · DOT 1.45 · LOCK 1.6 */
window.chartScenes = ({ B, tl, el, esc, px, common, W, H, C, bg }) => {
  if (C.theme !== "chart") return;
  const BUB = "M248 178 H552 Q636 178 636 262 V452 Q636 536 552 536 H372 L250 630 L276 536 H248 Q164 536 164 452 V262 Q164 178 248 178 Z";
  const MA = "M222 446 C276 420 318 398 360 380 S470 318 512 284 S546 260 564 252";
  // [x tâm, đỉnh râu, đáy râu, đỉnh thân, cao thân, tăng?]
  const CAN = [[249, 384, 478, 402, 56, 0], [313, 336, 452, 356, 78, 1], [377, 330, 404, 346, 40, 0], [441, 276, 392, 296, 76, 1], [505, 214, 338, 232, 88, 1]];
  const VOL = [[232, 500, 36], [296, 486, 50], [360, 506, 30], [424, 480, 56], [488, 468, 68]];
  const svgLogo = () => `
<svg viewBox="0 0 800 800" width="100%" height="100%" style="overflow:visible">
 <defs>
  <linearGradient id="cbGold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff1b8"/><stop offset=".35" stop-color="#fcd34d"/><stop offset=".7" stop-color="#f59e0b"/><stop offset="1" stop-color="#d97706"/></linearGradient>
  <linearGradient id="cbGlass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16263f"/><stop offset="1" stop-color="#0a1322"/></linearGradient>
  <linearGradient id="cbUp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6ee7a0"/><stop offset=".45" stop-color="#22c55e"/><stop offset="1" stop-color="#15803d"/></linearGradient>
  <linearGradient id="cbDn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fca5a5"/><stop offset=".45" stop-color="#ef4444"/><stop offset="1" stop-color="#b91c1c"/></linearGradient>
  <linearGradient id="cbMa" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#e2e8f0" stop-opacity=".85"/><stop offset=".6" stop-color="#fff"/><stop offset="1" stop-color="#fde68a"/></linearGradient>
  <filter id="cbSoft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="16"/></filter>
  <clipPath id="cbIn"><path d="${BUB}"/></clipPath>
 </defs>
 <path class="cbglass" d="${BUB}" fill="url(#cbGlass)" opacity="0"/>
 <g clip-path="url(#cbIn)">
  <g class="cbgrid" stroke="#7dd3fc" stroke-opacity=".10" stroke-width="2" opacity="0"><path d="M164 262 H636 M164 340 H636 M164 418 H636 M260 178 V536 M356 178 V536 M452 178 V536 M548 178 V536"/></g>
  ${VOL.map(([x, y, h]) => `<rect class="cbvol" x="${x}" y="${y}" width="34" height="${h}" fill="#7dd3fc" fill-opacity=".16"/>`).join("")}
 </g>
 <path class="cbglow" d="${BUB}" fill="none" stroke="#fbbf24" stroke-opacity=".55" stroke-width="30" filter="url(#cbSoft)" opacity="0"/>
 <path class="cbbub" d="${BUB}" fill="none" stroke="url(#cbGold)" stroke-width="24" stroke-linejoin="round" stroke-linecap="round"/>
 ${CAN.map(([x, w0, w1, b0, bh, up]) => `<g class="cbc"><line class="cbw" x1="${x}" y1="${w0}" x2="${x}" y2="${w1}" stroke="${up ? "#4ade80" : "#f87171"}" stroke-width="8" stroke-linecap="round"/>
  <rect class="cbb" x="${x - 20}" y="${b0}" width="40" height="${bh}" rx="7" fill="url(#${up ? "cbUp" : "cbDn"})"/></g>`).join("")}
 <path class="cbmaglow" d="${MA}" fill="none" stroke="#fde68a" stroke-opacity=".5" stroke-width="22" stroke-linecap="round" filter="url(#cbSoft)"/>
 <path class="cbma" d="${MA}" fill="none" stroke="url(#cbMa)" stroke-width="11" stroke-linecap="round"/>
 <circle class="cbhalo" cx="564" cy="252" r="30" fill="#fbbf24" fill-opacity=".25"/>
 <circle class="cbdot" cx="564" cy="252" r="16" fill="url(#cbGold)" stroke="#fff7d6" stroke-width="4"/>
</svg>`;
  const drawOn = (node, t, d, ease = "power2.inOut") => { const L = node.getTotalLength(); node.style.strokeDasharray = L; node.style.strokeDashoffset = L;
    tl.to(node, { strokeDashoffset: 0, duration: d, ease }, t); };

  B.brand = (s, d) => {
    el("div", "brbg", null, d);
    const t0 = s.t0, name = (s.name || C.brand || "BIỂU ĐỒ BIẾT NÓI").split(/\s+/), txt = s.sub || "";
    const half = Math.ceil(name.length / 2), l1 = name.slice(0, half).join(" "), l2 = name.slice(half).join(" ");
    const box = el("div", "cblogo", svgLogo(), d), q = (c) => [...box.querySelectorAll(c)];
    const bub = box.querySelector(".cbbub"), ma = box.querySelector(".cbma"), mag = box.querySelector(".cbmaglow");
    tl.set(box, { scale: 1.18 }, 0);
    drawOn(bub, t0 + 0.02, 0.6, "power2.inOut");
    tl.fromTo(q(".cbglass, .cbgrid"), { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, t0 + 0.3);
    tl.fromTo(q(".cbglow"), { opacity: 0 }, { opacity: 1, duration: 0.5, immediateRender: false }, t0 + 0.55);
    q(".cbc").forEach((g, k) => { const t = t0 + 0.45 + 0.12 * k;
      tl.fromTo(g.querySelector(".cbw"), { scaleY: 0, transformOrigin: "50% 50%" }, { scaleY: 1, duration: 0.2, ease: "power2.out", immediateRender: true }, t);
      tl.fromTo(g.querySelector(".cbb"), { scaleY: 0, transformOrigin: "50% 100%" }, { scaleY: 1, duration: 0.26, ease: "back.out(2.2)", immediateRender: true }, t + 0.02); });
    q(".cbvol").forEach((v, k) => tl.fromTo(v, { scaleY: 0, transformOrigin: "50% 100%" }, { scaleY: 1, duration: 0.25, ease: "power2.out", immediateRender: true }, t0 + 0.45 + 0.12 * k));
    drawOn(ma, t0 + 0.95, 0.5); drawOn(mag, t0 + 0.95, 0.5);
    tl.fromTo(q(".cbdot, .cbhalo"), { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.3, ease: "back.out(3)", immediateRender: true }, t0 + 1.45);
    tl.to(q(".cbhalo"), { scale: 1.8, opacity: 0, duration: 0.7, ease: "power2.out" }, t0 + 1.6);
    // khoá chữ: logo lùi trái + thu nhỏ, tên kênh 2 dòng bên phải
    tl.to(box, { x: -400, scale: 0.84, duration: 0.55, ease: "power3.inOut" }, t0 + 1.6);
    const a = el("div", "cbwm", esc(l1), d), b = el("div", "cbwm cbw2", esc(l2), d), rule = el("div", "cbrule", null, d), sub = el("div", "cbsub", "", d);
    [[a, 1.85], [b, 1.98]].forEach(([n, dt]) => tl.fromTo(n, { opacity: 0, y: 40, clipPath: "inset(-40% -5% 100% -5%)" },
      { opacity: 1, y: 0, clipPath: "inset(-40% -5% -30% -5%)", duration: 0.45, ease: "power3.out", immediateRender: false }, t0 + dt));
    tl.fromTo(rule, { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power3.inOut", immediateRender: false }, t0 + 2.15);
    const ch = [...txt], span = Math.min(0.55, 0.03 * ch.length);
    for (let k = 1; k <= ch.length; k++) tl.set(sub, { textContent: ch.slice(0, k).join("") }, t0 + 2.25 + span * (k / ch.length));
    tl.fromTo(d, { scale: 1 }, { scale: 1.025, duration: Math.max(0.5, s.t1 - t0), ease: "none", immediateRender: false }, t0);
  };

  /* candles : biểu đồ nến ngày thật (VN-Index…) + cột khối lượng + đường chỉ báo, dữ liệu do chartdata.py nhúng sẵn.
     {bars:[[t,o,h,l,c,v]…], lines:[{k,n,vals,color?,at?,label?}], title?, from, to, drawAt?, until?,
      marks:[{date, text, at, pos:"above"|"below", tone:"up"|"down"|"gold"}]}
     Nến hiện dần từ trái sang phải (drawAt→until), rồi các đường chỉ báo tự vẽ, rồi các mốc đánh dấu bật lên.
     sfx_long: tick nhẹ theo nhịp hiện nến, whoosh khi đường vẽ, thud khi mốc bật. */
  const SVGNS = "http://www.w3.org/2000/svg";
  const svgEl = (tag, attrs, parent) => { const e = document.createElementNS(SVGNS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); parent.appendChild(e); return e; };
  const nice = (span) => { const raw = span / 5, p = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p; return (m < 1.5 ? 1 : m < 3 ? 2 : m < 7 ? 5 : 10) * p; };
  const fmt = (v) => Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  const LINE_COLORS = ["#fbbf24", "#38bdf8", "#e879f9", "#f97316"];
  B.candles = (s, d) => {
    const bars = s.bars, n = bars.length, L = 150, R = 1740, T = 190, PB = 720, VT = 748, VB = 846;
    let lo = Infinity, hi = -Infinity, vmax = 0;
    bars.forEach((b) => { lo = Math.min(lo, b[3]); hi = Math.max(hi, b[2]); vmax = Math.max(vmax, b[5]); });
    (s.lines || []).forEach((ln) => ln.vals.forEach((v) => { if (v != null) { lo = Math.min(lo, v); hi = Math.max(hi, v); } }));
    const pad = (hi - lo) * 0.08; lo -= pad; hi += pad;
    const y = (v) => PB - (v - lo) / (hi - lo) * (PB - T), slot = (R - L) / n, cw = Math.max(2, slot * 0.64), x = (i) => L + slot * (i + 0.5);
    const g = svgEl("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d);
    const step = nice(hi - lo);
    for (let v = Math.ceil(lo / step) * step; v < hi; v += step) {
      svgEl("line", { x1: L, x2: R, y1: y(v), y2: y(v), stroke: "rgba(148,163,184,.14)", "stroke-width": 1.5 }, g);
      const t = svgEl("text", { x: R + 16, y: y(v) + 9, class: "cdax" }, g); t.textContent = fmt(v); }
    let lastM = "", lastX = -1e9;
    bars.forEach((b, i) => { const m = b[0].slice(0, 7); if (m !== lastM && x(i) - lastX > 130) { lastM = m; lastX = x(i);
      svgEl("line", { x1: x(i), x2: x(i), y1: T, y2: VB, stroke: "rgba(148,163,184,.08)", "stroke-width": 1.5 }, g);
      const t = svgEl("text", { x: x(i), y: VB + 40, class: "cdax", "text-anchor": "middle" }, g); t.textContent = "T" + (+b[0].slice(5, 7)) + "/" + b[0].slice(0, 4); } });
    const a0 = s.drawAt ?? s.t0 + 0.3, a1 = s.until ?? Math.min(s.t1 - 0.6, a0 + Math.max(1.2, n * 0.035));
    bars.forEach((b, i) => { const up = b[4] >= b[1], col = up ? "#22c55e" : "#ef4444", grp = svgEl("g", {}, g);
      svgEl("line", { x1: x(i), x2: x(i), y1: y(b[2]), y2: y(b[3]), stroke: col, "stroke-width": Math.max(1.5, cw * 0.16) }, grp);
      const top = y(Math.max(b[1], b[4])), bh = Math.max(2, Math.abs(y(b[1]) - y(b[4])));
      svgEl("rect", { x: x(i) - cw / 2, y: top, width: cw, height: bh, rx: Math.min(3, cw * 0.2), fill: col }, grp);
      const vh = (VB - VT) * b[5] / vmax;
      svgEl("rect", { x: x(i) - cw / 2, y: VB - vh, width: cw, height: vh, fill: col, "fill-opacity": 0.35 }, grp);
      tl.fromTo(grp, { opacity: 0 }, { opacity: 1, duration: 0.12, immediateRender: true }, a0 + (a1 - a0) * (i / n)); });
    (s.lines || []).forEach((ln, k) => { const col = ln.color || LINE_COLORS[k % LINE_COLORS.length];
      const pts = ln.vals.map((v, i) => (v == null ? null : `${x(i).toFixed(1)},${y(v).toFixed(1)}`)).filter(Boolean);
      if (pts.length < 2) return;
      const p = svgEl("polyline", { points: pts.join(" "), fill: "none", stroke: col, "stroke-width": 5, "stroke-linejoin": "round", "stroke-linecap": "round" }, g);
      const at = ln.at ?? a1 + 0.15 + 0.35 * k, len = p.getTotalLength(); p.style.strokeDasharray = len; p.style.strokeDashoffset = len;
      tl.to(p, { strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }, at);
      const last = ln.vals.length - 1 - [...ln.vals].reverse().findIndex((v) => v != null);
      const lb = svgEl("text", { x: x(last) - 6, y: y(ln.vals[last]) + (k % 2 ? 42 : -16), class: "cdln", fill: col, "text-anchor": "end" }, g);
      lb.textContent = ln.label || `${ln.k.toUpperCase()}${ln.n}`;
      tl.fromTo(lb, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: true }, at + 0.8); });
    (s.marks || []).forEach((mk) => { const i = bars.findIndex((b) => b[0] === mk.date); if (i < 0) return;
      const b = bars[i], above = mk.pos !== "below", py = above ? y(b[2]) - 26 : y(b[3]) + 26;
      const col = mk.tone === "up" ? "#22c55e" : mk.tone === "gold" ? "#fbbf24" : "#ef4444", grp = svgEl("g", {}, g);
      svgEl("circle", { cx: x(i), cy: (y(b[2]) + y(b[3])) / 2, r: Math.max(18, Math.abs(y(b[2]) - y(b[3])) / 2 + 12), fill: "none", stroke: col, "stroke-width": 4 }, grp);
      const lx = Math.min(R - 160, Math.max(L + 160, x(i) + (mk.dx ?? 0))), ly = (above ? py - 40 : py + 40) + (mk.dy ?? 0);
      const wpx = [...mk.text].length * 24 + 44, cy = (y(b[2]) + y(b[3])) / 2;
      svgEl("line", { x1: x(i), y1: cy, x2: lx, y2: ly, stroke: col, "stroke-width": 3, "stroke-dasharray": "6 6" }, grp);
      svgEl("rect", { x: lx - wpx / 2, y: ly - 32, width: wpx, height: 64, rx: 32, fill: "#0a1426", "fill-opacity": 0.92, stroke: col, "stroke-width": 3 }, grp);
      const t = svgEl("text", { x: lx, y: ly + 14, class: "cdmk", fill: col, "text-anchor": "middle" }, grp);
      t.textContent = mk.text;
      tl.fromTo(grp, { opacity: 0, scale: 0.6, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)", immediateRender: true }, mk.at); });
    const hd = el("div", "cdhd", `<b>${esc(s.title || "VN-INDEX · KHUNG NGÀY")}</b><span>${esc(s.range || "")}</span>`, d);
    tl.fromTo(hd, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.35, immediateRender: false }, s.t0 + 0.1);
    el("div", "cdsrc", esc(s.source || "DỮ LIỆU: HOSE · TRUY XUẤT QUA VNSTOCK · MINH HOẠ CÁCH ĐỌC, KHÔNG PHẢI KHUYẾN NGHỊ"), d);
    common(s, d);
  };

  /* race : các kênh tài sản "chạy đua" trên cùng trục % lãi/lỗ kể từ ngày đầu (chartdata.attach_race nhúng dates + vals).
     {dates:[…], series:[{label, color?, vals:[%…], note?}], money?: 20 (triệu mỗi kênh -> nhãn "20 tr → 19,7 tr"),
      title?, range?, drawAt?, until?, source?}
     Các đường cùng vẽ từ trái sang phải (drawAt→until), đầu mỗi đường có chấm + nhãn giá trị chạy theo; hết đường thì
     nhãn cuối đứng lại (xanh = lãi, đỏ = lỗ). sfx_long: whoosh lúc bắt đầu, tick nhẹ theo tháng, thud lúc dừng. */
  const pct = (v) => (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v).toFixed(1).replace(".", ",") + "%";
  // số kiểu Việt: 1.025 tr, 19,7 tr (B1 08/10: "1025 TR" thiếu dấu chấm hàng nghìn)
  const money = (m, v, u = "tr") => {
    const [i, d] = (m * (1 + v / 100)).toFixed(m >= 100 ? 0 : 1).split(".");
    return i.replace(/\B(?=(\d{3})+(?!\d))/g, ".") + (d ? "," + d : "") + " " + u;
  };
  B.race = (s, d) => {
    const n = s.dates.length, L = 170, R = 1500, T = 210, PB = 840;
    let lo = 0, hi = 0;
    s.series.forEach((q) => q.vals.forEach((v) => { lo = Math.min(lo, v); hi = Math.max(hi, v); }));
    const pad = Math.max(2, (hi - lo) * 0.12); lo -= pad; hi += pad;
    const y = (v) => PB - (v - lo) / (hi - lo) * (PB - T), x = (i) => L + (R - L) * i / Math.max(1, n - 1);
    const g = svgEl("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d);
    const step = nice(hi - lo);
    for (let v = Math.ceil(lo / step) * step; v < hi; v += step) {
      svgEl("line", { x1: L, x2: R, y1: y(v), y2: y(v), stroke: Math.abs(v) < 1e-9 ? "rgba(241,245,249,.55)" : "rgba(148,163,184,.14)",
        "stroke-width": Math.abs(v) < 1e-9 ? 3 : 1.5, "stroke-dasharray": Math.abs(v) < 1e-9 ? "10 8" : "" }, g);
      const t = svgEl("text", { x: L - 18, y: y(v) + 9, class: "cdax", "text-anchor": "end" }, g); t.textContent = pct(v); }
    let lastM = "", lastX = -1e9;
    s.dates.forEach((dt, i) => { const m = dt.slice(0, 7); if (m !== lastM && x(i) - lastX > 110) { lastM = m; lastX = x(i);
      const t = svgEl("text", { x: x(i), y: PB + 44, class: "cdax", "text-anchor": "middle" }, g); t.textContent = "T" + (+dt.slice(5, 7)); } });
    const a0 = s.drawAt ?? s.t0 + 0.5, a1 = s.until ?? Math.min(s.t1 - 1, a0 + 4);
    const clip = svgEl("clipPath", { id: "rc" + Math.round(s.t0 * 1000) }, svgEl("defs", {}, g)), cr = svgEl("rect", { x: L - 10, y: 0, width: 0, height: H }, clip);
    tl.fromTo(cr, { attr: { width: 0 } }, { attr: { width: R - L + 20 }, duration: a1 - a0, ease: "none", immediateRender: true }, a0);
    const heads = s.series.map((q, k) => { const col = q.color || LINE_COLORS[k % LINE_COLORS.length];
      const pts = q.vals.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(" ");
      svgEl("polyline", { points: pts, fill: "none", stroke: col, "stroke-width": 6, "stroke-linejoin": "round", "stroke-linecap": "round",
        "clip-path": `url(#${clip.id})` }, g);
      const dot = svgEl("circle", { r: 11, fill: col, stroke: "#0a1426", "stroke-width": 4, cx: x(0), cy: y(q.vals[0]), opacity: 0 }, g);
      const lb = el("div", "rclbl", `<b style="color:${col}">${esc(q.label)}</b><span></span>`, d);
      return { q, dot, lb, span: lb.querySelector("span") }; });
    // nhãn không được đè nhau (cả khi đang chạy): dàn theo thứ tự giá trị tại điểm i, cách nhau ≥ 74px
    const spread = (i) => { const e = heads.map((h) => ({ h, y: y(h.q.vals[i]) })).sort((a, b) => a.y - b.y);
      for (let k = 1; k < e.length; k++) e[k].y = Math.max(e[k].y, e[k - 1].y + 74);
      return new Map(e.map((z) => [z.h, z.y])); };
    const o = { p: 0 };
    const draw = () => { const i = Math.min(n - 1, Math.round(o.p * (n - 1))), ly = spread(i);
      heads.forEach((h) => { const v = h.q.vals[i], yy = ly.get(h);
        h.dot.setAttribute("cx", x(i)); h.dot.setAttribute("cy", y(v));
        h.lb.style.left = px(x(i) + 26); h.lb.style.top = px(yy - 26);
        h.span.textContent = s.money ? `${s.money} ${s.unit || "tr"} → ${money(s.money, v, s.unit || "tr")}` : pct(v);
        h.span.style.color = v > 0.05 ? "#4ade80" : v < -0.05 ? "#f87171" : "#cbd5e1"; }); };
    tl.set(heads.map((h) => h.dot), { opacity: 1 }, a0);
    tl.fromTo(heads.map((h) => h.lb), { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: true }, a0);
    tl.fromTo(o, { p: 0 }, { p: 0.999, duration: a1 - a0, ease: "none", immediateRender: true, onUpdate: draw }, a0);
    tl.to(o, { p: 1, duration: 0.01, onUpdate: draw }, a1);
    tl.add(() => {}, a1 + 0.02); draw();
    const hd = el("div", "cdhd", `<b>${esc(s.title || "100 TRIỆU, CHIA ĐỀU 5 KÊNH")}</b><span>${esc(s.range || "")}</span>`, d);
    tl.fromTo(hd, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.35, immediateRender: false }, s.t0 + 0.1);
    el("div", "cdsrc", esc(s.source || "DỮ LIỆU: HOSE, SJC (QUA VNSTOCK), COINGECKO · TIẾT KIỆM: LÃI ĐƠN GIẢ ĐỊNH · MINH HOẠ, KHÔNG PHẢI KHUYẾN NGHỊ"), d);
    common(s, d);
  };

  /* ---- dùng chung cho breadth + basket: thang màu 9 bậc (chartdata.bucket: -4..-1 giảm, 0 đứng, 1..4 tăng) ---- */
  // thang "board" cho % TRONG NGÀY (breadth base "prev"): bậc -4 (≤ −6,5%, sát sàn −7%) xanh lơ, 0 vàng (tham chiếu), 4 tím (sát trần)
  const BOARD = { "-4": "#22d3ee", "-3": "#ef4444", "-2": "#b3313f", "-1": "#7c2a39", "0": "#fbbf24", "1": "#1c6b4a", "2": "#219659", "3": "#2fc16c", "4": "#c084fc" };
  const HEAT = { "-4": "#ff5f6d", "-3": "#e4424f", "-2": "#b3313f", "-1": "#7c2a39", "0": "#64748b", "1": "#1c6b4a", "2": "#219659", "3": "#2fc16c", "4": "#63f095" };
  const vdate = (iso) => iso.split("-").reverse().join("/");
  const vnum = (v, nd = 1) => v.toFixed(nd).replace(".", ",");
  // chú giải màu (9 ô + nhãn), góc trái-trên tại (x0, y0) trong cột phải của cảnh
  // lgd (tuỳ chọn, từ chartdata khi base "prev"): {title, lo, hi} + pal (bảng màu thay HEAT)
  const heatLegend = (g, at, x0, y0, title, lgd, pal) => {
    const lg = svgEl("g", { opacity: 0 }, g), sw = 48, P = pal || HEAT;
    const tt = svgEl("text", { x: x0, y: y0 - 14, class: "cdlg" }, lg); tt.textContent = (lgd && lgd.title) || title || "% THAY ĐỔI SO VỚI 31/12/2025";
    [-4, -3, -2, -1, 0, 1, 2, 3, 4].forEach((b, k) => svgEl("rect", { x: x0 + k * (sw + 4), y: y0, width: sw, height: 20, rx: 4, fill: P[b] }, lg));
    [[(lgd && lgd.lo) || "≤ −30%", 0, "start"], ["0", 4.5, "middle"], [(lgd && lgd.hi) || "≥ +30%", 9, "end"]].forEach(([t, k, a]) => {
      const e = svgEl("text", { x: x0 + k * (sw + 4) - (a === "end" ? 4 : 0), y: y0 + 48, class: "cdlg", "text-anchor": a }, lg); e.textContent = t; });
    tl.fromTo(lg, { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, at);
  };
  const SRC_HOSE = "DỮ LIỆU: GIÁ ĐÓNG CỬA HOSE (VNSTOCK/VCI) · KÊNH TỰ TÍNH · MINH HOẠ QUÁ KHỨ, KHÔNG PHẢI KHUYẾN NGHỊ";

  /* breadth : lưới ~400 ô vuông, mỗi ô một cổ phiếu HOSE, màu = % thay đổi so với đóng cửa 31/12/2025 tại ngày `date`
     (chartdata.attach_breadth nhúng dots [[pct, bậc]…] đã xếp giảm mạnh nhất -> tăng mạnh nhất, stats, frames?).
     {date?, title?, range?, cols?: 20, drawAt?, until?, countAt?, countSub?: "GIẢM", countNote?, chipAt?, chip?: "VN-INDEX −0,9%",
      medianAt?, medianText?, animate?: {from, to?, every?, at, until}, source?}
     Ô hiện lần lượt theo thứ tự xếp (drawAt→until) nên lưới đọc như bản đồ nhiệt: đỏ đậm trên cùng, xanh dưới cùng.
     countAt: số mã giảm đếm từ 0 lên (0,9 s) · chipAt: thẻ VN-Index · medianAt: vạch vàng chia đôi 400 mã + nhãn trung vị.
     animate: ô đổi màu theo từng phiên (frames) trong [at, until]; ngày, bộ đếm, thẻ VN-Index chạy theo.
     sfx_long: tick theo nhịp ô hiện, tick dày khi đếm + thud lúc dừng, thud ở thẻ, tick mỗi khung ngày. */
  B.breadth = (s, d) => {
    const dots = s.dots, n = dots.length, st = s.stats || {}, fr = s.frames && s.frames.length ? s.frames : null;
    const cols = s.cols || 20, rows = Math.ceil(n / cols), CS = Math.min(34, Math.floor(690 / rows)), DS = CS - 6, GX = 150, GY = 186;
    const g = svgEl("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d);
    svgEl("rect", { x: GX - 16, y: GY - 16, width: cols * CS + 26, height: rows * CS + 26, rx: 20, fill: "rgba(8,16,32,.6)",
      stroke: "rgba(148,163,184,.18)", "stroke-width": 2 }, g);
    const gx = (k) => GX + (k % cols) * CS, gy = (k) => GY + Math.floor(k / cols) * CS;
    const b0 = fr ? fr[0].b : dots.map((q) => q[1]);
    const PAL = s.palette === "board" ? BOARD : HEAT;   // base "prev" (chartdata): màu kiểu bảng giá -- xanh lơ sàn, vàng đứng giá, tím trần
    const R = dots.map((q, k) => svgEl("rect", { x: gx(k), y: gy(k), width: DS, height: DS, rx: Math.round(DS * 0.24), fill: PAL[b0[k]] }, g));
    const a0 = s.drawAt ?? s.t0 + 0.4, a1 = s.until ?? Math.min(s.t1 - 0.8, a0 + 2.4);
    R.forEach((r, k) => tl.fromTo(r, { opacity: 0, scale: 0.2, transformOrigin: "50% 50%" },
      { opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.4)", immediateRender: true }, a0 + (a1 - a0) * (k / n)));
    const RX = GX + cols * CS + 80;
    heatLegend(g, a0, RX, 806, null, s.legend, PAL);
    const hd = el("div", "cdhd", `<b>${esc(s.title || `${n} CỔ PHIẾU HOSE · MỖI Ô MỘT MÃ`)}</b><span>${esc(s.range || vdate(s.date || st.date || ""))}</span>`, d);
    tl.fromTo(hd, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.35, immediateRender: false }, s.t0 + 0.1);
    // ngày đang hiển thị (chỉ khi animate)
    let dl = null;
    if (fr) { dl = el("div", "bddate", vdate(fr[0].d), d); dl.style.left = px(RX); dl.style.top = px(150);
      tl.fromTo(dl, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, a0); }
    // bộ đếm lớn
    let cb = null, cpct = null;
    const below0 = fr ? fr[0].below : st.below, n0 = fr ? fr[0].n : st.n;
    if (s.countAt != null) {
      const note = s.countNote ?? `<span>${vnum(fr ? fr[0].pb ?? 100 * below0 / n0 : st.pct_below)}%</span> · SO VỚI ĐÓNG CỬA 31/12/2025`;
      const cnt = el("div", "bdcnt", `<div class="n"><b>0</b><i> / ${n0}</i></div><div class="s">${esc(s.countSub || "GIẢM")}</div><div class="nt">${s.countNote ? esc(note) : note}</div>`, d);
      cnt.style.left = px(RX); cnt.style.top = px(fr ? 214 : 190);
      cb = cnt.querySelector("b"); cpct = cnt.querySelector(".nt span");
      tl.fromTo(cnt, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out", immediateRender: false }, s.countAt);
      const steps = 27;
      for (let m = 1; m <= steps; m++) { const p = m / steps, e = 1 - Math.pow(1 - p, 2.2);
        tl.set(cb, { textContent: String(Math.round(below0 * e)) }, s.countAt + 0.9 * p); }
    }
    // thẻ VN-Index
    let chipV = null;
    if (s.chipAt != null) {
      const v0 = fr ? fr[0].vni : st.vni;
      const html = s.chip ? esc(s.chip) : `<b>VN-INDEX</b> <span>${pct(v0)}</span>`;
      const chip = el("div", "bdchip", html, d); chip.style.left = px(RX); chip.style.top = px(640);
      chipV = s.chip ? null : chip.querySelector("span");
      if (chipV) chipV.style.color = v0 > 0.05 ? "#4ade80" : v0 < -0.05 ? "#f87171" : "#e2e8f0";
      tl.fromTo(chip, { opacity: 0, scale: 0.7, transformOrigin: "0% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)", immediateRender: false }, s.chipAt);
    }
    // trung vị: vạch vàng giữa hai nửa (n/2 rơi đúng đầu hàng) hoặc vòng quanh ô giữa
    if (s.medianAt != null) {
      const mi = Math.floor(n / 2), txt = s.medianText || `TRUNG VỊ ${st.median < 0 ? "−" : st.median > 0 ? "+" : ""}${vnum(Math.abs(st.median), 2)}%`, mg = svgEl("g", {}, g);
      let ly;
      if (mi % cols === 0) { ly = GY + (mi / cols) * CS - 3;
        const ln = svgEl("line", { x1: GX - 22, x2: RX - 24, y1: ly, y2: ly, stroke: "#fbbf24", "stroke-width": 5, "stroke-linecap": "round", "stroke-dasharray": "14 9" }, mg);
        tl.fromTo(ln, { attr: { x2: GX - 22 } }, { attr: { x2: RX - 24 }, duration: 0.5, ease: "power2.out", immediateRender: true }, s.medianAt);
      } else { ly = gy(mi) + DS / 2;
        const c = svgEl("circle", { cx: gx(mi) + DS / 2, cy: ly, r: DS * 0.95, fill: "none", stroke: "#fbbf24", "stroke-width": 5 }, mg);
        tl.fromTo(c, { opacity: 0, scale: 2, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)", immediateRender: true }, s.medianAt); }
      const ml = el("div", "bdmed", esc(txt), d); ml.style.left = px(RX); ml.style.top = px(ly + 10);
      tl.fromTo(ml, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.35, immediateRender: false }, s.medianAt + 0.3);
    }
    // đổi màu theo ngày
    if (fr) { const an = s.animate || {}, f0 = an.at ?? a1 + 0.4, f1 = an.until ?? Math.min(s.t1 - 0.6, f0 + 4);
      let prev = fr[0].b;
      fr.forEach((f, j) => { if (!j) return; const t = f0 + (f1 - f0) * j / (fr.length - 1);
        f.b.forEach((b, k) => { if (b !== prev[k]) tl.set(R[k], { attr: { fill: PAL[b] } }, t); });
        prev = f.b;
        tl.set(dl, { textContent: vdate(f.d) }, t);
        if (cb) { tl.set(cb, { textContent: String(f.below) }, t); if (cpct) tl.set(cpct, { textContent: vnum(f.pb ?? 100 * f.below / f.n) + "%" }, t); }
        if (chipV) tl.set(chipV, { textContent: pct(f.vni), color: f.vni > 0.05 ? "#4ade80" : f.vni < -0.05 ? "#f87171" : "#e2e8f0" }, t); }); }
    el("div", "cdsrc", esc(s.source || SRC_HOSE), d);
    common(s, d);
  };

  /* basket : treemap vốn hoá HOSE tại ngày `date`, mỗi ô một cổ phiếu (diện tích = giá × số CP niêm yết). Bố cục squarified
     tính sẵn ở chartdata.attach_basket -> rects [[mã, x, y, w, h, tỉ trọng %, % thay đổi, bậc, hạng]…] (mã "*" = ô gom N mã nhỏ).
     {date?, title?, range?, labels?: 10 | ["VIC"…], groupSmall?: 200, groupLabel?, tileInfo?: "share"|"pct"|"both"|"none",
      color?: "plain"|"pct", colorAt?, highlight?: ["VIC","VHM","VRE","VPL"], hlAt?,
      captions?: [{text: "VIC ≈ 21%" | k+v, at, tone?: "gold"|"up"|"down"|"blue", mark?: ["VIC"]|"top10"|"group"}], drawAt?, until?, source?}
     Ô lớn rơi xuống trước, vụn nhỏ sau (drawAt→until) · hlAt: viền vàng các mã highlight, ô khác tối đi · mỗi caption: thẻ
     bên phải + viền màu quanh các ô `mark`. sfx_long: tick theo ô hiện, thud ở hlAt và mỗi caption. */
  const BK_TONE = { gold: "#fbbf24", up: "#4ade80", down: "#f87171", blue: "#38bdf8" };
  const mixHex = (a, b, t) => { const p = (h, i) => parseInt(h.slice(1 + 2 * i, 3 + 2 * i), 16);
    return "#" + [0, 1, 2].map((i) => Math.round(p(a, i) + (p(b, i) - p(a, i)) * t).toString(16).padStart(2, "0")).join(""); };
  B.basket = (s, d) => {
    const rs = s.rects, N = rs.length, st = s.stats || {}, lab = new Set(s.labels || []), info = s.tileInfo || "share";
    const g = svgEl("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d);
    let bx0 = 1e9, by0 = 1e9, bx1 = 0, by1 = 0;
    rs.forEach((r) => { bx0 = Math.min(bx0, r[1]); by0 = Math.min(by0, r[2]); bx1 = Math.max(bx1, r[1] + r[3]); by1 = Math.max(by1, r[2] + r[4]); });
    svgEl("rect", { x: bx0 - 12, y: by0 - 12, width: bx1 - bx0 + 24, height: by1 - by0 + 24, rx: 18, fill: "rgba(8,16,32,.6)",
      stroke: "rgba(148,163,184,.18)", "stroke-width": 2 }, g);
    const tiles = svgEl("g", {}, g), marks = svgEl("g", {}, g);
    const plain = (r) => mixHex("#15274a", "#2f5f96", Math.max(0, Math.min(1, (Math.log10(Math.max(1e-3, r[5])) + 2.5) / 3.9)));
    const pctMode = s.color === "pct", colorAt = s.colorAt;
    const a0 = s.drawAt ?? s.t0 + 0.4, a1 = s.until ?? Math.min(s.t1 - 0.8, a0 + 2.2);
    const T = rs.map((r, k) => {
      const [sym, x, y, w, h] = r, outer = svgEl("g", {}, tiles), inner = svgEl("g", {}, outer), gp = Math.min(1.6, w / 5, h / 5);
      const fill0 = pctMode && colorAt == null ? HEAT[r[7]] : plain(r);
      const rc = svgEl("rect", { x: x + gp, y: y + gp, width: Math.max(0.4, w - 2 * gp), height: Math.max(0.4, h - 2 * gp), rx: Math.min(8, w / 6, h / 6) }, inner);
      rc.style.fill = fill0;
      let sub = null, t1 = null;
      if (lab.has(sym) || sym === "*") {
        const f = Math.max(0, Math.min(92, w * (sym === "*" ? 0.2 : 0.27), h * 0.36)), cx = x + w / 2, cy = y + h / 2;
        if (f >= 15) {
          const showSub = info !== "none" && h > f * 2.3, fs = Math.max(14, Math.round(f * 0.46));
          t1 = svgEl("text", { x: cx, y: cy + f * 0.34 - (showSub ? fs * 0.62 : 0), class: "bkt", "text-anchor": "middle", "font-size": Math.round(f) }, inner);
          t1.textContent = sym === "*" ? `${r[8]} MÃ` : sym;
          if (showSub) {
            sub = svgEl("text", { x: cx, y: cy + f * 0.34 + fs * 0.75, class: "bks", "text-anchor": "middle", "font-size": fs }, inner);
            const share = vnum(r[5], r[5] >= 1 ? 1 : 2) + "%";
            sub.textContent = info === "pct" ? pct(r[6]) : info === "both" ? `${share} · ${pct(r[6])}` : share;
          }
        }
      }
      const t = a0 + (a1 - a0) * Math.pow(k / N, 0.7);
      tl.fromTo(inner, { opacity: 0, scale: 0.86, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.3, ease: "power3.out", immediateRender: true }, t);
      return { r, outer, rc, sub, t1 };
    });
    // tô màu theo % thay đổi (quét từ ô lớn tới ô nhỏ trong 0,7 s)
    if (pctMode) {
      const at = colorAt ?? a0;
      T.forEach((q, k) => { const tk = at + 0.7 * Math.pow(k / N, 0.7), ink = Math.abs(q.r[7]) >= 3 && q.r[7] > 0;
        if (colorAt != null) tl.fromTo(q.rc, { fill: plain(q.r) }, { fill: HEAT[q.r[7]], duration: 0.35, ease: "none", immediateRender: false }, tk);
        if (ink) [q.t1, q.sub].forEach((e) => e && (colorAt != null ? tl.set(e, { fill: "#052e1a", stroke: "rgba(255,255,255,0)" }, tk + 0.2) : Object.assign(e.style, { fill: "#052e1a", stroke: "rgba(255,255,255,0)" })));
        if (colorAt != null && q.sub && info === "pct") tl.fromTo(q.sub, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: true }, tk + 0.2); });
      heatLegend(g, at, 1290, 222);
    }
    const find = (m) => (m === "group" ? T.filter((q) => q.r[0] === "*")
      : typeof m === "string" && /^top\d+$/.test(m) ? T.filter((q) => q.r[0] !== "*" && q.r[8] <= +m.slice(3))
      : T.filter((q) => (Array.isArray(m) ? m : [m]).includes(q.r[0])));
    // viền quanh ô: mỗi lúc chỉ MỘT bộ viền sáng -- bộ mới hiện thì bộ trước mờ đi (thẻ chú thích vẫn đứng)
    const evs = [];
    const outline = (qs, col, at) => { const g2 = svgEl("g", {}, marks);
      qs.forEach((q, j) => { const [, x, y, w, h] = q.r, ins = Math.min(3, w / 4, h / 4), rx = Math.min(8, w / 6, h / 6);
        const box = { x: x + ins, y: y + ins, width: Math.max(1, w - 2 * ins), height: Math.max(1, h - 2 * ins), rx, fill: "none", stroke: col };
        const gl = svgEl("rect", { ...box, "stroke-opacity": 0.35, "stroke-width": 14 }, g2);
        const o = svgEl("rect", { ...box, "stroke-width": 5, "stroke-linejoin": "round" }, g2);
        tl.fromTo([gl, o], { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out", immediateRender: true }, at + 0.04 * Math.min(j, 10)); });
      evs.push({ at, g2 }); };
    if (s.highlight && s.hlAt != null) {
      const hs = new Set(s.highlight), on = T.filter((q) => hs.has(q.r[0]));
      tl.to(T.filter((q) => !hs.has(q.r[0])).map((q) => q.outer), { opacity: 0.32, duration: 0.45, ease: "power2.out" }, s.hlAt);
      outline(on, "#fbbf24", s.hlAt);
    }
    (s.captions || []).forEach((c, i) => {
      let k = c.k, v = c.v;
      if (v == null) { const tx = c.text || "", j = tx.indexOf("≈"); if (j > 0) { k = tx.slice(0, j).trim(); v = tx.slice(j).trim(); } else { v = tx; k = k || ""; } }
      const col = BK_TONE[c.tone || "gold"] || c.tone;
      const cd = el("div", "bkcap", (k ? `<i>${esc(k)}</i>` : "") + `<b>${esc(v)}</b>`, d);
      cd.style.top = px(c.y ?? (pctMode ? 300 : 196) + i * 178); cd.style.setProperty("--c", col);
      tl.fromTo(cd, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.8)", immediateRender: false }, c.at);
      if (c.mark) outline(find(c.mark), col, c.at);
    });
    evs.sort((a, b) => a.at - b.at).forEach((e, i) => { if (i) tl.to(evs[i - 1].g2, { opacity: 0, duration: 0.35, ease: "power1.out" }, e.at); });
    const hd = el("div", "cdhd", `<b>${esc(s.title || "VỐN HOÁ HOSE · MỖI Ô MỘT CỔ PHIẾU")}</b><span>${esc(s.range || vdate(s.date || "") + " · DIỆN TÍCH Ô = VỐN HOÁ")}</span>`, d);
    tl.fromTo(hd, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.35, immediateRender: false }, s.t0 + 0.1);
    el("div", "cdsrc", esc(s.source || SRC_HOSE), d);
    common(s, d);
  };

  /* book : sổ lệnh GIẢ ĐỊNH (dạy cách khớp lệnh) -- không phải sổ lệnh thật của mã nào; luôn có nhãn "VÍ DỤ GIẢ ĐỊNH" (hypo: false để tắt).
     Hai chế độ:
     1) bảng giá — {ref, ceil?, floor?, rows:[{side:"buy"|"sell", price, qty, at?}], prices?:[…], match?:{price, at, text, sub?:{text, at}}}
        Thang giá ở giữa (giảm dần; màu theo tham chiếu: tím trần · vàng tham chiếu · xanh lơ sàn · xanh lá cao hơn · đỏ thấp hơn),
        cột MUA bên trái (thanh xanh mọc sang trái), cột BÁN bên phải (thanh đỏ mọc sang phải), dài theo khối lượng.
        match: khung vàng quanh hàng giá khớp + thẻ chữ dưới bảng (+ dòng phụ).
     2) hàng đợi ở một mức giá — {queue:{price, label?: "GIÁ SÀN", times:["09:00"…], mine?: k, at?, until?, labelAt?, hlAt?,
        eat?:[{at, k}], buy?:{text, at}, head?, mineText?}}
        Mỗi ô một lệnh bán xếp theo giờ đặt (trái = đầu hàng), hiện lần lượt (at→until) · labelAt: dòng "CỘT DƯ BÁN · n LỆNH" ·
        hlAt: ô thứ `mine` viền vàng + nhãn "LỆNH CỦA BẠN" · eat: một lệnh mua (thẻ xanh) đi vào, k ô đầu khớp (loé xanh, biến mất),
        cả hàng dồn lên, số lệnh chờ giảm theo · buy: thẻ xanh nói bên mua có bao nhiêu.
     sfx_long: tick theo từng hàng/ô, thud ở match/eat, tick ở hlAt. */
  const OB_UP = "#4ade80", OB_DN = "#f87171";
  B.book = (s, d) => {
    if (bg) bg(s, d, 0.82);
    const ref = s.ref, pcol = (p) => (p === s.ceil ? "#c084fc" : p === s.floor ? "#22d3ee" : ref == null || p === ref ? "#fbbf24" : p > ref ? OB_UP : OB_DN);
    const hd = el("div", "cdhd", `<b>${esc(s.title || "SỔ LỆNH GIẢ ĐỊNH")}</b><span>${esc(s.range || (ref != null ? "THAM CHIẾU " + fmt(ref) : ""))}</span>`, d);
    tl.fromTo(hd, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.35, immediateRender: false }, s.t0 + 0.1);
    if (s.hypo !== false) { const hy = el("div", "obhypo", esc(s.hypoText || "VÍ DỤ GIẢ ĐỊNH"), d);
      tl.fromTo(hy, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, s.t0 + 0.15); }
    const pop = (n, at, dy = 18) => tl.fromTo(n, { opacity: 0, y: dy }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, at);
    if (s.queue) {
      const q = s.queue, n = q.times.length, x0 = 520, x1 = 1780, slot = (x1 - x0) / n, bw = Math.max(40, slot - 12), BH = 150, LY = 440;
      const qa0 = q.at ?? s.t0 + 0.4, qa1 = q.until ?? qa0 + 1.6;
      const tag = el("div", "obtag", `<i>${esc(q.label || "GIÁ SÀN")}</i><b>${esc(fmt(q.price))}</b>`, d);
      Object.assign(tag.style, { left: px(150), top: px(LY - 6) }); tag.style.setProperty("--c", pcol(q.price));
      pop(tag, s.t0 + 0.2);
      const head = el("div", "obhead", esc(q.head || "← ĐẦU HÀNG: LỆNH ĐẶT SỚM NHẤT"), d); Object.assign(head.style, { left: px(x0 + 120), top: px(LY - 52) });
      pop(head, qa0);
      const boxes = q.times.map((t, k) => { const b = el("div", "obo", `<i>BÁN</i><b>${esc(t)}</b>`, d);
        Object.assign(b.style, { left: px(x0 + slot * k), top: px(LY), width: px(bw), height: px(BH), fontSize: px(Math.min(30, Math.floor(bw / 3.4))) });
        tl.fromTo(b, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.2)", immediateRender: false }, qa0 + (qa1 - qa0) * (k / n));
        return b; });
      // mọi tween dưới đây là fromTo giá trị tường minh: render song song tua tới bất kỳ khung nào vẫn ra đúng hình (tl.to nối tiếp thì không)
      if (q.mine != null && boxes[q.mine]) { const mb = boxes[q.mine], me = el("div", "obme", esc(q.mineText || "▲ LỆNH CỦA BẠN"), mb);
        const ha = q.hlAt ?? qa1 + 0.3;
        tl.fromTo(me, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)", immediateRender: false }, ha);
        tl.fromTo(mb, { borderColor: "rgba(34,211,238,.75)", backgroundColor: "rgba(34,211,238,.14)", boxShadow: "0 0 0px 0px rgba(251,191,36,0)" },
          { borderColor: "#fbbf24", backgroundColor: "rgba(251,191,36,.16)", boxShadow: "0 0 40px 6px rgba(251,191,36,.45)", duration: 0.35, immediateRender: false }, ha);
        tl.fromTo(mb.querySelectorAll("i, b"), { color: "#67e8f9" }, { color: "#fbbf24", duration: 0.35, immediateRender: false }, ha); }
      let cnt = null;
      if (q.labelAt != null) { const c = el("div", "obcnt", `${esc(q.cntText || "CỘT DƯ BÁN")} · <span>${n}</span> LỆNH ĐANG CHỜ`, d);
        Object.assign(c.style, { left: px(x0), top: px(LY + BH + 92) }); cnt = c.querySelector("span"); pop(c, q.labelAt); }
      if (q.buy) { const by = el("div", "obbuy", esc(q.buy.text), d); Object.assign(by.style, { left: px(150), top: px(262) }); pop(by, q.buy.at ?? qa1 + 0.4); }
      let gone = 0; const alive = boxes.slice();
      (q.eat || []).forEach((e) => { const k = Math.min(e.k || 1, alive.length - 1), eaten = alive.splice(0, k), g0 = gone;
        const tok = el("div", "obtok", "MUA", d); Object.assign(tok.style, { left: px(x0 + bw / 2 - 44), top: px(LY - 118) });
        tl.fromTo(tok, { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out", immediateRender: false }, e.at - 0.45);
        tl.fromTo(tok, { y: 0 }, { y: 96, duration: 0.2, ease: "power2.in", immediateRender: false }, e.at - 0.15);
        tl.fromTo(tok, { opacity: 1 }, { opacity: 0, duration: 0.2, immediateRender: false }, e.at + 0.1);
        tl.fromTo(eaten, { backgroundColor: "rgba(34,211,238,.14)", borderColor: "rgba(34,211,238,.75)" },
          { backgroundColor: "rgba(74,222,128,.55)", borderColor: OB_UP, duration: 0.15, immediateRender: false }, e.at);
        tl.fromTo(eaten, { opacity: 1 }, { opacity: 0, duration: 0.3, ease: "power2.in", immediateRender: false }, e.at + 0.3);   // không tween transform: đè x của lần dồn hàng
        gone += k;
        // GSAP đọc mảng đích lúc tween khởi tạo (lần render đầu) -> truyền BẢN SAO, vì `alive` còn bị splice ở lần ăn sau
        tl.fromTo(alive.slice(), { x: -g0 * slot }, { x: -gone * slot, duration: 0.5, ease: "power2.inOut", immediateRender: false }, e.at + 0.6);
        if (cnt) tl.set(cnt, { textContent: String(n - gone) }, e.at + 0.6); });
    } else {
      const rows = s.rows || [], prices = [...new Set([...(s.prices || []), ...rows.map((r) => r.price)])].sort((a, b) => b - a);
      const nR = prices.length, RH = Math.min(118, Math.floor(540 / Math.max(1, nR))), y0 = Math.round(560 - nR * RH / 2), rh = RH - 14;
      const maxQ = Math.max(1, ...rows.map((r) => r.qty || 0)), BL = 820, BR = 1100, LEN = 500;
      [["MUA", BL - 260, OB_UP], ["GIÁ", 960, "#cbd5e1"], ["BÁN", BR + 260, OB_DN]].forEach(([t, cx, c]) => {
        const h = el("div", "obh", esc(t), d); Object.assign(h.style, { left: px(cx - 150), top: px(y0 - 64), color: c }); pop(h, s.t0 + 0.2, 10); });
      const Y = {};
      prices.forEach((p, k) => { const y = y0 + k * RH; Y[p] = y;
        const r = el("div", "obrow", null, d); Object.assign(r.style, { top: px(y), height: px(rh) });
        const pl = el("div", "obp", esc(fmt(p)), d); Object.assign(pl.style, { top: px(y), height: px(rh), lineHeight: px(rh), color: pcol(p), fontSize: px(Math.min(56, Math.round(rh * 0.56))) });
        pop(r, s.t0 + 0.25 + 0.08 * k, 0); pop(pl, s.t0 + 0.25 + 0.08 * k, 0); });
      rows.forEach((r, k) => { const y = Y[r.price], w = Math.max(14, LEN * (r.qty || 0) / maxQ), buy = r.side === "buy", at = r.at ?? s.t0 + 0.5 + 0.12 * k;
        const b = el("div", "obbar " + (buy ? "buy" : "sell"), null, d);
        Object.assign(b.style, { left: px(buy ? BL - w : BR), width: px(w), top: px(y + rh * 0.18), height: px(rh * 0.64) });
        tl.fromTo(b, { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power3.out", immediateRender: true }, at);
        const ql = el("div", "obq", esc(fmt(r.qty)), d);
        Object.assign(ql.style, { left: px(buy ? BL - w - 216 : BR + w + 16), top: px(y), height: px(rh), lineHeight: px(rh), textAlign: buy ? "right" : "left", color: buy ? OB_UP : OB_DN });
        tl.fromTo(ql, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, at + 0.25); });
      if (s.match) { const m = s.match, y = Y[m.price] ?? y0;
        const box = el("div", "obm", null, d); Object.assign(box.style, { top: px(y - 7), height: px(rh + 14) });
        tl.fromTo(box, { opacity: 0, scale: 1.06 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, m.at);
        if (m.text) { const c = el("div", "obchip", esc(m.text), d); c.style.top = px(y0 + nR * RH + 24); pop(c, m.at + 0.15); }
        if (m.sub) { const sb = el("div", "obsub", esc(m.sub.text), d); sb.style.top = px(y0 + nR * RH + 124); pop(sb, m.sub.at ?? m.at + 0.6, 10); } }
    }
    if (!s.srcnote) el("div", "cdsrc", esc(s.source || "VÍ DỤ GIẢ ĐỊNH · MINH HOẠ CÁCH KHỚP LỆNH, KHÔNG PHẢI SỔ LỆNH THẬT CỦA MÃ NÀO"), d);
    common(s, d);
  };
};
