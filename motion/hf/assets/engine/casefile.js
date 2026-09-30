/* HỒ SƠ S-TIER — engine dựng cảnh từ dữ liệu (window.CASE, do motion/stier/build.py ghi).
   Mỗi cảnh là một "loại" (hero, date, doc, photo, map, mug, counter, ...), mọi mốc thời gian
   đã được build.py quy về GIÂY từ mốc từng từ của giọng đọc — engine chỉ vẽ, không đoán.
   Tất định: PRNG có hạt theo slug, không Math.random / Date / fetch.
   build.py (sfx) đặt tiếng động theo CÙNG các mốc + độ lệch cố định ghi chú ở từng loại. */
(function () {
  const C = window.CASE, DUR = C.dur;
  if (C.accent) document.documentElement.style.setProperty("--red", C.accent);
  const $ = (s) => document.querySelector(s);
  const el = (tag, cls, html, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (parent) parent.appendChild(e); return e; };
  const NS = "http://www.w3.org/2000/svg";
  const sv = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  let seed = C.seed || 1911; const rnd = () => { seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; };
  const norm = (w) => w.toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");
  const fsz = (text, max, width = 1000, k = 0.62) => Math.min(max, Math.floor(width / (Math.max(1, [...text].length) * k)));
  const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;");
  const IM = (k) => { const m = C.imgs[k]; if (!m) throw new Error("thiếu ảnh " + k); return m; };
  const px = (v) => v + "px";

  const tl = gsap.timeline({ paused: true });
  const show = (node, t0, t1, fade = 0.1) => {
    if (t0 > 0.001) tl.set(node, { autoAlpha: 0 }, 0);
    if (t0 <= 0.001) { node.style.opacity = 1; node.style.visibility = "visible"; tl.set(node, { autoAlpha: 1 }, 0); }   // khung 0 phải có hình (thumbnail)
    else tl.to(node, { autoAlpha: 1, duration: fade, ease: "none" }, t0);
    if (t1 != null && t1 < DUR - 0.01) tl.to(node, { autoAlpha: 0, duration: fade, ease: "none" }, t1 - fade);
  };
  const flash = (t, a = 0.5) => { tl.to("#flash", { opacity: a, duration: 0.04 }, Math.max(0, t)); tl.to("#flash", { opacity: 0, duration: 0.22 }, Math.max(0, t) + 0.04); };
  const leak = (t) => { tl.fromTo("#leak", { opacity: 0, x: -700 }, { opacity: 0.9, x: 0, duration: 0.35, ease: "power2.out", immediateRender: false }, t);
                        tl.to("#leak", { opacity: 0, x: 700, duration: 0.45, ease: "power2.in" }, t + 0.35); };
  // con dấu: rơi xuống, chạm lúc t+0.16 (sfx: thud ở t+0.16)
  const stamp = (node, t, rot = -8) => { tl.fromTo(node, { opacity: 0, scale: 2.4, rotation: rot }, { opacity: 0.95, scale: 1, rotation: rot, duration: 0.16, ease: "power4.in", immediateRender: false }, t);
                                         tl.to("#stage", { x: 10, duration: 0.03, yoyo: true, repeat: 3 }, t + 0.16); };
  const draw = (node, t, d, ease = "power2.inOut") => { const len = node.getTotalLength(); node.style.strokeDasharray = len; node.style.strokeDashoffset = len;
                                                         tl.to(node, { strokeDashoffset: 0, duration: d, ease }, t); };
  const credit = (d, text, top = 1360, t = 0) => { if (!text) return; const c = el("div", "credit mono", esc(text), d); c.style.top = px(top); tl.to(c, { opacity: 1, duration: 0.3 }, t); };
  const toneCls = (t) => ({ bw: "bw", sepia: "sepia", color: "color", dim: "dimbg" }[t || "sepia"]);
  const circleMark = (svg, x, y, r, t, k) => {
    const p = sv("path", { d: `M${x + r} ${y - 2} C${x + r} ${y - r - 6} ${x - r - 4} ${y - r} ${x - r} ${y + 2} C${x - r + 2} ${y + r + 4} ${x + r + 6} ${y + r} ${x + r - 2} ${y - 6}`,
      stroke: "var(--red)", "stroke-width": Math.max(4, r / 7), fill: "none", "stroke-linecap": "round" }, svg);
    draw(p, t, 0.25, "steps(5)");
  };
  const stage = $("#stage");
  const B = {};

  /* ---------- hero: khung tranh/ảnh in + tiêu đề + gạch + băng dán + vỡ dải + khép vòng ----------
     sfx: strike -> scratch; tape.at -> thud nhẹ; shatter.at -> whoosh(-0.62) + boom(+0.05); loop -> pad */
  B.hero = (s, d) => {
    const m = IM(s.img), gold = (s.frame || "gold") === "gold", pad = gold ? 48 : 22, extra = gold ? 0 : 58;
    const k = Math.min((s.maxW || (m.w > m.h ? 940 : 780)) / m.w, (s.maxH || 930) / m.h), hw = Math.round(m.w * k), hh = Math.round(m.h * k);
    const W = hw + 2 * pad, H = hh + 2 * pad + extra, top = Math.max(190, Math.round(730 - H / 2));
    const fb = el("div", "fbox", null, d); Object.assign(fb.style, { width: px(W), height: px(H), marginLeft: px(-W / 2), top: px(top) });
    el("div", gold ? "gold" : "printf", null, fb);
    const hole = el("div", "hole", null, fb); Object.assign(hole.style, { left: px(pad), top: px(pad), width: px(hw), height: px(hh) });
    const N = 14, sh = hh / N, slices = [];
    for (let i = 0; i < N; i++) {
      const sl = el("div", "slice " + toneCls(s.tone || "color"), null, hole);
      Object.assign(sl.style, { top: px(i * sh), height: px(sh + 1), width: px(hw), backgroundImage: `url(${m.src})`, backgroundSize: `${hw}px ${hh}px`, backgroundPosition: `0 ${-i * sh}px` });
      slices.push(sl);
    }
    const lines = (s.head || "").split("\n").filter(Boolean);
    const fs = lines.length ? fsz(lines.reduce((a, b) => (a.length > b.length ? a : b)), 72, 1020, 0.68) : 0;
    const htop = top + H + 34, words = [];
    lines.forEach((ln, li) => { const hl = el("div", "hline", null, d); hl.style.top = px(htop + li * fs * 1.08);
      ln.split(" ").forEach((w) => { const e = el("span", "hw", esc(w), hl); e.style.fontSize = px(fs); words.push(e); }); });
    const t0 = s.t0, tEnd = s.shatter ? s.shatter.at - 0.2 : s.t1;
    if (s.intro) { tl.fromTo(fb, { scale: 1.38 }, { scale: 1.0, duration: 0.75, ease: "power3.out" }, t0); tl.to(fb, { scale: 1.06, duration: Math.max(0.1, tEnd - t0 - 0.75), ease: "none" }, t0 + 0.75); flash(t0, 0.4); }
    else if (s.loop) {
      slices.forEach((sl, i) => { tl.set(sl, { x: (i % 2 ? 1 : -1) * (700 + (i * 53) % 260), opacity: 0 }, 0);
        tl.to(sl, { x: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, t0 + 0.02 + (N - i) * 0.02); });
      tl.fromTo(fb, { scale: 1.07 }, { scale: 1.0, duration: Math.max(0.3, s.t1 - t0), ease: "power2.out" }, t0);
    } else tl.fromTo(fb, { scale: 1.0 }, { scale: 1.06, duration: Math.max(0.1, tEnd - t0), ease: "none" }, t0);
    const ht = s.headTimes || words.map((_, i) => (s.headAt ?? t0 + 0.25) + i * (s.headStep || 0.14));
    words.forEach((w, i) => tl.fromTo(w, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.22, ease: "power3.out", immediateRender: false }, ht[Math.min(i, ht.length - 1)] - 0.05));
    let strike, tape;
    if (s.strike != null && lines.length === 1) {
      strike = el("div", "strike", null, d); strike.style.top = px(htop + fs * 0.5);
      tl.to(strike, { scaleX: 1, duration: 0.32, ease: "power3.inOut" }, s.strike);
      tl.to(words, { opacity: 0.35, duration: 0.3 }, s.strike + 0.2);
    }
    if (s.tape) {
      tape = el("div", "tape", esc(s.tape.text), d); tape.style.top = px(htop + lines.length * fs * 1.08 + 34);
      tl.fromTo(tape, { opacity: 0, y: 60, rotation: -9, xPercent: -50 }, { opacity: 1, y: 0, rotation: -3.5, xPercent: -50, duration: 0.35, ease: "back.out(2)", immediateRender: false }, s.tape.at - 0.05);
    }
    if (s.shatter) {
      const tb = s.shatter.at, txt = s.shatter.text || "";
      slices.forEach((sl, i) => tl.to(sl, { x: (i % 2 ? 1 : -1) * (700 + (i * 53) % 260), opacity: 0, duration: 0.55, ease: "power3.in" }, tb - 0.18 + i * 0.018));
      tl.to([...words, strike, tape].filter(Boolean), { opacity: 0, duration: 0.2 }, tb - 0.2);
      if (txt) { const sz = fsz(txt, 150, 980, 0.74); const sl = el("div", "slam", esc(txt), d); Object.assign(sl.style, { fontSize: px(sz), top: px(top + H / 2 - sz / 2) });
        tl.fromTo(sl, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in", immediateRender: false }, tb + 0.05); }
      tl.to(fb, { x: 14, duration: 0.03, yoyo: true, repeat: 5 }, tb + 0.23); flash(tb + 0.22, 0.35);
    }
  };

  /* ---------- date: nền tư liệu + chữ gõ + số lật + con dấu ----------
     sfx: mỗi ký tự dayAt+k*0.045 -> key; mỗi nhóm số groupAt -> 8 tick trong 0.55s; stamp.at+0.16 -> thud */
  B.date = (s, d) => {
    if (s.bg) { const m = IM(s.bg); const im = el("img", "abs " + toneCls("dim"), null, d); im.src = m.src;
      const k = Math.max(1260 / m.w, 1920 / m.h); Object.assign(im.style, { width: px(m.w * k), height: px(m.h * k), left: px(-90), top: 0 });
      tl.fromTo(im, { x: 0, scale: 1.08 }, { x: -140, scale: 1.0, duration: s.t1 - s.t0 + 0.3, ease: "none" }, s.t0);
      el("div", "layer", null, d).style.background = "linear-gradient(180deg, rgba(5,4,4,.25) 0%, rgba(5,4,4,.1) 35%, rgba(5,4,4,.85) 78%)"; }
    if (s.day) { const dy = el("div", "day mono", null, d);
      [...s.day].forEach((ch, k) => { const sp = el("span", null, ch === " " ? "&nbsp;" : esc(ch), dy); sp.style.opacity = 0; tl.set(sp, { opacity: 1 }, s.dayAt + k * 0.045); }); }
    const chars = [...s.date], D = chars.filter((c) => /\d/.test(c)).length, P = chars.length - D;
    const cw = Math.min(104, Math.floor((1000 - P * 34 - chars.length * 6) / Math.max(1, D))), fz = Math.min(140, Math.floor(cw * 1.3));
    const row = el("div", "date", null, d); if (s.top) row.style.top = px(s.top);
    const groups = [[]];
    chars.forEach((ch) => {
      if (!/\d/.test(ch)) { const sp = el("div", "dsep", ch === " " ? "&nbsp;" : esc(ch), row); sp.style.width = px(ch === " " ? 18 : 34); sp.style.fontSize = px(fz * 0.85); groups.push([]); return; }
      const g = el("div", "dg", null, row); g.style.width = px(cw); const r = el("div", "reel", null, g); const fin = +ch;
      const seq = []; for (let k = 0; k < 9; k++) seq.push((fin + 1 + k * 3) % 10); seq.push(fin);
      seq.forEach((v) => { const e = el("div", null, String(v), r); e.style.fontSize = px(fz); }); groups[groups.length - 1].push(r);
    });
    tl.set(row, { opacity: 0 }, 0); tl.to(row, { opacity: 1, duration: 0.15 }, s.groupAt[0] - 0.1);
    groups.filter((g) => g.length).forEach((g, gi) => g.forEach((r, j) => tl.fromTo(r, { y: 0 }, { y: -9 * 176, duration: 0.55, ease: "power3.out", immediateRender: false }, s.groupAt[gi] - 0.05 + j * 0.07)));
    if (s.sub) { const sb = el("div", "dsub mono", esc(s.sub.text), d); if (s.top) sb.style.top = px(s.top + 260); tl.to(sb, { opacity: 1, duration: 0.3 }, s.sub.at); }
    if (s.stamp) { const st = el("div", "stamp", esc(s.stamp.text), d); st.style.fontSize = px(fsz(s.stamp.text, 104, 760, 0.72)); st.style.left = px(150); st.style.top = px((s.top || 640) + 400); stamp(st, s.stamp.at, -9); }
  };

  /* ---------- doc: trang báo/tài liệu lớn, máy quay lia từng vùng ----------
     sfx: t0 -> màn trập; mỗi move.at-0.3 -> whoosh; tag.reveal -> scratch */
  B.doc = (s, d) => {
    const m = IM(s.img), wrap = el("div", "layer", null, d); wrap.style.background = "#16120e";
    const w = el("div", "docw " + toneCls(s.tone || "sepia"), null, wrap); Object.assign(w.style, { width: px(m.w), height: px(m.h) });
    const im = el("img", null, null, w); im.src = m.src;
    const cy = s.cy || 860;
    const cam = (x, y, z) => { const sc = z * 1080 / m.w; return { x: 540 - x * m.w * sc, y: cy - y * m.h * sc, scale: sc }; };
    const mv = s.moves && s.moves.length ? s.moves : [{ at: s.t0, x: 0.5, y: 0.3, z: 1.25 }, { at: s.t0 + 0.4, x: 0.5, y: 0.7, z: 1.25, d: Math.max(0.5, s.t1 - s.t0 - 0.5), ease: "none" }];
    tl.set(w, cam(mv[0].x, mv[0].y, mv[0].z), 0);
    mv.slice(1).forEach((q) => tl.to(w, { ...cam(q.x, q.y, q.z), duration: q.d || 0.8, ease: q.ease || "power3.inOut" }, q.at - 0.3));
    if (s.tag) { const tg = el("div", "tagline", esc(s.tag.text) + (s.tag.hidden ? ` <span class="redact">${esc(s.tag.hidden)}<i></i></span>` : ""), d);
      tl.fromTo(tg, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, s.tag.at - 0.1);
      if (s.tag.hidden && s.tag.reveal != null) tl.to(tg.querySelector(".redact i"), { scaleX: 0, duration: 0.35, ease: "power3.inOut" }, s.tag.reveal); }
    credit(d, s.credit, 1360, s.t0 + 0.3);
  };

  /* ---------- photo: ảnh tư liệu tràn khung / ảnh in, vòng tròn đánh dấu ----------
     sfx: t0 -> màn trập + boom nhẹ; mỗi circle.at -> scratch */
  B.photo = (s, d) => {
    const m = IM(s.img), mode = s.mode || "full", fx = (s.focus || [0.5, 0.4])[0], fy = (s.focus || [0.5, 0.4])[1];
    let area, iw, ih, il, it, holder;
    if (mode === "full") {
      area = el("div", "abs", null, d); Object.assign(area.style, { left: 0, top: px(190), width: px(1080), height: px(1540), overflow: "hidden" });
      const k = Math.max(1080 / m.w, 1540 / m.h); iw = m.w * k; ih = m.h * k;
      il = Math.min(0, Math.max(1080 - iw, 540 - fx * iw)); it = Math.min(0, Math.max(1540 - ih, 770 - fy * ih));
      holder = el("div", "phw", null, area); Object.assign(holder.style, { left: 0, top: 0, width: px(1080), height: px(1540), transformOrigin: `${il + fx * iw}px ${it + fy * ih}px` });
    } else {
      const k = Math.min((s.maxW || 860) / m.w, (s.maxH || 980) / m.h); iw = m.w * k; ih = m.h * k; il = 22; it = 22;
      area = el("div", "print", null, d); Object.assign(area.style, { width: px(iw + 44), height: px(ih + 100), left: px(540 - (iw + 44) / 2), top: px(Math.max(200, 800 - (ih + 100) / 2)) });
      holder = el("div", "phw", null, area); Object.assign(holder.style, { left: 0, top: 0, width: px(iw + 44), height: px(ih + 100) });
    }
    const im = el("img", toneCls(s.tone || "bw"), null, holder); im.src = m.src; Object.assign(im.style, { left: px(il), top: px(it), width: px(iw), height: px(ih) });
    const svg = sv("svg", { width: holder.style.width.replace("px", ""), height: holder.style.height.replace("px", "") }, holder);
    (s.circles || []).forEach((c) => circleMark(svg, il + c.x * iw, it + c.y * ih, c.r || 34, c.at));
    const z0 = s.z0 || 1.14, z1 = s.z1 || 1.0, dur = s.t1 - s.t0;
    if (mode === "full") {
      if ((s.reveal || "iris") === "iris") tl.fromTo(area, { clipPath: "circle(0% at 50% 45%)" }, { clipPath: "circle(150% at 50% 45%)", duration: 0.7, ease: "power3.out", immediateRender: false }, s.t0);
      else tl.fromTo(area, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power3.inOut", immediateRender: false }, s.t0);
      tl.fromTo(holder, { scale: z0 }, { scale: z1, duration: 0.7, ease: "power3.out", immediateRender: false }, s.t0);
      tl.to(holder, { scale: z1 * 1.06, duration: Math.max(0.2, dur - 0.7), ease: "none" }, s.t0 + 0.7);
    } else {
      tl.fromTo(area, { y: 140, scale: 1.12, rotation: 4, opacity: 0 }, { y: 0, scale: 1, rotation: s.rot ?? -2, opacity: 1, duration: 0.45, ease: "power3.out", immediateRender: false }, s.t0);
      tl.to(area, { scale: 1.04, duration: Math.max(0.2, dur - 0.45), ease: "none" }, s.t0 + 0.45);
    }
    if (s.label) { const lb = el("div", "boxlbl mono", esc(s.label.text), d); lb.style.top = px(s.label.y || 1120); tl.to(lb, { opacity: 1, duration: 0.25 }, s.label.at); }
    credit(d, s.credit, s.creditY || 1330, s.t0 + 0.2);
    if (s.stamp) { const st = el("div", "stamp", esc(s.stamp.text), d); st.style.fontSize = px(fsz(s.stamp.text, 104, 900 - (s.stamp.x || 330), 0.72)); st.style.left = px(s.stamp.x || 330); st.style.top = px(s.stamp.y || 1180); stamp(st, s.stamp.at, s.stamp.rot || -8); }
  };

  /* ---------- counter: số đếm lớn + nhãn (+ ảnh in) ----------
     sfx: tick theo từng bước (tối đa 28) theo ease power2.out từ at tới until; until -> thud */
  const vn = (n) => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  B.counter = (s, d) => {
    const str = (s.prefix || "") + vn(s.to) + (s.suffix || ""), fs = fsz(str, 300, 1000, 0.62);
    const ct = el("div", "count", esc((s.prefix || "") + vn(s.from || 0) + (s.suffix || "")), d); ct.style.fontSize = px(fs); if (s.top) ct.style.top = px(s.top);
    const top = (s.top || 360) + fs + 20;
    const o = { v: s.from || 0 };
    tl.to(o, { v: s.to, duration: Math.max(0.2, s.until - s.at), ease: "power2.out", onUpdate: () => { ct.textContent = (s.prefix || "") + vn(o.v) + (s.suffix || ""); } }, s.at);
    if (s.label) { const lb = el("div", "countlbl", esc(s.label), d); lb.style.top = px(top); lb.style.fontSize = px(fsz(s.label, 52, 980, 0.9));
      tl.fromTo(lb, { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power3.out", immediateRender: false }, s.labelAt ?? s.until - 0.1); }
    if (s.sub) { const sb = el("div", "countsub mono", esc(s.sub.text), d); sb.style.top = px(top + 90); tl.to(sb, { opacity: 1, duration: 0.3 }, s.sub.at); }
    if (s.img) { const m = IM(s.img), k = Math.min(520 / m.w, 480 / m.h), w = m.w * k, h = m.h * k;
      const pr = el("div", "print", null, d); Object.assign(pr.style, { left: px(540 - (w + 36) / 2), top: px(top + 170), width: px(w + 36), height: px(h + 84) });
      const im = el("img", "abs " + toneCls(s.tone || "bw"), null, pr); im.src = m.src; Object.assign(im.style, { left: px(18), top: px(18), width: px(w), height: px(h) });
      tl.fromTo(pr, { opacity: 0, y: 80, rotation: 6 }, { opacity: 1, y: 0, rotation: -3, duration: 0.4, ease: "power3.out", immediateRender: false }, s.imgAt ?? s.t0 + 0.2); }
  };

  /* ---------- calendar: N ô bị gạch chéo ----------
     sfx: mỗi ô 2 nét scratch ở at+k*step và at+k*step+0.06 */
  B.calendar = (s, d) => {
    const n = s.n, cols = n <= 7 ? n : n <= 14 ? 7 : n <= 30 ? 10 : 13, rows = Math.ceil(n / cols), gap = n <= 7 ? 14 : 10;
    const w = Math.floor((952 - (cols - 1) * gap) / cols), h = Math.round(w * (n <= 7 ? 1.7 : 1.3));
    if (s.title) { const t = el("div", "calt", esc(s.title).replace(/\*(.+?)\*/g, "<em>$1</em>"), d); t.style.fontSize = px(fsz(s.title, 62, 1000, 0.6));
      tl.fromTo(t, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, immediateRender: false }, s.t0); }
    const cal = el("div", "cal", null, d); cal.style.top = px(Math.max(640, 900 - (rows * (h + gap)) / 2)); cal.style.gap = px(gap);
    for (let k = 0; k < n; k++) {
      const c = el("div", "cell", `<b>${k + 1}</b><i>${esc(s.unit || "NGÀY")}</i>`, cal); Object.assign(c.style, { width: px(w), height: px(h) });
      c.querySelector("b").style.fontSize = px(Math.round(w * 0.55)); c.querySelector("b").style.top = px(Math.round(h * 0.14)); c.querySelector("i").style.fontSize = px(Math.max(14, Math.round(w * 0.16)));
      const g = sv("svg", { viewBox: "0 0 100 150", preserveAspectRatio: "none" }, c);
      const p1 = sv("path", { d: `M14 ${24 + k % 3} Q52 80 ${86 - k % 2} 128`, stroke: "var(--red)", "stroke-width": 9, fill: "none", "stroke-linecap": "round" }, g);
      const p2 = sv("path", { d: `M${84 + k % 2} 22 Q46 78 16 ${126 - k % 3}`, stroke: "var(--red)", "stroke-width": 9, fill: "none", "stroke-linecap": "round" }, g);
      tl.fromTo(c, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.2, ease: "back.out(2)", immediateRender: false }, s.t0 + 0.05 + k * Math.min(0.05, 0.6 / n));
      if (k < (s.cross ?? n)) { draw(p1, s.at + k * s.step, 0.12, "steps(3)"); draw(p2, s.at + k * s.step + 0.06, 0.12, "steps(3)"); }
    }
  };

  /* ---------- clock: kim quay, đổi nhãn ngày, "+N" ----------
     sfx: tick đều ~0.1s suốt cảnh; plusAt -> thud */
  B.clock = (s, d) => {
    const cd = el("div", "clockday", null, d); const sp = el("span", null, esc(s.from || ""), cd);
    const g = sv("svg", { class: "layer", viewBox: "0 0 1080 1920" }, d);
    sv("circle", { cx: 540, cy: 780, r: 290, fill: "rgba(239,228,203,.05)", stroke: "#e9ddc4", "stroke-width": 6 }, g);
    for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; sv("line", { x1: 540 + Math.sin(a) * 250, y1: 780 - Math.cos(a) * 250, x2: 540 + Math.sin(a) * 272, y2: 780 - Math.cos(a) * 272, stroke: "#e9ddc4", "stroke-width": k % 3 ? 4 : 9 }, g); }
    const hh = sv("line", { x1: 540, y1: 780, x2: 540, y2: 610, stroke: "#fff", "stroke-width": 16, "stroke-linecap": "round" }, g);
    const mh = sv("line", { x1: 540, y1: 780, x2: 540, y2: 540, stroke: "var(--red)", "stroke-width": 9, "stroke-linecap": "round" }, g);
    sv("circle", { cx: 540, cy: 780, r: 18, fill: "var(--red)" }, g);
    const dur = s.t1 - s.t0, turns = s.turns || 2;
    tl.fromTo(mh, { rotation: 0 }, { rotation: 360 * turns, svgOrigin: "540 780", duration: dur, ease: "power2.inOut", immediateRender: false }, s.t0);
    tl.fromTo(hh, { rotation: 0 }, { rotation: 30 * turns, svgOrigin: "540 780", duration: dur, ease: "power2.inOut", immediateRender: false }, s.t0);
    if (s.to) { tl.to(sp, { y: -30, opacity: 0, duration: 0.15 }, s.swap - 0.15); tl.set(sp, { textContent: s.to }, s.swap); tl.fromTo(sp, { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.2, immediateRender: false }, s.swap + 0.01); }
    if (s.plus) { const p = el("div", "plus", esc(s.plus), d); p.style.fontSize = px(fsz(s.plus, 92, 980, 0.72));
      tl.fromTo(p, { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in", immediateRender: false }, s.plusAt - 0.1); }
  };

  /* ---------- file: thẻ hồ sơ giấy, lật 3D + con dấu ----------
     sfx: t0 -> whoosh; stamp.at+0.16 -> thud */
  B.file = (s, d) => {
    const cd = el("div", "card", null, d); el("div", "clip", null, cd);
    el("div", "k", esc(s.k || "HỒ SƠ"), cd);
    const lines = (s.name || "").split("\n"), longest = lines.reduce((a, b) => (a.length > b.length ? a : b), "");
    const n = el("div", "n", lines.map(esc).join("<br/>"), cd); n.style.fontSize = px(fsz(longest, 112, s.img ? 430 : 720, 0.6));
    if (s.desc) el("div", "d", esc(s.desc), cd);
    el("div", "ln", null, cd);
    if (s.img) { const im = el("img", "pic bw", null, cd); im.src = IM(s.img).src; if (s.imgPos) im.style.objectPosition = s.imgPos; }
    tl.fromTo(cd, { rotationX: 70, y: 300, opacity: 0, rotation: 6 }, { rotationX: 0, y: 0, opacity: 1, rotation: -3, duration: 0.5, ease: "power3.out", transformPerspective: 1400, immediateRender: false }, s.t0);
    tl.to(cd, { scale: 1.04, duration: Math.max(0.2, s.t1 - s.t0 - 0.5), ease: "none" }, s.t0 + 0.5);
    if (s.stamp) { const st = el("div", "stamp ink", esc(s.stamp.text), d); st.style.left = px(s.stamp.x || 330); st.style.top = px(s.stamp.y || 930); st.style.fontSize = px(fsz(s.stamp.text, 92, 560, 0.72)); stamp(st, s.stamp.at, -11); }
  };

  /* ---------- crowd: đám đông bóng đen ngược sáng ----------
     sfx: rì rầm suốt cảnh */
  B.crowd = (s, d) => {
    el("div", "layer wall7", null, d);
    if ((s.object || "frame") === "frame") { const f = el("div", "minif", null, d); tl.fromTo(f, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, immediateRender: false }, s.t0); }
    el("div", "layer floor7", null, d); const cr = el("div", "layer", null, d);
    for (let row = 0; row < 8; row++) {
      const depth = row / 7, y = 760 + Math.pow(depth, 1.35) * 720, sc = 0.5 + depth * 1.9, span = 520 + depth * 1100, cnt = 7 + row, shade = Math.round(96 - depth * 90);
      for (let j = 0; j < cnt; j++) {
        const fg = el("div", "fig", null, cr); const x = 540 + (j / (cnt - 1) - 0.5) * span + (rnd() - 0.5) * 60 * (0.5 + depth);
        Object.assign(fg.style, { left: px(x - 23), top: px(y - 120 + (rnd() - 0.5) * 18), transform: `scale(${sc * (0.88 + rnd() * 0.22)})` });
        fg.style.setProperty("--c", `rgb(${shade + 8},${shade + 2},${Math.max(0, shade - 4)})`);
        tl.fromTo(fg, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.18, ease: "power2.out", immediateRender: false }, s.t0 + 0.02 + (7 - row) * 0.07 + rnd() * 0.2);
      }
    }
    tl.to(cr, { scale: 1.08, transformOrigin: "50% 40%", duration: s.t1 - s.t0 + 0.2, ease: "none" }, s.t0);
    if (s.label) { const lb = el("div", "boxlbl mono", esc(s.label.text), d); lb.style.top = px(1220); tl.to(lb, { opacity: 1, duration: 0.25 }, s.label.at); }
  };

  /* ---- lớp phủ dùng chung: ảnh hồ sơ (mugshot) + con dấu + song sắt + chữ lớn ----
     sfx: mug.at-0.13 -> thud; stamp.at+0.16 -> boom; bars.at+0.35+k*0.035 -> clank; */
  const overlay = (s, d, pos) => {
    const L = pos === "center" ? 305 : 70, T = pos === "center" ? 560 : 860;
    if (s.mug) {
      const mg = el("div", "mug", null, d); Object.assign(mg.style, { left: px(L), top: px(T) });
      const im = el("img", null, null, mg); im.src = IM(s.mug.img).src; if (s.mug.pos) im.style.objectPosition = s.mug.pos;
      const nm = el("div", "nm", esc(s.mug.name || ""), mg); const bar = el("i", null, null, nm);
      nm.style.fontSize = px(fsz(s.mug.name || "", 30, 420, 0.66));
      tl.fromTo(mg, { opacity: 0, scale: 1.7, rotation: 10 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.22, ease: "power4.in", immediateRender: false }, s.mug.at - 0.35);
      if (s.mug.reveal != null) tl.to(bar, { scaleX: 0, duration: 0.35, ease: "power3.inOut" }, s.mug.reveal); else tl.set(bar, { scaleX: 0 }, 0);
    }
    if (s.stamp) { const st = el("div", "stamp", esc(s.stamp.text), d); st.style.fontSize = px(fsz(s.stamp.text, 100, 400, 0.72));
      Object.assign(st.style, pos === "center" ? { left: px(250), top: px(1250) } : { left: px(600), top: px(1250) }); stamp(st, s.stamp.at);
      if (s.bars) tl.to(st, { opacity: 0, duration: 0.2 }, s.bars.at); }
    if (s.bars) { const b = el("div", "bars", null, d); Object.assign(b.style, { left: px(L), top: px(T), width: px(470), height: px(580) });
      for (let k = 0; k < 8; k++) { const r = el("div", "bar2", null, b); r.style.left = px(18 + k * 60); r.style.height = px(580); tl.set(r, { y: -600 }, 0);
        tl.fromTo(r, { y: -600 }, { y: 0, duration: 0.3, ease: "power4.in", immediateRender: false }, s.bars.at + 0.05 + k * 0.035); } }
    if (s.big) { const bg = el("div", "big", esc(s.big.text) + (s.big.small ? `<small>${esc(s.big.small)}</small>` : ""), d);
      bg.style.fontSize = px(fsz(s.big.text, 210, 900, 0.62));
      Object.assign(bg.style, pos === "center" ? { left: px(40), right: px(40), top: px(250), textAlign: "center" } : { right: px(70), top: px(430), textAlign: "right" });
      tl.fromTo(bg, { opacity: 0, x: pos === "center" ? 0 : 80, y: pos === "center" ? 40 : 0 }, { opacity: 1, x: 0, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, s.big.at - 0.12); }
  };

  /* ---------- map: biên giới thật tự vẽ, ghim, tuyến đường ----------
     sfx: t0-0.3 -> whoosh; pin.at -> blip; route at..until -> tông lên */
  B.map = (s, d) => {
    const G = C.geo, svg = sv("svg", { class: "layer", viewBox: "0 0 1080 1920" }, d);
    const borders = G.countries.slice().sort((a, b) => a.focus - b.focus).map((c) => [sv("path", { d: c.d, class: "ctry" + (c.focus ? " focus" : "") }, svg), c.focus]);
    borders.forEach(([p, f], k) => draw(p, s.t0 - 0.05 + (f ? 0.1 : 0) + k * 0.03, f ? 0.9 : 0.7));
    G.countries.filter((c) => c.label && c.lx > 0).forEach((c) => { const t = sv("text", { x: c.lx, y: c.ly, class: "clbl", "text-anchor": "middle" }, svg); t.textContent = c.label;
      tl.fromTo(t, { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, s.t0 + 0.5); });
    const P = (n) => G.pins.find((p) => p.name === n);
    (s.routes || []).forEach((r) => { const a = P(r.from), b = P(r.to), bend = r.bend ?? 0.25;
      const mx = (a.x + b.x) / 2 - (b.y - a.y) * bend, my = (a.y + b.y) / 2 + (b.x - a.x) * bend;
      const dd = `M${a.x} ${a.y} Q${mx} ${my} ${b.x} ${b.y}`;
      const rp = sv("path", { d: dd, stroke: "var(--red)", "stroke-width": 7, fill: "none", "stroke-linecap": "round" }, svg);
      sv("path", { d: dd, stroke: "#060505", "stroke-width": 9, fill: "none", "stroke-dasharray": "2 22" }, svg);
      draw(rp, r.at, Math.max(0.3, r.until - r.at), "power1.inOut"); });
    (s.pins || []).forEach((q) => { const p = P(q.name), g = sv("g", {}, svg);
      const ring = sv("circle", { cx: p.x, cy: p.y, r: 34, fill: "none", stroke: "var(--red)", "stroke-width": 4 }, g);
      sv("circle", { cx: p.x, cy: p.y, r: 16, fill: "var(--red)" }, g);
      const side = q.side || (p.x > 700 ? "t" : "r");
      const t = sv("text", { x: side === "r" ? p.x + 40 : side === "l" ? p.x - 40 : p.x, y: side === "t" ? p.y - 56 : p.y + 12, class: "pinlbl", "text-anchor": side === "r" ? "start" : side === "l" ? "end" : "middle" }, g);
      t.textContent = q.label || p.label || p.name;
      tl.fromTo(g, { opacity: 0, y: -70 }, { opacity: 1, y: 0, duration: 0.35, ease: "bounce.out", immediateRender: false }, q.at);
      tl.fromTo(ring, { scale: 0.4, transformOrigin: "50% 50%" }, { scale: 2.2, opacity: 0, duration: 0.8, ease: "power2.out", immediateRender: false }, q.at + 0.25); });
    const zt = s.zoom ? P(s.zoom) : null;
    if (zt) tl.to(svg, { scale: 1.12, transformOrigin: `${(zt.x / 10.8).toFixed(1)}% ${(zt.y / 19.2).toFixed(1)}%`, duration: s.t1 - s.t0, ease: "none" }, s.t0);
    if (s.dimAt != null) tl.to(svg, { opacity: 0.25, duration: 0.3 }, s.dimAt);
    overlay(s, d, "left");
  };

  /* ---------- mug: ảnh hồ sơ đứng riêng trên nền số tù ---------- */
  B.mug = (s, d) => {
    if (s.ghost) { const g = el("div", "ghost", esc(s.ghost), d); g.style.fontSize = px(fsz(s.ghost, 330, 1120, 0.62)); g.style.top = px(1000); }
    overlay(s, d, "center");
  };

  /* ---------- question: lặng (sfx: tắt nền trầm) ---------- */
  B.question = (s, d) => { const a = el("div", "ask", esc(s.text), d); a.style.fontSize = px(fsz(s.text, 96, 1000, 0.5));
    tl.fromTo(a, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, immediateRender: false }, s.t0 + 0.02); };

  /* ---------- quote: trích dẫn gõ máy chữ trên giấy ----------
     sfx: key mỗi ký tự (tối đa 40, rải đều) từ at trong typeDur */
  B.quote = (s, d) => {
    const pp = el("div", "qpaper", null, d); el("div", "qm", "“", pp);
    const qt = el("div", "qt", null, pp); const L = [...s.text].length; qt.style.fontSize = px(L < 60 ? 54 : L < 120 ? 44 : 36);
    const spans = [...s.text].map((ch) => el("span", null, esc(ch), qt));
    spans.forEach((sp, k) => tl.set(sp, { opacity: 1 }, s.at + (k / L) * s.typeDur));
    if (s.by) { const by = el("div", "by mono", "— " + esc(s.by), pp); tl.to(by, { opacity: 1, duration: 0.3 }, s.at + s.typeDur); }
    tl.fromTo(pp, { opacity: 0, y: 80, rotation: 2 }, { opacity: 1, y: 0, rotation: -1.5, duration: 0.4, ease: "power3.out", immediateRender: false }, s.t0);
    tl.to(pp, { scale: 1.03, duration: Math.max(0.2, s.t1 - s.t0 - 0.4), ease: "none" }, s.t0 + 0.4);
  };

  /* ---------- kinetic: chữ lớn xếp tầng, từng dòng đập vào theo lời ----------
     sfx: mỗi item.at -> thud nhẹ */
  B.kinetic = (s, d) => {
    const it = s.items, sizes = it.map((q) => q.size || fsz(q.text, 150, 960, 0.74)), total = sizes.reduce((a, b) => a + b * 1.08, 0);
    let y = Math.max(300, 820 - total / 2);
    it.forEach((q, k) => { const e = el("div", "kin" + (q.acc ? " acc" : "") + (q.serif ? " serif" : ""), esc(q.text), d); Object.assign(e.style, { fontSize: px(sizes[k]), top: px(y) }); y += sizes[k] * 1.08;
      tl.fromTo(e, { opacity: 0, scale: 1.35, y: -20 }, { opacity: 1, scale: 1, y: 0, duration: 0.2, ease: "power4.in", immediateRender: false }, q.at - 0.08); });
    if (s.bg) { const m = IM(s.bg), im = el("img", "abs " + toneCls("dim"), null, d); im.src = m.src; const k = Math.max(1080 / m.w, 1920 / m.h);
      Object.assign(im.style, { width: px(m.w * k), height: px(m.h * k), left: px(540 - m.w * k / 2), top: px(960 - m.h * k / 2), zIndex: -1, opacity: 0.55 });
      d.insertBefore(im, d.firstChild); tl.fromTo(im, { scale: 1.1 }, { scale: 1.0, duration: s.t1 - s.t0, ease: "none", immediateRender: false }, s.t0); }
  };

  /* ---------- evidence: tang vật dưới đèn + nhãn chú thích ----------
     sfx: t0 -> màn trập; mỗi callout.at -> tick */
  B.evidence = (s, d) => {
    el("div", "layer", null, d).style.background = "radial-gradient(55% 40% at 50% 42%, #3a3026 0%, #120e0b 70%, #060505 100%)";
    const m = IM(s.img), k = Math.min((s.maxW || 900) / m.w, (s.maxH || 980) / m.h), w = m.w * k, h = m.h * k, L = 540 - w / 2, T = Math.max(300, 800 - h / 2);
    const holder = el("div", "phw", null, d); Object.assign(holder.style, { left: px(L), top: px(T), width: px(w), height: px(h) });
    const im = el("img", toneCls(s.tone || "color"), null, holder); im.src = m.src; Object.assign(im.style, { left: 0, top: 0, width: px(w), height: px(h), boxShadow: "0 40px 120px rgba(0,0,0,.9)" });
    tl.fromTo(holder, { opacity: 0, scale: 1.12 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out", immediateRender: false }, s.t0);
    tl.to(holder, { scale: 1.05, duration: Math.max(0.2, s.t1 - s.t0 - 0.5), ease: "none" }, s.t0 + 0.5);
    if (s.tag) { const tg = el("div", "evtag", esc(s.tag), d); tl.fromTo(tg, { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)", immediateRender: false }, s.t0 + 0.2); }
    const svg = sv("svg", { class: "layer", viewBox: "0 0 1080 1920" }, d);
    (s.callouts || []).forEach((c) => { const x = L + c.x * w, y = T + c.y * h, right = (c.side || (c.x < 0.5 ? "l" : "r")) === "r", lx = right ? 760 : 320;
      const ln = sv("path", { d: `M${x} ${y} L${lx} ${y}`, stroke: "#fff", "stroke-width": 3, fill: "none" }, svg); sv("circle", { cx: x, cy: y, r: 10, fill: "var(--red)" }, svg);
      draw(ln, c.at, 0.25);
      const co = el("div", "co", esc(c.text), d); Object.assign(co.style, right ? { left: px(lx + 6), top: px(y - 26) } : { right: px(1080 - lx + 6), top: px(y - 26) });
      tl.to(co, { opacity: 1, duration: 0.2 }, c.at + 0.2); });
    credit(d, s.credit, 1360, s.t0 + 0.3);
  };

  /* ---------- split: hai ảnh đối chiếu + dấu (= ≠ →) ----------
     sfx: a.at, b.at -> thud; signAt -> boom */
  B.split = (s, d) => {
    if (s.title) { const t = el("div", "spt", esc(s.title), d); t.style.fontSize = px(fsz(s.title, 54, 1000, 0.6)); tl.fromTo(t, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, immediateRender: false }, s.t0); }
    [["a", 50, -3], ["b", 560, 3]].forEach(([key, left, rot]) => { const q = s[key]; const w = el("div", "splitw", null, d); w.style.left = px(left);
      const pr = el("div", "print", null, w); const im = el("img", toneCls(q.tone || "bw"), null, pr); im.src = IM(q.img).src; if (q.pos) im.style.objectPosition = q.pos;
      const lb = el("div", "lb", esc(q.label || ""), pr); lb.style.fontSize = px(fsz(q.label || "", 30, 420, 0.66));
      tl.fromTo(w, { opacity: 0, y: 120, rotation: rot * 3 }, { opacity: 1, y: 0, rotation: rot, duration: 0.4, ease: "power3.out", immediateRender: false }, q.at - 0.2); });
    if (s.sign) { const sg = el("div", "sign", esc(s.sign), d); tl.fromTo(sg, { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in", immediateRender: false }, s.signAt - 0.1); }
  };

  /* ---------- timeline: mốc năm dọc ----------
     sfx: mỗi item.at -> tick + thud nhẹ */
  B.timeline = (s, d) => {
    const n = s.items.length, gap = Math.min(250, 860 / n), line = el("div", "tlx", null, d); line.style.height = px(gap * (n - 1) + 60);
    tl.fromTo(line, { scaleY: 0 }, { scaleY: 1, duration: Math.max(0.4, s.items[n - 1].at - s.t0), ease: "none", immediateRender: false }, s.t0);
    s.items.forEach((q, k) => { const e = el("div", "tli", `<div class="dot"></div><div class="yr">${esc(q.year)}</div><div class="tx">${esc(q.text || "")}</div>`, d); e.style.top = px(410 + k * gap);
      tl.fromTo(e, { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, q.at - 0.1); });
  };

  /* ---------- ledger: sổ sách tiền ----------
     sfx: mỗi row.at -> key x3; total.at -> thud */
  B.ledger = (s, d) => {
    const lg = el("div", "ledger", null, d); if (s.title) el("div", "lt", esc(s.title), lg);
    const rows = [...(s.rows || []), ...(s.total ? [{ ...s.total, tot: true }] : [])];
    rows.forEach((r) => { const e = el("div", "row" + (r.tot ? " tot" : ""), `<span>${esc(r.k)}</span><span>${esc(r.v)}</span>`, lg);
      tl.fromTo(e, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25, immediateRender: false }, r.at - 0.05); });
    tl.fromTo(lg, { opacity: 0, y: 80, rotation: 2 }, { opacity: 1, y: 0, rotation: -1.2, duration: 0.4, ease: "power3.out", immediateRender: false }, s.t0);
  };

  /* ---------- slam: một dòng chữ đập mạnh trên nền tư liệu tối ----------
     sfx: at -> boom */
  B.slam = (s, d) => {
    if (s.bg) { const m = IM(s.bg), im = el("img", "abs " + toneCls("dim"), null, d); im.src = m.src; const k = Math.max(1080 / m.w, 1920 / m.h);
      Object.assign(im.style, { width: px(m.w * k), height: px(m.h * k), left: px(540 - m.w * k / 2), top: px(960 - m.h * k / 2) });
      tl.fromTo(im, { scale: 1.12 }, { scale: 1.0, duration: s.t1 - s.t0, ease: "none", immediateRender: false }, s.t0); }
    const lines = s.text.split("\n"), fs = fsz(lines.reduce((a, b) => (a.length > b.length ? a : b)), 170, 980, 0.74);
    const sl = el("div", "slam", lines.map(esc).join("<br/>"), d); Object.assign(sl.style, { fontSize: px(fs), top: px(820 - fs * lines.length / 2), lineHeight: 1.02, color: s.white ? "#fff" : "" });
    tl.fromTo(sl, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in", immediateRender: false }, s.at - 0.13);
    if (s.sub) { const sb = el("div", "dsub mono", esc(s.sub), d); sb.style.top = px(840 + fs * lines.length / 2 + 30); tl.to(sb, { opacity: 1, duration: 0.3 }, s.at + 0.3); }
    tl.to("#stage", { x: 12, duration: 0.03, yoyo: true, repeat: 5 }, s.at + 0.05);
  };

  // ---------- dựng cảnh ----------
  C.scenes.forEach((s, i) => {
    const d = el("div", "scene", null, stage); show(d, s.t0, s.t1, s.type === "question" ? 0.06 : 0.1);
    if (!B[s.type]) throw new Error("loại cảnh lạ: " + s.type);
    B[s.type](s, d);
    if (i > 0) { const tr = s.tr || ["leak", "flash", "cut"][i % 3]; if (tr === "leak") leak(s.t0 - 0.08); else if (tr === "flash") flash(s.t0, 0.25); }
  });

  // ---------- không khí ----------
  for (let i = 0; i < 38; i++) { const m = el("div", "mote", null, $("#motes")); Object.assign(m.style, { left: px(rnd() * 1080), top: px(rnd() * 1920), transform: `scale(${0.5 + rnd() * 1.4})` });
    tl.to(m, { y: -160 - rnd() * 260, x: (rnd() - 0.5) * 140, opacity: 0.2 + rnd() * 0.6, duration: DUR, ease: "none" }, 0); }
  tl.to("#prog i", { scaleX: 1, duration: DUR, ease: "none" }, 0);
  for (let k = 0; k < Math.ceil(DUR * 2); k++) tl.set("#grain", { opacity: 0.08 + ((k * 37) % 7) / 100 }, k * 0.5);
  $("#kicker .t").innerHTML = esc(C.kicker) + `<small>${esc(C.sub || "")}</small>`;

  // ---------- phụ đề: cụm 2–4 từ, một màu nhấn ----------
  const ACC = new Set((C.acc || []).map(norm));
  const caps = $("#caps"), chunks = [];
  C.lines.forEach((ln) => { let cur = []; ln.words.forEach((w, k) => { cur.push(w);
    if (/[.,…?!:;]$/.test(w.w) || cur.length >= 4 || k === ln.words.length - 1) { chunks.push(cur); cur = []; } }); });
  chunks.forEach((c, n) => { const box = el("div", "cap", null, caps);
    c.forEach((w) => { const clean = w.w.replace(/["“”]/g, ""), acc = ACC.has(norm(w.w)) || /\d/.test(w.w);
      const sp = el("span", "cw" + (acc ? " acc" : ""), esc(clean), box); tl.to(sp, { opacity: 1, duration: 0.08 }, w.t); });
    const t0 = c[0].t - 0.06, nx = chunks[n + 1], t1 = nx ? nx[0].t - 0.06 : DUR;
    tl.set(box, { opacity: 1 }, t0); tl.set(box, { opacity: 0 }, t1); });
  C.scenes.filter((s) => s.type === "question").forEach((s) => { tl.set("#caps", { opacity: 0 }, s.t0 - 0.01); tl.set("#caps", { opacity: 1 }, s.t1); });

  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = tl;
})();
