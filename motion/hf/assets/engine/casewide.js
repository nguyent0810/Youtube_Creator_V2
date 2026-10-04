/* HỒ SƠ DÀI 16:9 — engine dựng cảnh từ dữ liệu (window.CASE, do motion/long/build_long.py ghi) cho video dài.
   Anh em ngang của casefile.js: cùng triết lý (mọi mốc đã quy về GIÂY từ mốc từng từ của giọng đọc,
   engine chỉ vẽ), cùng tất định (PRNG có hạt, không Math.random / Date / fetch).
   Video B-roll: thẻ <video> được build_long.py NƯỚNG TĨNH vào HTML (compiler HyperFrames chỉ đếm media
   khai báo tĩnh) — cảnh chỉ tham chiếu bằng s.vid và đẩy/chỉnh khung trên timeline.
   sfx_long.py đặt tiếng động theo CÙNG các mốc + độ lệch ghi chú ở từng loại cảnh. */
(function () {
  const C = window.CASE, DUR = C.dur;
  if (C.accent) document.documentElement.style.setProperty("--red", C.accent);
  if (C.look) Object.entries(C.look.vars || {}).forEach(([k, v]) => document.documentElement.style.setProperty(k, v));   // diện mạo riêng từng video (motion/variety.py)
  if (C.look && C.look.vars && C.look.vars["--bed1"])   // nền theo look, kể cả theme noir/shanghai (vốn ghi cứng màu nền)
    document.getElementById("bed").style.background = `radial-gradient(110% 90% at 50% 30%, ${C.look.vars["--bed1"]} 0%, ${C.look.vars["--bed2"]} 55%, #040303 100%)`;
  const $ = (s) => document.querySelector(s);
  const el = (tag, cls, html, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (parent) parent.appendChild(e); return e; };
  const ROOT = document.getElementById("root");
  if (C.theme) ROOT.classList.add("th-" + C.theme);
  if (C.theme === "noir") { el("div", "lbx t", null, ROOT); el("div", "lbx b", null, ROOT); el("div", "layer", null, ROOT).id = "flick"; }   // khung điện ảnh + nhấp nháy phim
  if (C.theme === "shanghai") { const dc = el("div", null, '<i class="a"></i><i class="b"></i><i class="c"></i><i class="d"></i>', ROOT); dc.id = "deco";
    el("div", "layer", null, ROOT).id = "flick"; }   // khung deco mạ vàng
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
    // film: tư liệu cũ -> nhấp nháy sáng tối 12 hình/giây + vệt xước dọc (sfx: tiếng máy chiếu)
    if (s.film && $("#flick")) { const n = Math.ceil((s.t1 - s.t0) * 12);
      for (let k = 0; k < n; k++) tl.set("#flick", { opacity: rnd() * 0.07 }, s.t0 + k / 12);
      tl.set("#flick", { opacity: 0 }, s.t1);
      for (let j = 0; j < 2; j++) { const sc = el("div", "scr", null, d); sc.style.left = px(200 + rnd() * 1500);
        for (let k = 0; k < n; k += 2) tl.set(sc, { opacity: rnd() > 0.55 ? 0.6 : 0, x: (rnd() - 0.5) * 30 }, s.t0 + k / 12); } }
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
  const HAN = ["〇", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "十三", "十四", "十五", "十六"];
  // thẻ chương deco (theme shanghai): số Hán tự viền vàng, quạt deco, tiêu đề giữa. sfx giống chapter thường
  const decoChapter = (s, d) => {
    bg(s, d, 0.7);
    const w = el("div", "dch", null, d); el("div", "fan", null, w);
    const num = el("div", "num", esc(s.num || HAN[+s.no] || s.no), w);
    const k = el("div", "k", esc(s.k || "CHƯƠNG " + s.no), w);
    const lines = (s.title || "").split("\n"), fs = fsz(lines.reduce((a, b) => (a.length > b.length ? a : b)), 104, 1500, 0.58);
    const tt = el("div", "t", lines.map(esc).join("<br/>"), w); tt.style.fontSize = px(fs);
    const rule = el("div", "rule", null, w);
    let sb; if (s.sub) sb = el("div", "s", esc(s.sub), w);
    const ta = s.titleAt ?? s.t0 + 0.35;
    tl.fromTo(num, { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.9, ease: "power3.out", immediateRender: false }, s.t0 + 0.05);
    tl.fromTo(k, { opacity: 0, letterSpacing: "1em" }, { opacity: 1, letterSpacing: "0.5em", duration: 0.6, immediateRender: false }, s.t0 + 0.25);
    tl.fromTo(tt, { opacity: 0, y: 30, clipPath: "inset(0% 0% 100% 0%)" }, { opacity: 1, y: 0, clipPath: "inset(0% 0% 0% 0%)", duration: 0.55, ease: "power3.out", immediateRender: false }, ta - 0.05);
    tl.fromTo(rule, { width: 0 }, { width: 520, duration: 0.6, ease: "power2.inOut", immediateRender: false }, ta + 0.2);
    if (sb) tl.fromTo(sb, { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, ta + 0.5);
    tl.to(w, { scale: 1.04, duration: Math.max(0.3, s.t1 - s.t0), ease: "none" }, s.t0);
  };

  B.chapter = (s, d) => {
    if (C.theme === "shanghai" && !s.classic) return decoChapter(s, d);
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
  const { BEAT, SLAM, beat } = makeBeat({ tl, el, esc, rnd });   // beat.js: thư viện hiệu ứng chữ dùng chung với casefile

  const kinetic = (items, d, align) => {
    const sizes = items.map((q) => q.size || fsz(q.text, q.sm ? 56 : 130, 1650, q.serif ? 0.62 : 0.66)), total = sizes.reduce((a, b) => a + b * 1.22, 0);
    let y = Math.max(130, 470 - total / 2);
    items.forEach((q, k) => { const e = el("div", "kin" + (q.acc ? " acc" : "") + (q.serif ? " serif" : "") + (q.sm ? " sm" : "") + (align === "l" ? " l" : ""), esc(q.text), d);
      Object.assign(e.style, { fontSize: px(sizes[k]), top: px(y) }); y += sizes[k] * 1.22;
      beat(e, q); });
  };
  B.kinetic = (s, d) => { bg(s, d, 0.62);
    const it = s.items.map((q) => ({ ...q })), f = it.reduce((a, q) => (q.at < a.at ? q : a), it[0]);
    if (f.at - s.t0 > 2.0) f.at = s.t0 + 0.5;   // dòng đầu đến muộn -> hiện sớm làm tiêu đề, tránh màn trống
    kinetic(it, d, s.align); common(s, d); };

  /* ---------- slam: một dòng chữ đập mạnh trên nền tư liệu tối ----------
     sfx: at -> boom (theo fx, xem sfx_long.py) */
  B.slam = (s, d) => {
    bg(s, d, 0.6);
    const lines = s.text.split("\n"), fs = fsz(lines.reduce((a, b) => (a.length > b.length ? a : b)), 190, 1700, 0.66);
    const sl = el("div", "slam", lines.map(esc).join("<br/>"), d); Object.assign(sl.style, { fontSize: px(fs), top: px(460 - fs * lines.length / 2), lineHeight: 1.02, color: s.white ? "#fff" : "" });
    if (s.fx && s.fx !== "punch" && SLAM[s.fx]) { SLAM[s.fx](sl, s, fs, lines);
      if (s.sub) { const sb = el("div", "dsub", esc(s.sub), d); sb.style.top = px(480 + fs * lines.length / 2 + 20); tl.to(sb, { opacity: 1, duration: 0.3 }, s.at + 0.3); }
      common(s, d); return; }
    if (s.at - s.t0 > 1.6) {   // cú đập đến muộn -> chữ hiện mờ trước (khỏi trống màn), rồi mới đập
      tl.fromTo(sl, { opacity: 0, scale: 1.04 }, { opacity: 0.16, scale: 1, duration: 0.6, immediateRender: false }, s.t0 + 0.2);
      tl.to(sl, { scale: 1.6, duration: 0.01 }, s.at - 0.14);
      tl.to(sl, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }, s.at - 0.13);
    } else tl.fromTo(sl, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in", immediateRender: false }, s.at - 0.13);
    if (s.sub) { const sb = el("div", "dsub", esc(s.sub), d); sb.style.top = px(480 + fs * lines.length / 2 + 20); tl.to(sb, { opacity: 1, duration: 0.3 }, s.at + 0.3); }
    tl.to("#stage", { x: 10, duration: 0.03, yoyo: true, repeat: 5 }, s.at + 0.05);
    common(s, d);
  };

  /* ---------- brand: logo kênh 2–3 giây, đặt ngay sau cold open (câu "Đây là hồ sơ X") ----------
     {sub: "HỒ SƠ · TAM GIÁC VÀNG", bg?}. Vạch đỏ mọc giữa màn, chữ tên kênh tách từ tâm ra, dòng hồ sơ gõ chữ.
     sfx (sfx_long): whoosh trước t0, âm hiệu 2 nốt + ngân chuông; nhạc nền được né trong cảnh này. */
  const BRAND = "INTO THE KILLER’S MIND";
  B.brand = (s, d) => {
    if (s.bg) bg(s, d, 0.86); else el("div", "brbg", null, d);
    const t0 = s.t0, bar = el("div", "brbar", null, d), wm = el("div", "brwm", esc(s.name || BRAND), d);
    const sub = el("div", "brsub", "", d), rule = el("div", "brrule", null, d), txt = s.sub || "";
    tl.fromTo(bar, { scaleY: 0 }, { scaleY: 1, duration: 0.28, ease: "power3.out", immediateRender: false }, t0 + 0.02);
    tl.to(bar, { scaleX: 60, opacity: 0, duration: 0.35, ease: "power2.in" }, t0 + 0.32);
    tl.fromTo(wm, { opacity: 0, letterSpacing: "0.6em", clipPath: "inset(0 50% 0 50%)", filter: "blur(10px)" },
      { opacity: 1, letterSpacing: "0.14em", clipPath: "inset(0 0% 0 0%)", filter: "blur(0px)", duration: 0.7, ease: "expo.out", immediateRender: false }, t0 + 0.38);
    tl.fromTo(rule, { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power3.inOut", immediateRender: false }, t0 + 0.75);
    const chars = [...txt], span = Math.min(0.7, 0.04 * chars.length);
    for (let k = 1; k <= chars.length; k++) tl.set(sub, { textContent: chars.slice(0, k).join("") }, t0 + 0.95 + span * (k / chars.length));
    tl.to(wm, { scale: 1.035, duration: Math.max(0.3, s.t1 - t0 - 0.4), ease: "none" }, t0 + 0.4);
    if ($("#flick")) for (let k = 0; k < 10; k++) tl.set("#flick", { opacity: rnd() * 0.06 }, t0 + 0.38 + k / 12);
  };

  /* ---------- endcard: 20 giây cuối cho end screen của YouTube (gắn trong Studio) ----------
     Chừa ô video "XEM TIẾP" bên trái và ô tròn "ĐĂNG KÝ" bên phải đúng chỗ YouTube đặt phần tử; nền ảnh tư liệu tối dần. */
  B.endcard = (s, d) => {
    if (s.bg) bg(s, d, 0.88); else el("div", "brbg", null, d);
    const wm = el("div", "ecwm", esc(BRAND), d), sub = el("div", "ecsub", esc(s.sub || "HỒ SƠ TIẾP THEO"), d);
    const box = el("div", "ecbox", "<span>XEM TIẾP</span>", d), cir = el("div", "eccir", "<span>ĐĂNG KÝ</span>", d);
    const note = el("div", "ecnote", esc(s.note || "Cảm ơn bạn đã xem hồ sơ này"), d);
    tl.fromTo(wm, { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out", immediateRender: false }, s.t0 + 0.2);
    tl.fromTo(sub, { opacity: 0 }, { opacity: 1, duration: 0.5, immediateRender: false }, s.t0 + 0.5);
    tl.fromTo([box, cir], { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 0.6, ease: "power3.out", stagger: 0.15, immediateRender: false }, s.t0 + 0.6);
    tl.fromTo(note, { opacity: 0 }, { opacity: 1, duration: 0.6, immediateRender: false }, s.t0 + 1.2);
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
    const pp = el("div", "qpaper", null, d); el("div", "qm", "“", pp); if (s.dy || s.lbl) el("div", "dy", s.lbl || "DIỄN Ý", pp);
    const qt = el("div", "qt", null, pp); const L = [...s.text].length; qt.style.fontSize = px(L < 70 ? 50 : L < 140 ? 40 : 32);
    const spans = [...s.text].map((ch) => el("span", null, esc(ch), qt));
    spans.forEach((sp, k) => tl.set(sp, { opacity: 1 }, s.at + (k / L) * s.typeDur));
    if (s.by) { const by = el("div", "by", "— " + esc(s.by), pp); tl.to(by, { opacity: 1, duration: 0.3 }, s.at - s.t0 > 2.0 ? s.t0 + 0.6 : s.at + s.typeDur); }
    // radio: câu này đọc bằng GIỌNG TRÍCH lọc radio -> sóng âm + nhãn "giọng đọc minh hoạ" (không phải băng ghi âm thật)
    if (s.radio) { el("div", "vt", "GIỌNG ĐỌC MINH HỌA", pp); const wv = el("div", "qwave", null, pp), bars = [];
      for (let k = 0; k < 18; k++) bars.push(el("i", null, null, wv));
      const a = s.voiceAt ?? s.at - 0.2, z = Math.min(s.t1, s.voiceEnd ?? s.at + s.typeDur / 0.75);
      for (let t = a; t < z; t += 0.1) bars.forEach((b) => tl.to(b, { scaleY: 0.15 + rnd() * 0.85, duration: 0.1, ease: "none" }, t));
      tl.to(bars, { scaleY: 0.12, duration: 0.2 }, z); }
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

  /* ================= cảnh riêng của theme noir (Mafia Ý) ================= */
  let UID = 0;

  /* ---------- seismo: băng địa chấn cuộn dưới kim; vụ nổ thành cú vọt đúng hitAt ----------
     {label, read, hit, hitAt}. sfx: kim cào giấy suốt cảnh; hitAt -> boom lớn */
  B.seismo = (s, d) => {
    bg(s, d, 0.85);
    const box = el("div", "seis", null, d);
    if (s.label) el("div", "lb", esc(s.label), box);
    if (s.read) el("div", "rd", esc(s.read), box);
    const NX = 1400, v = 230, dur = s.t1 - s.t0 + 0.5, hitX = NX + v * (s.hitAt - s.t0), L = NX + v * dur + 60, cy = 320;
    let dd = `M0 ${cy}`;
    for (let x = 4; x <= L; x += 4) {
      const r = x - hitX; let a = 2.5 + rnd() * 3;
      if (r > -30 && r < 0) a = 6 + (30 + r) * 0.6;
      if (r >= 0) a = 270 * Math.exp(-r / 260) + 4;
      dd += ` L${x} ${(cy + (rnd() * 2 - 1) * a * (r >= 0 ? 0.6 + 0.4 * Math.abs(Math.sin(r / 9)) : 1)).toFixed(1)}`;
    }
    const svg = sv("svg", { width: W, height: 640, style: "position:absolute;left:0;top:0;overflow:hidden" }, box), id = "sc" + (++UID);
    sv("rect", { x: 0, y: 0, width: NX, height: 640 }, sv("clipPath", { id }, sv("defs", {}, svg)));
    const g = sv("g", {}, sv("g", { "clip-path": `url(#${id})` }, svg));
    sv("path", { d: dd, stroke: "#1a1412", "stroke-width": 2.4, fill: "none", "stroke-linejoin": "round" }, g);
    sv("line", { x1: NX, y1: 40, x2: NX, y2: 600, stroke: "rgba(90,29,22,.5)", "stroke-width": 2 }, svg);
    const pen = sv("circle", { cx: NX, cy, r: 9, fill: "var(--red)" }, svg);
    tl.fromTo(g, { x: 0 }, { x: -v * dur, duration: dur, ease: "none", immediateRender: false }, s.t0);
    for (let k = 0; k < 14; k++) tl.set(pen, { attr: { cy: cy + (rnd() * 2 - 1) * 260 * Math.exp(-k / 5) } }, s.hitAt + k * 0.05);
    tl.set(pen, { attr: { cy } }, s.hitAt + 0.75);
    if (s.hit) { const h = el("div", "hit", esc(s.hit), box); tl.fromTo(h, { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.in", immediateRender: false }, s.hitAt + 0.35); }
    flash(s.hitAt, 0.35); tl.to("#stage", { x: 14, duration: 0.03, yoyo: true, repeat: 9 }, s.hitAt);
    tl.fromTo(box, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, immediateRender: false }, s.t0);
    common(s, d);
  };

  /* ---------- saint: thẻ hình thánh bốc cháy từ đáy lên (lời thề nhập hội) ----------
     {img, burnAt, burnDur, burnTo (% bán kính cháy, mặc định 135 = cháy hết), kin}. sfx: burnAt-0.5 quẹt diêm; burnAt..+burnDur lửa lách tách */
  B.saint = (s, d) => {
    bg(s, d, 0.85);
    const glow = el("div", "glowfire", null, d);
    const c = el("div", "saint", null, d), im = el("img", toneCls(s.tone || "sepia"), null, c); im.src = IM(s.img).src; if (s.pos) im.style.objectPosition = s.pos;
    if (!document.getElementById("burnwarp")) {   // mép cháy răng cưa: bẻ cong vòng lửa bằng nhiễu (mặt nạ vẫn tròn nhưng bị vòng lửa che)
      const svg = sv("svg", { width: 0, height: 0, style: "position:absolute" }, ROOT), f = sv("filter", { id: "burnwarp" }, svg);
      sv("feTurbulence", { type: "fractalNoise", baseFrequency: ".02", numOctaves: 3, seed: 11 }, f); sv("feDisplacementMap", { in: "SourceGraphic", scale: 60 }, f); }
    el("div", "fr", null, c); el("div", "burn", null, c).style.filter = "url(#burnwarp)";
    tl.fromTo(c, { opacity: 0, y: 60, rotation: -3 }, { opacity: 1, y: 0, rotation: -1, duration: 0.6, ease: "power3.out", immediateRender: false }, s.t0);
    tl.to(c, { scale: 1.05, duration: Math.max(0.3, s.t1 - s.t0), ease: "none" }, s.t0 + 0.6);
    tl.fromTo(c, { "--b": "0%" }, { "--b": (s.burnTo ?? 135) + "%", duration: s.burnDur, ease: "power1.in", immediateRender: false }, s.burnAt);
    tl.fromTo(glow, { opacity: 0 }, { opacity: 1, duration: 0.6, immediateRender: false }, s.burnAt - 0.2);
    for (let k = 0; k < Math.round(s.burnDur * 10); k++) tl.set(glow, { opacity: 0.7 + rnd() * 0.3 }, s.burnAt + 0.4 + k * 0.1);
    tl.to(glow, { opacity: 0, duration: 0.8 }, s.burnAt + s.burnDur);
    for (let k = 0; k < 46; k++) { const e = el("div", "ember", null, d), f = k / 46, t = s.burnAt + f * s.burnDur * 0.95;
      Object.assign(e.style, { left: px(W / 2 - 230 + rnd() * 460), top: px(870 - f * 760 + rnd() * 40) });
      tl.fromTo(e, { opacity: 0, x: 0, y: 0 }, { opacity: 1, duration: 0.1, immediateRender: false }, t);
      tl.to(e, { x: (rnd() - 0.5) * 160, y: -(160 + rnd() * 260), opacity: 0, duration: 1.2 + rnd() * 0.8, ease: "power1.out" }, t + 0.1); }
    if (s.kin) kinetic(s.kin, d, s.align);
    common(s, d);
  };

  /* ---------- paper: trang nhất báo MÔ PHỎNG xoáy vào (kiểu phim cũ) ----------
     {mast, date, ed, head (tiếng Ý), vi (dịch), img}. sfx: whoosh xoáy; t0+0.9 -> thud + giấy */
  B.paper = (s, d) => {
    bg(s, d, 0.85);
    const p = el("div", "npaper", null, d);
    el("div", "ms", esc(s.mast || "LA CRONACA"), p);
    el("div", "dl", `<span>${esc(s.date || "")}</span><span>${esc(s.ed || "EDIZIONE STRAORDINARIA")}</span>`, p);
    const hl = s.head.split("\n"), hd = el("div", "hd", hl.map(esc).join("<br/>"), p);
    hd.style.fontSize = px(fsz(hl.reduce((a, b) => (a.length > b.length ? a : b)), 118, 1060, 0.62));
    if (s.vi) el("div", "vi", esc(s.vi), p);
    const cols = el("div", "cols", null, p); el("div", null, null, cols);
    if (s.img) { const ph = el("div", "ph", null, cols); ph.style.backgroundImage = `url(${IM(s.img).src})`; }
    el("div", null, null, cols); el("div", null, null, cols);
    tl.fromTo(p, { opacity: 0, rotation: -540, scale: 0.08 }, { opacity: 1, rotation: -2, scale: 1, duration: 0.9, ease: "power3.out", immediateRender: false }, s.t0);
    tl.to(p, { scale: 1.06, rotation: 0, duration: Math.max(0.3, s.t1 - s.t0 - 0.9), ease: "none" }, s.t0 + 0.9);
    common({ ...s, illus: s.illus ?? "MÔ PHỎNG TRANG BÁO" }, d);
  };

  /* ---------- pizzini: mẩu giấy đánh máy + mật mã chữ -> số (bảng chữ Ý 21 chữ, cộng 3: A=4 … Z=24) ----------
     {notes:[{text, at, x, y, rot, typeDur}], cipher:{word, key, at, decodeAt}}. sfx: key theo ký tự; mỗi số -> tick; decode -> thud */
  const IT = "ABCDEFGHILMNOPQRSTUVZ";
  B.pizzini = (s, d) => {
    bg(s, d, 0.82);
    (s.notes || []).forEach((n) => { const z = el("div", "pz" + (n.text.length < 40 ? " big" : ""), null, d); Object.assign(z.style, { left: px(n.x ?? 700), top: px(n.y ?? 170) });
      const tx = el("div", "tx", null, z), sp = [...n.text].map((ch) => el("span", null, ch === "\n" ? "<br/>" : esc(ch), tx));
      tl.fromTo(z, { opacity: 0, y: 40, rotation: (n.rot ?? -2) * 3 }, { opacity: 1, y: 0, rotation: n.rot ?? -2, duration: 0.35, ease: "power3.out", immediateRender: false }, n.at - 0.4);
      sp.forEach((e, k) => tl.set(e, { opacity: 1 }, n.at + (k / sp.length) * n.typeDur)); });
    if (s.cipher) { const c = s.cipher, row = el("div", "ciph", null, d);
      if (c.key) { const kk = el("div", "ciphk", esc(c.key), d); tl.to(kk, { opacity: 1, duration: 0.3 }, c.at - 0.3); }
      [...c.word].forEach((ch, k) => { const b = el("div", "c", `<div class="n">${IT.indexOf(ch) + 4}</div><div class="l">${esc(ch)}</div>`, row);
        tl.fromTo(b, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.2, immediateRender: false }, c.at + k * 0.18);
        tl.to(b.querySelector(".l"), { opacity: 1, duration: 0.2 }, c.decodeAt + k * 0.15); }); }
    common(s, d);
  };

  /* ---------- dots: mỗi chấm một người; nhóm đổi màu theo lời ----------
     {total, title, cols, groups:[{from, n, cls: red|hollow|gold|ghost, label, at}]}. sfx: rào tick khi hiện; group.at -> tone + thud */
  B.dots = (s, d) => {
    bg(s, d, 0.88);
    const N = s.total, cols = s.cols || Math.ceil(Math.sqrt(N * 2.8)), rows = Math.ceil(N / cols);
    const cell = Math.min(1500 / cols, (s.gh || 500) / rows), r = cell * 0.36, x0 = W / 2 - cols * cell / 2, y0 = s.y0 ?? 230, dots = [];
    for (let k = 0; k < N; k++) { const e = el("div", "dt", null, d);
      Object.assign(e.style, { left: px(x0 + (k % cols) * cell + cell / 2 - r), top: px(y0 + Math.floor(k / cols) * cell + cell / 2 - r), width: px(r * 2), height: px(r * 2), opacity: 0 });
      dots.push(e); tl.set(e, { opacity: 1 }, s.t0 + 0.2 + (k / N) * (s.appearDur ?? 1.2)); }
    if (s.title) { const t = el("div", "dtt", esc(s.title), d); t.style.fontSize = px(fsz(s.title, 60, 1700, 0.6)); tl.to(t, { opacity: 1, duration: 0.3 }, s.t0 + 0.1); }
    const leg = el("div", "dleg", null, d); leg.style.top = px(y0 + rows * cell + 34);
    (s.groups || []).forEach((g) => { const part = dots.slice(g.from || 0, (g.from || 0) + g.n);
      part.forEach((e, k) => tl.set(e, { attr: { class: "dt " + g.cls } }, g.at + (k / part.length) * 0.8));
      if (g.label) { const it = el("div", "g", `<i class="dt ${g.cls}" style="position:static"></i>${esc(g.label)}`, leg); tl.to(it, { opacity: 1, duration: 0.3 }, g.at); } });
    common(s, d);
  };

  /* ---------- board: bảng điều tra — ảnh polaroid ghim, dây đỏ nối ----------
     {pins:[{id, img?, label, x, y, w, h, rot, at, note}], links:[{a, b, at}]}. sfx: pin.at -> thud; link.at -> scratch */
  B.board = (s, d) => {
    el("div", "cork", null, d);
    const svg = sv("svg", { class: "layer", viewBox: `0 0 ${W} ${H}`, style: "z-index:3" }, d), P = {};
    (s.pins || []).forEach((q) => { const w = q.w || 230, h = q.img ? (q.h || 270) : 0, e = el("div", "pol" + (q.note ? " note" : ""), null, d);
      Object.assign(e.style, { left: px(q.x - w / 2 - 14), top: px(q.y - h / 2 - 14), zIndex: 2, width: q.img ? "auto" : px(w + 28) });
      if (q.img) { const im = el("img", toneCls(q.tone || "bw"), null, e); im.src = IM(q.img).src; Object.assign(im.style, { width: px(w), height: px(h) }); if (q.pos) im.style.objectPosition = q.pos; }
      el("div", "pl", esc(q.label || ""), e); el("div", "pin", null, e);
      P[q.id] = { x: q.x, y: q.y - h / 2 - 2 };
      const rot = q.rot ?? Math.round((rnd() * 6 - 3) * 10) / 10;
      tl.fromTo(e, { opacity: 0, scale: 1.25, rotation: rot * 3 }, { opacity: 1, scale: 1, rotation: rot, duration: 0.25, ease: "power3.in", immediateRender: false }, q.at - 0.2); });
    (s.links || []).forEach((l) => { const a = P[l.a], b = P[l.b]; if (!a || !b) throw new Error("dây nối thiếu ghim " + l.a + "/" + l.b);
      const p = sv("path", { d: `M${a.x} ${a.y} Q${(a.x + b.x) / 2} ${Math.max(a.y, b.y) + 70} ${b.x} ${b.y}`, class: "bstr" }, svg); draw(p, l.at, 0.45, "power1.inOut"); });
    common(s, d);
  };

  /* ---------- memorial: tên khắc trên đá + ánh nến ----------
     {title, names:[{n, s, at}], fs}. sfx: t0+0.2 -> chuông nhà thờ; name.at -> thud rất nhẹ */
  B.memorial = (s, d) => {
    el("div", "marble", null, d);
    const cdl = el("div", "candle", null, d); cdl.style.left = px(W / 2);
    for (let k = 0; k < Math.ceil((s.t1 - s.t0) * 8); k++) tl.set(cdl, { opacity: 0.7 + rnd() * 0.3 }, s.t0 + k / 8);
    if (s.title) { const t = el("div", "mtt", esc(s.title), d); tl.to(t, { opacity: 1, duration: 0.6 }, s.t0 + 0.2); }
    const n = s.names.length, cols = n > 6 ? 2 : 1, per = Math.ceil(n / cols), fs = s.fs || (n > 6 ? 48 : 60), gap = fs * (s.names.some((q) => q.s) ? 1.95 : 1.45);
    const y0 = Math.max(205, 520 - (per * gap) / 2);
    s.names.forEach((q, k) => { const c = Math.floor(k / per), e = el("div", "mnm", esc(q.n) + (q.s ? `<small>${esc(q.s)}</small>` : ""), d);
      Object.assign(e.style, { fontSize: px(fs), top: px(y0 + (k % per) * gap) });
      if (cols === 2) Object.assign(e.style, { left: px(c === 0 ? 120 : 980), right: "auto", width: "820px" });
      tl.fromTo(e, { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.7, immediateRender: false }, q.at - 0.1); });
    common(s, d);
  };

  /* ---------- calendar: lịch xé từ ngày `from`, xé `days` trang, dừng đúng endAt ----------
     {from:[d, m, y], days, endAt, label}. sfx: mỗi trang -> tick giấy; nhịp tim dồn; endAt -> boom */
  const MON = ["GENNAIO", "FEBBRAIO", "MARZO", "APRILE", "MAGGIO", "GIUGNO", "LUGLIO", "AGOSTO", "SETTEMBRE", "OTTOBRE", "NOVEMBRE", "DICEMBRE"];
  const MDAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  const addDays = ([dd, mm, yy], k) => { dd += k; while (dd > MDAYS[mm - 1] + (mm === 2 && yy % 4 === 0 ? 1 : 0)) { dd -= MDAYS[mm - 1] + (mm === 2 && yy % 4 === 0 ? 1 : 0); mm++; if (mm > 12) { mm = 1; yy++; } } return [dd, mm, yy]; };
  B.calendar = (s, d) => {
    bg(s, d, 0.85);
    const cal = el("div", "cal", null, d), N = s.days, a = s.t0 + 0.7, span = s.endAt - a, pages = [];
    for (let k = N; k >= 0; k--) { const [dd, mm, yy] = addDays(s.from, k), pg = el("div", "pg", `<div class="mo">${MON[mm - 1]}</div><div class="dd">${dd}</div><div class="yy">${yy}</div>`, cal); pages[k] = pg; }
    tl.fromTo(cal, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out", immediateRender: false }, s.t0);
    const cnt = el("div", "calc", `${esc(s.label || "NGÀY")} <b>0</b>`, d), b = cnt.querySelector("b");
    tl.to(cnt, { opacity: 1, duration: 0.3 }, a - 0.2);
    for (let k = 0; k < N; k++) { const t = a + span * (0.5 - 0.5 * Math.cos(Math.PI * (k + 1) / N)) - 0.3;
      tl.to(pages[k], { rotationX: -110, y: -120, opacity: 0, duration: 0.3, ease: "power2.in" }, t);
      tl.set(b, { textContent: String(k + 1) }, t + 0.15); }
    tl.fromTo(pages[N], { boxShadow: "0 40px 100px rgba(0,0,0,.8)" }, { boxShadow: "0 0 0 10px #c8102e, 0 40px 100px rgba(0,0,0,.8)", duration: 0.2, immediateRender: false }, s.endAt);
    tl.to("#stage", { x: 10, duration: 0.03, yoyo: true, repeat: 5 }, s.endAt);
    common(s, d);
  };

  /* ---------- sticker: tờ dán kiểu cáo phó đập lên tường ----------
     {items:[{it, vi, at, x, y, rot, sm}]}. sfx: item.at -> slap */
  B.sticker = (s, d) => {
    bg(s, d, s.veil ?? 0.55);
    s.items.forEach((q) => { const w = q.sm ? 420 : 760, e = el("div", "stk" + (q.sm ? " sm" : ""), `<div class="it">${esc(q.it).replace(/\n/g, "<br/>")}</div>${q.vi ? `<div class="vi">${esc(q.vi)}</div>` : ""}`, d);
      Object.assign(e.style, { left: px((q.x ?? W / 2) - w / 2), top: px(q.y ?? 300) });
      tl.fromTo(e, { opacity: 0, scale: 1.35, rotation: (q.rot ?? -2) * 2 }, { opacity: 1, scale: 1, rotation: q.rot ?? -2, duration: 0.16, ease: "power4.in", immediateRender: false }, q.at - 0.16); });
    common(s, d);
  };

  /* ---------- sketch: tranh minh hoạ nét mực, vẽ dần từng nét (on twos) ----------
     {art: boy|dinner|boat, title, drawDur}. Luôn gắn nhãn TRANH MINH HỌA. sfx: tiếng bút sột soạt suốt lúc vẽ */
  const C2 = (x, y, r) => `M${x + r} ${y} a${r} ${r} 0 1 1 ${-2 * r} 0 a${r} ${r} 0 1 1 ${2 * r} 0`;
  // nét người/la kiểu storyboard (không vẽ mặt) cho các tranh minh họa
  const MAN = (x, y, gun) => `M${x + 9} ${y} a9 9 0 1 1 -18 0 a9 9 0 1 1 18 0 M${x - 14} ${y - 6} L${x + 14} ${y - 6} M${x} ${y + 9} L${x - 2} ${y + 55}`
    + ` M${x} ${y + 22} L${x - 16} ${y + 44} M${x} ${y + 22} L${x + 16} ${y + 40} M${x - 2} ${y + 55} L${x - 14} ${y + 92} M${x - 2} ${y + 55} L${x + 12} ${y + 92}`
    + (gun ? ` M${x + 10} ${y + 14} L${x - 12} ${y + 60}` : "");
  const MULE = (x, y) => `M${x} ${y} Q${x + 45} ${y - 18} ${x + 90} ${y} L${x + 92} ${y + 26} Q${x + 45} ${y + 36} ${x} ${y + 26} Z M${x + 90} ${y + 4} L${x + 112} ${y - 24} L${x + 124} ${y - 16} L${x + 104} ${y + 12}`
    + ` M${x + 8} ${y + 26} L${x + 4} ${y + 64} M${x + 24} ${y + 28} L${x + 26} ${y + 64} M${x + 70} ${y + 28} L${x + 66} ${y + 64} M${x + 86} ${y + 26} L${x + 90} ${y + 64}`
    + ` M${x + 18} ${y - 6} L${x + 18} ${y - 34} L${x + 72} ${y - 34} L${x + 72} ${y - 6} M${x + 18} ${y - 20} L${x + 72} ${y - 20}`;
  const CHUTE = (x, y) => `M${x - 46} ${y} Q${x} ${y - 70} ${x + 46} ${y} Q${x + 23} ${y - 12} ${x} ${y} Q${x - 23} ${y - 12} ${x - 46} ${y} M${x - 46} ${y} L${x - 12} ${y + 70} M${x + 46} ${y} L${x + 12} ${y + 70} M${x} ${y} L${x} ${y + 70}`
    + ` M${x - 16} ${y + 70} L${x + 16} ${y + 70} L${x + 16} ${y + 98} L${x - 16} ${y + 98} Z`;
  const DESK = (x, y) => `M${x} ${y} L${x + 150} ${y} M${x + 10} ${y} L${x + 10} ${y + 60} M${x + 140} ${y} L${x + 140} ${y + 60} M${x + 40} ${y - 62} L${x + 110} ${y - 62} L${x + 110} ${y - 12} L${x + 40} ${y - 12} Z M${x + 75} ${y - 12} L${x + 75} ${y}`
    + ` M${x + 84} ${y + 34} a14 14 0 1 1 -28 0 a14 14 0 1 1 28 0 M${x + 70} ${y + 48} L${x + 70} ${y + 96} M${x + 50} ${y + 96} L${x + 92} ${y + 96}`;
  const POPPY = (x, y, h) => `M${x} ${y} Q${x - 6} ${y - h / 2} ${x + 2} ${y - h} M${x + 2} ${y - h} a9 11 0 1 1 0.1 0 M${x - 2} ${y - h * 0.4} q-16 -6 -22 -20`;
  const SKETCH = {
    boy: [
      ["M80 700 L1420 700", 3], ["M150 700 L150 300 L430 250 L430 700", 3], ["M190 360 L270 350 L270 430 L190 440 Z", 2], ["M320 340 L400 330 L400 410 L320 420 Z", 2],
      ["M120 300 L460 245 L470 275 L130 330 Z", 2.5], ["M1100 700 L1100 330 L1380 360 L1380 700", 3], ["M1150 420 L1240 425 L1240 520 L1150 515 Z", 2],
      [C2(750, 330, 34), 4], ["M690 322 Q750 262 810 322", 4], ["M750 364 L744 500", 5], ["M748 398 L700 432", 4], ["M752 398 L798 420", 4],
      ["M744 500 L722 610 L706 690", 5], ["M744 500 L774 600 L792 690", 5], ["M560 392 L940 372", 4],
      ["M582 391 L560 520 M582 391 L612 520", 2], ["M542 520 Q586 592 630 520 Z", 3.5], [C2(570, 528, 13) + " " + C2(598, 524, 13), 2.5],
      ["M920 374 L898 505 M920 374 L950 505", 2], ["M880 505 Q924 577 968 505 Z", 3.5], [C2(910, 513, 13) + " " + C2(938, 509, 13), 2.5],
    ],
    dinner: [
      ["M80 720 L1420 720", 3], ["M300 720 L500 560 L1000 560 L1200 720", 2.5], ["M500 560 L500 120 M1000 560 L1000 120", 2],
      ["M560 560 L560 260 L720 260 L720 560", 3], ["M720 260 L800 292 L800 592 L720 560", 3],
      [C2(640, 330, 24), 3], ["M640 354 L636 470 M640 380 L610 430 M640 380 L668 432 M636 470 L620 552 M636 470 L654 552", 3],
      ["M520 610 a230 60 0 1 0 460 0 a230 60 0 1 0 -460 0", 4], ["M600 660 L588 720 M900 660 L912 720", 4],
      ["M620 600 a40 10 0 1 0 80 0 a40 10 0 1 0 -80 0 M800 596 a40 10 0 1 0 80 0 a40 10 0 1 0 -80 0 M720 616 a34 9 0 1 0 68 0 a34 9 0 1 0 -68 0", 2.5],
      ["M750 120 L750 226", 2], ["M700 228 L800 228 L780 196 L720 196 Z", 3],
      ["M400 560 L400 720 M400 640 L480 640 L480 720", 3.5], ["M1100 560 L1100 720 M1100 640 L1020 640 L1020 720", 3.5],
    ],
    boat: [
      ["M80 470 Q300 420 500 470 T900 460 T1420 470", 2], ["M80 640 Q380 620 700 640 T1420 640", 2], ["M120 690 Q420 670 740 690 T1420 690", 2],
      ["M440 560 Q750 640 1110 560 L1070 604 Q750 664 482 604 Z", 4.5], ["M760 566 L760 180", 4],
      ["M760 190 L982 232 L1002 522 L760 542 Z", 3.5], ["M760 262 L990 292 M760 332 L996 362 M760 402 L999 430 M760 472 L1001 492", 2],
      ["M560 548 q20 -32 42 0 M610 552 q20 -32 42 0 M660 556 q20 -32 42 0", 3], [C2(1044, 468, 18), 3], ["M1044 486 L1034 552", 4],
      ["M1066 420 L980 690", 3],
    ],
    // từ đường: hoành phi, bài vị, lư hương — cửa sau mở vào xưởng (bình cầu, bếp lửa)
    altar: [
      ["M80 720 L1420 720", 3], ["M200 720 L200 140 M1300 720 L1300 140", 3], ["M160 140 L1340 140 M160 170 L1340 170", 2.5],
      ["M560 200 L940 200 L940 290 L560 290 Z", 3], ["M580 215 L920 215 L920 275 L580 275 Z", 1.5],
      ["M620 230 l30 0 l-10 30 M700 230 l0 32 M690 245 l24 0 M780 228 l20 34 M800 228 l-20 34 M860 230 l24 0 l0 30", 2],
      ["M640 430 L680 430 L680 340 L660 325 L640 340 Z M820 430 L860 430 L860 340 L840 325 L820 340 Z", 2.5], ["M730 400 L730 330 L750 315 L770 330 L770 400", 2.5],
      ["M520 430 L980 430 L980 450 L520 450 Z", 3], ["M545 450 L545 720 M955 450 L955 720", 4], ["M560 450 L560 620 L940 620 L940 450", 2],
      ["M720 430 L725 400 L775 400 L780 430", 3], ["M740 400 L736 350 M750 400 L750 345 M760 400 L764 350", 1.5], ["M750 340 q-15 -20 0 -40 q15 -20 0 -40", 1.5],
      ["M1060 720 L1060 380 L1220 380 L1220 720", 3], ["M1070 630 L1210 630", 3],
      ["M1095 520 L1115 520 M1100 520 L1100 570 L1080 630 M1115 520 L1115 570 L1135 630", 2.5], ["M1158 560 L1180 560 M1163 560 L1163 590 L1150 630 M1177 560 L1177 590 L1190 630", 2.5],
      ["M1105 680 q8 -14 0 -26 q14 10 6 26 M1165 680 q8 -14 0 -26 q14 10 6 26", 2], ["M1080 690 L1200 690", 2.5],
    ],
    // nhà thạch khố môn bên ngoài — mặt cắt bên trong là tường bê tông, lỗ châu mai, nòng súng
    pillbox: [
      ["M80 720 L1420 720", 3], ["M250 720 L250 260 L750 260 L750 720", 3], ["M220 260 L500 160 L780 260", 3],
      ["M420 720 L420 470 L580 470 L580 720", 3], ["M400 470 Q500 400 600 470", 3], ["M500 470 L500 720", 2],
      ["M300 320 L380 320 L380 400 L300 400 Z M620 320 L700 320 L700 400 L620 400 Z", 2],
      ["M770 500 L830 500 M815 488 L830 500 L815 512", 2.5],
      ["M850 720 L850 260 L1350 260 L1350 720", 3], ["M820 260 L1100 160 L1380 260", 3], ["M890 720 L890 300 L1310 300 L1310 720", 2],
      ["M850 700 L890 660 M850 640 L890 600 M850 580 L890 540 M850 400 L890 360 M850 340 L890 300 M1310 700 L1350 660 M1310 640 L1350 600 M1310 580 L1350 540 M1310 520 L1350 480 M1310 460 L1350 420 M1310 400 L1350 360 M1310 340 L1350 300", 1.5],
      ["M840 470 L900 470 M840 490 L900 490", 3], ["M905 480 L1010 480", 6],
      [C2(1060, 446, 22), 3], ["M1056 468 L1084 560 L1044 640 M1084 560 L1124 640", 3.5], ["M1062 492 L1008 482", 3.5],
    ],
    // tàu khách rời bến — một bóng người đứng lại trên cầu tàu
    liner: [
      ["M80 560 Q400 540 750 560 T1420 560", 2], ["M80 640 Q450 620 800 640 T1420 640", 2], ["M80 700 Q500 685 900 700 T1420 700", 1.5],
      ["M80 520 L380 520 L380 545 L80 545 Z", 3], ["M120 545 L120 600 M200 545 L200 600 M280 545 L280 600 M360 545 L360 600", 3],
      [C2(300, 470, 13), 2.5], ["M300 483 L298 520 M299 495 L284 512 M299 495 L314 512", 2.5],
      ["M600 470 L1380 470 L1330 560 L650 560 Z", 4.5], ["M720 470 L720 410 L1220 410 L1220 470", 3], ["M800 410 L800 360 L1140 360 L1140 410", 3],
      [C2(720, 510, 9) + " " + C2(800, 510, 9) + " " + C2(880, 510, 9) + " " + C2(960, 510, 9) + " " + C2(1040, 510, 9) + " " + C2(1120, 510, 9) + " " + C2(1200, 510, 9), 2],
      ["M880 360 L870 260 L930 260 L940 360 M1020 360 L1010 260 L1070 260 L1080 360", 3.5],
      ["M900 255 q-40 -40 -100 -30 q-60 10 -110 -20 M1040 255 q-40 -40 -100 -30 q-60 10 -110 -20", 2],
      ["M1300 470 L1300 300", 2.5], ["M1300 300 L1350 315 L1300 330", 2], ["M1380 520 q30 10 60 0 M1370 545 q40 10 70 0", 2],
    ],
    // ngựa chồm lên trong sân tối, cạnh xe kéo; một vật nằm dưới đất
    horse: [
      ["M80 720 L1420 720", 3], ["M120 720 L120 200 M1380 720 L1380 200", 2.5],
      [C2(1050, 620, 100), 4], ["M1050 520 L1050 720 M950 620 L1150 620 M980 550 L1120 690 M1120 550 L980 690", 2],
      ["M900 520 L1300 520 L1300 440 L900 440 Z", 3.5], ["M900 500 L700 470 M900 520 L700 500", 3],
      ["M520 420 Q600 360 700 400 Q720 440 690 480 Q600 500 540 470 Z", 4], ["M690 420 Q720 330 760 300 L800 320 L790 345 L750 350 Q730 400 700 440", 3.5],
      ["M680 460 L730 420 L760 440 M660 470 L700 520 L740 500", 3.5], ["M560 480 L540 600 L560 720 M600 490 L610 600 L590 720", 4],
      ["M520 430 Q470 450 460 520", 3], ["M720 340 q-10 20 -5 40 M735 325 q-10 20 -5 40", 2],
      ["M300 700 Q360 660 440 690 Q460 710 420 720 L300 720 Z", 3],
    ],
    // phòng trọ: hàng người ngủ gục trên sợi dây thừng căng ngang (2 xu)
    rope: [
      ["M80 720 L1420 720", 3], ["M80 160 L1420 160", 2], ["M640 200 L860 200 L860 330 L640 330 Z M750 200 L750 330 M640 265 L860 265", 2],
      ["M150 600 L1350 600 M150 620 L1350 620 M200 620 L200 720 M700 620 L700 720 M1300 620 L1300 720", 3],
      ["M120 400 L120 720 M1380 400 L1380 720", 4], ["M120 470 Q750 492 1380 470", 4],
      [C2(340, 455, 26) + " " + C2(600, 458, 26) + " " + C2(860, 459, 26) + " " + C2(1120, 456, 26), 3],
      ["M300 600 Q290 530 330 482 M560 600 Q550 530 590 485 M820 600 Q810 530 850 486 M1080 600 Q1070 530 1110 483", 3.5],
      ["M330 485 L390 480 L398 515 M590 488 L650 484 L658 518 M850 489 L910 485 L918 520 M1110 486 L1170 482 L1178 516", 3],
      ["M300 600 L330 700 M560 600 L590 700 M820 600 L850 700 M1080 600 L1110 700", 3],
    ],
    // cảnh sát xách đèn bão rọi vào góc quảng trường
    lantern: [
      ["M80 720 L1420 720 M300 720 L620 420 M1200 720 L880 420", 2], ["M80 160 L620 420 M1420 160 L880 420 M620 420 L880 420 L880 160 M620 420 L620 160", 2],
      ["M380 300 Q410 250 440 300 Z", 3], [C2(410, 325, 24), 3], ["M380 350 L350 560 L470 560 L440 350 Z", 3.5], ["M380 560 L370 700 M440 560 L455 700", 4],
      ["M440 380 L520 430", 4], ["M510 430 L540 430 L545 470 L505 470 Z", 3], ["M545 450 L1100 600 M545 462 L1100 700", 1.5],
      ["M1050 640 Q1120 610 1190 650 Q1180 690 1100 690 Z", 3],
    ],
    // chiếc hộp bưu kiện nhỏ buộc dây, có nhãn và dấu bưu điện
    parcel: [
      ["M200 640 L1300 640", 3], ["M520 380 L880 340 L1040 420 L680 470 Z", 4], ["M520 380 L520 560 L680 650 L680 470", 4], ["M680 650 L1040 590 L1040 420", 4],
      ["M600 425 L960 380 M780 360 L860 445", 2], ["M600 425 L600 605 M960 380 L960 610", 2],
      ["M560 470 L640 505 L640 560 L560 525 Z", 2], ["M570 495 l50 22 M570 510 l40 18", 1.5], [C2(900, 520, 40), 2],
    ],
    // cửa phòng số 13: ô kính vỡ, bàn tay thò vào mở then, áo khoác chắn gió
    window: [
      ["M80 720 L1420 720", 3], ["M400 720 L400 180 L680 180 L680 720", 3.5], ["M440 240 L640 240 L640 420 L440 420 Z M440 470 L640 470 L640 680 L440 680 Z", 2],
      ["M640 450 L690 450", 3], ["M760 250 L1140 250 L1140 560 L760 560 Z M950 250 L950 560 M760 405 L1140 405", 3],
      ["M760 470 L820 430 L860 480 L800 520 Z M820 430 L840 405 M860 480 L900 470", 2],
      ["M700 470 Q760 470 810 475 M700 495 Q760 495 805 495", 3], ["M810 475 l20 -6 M810 482 l22 0 M808 490 l20 6", 2],
      ["M970 270 Q1050 300 1120 270 L1110 390 Q1040 370 980 390 Z", 2], ["M1300 720 L1300 300 M1270 300 L1330 300 L1320 250 L1280 250 Z", 3],
    ],
    // người đánh xe đứng cạnh cổng chuồng ngựa, "tấm bạt" dưới đất, xe phía sau
    carter: [
      ["M80 720 L1420 720", 3], ["M200 720 L200 260 L620 260 L620 720 M200 260 L410 200 L620 260", 3],
      ["M260 300 L260 720 M330 300 L330 720 M400 300 L400 720 M470 300 L470 720 M540 300 L540 720", 2],
      ["M240 710 Q330 660 450 690 Q480 710 450 720 L240 720 Z", 3],
      ["M820 290 Q860 260 900 290 L910 300 L810 300 Z", 3], [C2(860, 325, 26), 3], ["M820 355 L790 560 L930 560 L900 355 Z", 3.5],
      ["M820 560 L815 700 M900 560 L905 700", 4], ["M820 380 L780 480 M900 380 L940 480", 3.5],
      [C2(1250, 620, 90), 3.5], ["M1100 520 L1420 520 L1420 450 L1100 450 Z", 3], ["M1250 530 L1250 710 M1160 620 L1340 620", 2],
      ["M100 600 Q400 580 700 600 M800 640 Q1100 620 1400 640", 1.5],
    ],
    // đoàn la thồ và người cầm súng lội qua sông, núi phía sau (trận Ban Khwan 1967)
    convoy: [
      ["M80 300 L250 190 L400 260 L560 160 L740 250 L900 180 L1080 250 L1240 170 L1420 260", 2],
      ["M80 560 Q400 540 750 560 T1420 560", 2], ["M80 640 Q420 620 760 640 T1420 640", 1.5], ["M80 710 Q450 690 820 710 T1420 710", 1.5],
      [MULE(160, 470), 3], [MAN(330, 420, 1), 3], [MULE(470, 486), 3], [MAN(640, 436, 1), 3], [MULE(780, 470), 3], [MAN(950, 420, 1), 3],
      [MULE(1090, 486), 3], [MAN(1270, 436, 1), 3],
    ],
    // máy bay vận tải không phù hiệu thả dù tiếp tế xuống thung lũng rừng (Chiến dịch Giấy)
    airdrop: [
      ["M80 720 L260 600 L420 680 L600 560 L780 660 L960 580 L1160 670 L1420 590", 2.5],
      ["M150 720 q20 -40 40 0 M330 700 q20 -40 40 0 M700 690 q20 -40 40 0 M1050 700 q20 -40 40 0 M1300 690 q20 -40 40 0", 2],
      ["M520 150 Q760 120 1000 150 Q1040 160 1000 172 Q760 195 540 170 Z", 4], ["M700 156 L640 230 L700 230 L800 162", 3.5], ["M760 150 L820 100 L860 102 L800 152", 2.5],
      ["M540 160 L480 120 L520 120 L590 156", 3],
      [CHUTE(560, 300), 3], [CHUTE(760, 340), 3], [CHUTE(960, 290), 3], [CHUTE(1140, 360), 3],
    ],
    // phòng giam: song sắt, cửa sổ nhỏ trên cao, một người ngồi đọc sách (nhà tù Mandalay 1969)
    prison: [
      ["M80 720 L1420 720", 3], ["M300 120 L300 720 M1200 120 L1200 720 M300 120 L1200 120", 3],
      ["M640 200 L860 200 L860 320 L640 320 Z M695 200 L695 320 M750 200 L750 320 M805 200 L805 320", 2.5],
      ["M350 120 L350 720 M430 120 L430 720 M510 120 L510 720 M1000 120 L1000 720 M1080 120 L1080 720 M1150 120 L1150 720", 4],
      ["M600 560 L900 560 L900 590 L600 590 Z M620 590 L620 720 M880 590 L880 720", 3],
      [C2(750, 420, 26), 3.5], ["M750 446 L746 556 M748 476 L712 516 L760 520 M750 476 L786 512 L740 522", 3.5],
      ["M712 510 L790 510 L800 540 L702 540 Z", 2.5], ["M746 556 L700 560 L690 640 M746 556 L800 560 L810 640", 3.5],
    ],
    // phòng lừa đảo trực tuyến: dãy bàn máy tính, người ngồi quay lưng, cửa sổ chấn song, đồng hồ trên tường
    scamroom: [
      ["M80 720 L1420 720", 3], ["M80 150 L1420 150", 2], ["M1180 190 L1340 190 L1340 330 L1180 330 Z M1220 190 L1220 330 M1260 190 L1260 330 M1300 190 L1300 330", 3],
      [C2(260, 230, 40), 3], ["M260 230 L260 204 M260 230 L282 240", 2.5],
      [DESK(140, 470), 3], [DESK(420, 470), 3], [DESK(700, 470), 3], [DESK(980, 470), 3],
      ["M140 600 L1260 600", 1.5],
    ],
    // nông dân đội nón lá thu hoạch nhựa anh túc trên sườn núi
    harvest: [
      ["M80 720 Q500 520 1420 600", 3], ["M80 300 L260 210 L420 270 L620 190 L820 260 L1040 200 L1260 260 L1420 220", 2],
      [POPPY(200, 700, 120) + " " + POPPY(270, 690, 140) + " " + POPPY(340, 676, 110) + " " + POPPY(420, 664, 130), 2.5],
      [POPPY(980, 590, 130) + " " + POPPY(1060, 588, 110) + " " + POPPY(1140, 590, 140) + " " + POPPY(1220, 594, 120) + " " + POPPY(1300, 600, 130), 2.5],
      ["M640 420 L760 420 L700 380 Z", 3.5], ["M700 420 Q690 470 650 500 M700 430 Q720 480 760 520 L780 600 M650 500 L630 610", 3.5],
      ["M676 470 L620 520 M720 470 L770 470 L790 500", 3], ["M760 520 L840 520 L830 590 L770 590 Z", 3],
    ],
    // tháp sòng bạc mái vòm bên bờ sông, phà chạy ngang (đặc khu hôm nay)
    casino: [
      ["M80 600 Q400 580 750 600 T1420 600", 2], ["M80 680 Q450 660 800 680 T1420 680", 1.5],
      ["M80 560 L1420 560", 2.5], ["M640 560 L640 260 L860 260 L860 560", 3.5], ["M620 260 L880 260 L860 230 L640 230 Z", 3],
      ["M690 230 Q750 120 810 230", 3.5], ["M750 150 L750 100", 2.5],
      ["M670 300 L830 300 M670 350 L830 350 M670 400 L830 400 M670 450 L830 450 M670 500 L830 500", 1.5],
      ["M420 560 L420 380 L560 380 L560 560 M960 560 L960 400 L1120 400 L1120 560 M1160 560 L1160 450 L1260 450 L1260 560", 3],
      ["M300 640 L460 640 L440 662 L320 662 Z M350 640 L350 615 L410 615 L410 640", 3],
    ],
    // máy bay chao đảo giữa mưa trên dãy núi
    plane: [
      ["M80 720 L300 480 L460 640 L640 400 L860 660 L1040 460 L1250 640 L1420 520", 3],
      ["M200 120 L180 180 M320 90 L300 150 M440 140 L420 200 M1120 110 L1100 170 M1240 160 L1220 220 M1360 100 L1340 160 M260 260 L240 320 M1300 300 L1280 360 M380 380 L360 440 M1180 360 L1160 420", 1.5],
      ["M520 300 Q760 270 1000 300 Q1040 310 1000 322 Q760 345 540 320 Z", 4], ["M540 312 L480 250 L520 250 L590 300", 3], ["M520 318 L470 340 L540 330", 2.5],
      ["M720 318 L640 400 L700 400 L820 322", 3.5], ["M740 300 L820 250 L860 252 L800 302", 2.5], ["M960 300 Q985 296 1000 304", 2],
      ["M480 280 q-80 -30 -160 -10 q-80 20 -150 -20", 2], ["M1200 60 L1170 170 L1210 170 L1170 290", 3],
    ],
    // pháo đài đá 1847 bên bờ vịnh: tường đá, vọng lâu, cổng nam, nòng pháo; núi phía sau
    fort: [
      ["M80 300 L260 180 L420 260 L560 150 L760 250 L900 170 L1120 260 L1260 190 L1420 280", 2],
      ["M80 720 L1420 720", 3], ["M80 680 Q400 660 700 680 T1420 680", 1.5],
      ["M220 640 L220 400 L1280 400 L1280 640", 4], ["M220 400 L220 370 L260 370 L260 400 M320 400 L320 370 L360 370 L360 400 M420 400 L420 370 L460 370 L460 400 M1040 400 L1040 370 L1080 370 L1080 400 M1140 400 L1140 370 L1180 370 L1180 400 M1240 400 L1240 370 L1280 370 L1280 400", 2.5],
      ["M640 640 L640 500 Q750 430 860 500 L860 640", 4], ["M750 470 L750 640", 2],
      ["M600 400 L600 300 L900 300 L900 400 M570 300 L750 230 L930 300", 3.5], ["M680 330 L820 330 L820 380 L680 380 Z", 2.5],
      ["M260 440 L360 440 L360 520 L260 520 Z M1140 440 L1240 440 L1240 520 L1140 520 Z", 2],
      ["M300 600 L470 600 M300 620 L470 620 M1030 600 L1200 600 M1030 620 L1200 620", 1.5],
      ["M400 470 L330 455 M1100 470 L1170 455 M520 470 L460 455 M980 470 L1040 455", 5],
      ["M250 560 L1250 560", 1.2], ["M250 480 L590 480 M910 480 L1250 480", 1.2],
    ],
    // cô gái đứng trên boong tàu, ôm hộp kèn, bến cảng Hồng Kông phía trước
    oboe: [
      ["M80 560 Q400 540 750 560 T1420 560", 2], ["M80 640 Q450 620 800 640 T1420 640", 2],
      ["M900 520 L960 430 L1010 470 L1080 360 L1130 420 L1200 330 L1260 410 L1320 380 L1420 450", 2.5],
      ["M940 520 L940 470 L980 470 L980 520 M1010 520 L1010 440 L1050 440 L1050 520 M1090 520 L1090 400 L1130 400 L1130 520 M1170 520 L1170 450 L1210 450 L1210 520", 2],
      ["M80 600 L760 600 L700 700 L80 700", 4.5], ["M80 600 L80 520 M200 600 L200 520 M320 600 L320 520 M440 600 L440 520 M560 600 L560 520 M80 520 L620 520", 2.5],
      [C2(380, 330, 30), 3.5], ["M352 318 Q380 280 410 318 L414 350 M350 318 L346 352", 2.5],
      ["M380 360 L372 470 M376 390 L330 430 M378 390 L420 430", 3.5], ["M340 470 L410 470 L420 540 L330 540 Z", 3],
      ["M372 540 L360 600 M392 540 L400 600", 3.5], ["M310 420 L450 420 L450 450 L310 450 Z", 3], ["M330 435 L430 435", 1.5],
      ["M600 200 q30 -20 60 0 q30 -20 60 0 M700 150 q20 -14 40 0 q20 -14 40 0", 1.5],
    ],
    // mặt cắt: hai tấm bia đá nằm dưới lòng đất, bên trên là những khối nhà chồng chất
    plaque: [
      ["M80 420 L1420 420", 3], ["M80 440 L1420 440", 1.5],
      ["M140 420 L140 120 L300 120 L300 420 M300 420 L300 80 L470 80 L470 420 M470 420 L470 150 L620 150 L620 420 M620 420 L620 60 L800 60 L800 420 M800 420 L800 130 L960 130 L960 420 M960 420 L960 90 L1130 90 L1130 420 M1130 420 L1130 160 L1300 160 L1300 420", 2.5],
      ["M170 160 L270 160 M170 200 L270 200 M170 240 L270 240 M330 120 L440 120 M330 160 L440 160 M330 200 L440 200 M650 100 L770 100 M650 140 L770 140 M650 180 L770 180 M990 130 L1100 130 M990 170 L1100 170 M990 210 L1100 210", 1.5],
      ["M520 70 L520 40 M560 70 L560 30 M900 90 L900 50 M1060 60 L1060 20", 2],
      ["M120 480 Q300 470 500 490 T900 480 T1380 490 M120 560 Q350 545 600 565 T1100 555 T1380 565 M120 660 Q400 650 700 665 T1380 660", 1.2],
      ["M470 580 L690 560 L700 650 L480 670 Z", 4], ["M520 595 L520 640 M560 592 L560 636 M600 588 L600 634 M640 585 L640 630", 2],
      ["M760 600 L1040 580 L1050 660 L770 680 Z", 4], ["M800 615 L800 660 M850 612 L850 656 M900 608 L900 652 M950 604 L950 648 M1000 600 L1000 644", 2],
      ["M560 520 L560 545 M552 535 L560 548 L568 535 M900 520 L900 548 M892 538 L900 551 L908 538", 2],
    ],
  };
  B.sketch = (s, d) => {
    el("div", "skbg", null, d);
    const svg = sv("svg", { class: "sksvg", viewBox: "0 0 1500 820" }, d), id = "skw" + (++UID);
    const f = sv("filter", { id }, sv("defs", {}, svg));
    sv("feTurbulence", { type: "fractalNoise", baseFrequency: ".035", numOctaves: 2, seed: 3 }, f); sv("feDisplacementMap", { in: "SourceGraphic", scale: 3.5 }, f);
    const g = sv("g", { filter: `url(#${id})` }, svg), paths = SKETCH[s.art] || SKETCH.boy;
    const dd = s.drawDur ?? Math.min(4.5, (s.t1 - s.t0) * 0.7), n = paths.length;
    paths.forEach(([pd, w], k) => { const p = sv("path", { d: pd, class: "ink", "stroke-width": w }, g); draw(p, s.t0 + 0.3 + (k / n) * dd, Math.max(0.25, dd / n * 1.6), "steps(6)"); });
    tl.fromTo(svg, { scale: 1.0 }, { scale: 1.05, duration: Math.max(0.3, s.t1 - s.t0), ease: "none", immediateRender: false }, s.t0);
    if (s.title) { const t = el("div", "sktitle", esc(s.title), d); tl.to(t, { opacity: 1, duration: 0.5 }, s.t0 + 0.3 + dd); }
    common({ ...s, illus: s.illus ?? "TRANH MINH HỌA" }, d);
  };

  // chuyển cảnh tự xoay vòng (theme có autoTr): chọn kiểu ít dùng nhất, không trùng kiểu vừa dùng, tất định theo seed
  const TR = {
    push: [{ x: 140, opacity: 0 }, { x: 0, opacity: 1 }], pushup: [{ y: 110, opacity: 0 }, { y: 0, opacity: 1 }],
    zoom: [{ scale: 1.14, opacity: 0 }, { scale: 1, opacity: 1 }], wipe: [{ clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)" }],
    iris: [{ clipPath: "circle(0% at 50% 50%)" }, { clipPath: "circle(80% at 50% 50%)" }], blurfade: [{ filter: "blur(16px)", opacity: 0 }, { filter: "blur(0px)", opacity: 1 }],
  };
  const trUse = {}; let trLast = null;
  const pickTr = () => { const ks = Object.keys(TR).filter((k) => k !== trLast); let best = null, bu = 1e9;
    ks.forEach((k) => { const u = (trUse[k] || 0) + rnd() * 0.9; if (u < bu) { bu = u; best = k; } }); trUse[best] = (trUse[best] || 0) + 1; trLast = best; return best; };

  // ---------- dựng cảnh ----------
  C.scenes.forEach((s, i) => {
    const d = el("div", "scene", null, stage); show(d, s.t0, s.t1, s.type === "question" ? 0.12 : s.fade ?? 0.3);
    if (!B[s.type]) throw new Error("loại cảnh lạ: " + s.type);
    B[s.type](s, d);
    if (i > 0) {
      let tr = s.tr || (s.type === "chapter" ? "leak" : "cut");
      if (C.autoTr && !s.tr && !["chapter", "question", "slam"].includes(s.type)) tr = pickTr();
      if (tr === "leak") leak(s.t0 - 0.1); else if (tr === "flash") flash(s.t0, 0.3);
      else if (TR[tr]) tl.fromTo(d, TR[tr][0], { ...TR[tr][1], duration: 0.5, ease: "power3.out", immediateRender: false }, s.t0 - 0.12);
    }
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
  C.scenes.filter((s) => s.type === "question" || s.type === "chapter" || s.type === "endcard" || s.nocaps).forEach((s) => { tl.set("#caps", { opacity: 0 }, s.t0 - 0.01); tl.set("#caps", { opacity: 1 }, s.t1); });
  C.scenes.filter((s) => s.type === "endcard").forEach((s) => tl.to(["#hud", "#prog"], { opacity: 0, duration: 0.4 }, s.t0));

  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = tl;
})();
