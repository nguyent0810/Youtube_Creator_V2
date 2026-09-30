/* HỒ SƠ DÀI 16:9 — engine dựng cảnh từ dữ liệu (window.CASE, do motion/long/build_long.py ghi) cho video dài.
   Anh em ngang của casefile.js: cùng triết lý (mọi mốc đã quy về GIÂY từ mốc từng từ của giọng đọc,
   engine chỉ vẽ), cùng tất định (PRNG có hạt, không Math.random / Date / fetch).
   Video B-roll: thẻ <video> được build_long.py NƯỚNG TĨNH vào HTML (compiler HyperFrames chỉ đếm media
   khai báo tĩnh) — cảnh chỉ tham chiếu bằng s.vid và đẩy/chỉnh khung trên timeline.
   sfx_long.py đặt tiếng động theo CÙNG các mốc + độ lệch ghi chú ở từng loại cảnh. */
(function () {
  const C = window.CASE, DUR = C.dur;
  if (C.accent) document.documentElement.style.setProperty("--red", C.accent);
  const $ = (s) => document.querySelector(s);
  const el = (tag, cls, html, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (parent) parent.appendChild(e); return e; };
  const NS = "http://www.w3.org/2000/svg";
  const sv = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  let seed = C.seed || 1995; const rnd = () => { seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; };
  const norm = (w) => w.toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");
  const fsz = (text, max, width = 1700, k = 0.6) => Math.min(max, Math.floor(width / (Math.max(1, [...text].length) * k)));
  const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;");
  const rich = (t) => esc(t).replace(/\*(.+?)\*/g, "<b>$1</b>");
  const IM = (k) => { const m = C.imgs[k]; if (!m) throw new Error("thiếu ảnh " + k); return m; };
  const px = (v) => v + "px";
  const W = 1920, H = 1080;

  const tl = gsap.timeline({ paused: true });
  const show = (node, t0, t1, fade = 0.25) => {
    if (t0 > 0.001) tl.set(node, { autoAlpha: 0 }, 0);
    if (t0 <= 0.001) { node.style.opacity = 1; node.style.visibility = "visible"; tl.set(node, { autoAlpha: 1 }, 0); }   // khung 0 phải có hình
    else tl.to(node, { autoAlpha: 1, duration: fade, ease: "none" }, t0 - fade * 0.5);
    if (t1 != null && t1 < DUR - 0.01) tl.to(node, { autoAlpha: 0, duration: fade, ease: "none" }, t1 - fade * 0.5);
  };
  const flash = (t, a = 0.5) => { tl.to("#flash", { opacity: a, duration: 0.04 }, Math.max(0, t)); tl.to("#flash", { opacity: 0, duration: 0.25 }, Math.max(0, t) + 0.04); };
  const leak = (t) => { tl.fromTo("#leak", { opacity: 0, x: -1100 }, { opacity: 0.85, x: 0, duration: 0.4, ease: "power2.out", immediateRender: false }, t);
                        tl.to("#leak", { opacity: 0, x: 1100, duration: 0.5, ease: "power2.in" }, t + 0.4); };
  // con dấu: rơi xuống, chạm lúc t+0.16 (sfx: thud ở t+0.16)
  const stamp = (node, t, rot = -8) => { tl.fromTo(node, { opacity: 0, scale: 2.4, rotation: rot }, { opacity: 0.95, scale: 1, rotation: rot, duration: 0.16, ease: "power4.in", immediateRender: false }, t);
                                         tl.to("#stage", { x: 8, duration: 0.03, yoyo: true, repeat: 3 }, t + 0.16); };
  const draw = (node, t, d, ease = "power2.inOut") => { const len = node.getTotalLength(); node.style.strokeDasharray = len; node.style.strokeDashoffset = len;
                                                         tl.to(node, { strokeDashoffset: 0, duration: d, ease }, t); };
  const toneCls = (t) => ({ bw: "bw", sepia: "sepia", color: "color", dim: "dimbg", noir: "noir", night: "night" }[t || "sepia"]);
  const circleMark = (svg, x, y, r, t) => {
    const p = sv("path", { d: `M${x + r} ${y - 2} C${x + r} ${y - r - 6} ${x - r - 4} ${y - r} ${x - r} ${y + 2} C${x - r + 2} ${y + r + 4} ${x + r + 6} ${y + r} ${x + r - 2} ${y - 6}`,
      stroke: "var(--red)", "stroke-width": Math.max(4, r / 7), fill: "none", "stroke-linecap": "round" }, svg);
    draw(p, t, 0.25, "steps(5)");
  };
  const stage = $("#stage");
  const B = {};

  /* ---- lớp phủ dùng chung cho mọi cảnh ----
     label {k, v, s, at}: nhãn góc dưới trái (sfx: tick ở at)
     tag {text, at}: thẻ tang vật góc trên trái; credit: dòng ghi nguồn ảnh; illus: "ẢNH/VIDEO MINH HỌA"
     stamp {text, at, x, y, rot}: con dấu (sfx: thud ở at+0.16) */
  const common = (s, d) => {
    if (s.label && typeof s.label === "object") { const lb = el("div", "lower", null, d);
      if (s.label.k) el("div", "k", esc(s.label.k), lb);
      if (s.label.v) { const v = el("div", "v", esc(s.label.v), lb); v.style.fontSize = px(fsz(s.label.v, 54, 1300, 0.58)); }
      if (s.label.s) el("div", "s", esc(s.label.s), lb);
      tl.fromTo(lb, { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out", immediateRender: false }, s.label.at ?? s.t0 + 0.4); }
    if (s.tag) { const tg = el("div", "tagt", esc(s.tag.text || s.tag), d);
      tl.fromTo(tg, { opacity: 0, y: -24 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)", immediateRender: false }, s.tag.at ?? s.t0 + 0.25); }
    const ck = s.img || s.bg, ci = ck && C.imgs[ck];
    const ctext = typeof s.credit === "string" ? s.credit : (s.credit !== false && ci && ci.lic) ? ("ẢNH: " + (ci.pd ? "TƯ LIỆU · PHẠM VI CÔNG CỘNG" : (ci.by ? ci.by.toUpperCase().slice(0, 40) + " · " : "") + ci.lic.toUpperCase())) : null;
    if (ctext) { const c = el("div", "credit", esc(ctext), d); tl.to(c, { opacity: 1, duration: 0.4 }, s.t0 + 0.3); }
    if (s.illus) el("div", "illus", s.illus === true ? "ẢNH MINH HỌA" : esc(s.illus), d);
    if (s.stamp) { const st = el("div", "stamp" + (s.stamp.ink ? " ink" : ""), esc(s.stamp.text), d); st.style.fontSize = px(fsz(s.stamp.text, 84, 760, 0.72));
      st.style.left = px(s.stamp.x ?? 1150); st.style.top = px(s.stamp.y ?? 560); stamp(st, s.stamp.at, s.stamp.rot ?? -8); }
  };

  /* ---- nền video (B-roll) cho mọi cảnh có s.vid: đẩy máy chậm + màn che ---- */
  const vidbg = (s, d, veil) => {
    const v = document.getElementById(s.vid); if (!v) throw new Error("thiếu video " + s.vid);
    const dur = Math.max(0.2, s.t1 - s.t0 + 0.3), z0 = s.z0 ?? 1.07, z1 = s.z1 ?? 1.0, dx = s.pan === "l" ? 50 : s.pan === "r" ? -50 : 0;
    tl.fromTo(v, { scale: z0, x: dx }, { scale: z1, x: -dx, duration: dur, ease: "none", immediateRender: false }, s.t0 - 0.15);
    const vl = el("div", "veil", null, d);
    vl.style.background = `linear-gradient(90deg, rgba(5,4,4,${veil + 0.12}) 0%, rgba(5,4,4,${veil}) 55%, rgba(5,4,4,${Math.max(0, veil - 0.1)}) 100%)`;
  };
  const imgbg = (s, d, key, veil = 0.6) => {   // nền ảnh tĩnh mờ cho cảnh chữ
    const m = IM(key), im = el("img", "abs " + toneCls(s.bgTone || "dim"), null, d); im.src = m.src; const k = Math.max(W / m.w, H / m.h);
    Object.assign(im.style, { width: px(m.w * k), height: px(m.h * k), left: px(W / 2 - m.w * k / 2), top: px(H / 2 - m.h * k / 2), opacity: 1 - veil * 0.5 });
    tl.fromTo(im, { scale: 1.1 }, { scale: 1.0, duration: Math.max(0.2, s.t1 - s.t0), ease: "none", immediateRender: false }, s.t0);
  };
  const bg = (s, d, veil) => { if (s.vid) vidbg(s, d, veil); else if (s.bg) imgbg(s, d, s.bg, veil); };

  /* ---------- chapter: thẻ chương — số khổng lồ viền, tiêu đề, vạch đỏ ----------
     sfx: t0 -> boom trầm + whoosh; titleAt -> thud */
  B.chapter = (s, d) => {
    bg(s, d, 0.62);
    const no = el("div", "chno", esc(s.no), d);
    const k = el("div", "chk", esc(s.k || "CHƯƠNG " + s.no), d);
    const lines = (s.title || "").split("\n"), fs = fsz(lines.reduce((a, b) => (a.length > b.length ? a : b)), 120, 1650, 0.6);
    const tt = el("div", "cht", lines.map(esc).join("<br/>"), d); tt.style.fontSize = px(fs);
    const bar = el("div", "chbar", null, d); const by = 650 + fs * 1.02 * lines.length + 26; Object.assign(bar.style, { top: px(by), width: px(260) });
    let sb; if (s.sub) { sb = el("div", "chs", esc(s.sub), d); sb.style.top = px(by + 34); }
    const ta = s.titleAt ?? s.t0 + 0.35;
    tl.fromTo(no, { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.8, ease: "power3.out", immediateRender: false }, s.t0 + 0.05);
    tl.to(no, { x: 40, duration: Math.max(0.3, s.t1 - s.t0 - 0.8), ease: "none" }, s.t0 + 0.85);
    tl.fromTo(k, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, s.t0 + 0.2);
    tl.fromTo(tt, { opacity: 0, y: 40, clipPath: "inset(0% 0% 100% 0%)" }, { opacity: 1, y: 0, clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.out", immediateRender: false }, ta - 0.05);
    tl.fromTo(bar, { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power3.inOut", immediateRender: false }, ta + 0.25);
    if (sb) tl.fromTo(sb, { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, ta + 0.5);
  };

  /* ---------- broll: video tư liệu tràn khung + chữ phủ tuỳ chọn ----------
     sfx: không (nền nhạc lo); kin.at -> thud nhẹ */
  B.broll = (s, d) => { vidbg(s, d, s.veil ?? 0.28); if (s.kin) kinetic(s.kin, d, s.align); common(s, d); };

  /* ---------- photo: ảnh tư liệu tràn khung, Ken Burns theo tiêu điểm ----------
     sfx: t0 -> màn trập + boom nhẹ; circle.at -> scratch */
  B.photo = (s, d) => {
    const m = IM(s.img), fx = (s.focus || [0.5, 0.4])[0], fy = (s.focus || [0.5, 0.4])[1];
    const area = el("div", "abs", null, d); Object.assign(area.style, { left: 0, top: 0, width: px(W), height: px(H), overflow: "hidden" });
    const k = Math.max(W / m.w, H / m.h), iw = m.w * k, ih = m.h * k;
    const il = Math.min(0, Math.max(W - iw, W / 2 - fx * iw)), it = Math.min(0, Math.max(H - ih, H / 2 - fy * ih));
    const holder = el("div", "phw", null, area); Object.assign(holder.style, { left: 0, top: 0, width: px(W), height: px(H), transformOrigin: `${il + fx * iw}px ${it + fy * ih}px` });
    const im = el("img", toneCls(s.tone || "sepia"), null, holder); im.src = m.src; Object.assign(im.style, { left: px(il), top: px(it), width: px(iw), height: px(ih) });
    const svg = sv("svg", { width: W, height: H }, holder);
    (s.circles || []).forEach((c) => circleMark(svg, il + c.x * iw, it + c.y * ih, c.r || 60, c.at));
    const mv = s.move || "in", dur = Math.max(0.3, s.t1 - s.t0 + 0.3);
    const from = mv === "out" ? { scale: 1.14 } : mv === "pan" ? { scale: 1.12, x: 60 } : { scale: 1.0 };
    const to = mv === "out" ? { scale: 1.0 } : mv === "pan" ? { scale: 1.12, x: -60 } : { scale: 1.12 };
    tl.fromTo(holder, from, { ...to, duration: dur, ease: "none", immediateRender: false }, s.t0 - 0.15);
    if (s.veil) { const vl = el("div", "veil", null, d); vl.style.background = `rgba(5,4,4,${s.veil})`; }
    if (s.kin) kinetic(s.kin, d, s.align);
    common(s, d);
  };

  /* ---------- print: ảnh in trên nền mờ của chính nó + khối chữ bên cạnh ----------
     (ảnh dọc / chân dung trong khung ngang). side {k, h, hAt, lines:[{text, at}]}
     sfx: t0 -> whoosh + thud nhẹ lúc ảnh chạm; mỗi line.at -> tick */
  B.print = (s, d) => {
    const m = IM(s.img), right = !!s.right;
    const bgk = Math.max(W / m.w, H / m.h), bgi = el("img", "blurbg", null, d); bgi.src = m.src;
    Object.assign(bgi.style, { width: px(m.w * bgk * 1.1), height: px(m.h * bgk * 1.1), left: px(W / 2 - m.w * bgk * 0.55), top: px(H / 2 - m.h * bgk * 0.55) });
    const k = Math.min((s.maxW || 760) / m.w, (s.maxH || 700) / m.h), iw = Math.round(m.w * k), ih = Math.round(m.h * k);
    const pw = iw + 40, ph = ih + 40 + (s.caption ? 50 : 0), px0 = right ? W - 130 - pw : 130, py0 = Math.round(470 - ph / 2);
    const pr = el("div", "print", null, d); Object.assign(pr.style, { left: px(px0), top: px(Math.max(110, py0)), width: px(pw), height: px(ph) });
    const im = el("img", toneCls(s.tone || "bw"), null, pr); im.src = m.src; Object.assign(im.style, { left: px(20), top: px(20), width: px(iw), height: px(ih) });
    if (s.pos) { im.style.objectFit = "cover"; im.style.objectPosition = s.pos; }
    if (s.caption) { const cp = el("div", "mono", esc(s.caption), pr); Object.assign(cp.style, { position: "absolute", left: "20px", right: "20px", bottom: "14px", textAlign: "center", fontSize: "20px", fontWeight: 700, letterSpacing: ".14em", color: "#3a332b", whiteSpace: "nowrap", overflow: "hidden" }); }
    const svg = sv("svg", { width: pw, height: ph, style: "position:absolute;left:0;top:0;overflow:visible" }, pr);
    (s.circles || []).forEach((c) => circleMark(svg, 20 + c.x * iw, 20 + c.y * ih, c.r || 50, c.at));
    const rot = s.rot ?? (right ? 2 : -2);
    tl.fromTo(pr, { opacity: 0, y: 120, rotation: rot * 3, scale: 1.08 }, { opacity: 1, y: 0, rotation: rot, scale: 1, duration: 0.5, ease: "power3.out", immediateRender: false }, s.t0);
    tl.to(pr, { scale: 1.04, duration: Math.max(0.2, s.t1 - s.t0 - 0.5), ease: "none" }, s.t0 + 0.5);
    if (s.side) {
      const sx = right ? 120 : px0 + pw + 90, sw = right ? px0 - 120 - 90 : W - sx - 110;
      const sd = el("div", "side", null, d); Object.assign(sd.style, { left: px(sx), width: px(sw), top: px(s.side.top ?? 200) });
      if (s.side.k) { const kk = el("div", "k", esc(s.side.k), sd); tl.to(kk, { opacity: 1, duration: 0.3 }, s.t0 + 0.25); }
      if (s.side.h) { const hl = s.side.h.split("\n"); const hh = el("div", "h", hl.map(esc).join("<br/>"), sd);
        hh.style.fontSize = px(fsz(hl.reduce((a, b) => (a.length > b.length ? a : b)), 84, sw, 0.56));
        tl.fromTo(hh, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out", immediateRender: false }, s.side.hAt ?? s.t0 + 0.4); }
      (s.side.lines || []).forEach((q) => { const ln = el("div", "ln", rich(q.text), sd);
        tl.fromTo(ln, { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, q.at - 0.05); });
    }
    common(s, d);
  };

  /* ---------- file: ảnh hồ sơ bên trái + thẻ giấy bên phải, các dòng hiện theo lời ----------
     sfx: t0 -> whoosh; mỗi row.at -> key x2; stamp.at+0.16 -> thud */
  B.file = (s, d) => {
    bg(s, d, 0.72);
    let fp;
    if (s.img) { fp = el("div", "fpic", null, d); const im = el("img", toneCls(s.tone || "bw"), null, fp); im.src = IM(s.img).src; if (s.pos) im.style.objectPosition = s.pos;
      el("div", "cap2", esc(s.cap || s.name.replace("\n", " ")), fp);
      tl.fromTo(fp, { opacity: 0, x: -160, rotation: -8 }, { opacity: 1, x: 0, rotation: -3, duration: 0.5, ease: "power3.out", immediateRender: false }, s.t0); }
    const cd = el("div", "fcard", null, d); el("div", "clip", null, cd); if (!s.img) cd.style.left = px(460);
    el("div", "k", esc(s.k || "HỒ SƠ"), cd);
    const lines = (s.name || "").split("\n"), longest = lines.reduce((a, b) => (a.length > b.length ? a : b), "");
    const n = el("div", "n", lines.map(esc).join("<br/>"), cd); n.style.fontSize = px(fsz(longest, 100, 860, 0.58));
    if (s.desc) el("div", "d", esc(s.desc), cd);
    el("div", "ln", null, cd);
    (s.rows || []).forEach((r) => { const e = el("div", "row", `<span>${esc(r.k)}</span><span>${rich(r.v)}</span>`, cd);
      tl.fromTo(e, { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.28, immediateRender: false }, r.at - 0.05); });
    tl.fromTo(cd, { rotationX: 60, y: 260, opacity: 0, rotation: 4 }, { rotationX: 0, y: 0, opacity: 1, rotation: 1.5, duration: 0.55, ease: "power3.out", transformPerspective: 1600, immediateRender: false }, s.t0 + 0.12);
    tl.to([cd, fp].filter(Boolean), { scale: 1.03, duration: Math.max(0.2, s.t1 - s.t0 - 0.6), ease: "none" }, s.t0 + 0.6);
    common(s, d);
  };

  /* ---------- kinetic: chữ lớn xếp tầng, từng dòng đập vào theo lời ----------
     sfx: mỗi item.at -> thud nhẹ */
  const kinetic = (items, d, align) => {
    const sizes = items.map((q) => q.size || fsz(q.text, q.sm ? 56 : 130, 1650, q.serif ? 0.62 : 0.66)), total = sizes.reduce((a, b) => a + b * 1.22, 0);
    let y = Math.max(130, 470 - total / 2);
    items.forEach((q, k) => { const e = el("div", "kin" + (q.acc ? " acc" : "") + (q.serif ? " serif" : "") + (q.sm ? " sm" : "") + (align === "l" ? " l" : ""), esc(q.text), d);
      Object.assign(e.style, { fontSize: px(sizes[k]), top: px(y) }); y += sizes[k] * 1.22;
      tl.fromTo(e, { opacity: 0, scale: 1.3, y: -16 }, { opacity: 1, scale: 1, y: 0, duration: 0.2, ease: "power4.in", immediateRender: false }, q.at - 0.08); });
  };
  B.kinetic = (s, d) => { bg(s, d, 0.62); kinetic(s.items, d, s.align); common(s, d); };

  /* ---------- slam: một dòng chữ đập mạnh trên nền tư liệu tối ----------
     sfx: at -> boom */
  B.slam = (s, d) => {
    bg(s, d, 0.6);
    const lines = s.text.split("\n"), fs = fsz(lines.reduce((a, b) => (a.length > b.length ? a : b)), 190, 1700, 0.66);
    const sl = el("div", "slam", lines.map(esc).join("<br/>"), d); Object.assign(sl.style, { fontSize: px(fs), top: px(460 - fs * lines.length / 2), lineHeight: 1.02, color: s.white ? "#fff" : "" });
    tl.fromTo(sl, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in", immediateRender: false }, s.at - 0.13);
    if (s.sub) { const sb = el("div", "dsub", esc(s.sub), d); sb.style.top = px(480 + fs * lines.length / 2 + 20); tl.to(sb, { opacity: 1, duration: 0.3 }, s.at + 0.3); }
    tl.to("#stage", { x: 10, duration: 0.03, yoyo: true, repeat: 5 }, s.at + 0.05);
    common(s, d);
  };

  /* ---------- question: câu hỏi lặng (sfx: tắt nền) ---------- */
  B.question = (s, d) => { bg(s, d, 0.75); const a = el("div", "ask", esc(s.text).replace(/\n/g, "<br/>"), d);
    a.style.fontSize = px(fsz(s.text.split("\n").reduce((x, y) => (x.length > y.length ? x : y)), 92, 1600, 0.5));
    tl.fromTo(a, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.45, immediateRender: false }, s.t0 + 0.05); };

  /* ---------- counter: số đếm lớn + nhãn (+ ảnh in bên trái) ----------
     sfx: tick theo từng bước (tối đa 28) từ at tới until; until -> thud */
  const vn = (n) => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  B.counter = (s, d) => {
    bg(s, d, 0.72);
    let cx0 = 0, cw = W;
    if (s.img) { const m = IM(s.img), k = Math.min(600 / m.w, 640 / m.h), w = m.w * k, h = m.h * k;
      const pr = el("div", "print", null, d); Object.assign(pr.style, { left: px(140), top: px(470 - (h + 36) / 2), width: px(w + 36), height: px(h + 36) });
      const im = el("img", toneCls(s.tone || "bw"), null, pr); im.src = m.src; Object.assign(im.style, { left: px(18), top: px(18), width: px(w), height: px(h) });
      tl.fromTo(pr, { opacity: 0, y: 80, rotation: 6 }, { opacity: 1, y: 0, rotation: -2, duration: 0.45, ease: "power3.out", immediateRender: false }, s.imgAt ?? s.t0 + 0.1);
      cx0 = w + 220; cw = W - cx0 - 60; }
    const str = (s.prefix || "") + vn(s.to) + (s.suffix || ""), fs = fsz(str, 260, cw - 80, 0.6);
    const ct = el("div", "count", esc((s.prefix || "") + vn(s.from || 0) + (s.suffix || "")), d); Object.assign(ct.style, { fontSize: px(fs), top: px(s.top ?? 360 - fs / 2 + 40), left: px(cx0), width: px(cw), right: "auto" });
    const top = (s.top ?? 360 - fs / 2 + 40) + fs * 1.06 + 34, o = { v: s.from || 0 };
    tl.fromTo(ct, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, s.at - 0.15);
    tl.to(o, { v: s.to, duration: Math.max(0.2, s.until - s.at), ease: "power2.out", onUpdate: () => { ct.textContent = (s.prefix || "") + vn(o.v) + (s.suffix || ""); } }, s.at);
    if (s.label) { const lb = el("div", "countlbl", esc(s.label), d); Object.assign(lb.style, { top: px(top), left: px(cx0), width: px(cw), right: "auto", fontSize: px(fsz(s.label, 44, cw - 60, 0.82)) });
      tl.fromTo(lb, { opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power3.out", immediateRender: false }, s.labelAt ?? s.until - 0.1); }
    if (s.sub) { const sb = el("div", "countsub", esc(s.sub.text), d); Object.assign(sb.style, { top: px(top + 76), left: px(cx0), width: px(cw), right: "auto" }); tl.to(sb, { opacity: 1, duration: 0.3 }, s.sub.at); }
    common(s, d);
  };

  /* ---------- bars: biểu đồ cột mọc lên theo lời ----------
     sfx: mỗi item.at -> tông lên ngắn + thud nhẹ lúc chạm */
  B.bars = (s, d) => {
    bg(s, d, 0.8);
    const ch = el("div", "bch", null, d); if (s.title) el("div", "t", esc(s.title), ch); if (s.unit) el("div", "u", esc(s.unit), ch);
    el("div", "base", null, ch);
    const n = s.items.length, cw = 1620, slot = cw / n, bw = Math.min(170, slot * 0.56), mx = s.max || Math.max(...s.items.map((q) => q.v)), hmax = 470;
    s.items.forEach((q, k) => { const x = slot * k + slot / 2, h = Math.max(4, hmax * q.v / mx);
      const b = el("div", "bb" + (q.acc ? " acc" : ""), null, ch); Object.assign(b.style, { left: px(x - bw / 2), width: px(bw), height: px(h) });
      const v = el("div", "bv2", esc(q.lbl ?? vn(q.v)), ch); Object.assign(v.style, { left: px(x - 150), width: "300px", bottom: px(63 + h + 10) });
      const kk = el("div", "bk", esc(q.k), ch); Object.assign(kk.style, { left: px(x - 150), width: "300px" });
      tl.to(kk, { opacity: 1, duration: 0.2 }, s.t0 + 0.1 + k * 0.05);
      tl.to(b, { scaleY: 1, duration: 0.5, ease: "power3.out" }, q.at);
      tl.fromTo(v, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, immediateRender: false }, q.at + 0.35); });
    tl.fromTo(ch, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, s.t0);
    common(s, d);
  };

  /* ---------- timeline: mốc năm nằm ngang ----------
     sfx: mỗi item.at -> tick + thud nhẹ */
  B.timeline = (s, d) => {
    bg(s, d, 0.78);
    const n = s.items.length, x0 = 240, x1 = 1680, gap = n > 1 ? (x1 - x0) / (n - 1) : 0;
    const line = el("div", "tlh", null, d); Object.assign(line.style, { left: px(x0 - 60), width: px(x1 - x0 + 120) });
    tl.fromTo(line, { scaleX: 0 }, { scaleX: 1, duration: Math.max(0.4, s.items[n - 1].at - s.t0), ease: "none", immediateRender: false }, s.t0);
    s.items.forEach((q, k) => { const up = k % 2 === 0, e = el("div", "tlp", null, d);
      e.innerHTML = up ? `<div class="yr">${esc(q.year)}</div><div class="tx">${rich(q.text || "")}</div><div class="dot" style="margin-top:22px"></div>`
                       : `<div class="dot" style="margin-bottom:22px"></div><div class="yr">${esc(q.year)}</div><div class="tx">${rich(q.text || "")}</div>`;
      Object.assign(e.style, { left: px(x0 + gap * k) }); if (up) e.style.bottom = px(H - 533); else e.style.top = px(507);
      tl.fromTo(e, { opacity: 0, y: up ? -30 : 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, q.at - 0.1); });
    common(s, d);
  };

  /* ---------- map: biên giới thật tự vẽ, ghim, tuyến ----------
     sfx: t0-0.3 -> whoosh; pin.at -> blip; route at..until -> tông lên */
  B.map = (s, d) => {
    const G = C.geo[s.geo || "main"], svg = sv("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d);
    const borders = G.countries.slice().sort((a, b) => a.focus - b.focus).map((c) => [sv("path", { d: c.d, class: "ctry" + (c.focus ? " focus" : "") }, svg), c.focus]);
    borders.forEach(([p, f], k) => draw(p, s.t0 - 0.05 + (f ? 0.1 : 0) + k * 0.03, f ? 1.0 : 0.7));
    G.countries.filter((c) => c.label && c.lx > 0).forEach((c) => { const t = sv("text", { x: c.lx, y: c.ly, class: "clbl", "text-anchor": "middle" }, svg); t.textContent = c.label;
      tl.fromTo(t, { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, s.t0 + 0.5); });
    const P = (n) => { const p = G.pins.find((q) => q.name === n); if (!p) throw new Error("thiếu ghim " + n); return p; };
    (s.routes || []).forEach((r) => { const a = P(r.from), b = P(r.to), bend = r.bend ?? 0.25;
      const mx = (a.x + b.x) / 2 - (b.y - a.y) * bend, my = (a.y + b.y) / 2 + (b.x - a.x) * bend, dd = `M${a.x} ${a.y} Q${mx} ${my} ${b.x} ${b.y}`;
      const rp = sv("path", { d: dd, stroke: "var(--red)", "stroke-width": 6, fill: "none", "stroke-linecap": "round" }, svg);
      sv("path", { d: dd, stroke: "#060505", "stroke-width": 8, fill: "none", "stroke-dasharray": "2 20" }, svg);
      draw(rp, r.at, Math.max(0.3, r.until - r.at), "power1.inOut"); });
    (s.pins || []).forEach((q) => { const p = P(q.name), g = sv("g", {}, svg);
      const ring = sv("circle", { cx: p.x, cy: p.y, r: 30, fill: "none", stroke: "var(--red)", "stroke-width": 4 }, g);
      sv("circle", { cx: p.x, cy: p.y, r: 13, fill: "var(--red)" }, g);
      const lbl = q.label || p.label || p.name, lw = [...lbl].length * 18 + 40;
      let side = q.side || "r";
      if (side === "r" && p.x + lw > W - 40) side = "l";
      if (side === "l" && p.x - lw < 40) side = "r";
      const tx = side === "r" ? p.x + 36 : side === "l" ? p.x - 36 : p.x, ta = side === "r" ? "start" : side === "l" ? "end" : "middle";
      const t = sv("text", { x: tx, y: side === "t" ? p.y - 48 : p.y + 10, class: "pinlbl", "text-anchor": ta }, g); t.textContent = lbl;
      if (q.sub) { const t2 = sv("text", { x: tx, y: (side === "t" ? p.y - 48 : p.y + 10) + 30, class: "pinsub", "text-anchor": ta }, g); t2.textContent = q.sub; }
      tl.fromTo(g, { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.35, ease: "bounce.out", immediateRender: false }, q.at);
      tl.fromTo(ring, { scale: 0.4, transformOrigin: "50% 50%" }, { scale: 2.2, opacity: 0, duration: 0.8, ease: "power2.out", immediateRender: false }, q.at + 0.25); });
    const zt = s.zoom ? P(s.zoom) : null;
    if (zt) tl.to(svg, { scale: s.zoomK || 1.15, transformOrigin: `${(zt.x / 19.2).toFixed(1)}% ${(zt.y / 10.8).toFixed(1)}%`, duration: s.t1 - s.t0, ease: "none" }, s.t0);
    common(s, d);
  };

  /* ---------- quote: trích dẫn gõ máy chữ ----------
     dy=true -> nhãn "DIỄN Ý" (không phải nguyên văn). sfx: key mỗi ký tự (tối đa 40) từ at trong typeDur */
  B.quote = (s, d) => {
    bg(s, d, 0.8);
    const pp = el("div", "qpaper", null, d); el("div", "qm", "“", pp); if (s.dy) el("div", "dy", "DIỄN Ý", pp);
    const qt = el("div", "qt", null, pp); const L = [...s.text].length; qt.style.fontSize = px(L < 70 ? 50 : L < 140 ? 40 : 32);
    const spans = [...s.text].map((ch) => el("span", null, esc(ch), qt));
    spans.forEach((sp, k) => tl.set(sp, { opacity: 1 }, s.at + (k / L) * s.typeDur));
    if (s.by) { const by = el("div", "by", "— " + esc(s.by), pp); tl.to(by, { opacity: 1, duration: 0.3 }, s.at + s.typeDur); }
    tl.fromTo(pp, { opacity: 0, y: 80, rotation: 1.5 }, { opacity: 1, y: 0, rotation: -1, duration: 0.45, ease: "power3.out", immediateRender: false }, s.t0);
    tl.to(pp, { scale: 1.03, duration: Math.max(0.2, s.t1 - s.t0 - 0.45), ease: "none" }, s.t0 + 0.45);
    common(s, d);
  };

  /* ---------- org: sơ đồ "gia đình" — nút theo tầng, dây nối vẽ khi nút hiện ----------
     nodes [{id, t, s, p (id cha), at, cls: top|acc}]. sfx: mỗi node.at -> tick + thud nhẹ */
  B.org = (s, d) => {
    bg(s, d, 0.8);
    const depth = {}, byLv = {};
    s.nodes.forEach((q) => { depth[q.id] = q.p ? depth[q.p] + 1 : 0; (byLv[depth[q.id]] = byLv[depth[q.id]] || []).push(q); });
    const lv = Object.keys(byLv).length, y0 = s.y0 ?? 150, gy = Math.min(200, (820 - y0) / Math.max(1, lv - 1 || 1));
    const pos = {};
    Object.entries(byLv).forEach(([L, arr]) => { const n = arr.length, span = Math.min(1700, n * 420); arr.forEach((q, k) => { pos[q.id] = { x: W / 2 - span / 2 + span * (k + 0.5) / n, y: y0 + L * gy }; }); });
    const svg = sv("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d);
    s.nodes.forEach((q) => {
      const P = pos[q.id], e = el("div", "onode" + (q.cls ? " " + q.cls : ""), `<div class="t">${esc(q.t)}</div>${q.s ? `<div class="s">${esc(q.s)}</div>` : ""}`, d);
      Object.assign(e.style, { left: px(P.x), top: px(P.y) });
      tl.fromTo(e, { opacity: 0, y: -20, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, q.at);
      if (q.p) { const A = pos[q.p], ln = sv("path", { d: `M${A.x} ${A.y + 86} C${A.x} ${A.y + 86 + gy * 0.4} ${P.x} ${P.y - gy * 0.4} ${P.x} ${P.y}`, class: "oline" }, svg); draw(ln, q.at - 0.25, 0.3); }
    });
    common(s, d);
  };

  /* ---------- ledger: sổ sách tiền ----------
     sfx: mỗi row.at -> key x3; total.at -> thud */
  B.ledger = (s, d) => {
    bg(s, d, 0.8);
    const lg = el("div", "ledger", null, d); if (s.title) el("div", "lt", esc(s.title), lg);
    const rows = [...(s.rows || []), ...(s.total ? [{ ...s.total, tot: true }] : [])];
    rows.forEach((r) => { const e = el("div", "row" + (r.tot ? " tot" : ""), `<span>${esc(r.k)}</span><span>${esc(r.v)}</span>`, lg);
      tl.fromTo(e, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25, immediateRender: false }, r.at - 0.05); });
    tl.fromTo(lg, { opacity: 0, y: 80, rotation: 1.5 }, { opacity: 1, y: 0, rotation: -1, duration: 0.4, ease: "power3.out", immediateRender: false }, s.t0);
    common(s, d);
  };

  /* ---------- split: hai ảnh đối chiếu + dấu ----------
     sfx: a.at, b.at -> thud; signAt -> boom */
  B.split = (s, d) => {
    bg(s, d, 0.82);
    if (s.title) { const t = el("div", "spt", esc(s.title), d); t.style.fontSize = px(fsz(s.title, 44, 1700, 0.6)); tl.fromTo(t, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, immediateRender: false }, s.t0); }
    [["a", 300, -3], ["b", 1060, 3]].forEach(([key, left, rot]) => { const q = s[key]; const w = el("div", "splitw", null, d); w.style.left = px(left);
      const pr = el("div", "print", null, w); const im = el("img", toneCls(q.tone || "bw"), null, pr); im.src = IM(q.img).src; if (q.pos) im.style.objectPosition = q.pos;
      const lb = el("div", "lb", esc(q.label || ""), pr); lb.style.fontSize = px(fsz(q.label || "", 26, 500, 0.62));
      tl.fromTo(w, { opacity: 0, y: 120, rotation: rot * 3 }, { opacity: 1, y: 0, rotation: rot, duration: 0.4, ease: "power3.out", immediateRender: false }, q.at - 0.2); });
    if (s.sign) { const sg = el("div", "sign", esc(s.sign), d); tl.fromTo(sg, { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in", immediateRender: false }, s.signAt - 0.1); }
    common(s, d);
  };

  /* ---------- date: chữ gõ + số lật ----------
     sfx: mỗi ký tự dayAt+k*0.045 -> key; mỗi nhóm số groupAt -> 8 tick trong 0.55s; stamp.at+0.16 -> thud */
  B.date = (s, d) => {
    bg(s, d, 0.62);
    if (s.day) { const dy = el("div", "day", null, d);
      [...s.day].forEach((ch, k) => { const sp = el("span", null, ch === " " ? "&nbsp;" : esc(ch), dy); sp.style.opacity = 0; tl.set(sp, { opacity: 1 }, s.dayAt + k * 0.045); }); }
    const chars = [...s.date], D = chars.filter((c) => /\d/.test(c)).length, P = chars.length - D;
    const cw = Math.min(130, Math.floor((1600 - P * 44 - chars.length * 8) / Math.max(1, D))), fz = Math.min(160, Math.floor(cw * 1.3));
    const row = el("div", "date", null, d);
    const groups = [[]];
    chars.forEach((ch) => {
      if (!/\d/.test(ch)) { const sp = el("div", "dsep", ch === " " ? "&nbsp;" : esc(ch), row); sp.style.width = px(ch === " " ? 24 : 44); sp.style.fontSize = px(fz * 0.85); groups.push([]); return; }
      const g = el("div", "dg", null, row); g.style.width = px(cw); const r = el("div", "reel", null, g); const fin = +ch;
      const seq = []; for (let k = 0; k < 9; k++) seq.push((fin + 1 + k * 3) % 10); seq.push(fin);
      seq.forEach((v) => { const e = el("div", null, String(v), r); e.style.fontSize = px(fz); }); groups[groups.length - 1].push(r);
    });
    tl.set(row, { opacity: 0 }, 0); tl.to(row, { opacity: 1, duration: 0.15 }, s.groupAt[0] - 0.1);
    groups.filter((g) => g.length).forEach((g, gi) => g.forEach((r, j) => tl.fromTo(r, { y: 0 }, { y: -9 * 200, duration: 0.55, ease: "power3.out", immediateRender: false }, s.groupAt[gi] - 0.05 + j * 0.07)));
    if (s.sub) { const sb = el("div", "dsub", esc(s.sub.text), d); sb.style.top = px(600); tl.to(sb, { opacity: 1, duration: 0.3 }, s.sub.at); }
    common(s, d);
  };

  /* ---------- cards: ván Oicho-Kabu 8-9-3 — lật bài, đọc YA-KU-ZA, cộng 20, ra 0 điểm ----------
     sfx: mỗi flip.at -> whoosh ngắn + tick; sumAt -> thud; zeroAt -> boom */
  B.cards = (s, d) => {
    bg(s, d, 0.7);
    const n = s.cards.length, cw = 250, gap = 90, x0 = W / 2 - (n * cw + (n - 1) * gap) / 2;
    s.cards.forEach((v, k) => { const c = el("div", "okc", null, d); c.style.left = px(x0 + k * (cw + gap));
      const inn = el("div", "in", null, c); el("div", "b", null, inn); el("div", "f", esc(v), inn);
      tl.fromTo(c, { opacity: 0, y: -200, rotation: (k - 1) * 8 }, { opacity: 1, y: 0, rotation: (k - 1) * 3, duration: 0.35, ease: "power3.out", immediateRender: false }, s.t0 + 0.1 + k * 0.12);
      tl.to(inn, { rotationY: 180, duration: 0.45, ease: "power2.inOut" }, s.flips[k]);
      if (s.reads) { const rd = el("div", "rd", esc(s.reads[k]), c); tl.to(rd, { opacity: 1, duration: 0.25 }, s.readAt ? s.readAt[k] - 0.05 : s.flips[k] + 0.35); } });
    if (s.sumAt != null) { const sm = el("div", "oksum", `${esc(s.cards.join(" + "))} = <em>${esc(s.sum)}</em>`, d);
      tl.fromTo(sm, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, immediateRender: false }, s.sumAt - 0.1);
      if (s.zeroAt != null) { tl.to(sm, { opacity: 0, duration: 0.15 }, s.zeroAt - 0.15);
        const z = el("div", "oksum", `<em>${esc(s.zero)}</em>`, d); z.style.fontSize = "120px"; tl.fromTo(z, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in", immediateRender: false }, s.zeroAt - 0.1); } }
    common(s, d);
  };

  /* ---------- evidence: tang vật dưới đèn + nhãn chú thích ----------
     sfx: t0 -> màn trập; mỗi callout.at -> tick */
  B.evidence = (s, d) => {
    el("div", "evbg", null, d);
    const m = IM(s.img), k = Math.min((s.maxW || 900) / m.w, (s.maxH || 700) / m.h), w = m.w * k, h = m.h * k, L = W / 2 - w / 2, T = Math.max(120, 470 - h / 2);
    const holder = el("div", "phw", null, d); Object.assign(holder.style, { left: px(L), top: px(T), width: px(w), height: px(h) });
    const im = el("img", toneCls(s.tone || "color"), null, holder); im.src = m.src; Object.assign(im.style, { left: 0, top: 0, width: px(w), height: px(h), boxShadow: "0 40px 120px rgba(0,0,0,.9)" });
    tl.fromTo(holder, { opacity: 0, scale: 1.1 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out", immediateRender: false }, s.t0);
    tl.to(holder, { scale: 1.05, duration: Math.max(0.2, s.t1 - s.t0 - 0.5), ease: "none" }, s.t0 + 0.5);
    const svg = sv("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d);
    (s.callouts || []).forEach((c) => { const x = L + c.x * w, y = T + c.y * h, right = (c.side || (c.x < 0.5 ? "l" : "r")) === "r", lx = right ? L + w + 70 : L - 70;
      const ln = sv("path", { d: `M${x} ${y} L${lx} ${y}`, stroke: "#fff", "stroke-width": 3, fill: "none" }, svg); sv("circle", { cx: x, cy: y, r: 9, fill: "var(--red)" }, svg);
      draw(ln, c.at, 0.25);
      const co = el("div", "co", esc(c.text), d); Object.assign(co.style, right ? { left: px(lx + 6), top: px(y - 22) } : { right: px(W - lx + 6), top: px(y - 22) });
      tl.to(co, { opacity: 1, duration: 0.2 }, c.at + 0.2); });
    common(s, d);
  };

  // ---------- dựng cảnh ----------
  C.scenes.forEach((s, i) => {
    const d = el("div", "scene", null, stage); show(d, s.t0, s.t1, s.type === "question" ? 0.12 : s.fade ?? 0.3);
    if (!B[s.type]) throw new Error("loại cảnh lạ: " + s.type);
    B[s.type](s, d);
    if (i > 0) { const tr = s.tr || (s.type === "chapter" ? "leak" : "cut"); if (tr === "leak") leak(s.t0 - 0.1); else if (tr === "flash") flash(s.t0, 0.3); }
  });

  // ---------- không khí ----------
  for (let i = 0; i < 30; i++) { const m = el("div", "mote", null, $("#motes")); Object.assign(m.style, { left: px(rnd() * W), top: px(rnd() * H), transform: `scale(${0.5 + rnd() * 1.4})` });
    tl.to(m, { y: -120 - rnd() * 220, x: (rnd() - 0.5) * 200, opacity: 0.15 + rnd() * 0.5, duration: DUR, ease: "none" }, 0); }
  tl.fromTo("#prog i", { scaleX: C.prog0 || 0 }, { scaleX: C.prog1 || 1, duration: DUR, ease: "none" }, 0);
  for (let k = 0; k < Math.ceil(DUR * 2); k++) tl.set("#grain", { opacity: 0.07 + ((k * 37) % 7) / 100 }, k * 0.5);
  $("#hud .t").innerHTML = (C.hud.k ? `<b>${esc(C.hud.k)}</b>` : "") + esc(C.hud.t || "");

  // ---------- phụ đề: cụm tối đa 7 từ, một màu nhấn ----------
  const ACC = new Set((C.acc || []).map(norm));
  const caps = $("#caps"), chunks = [];
  C.lines.forEach((ln) => { let cur = []; ln.words.forEach((w, k) => { cur.push(w);
    const n = cur.length, punct = /[.,…?!:;]$/.test(w.w);
    if ((punct && n >= 2) || n >= 7 || k === ln.words.length - 1) { chunks.push(cur); cur = []; } }); });
  chunks.forEach((c, n) => { const box = el("div", "cap", null, caps);
    c.forEach((w) => { const clean = w.w.replace(/["“”]/g, ""), acc = ACC.has(norm(w.w)) || /\d/.test(w.w);
      const sp = el("span", "cw" + (acc ? " acc" : ""), esc(clean), box); tl.to(sp, { opacity: 1, duration: 0.08 }, w.t); });
    box.style.fontSize = px(fsz(c.map((w) => w.w).join(" "), 44, 1560, 0.52));
    const t0 = c[0].t - 0.06, nx = chunks[n + 1], t1 = nx ? Math.min(nx[0].t - 0.06, c[c.length - 1].t + c[c.length - 1].d + 0.6) : DUR;
    tl.set(box, { opacity: 1 }, t0); tl.set(box, { opacity: 0 }, t1); });
  C.scenes.filter((s) => s.type === "question" || s.type === "chapter" || s.nocaps).forEach((s) => { tl.set("#caps", { opacity: 0 }, s.t0 - 0.01); tl.set("#caps", { opacity: 1 }, s.t1); });

  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = tl;
})();
