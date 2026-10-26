/* HỒ SƠ S-TIER — engine dựng cảnh từ dữ liệu (window.CASE, do motion/stier/build.py ghi).
   Mỗi cảnh là một "loại" (hero, date, doc, photo, map, mug, counter, ...), mọi mốc thời gian
   đã được build.py quy về GIÂY từ mốc từng từ của giọng đọc — engine chỉ vẽ, không đoán.
   Tất định: PRNG có hạt theo slug, không Math.random / Date / fetch.
   build.py (sfx) đặt tiếng động theo CÙNG các mốc + độ lệch cố định ghi chú ở từng loại. */
(function () {
  const C = window.CASE, DUR = C.dur;
  // Giao diện theo kênh (motion/stier/themes.py): class trên #root do build.py ghi; ở đây chỉ nhãn/mặc định.
  const TH = C.theme || {}, LB = TH.labels || {};
  const LK = C.look || {};   // thư viện look của Short phối (motion/stier/looks.py); không có -> mặc định cũ
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
  // màu ngữ nghĩa bảng giá VN (kênh CK): xanh = tăng, đỏ = giảm, vàng = tham chiếu. Spec ghi "c": "up"/"down"/"ref"/"dim" hoặc mã màu.
  const CC = { up: "#22c55e", down: "#ef4444", ref: "#fbbf24", dim: "#64748b", ink: "#e2e8f0" };
  const ccol = (c) => CC[c] || c || "var(--red)";

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
  const toneCls = (t) => ({ bw: "bw", sepia: "sepia", color: "color", dim: "dimbg" }[t || TH.tone || "sepia"]);
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
    const m = IM(s.img), gold = (s.frame || TH.frame || "gold") === "gold", pad = gold ? 48 : 22, extra = gold ? 0 : 58;
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
    const w = el("div", "docw " + toneCls(s.tone), null, wrap); Object.assign(w.style, { width: px(m.w), height: px(m.h) });
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
    const m = IM(s.img), fx = (s.focus || [0.5, 0.4])[0], fy = (s.focus || [0.5, 0.4])[1];
    const mode = s.mode || (m.w / m.h > 1.05 && !s.focus ? "print" : "full");   // ảnh ngang trên khung dọc: tràn khung mất 1/3 hai bên -> vào khung in; có "focus" = người viết đã chọn cách cắt
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
      if (C.mix) { gsap.set(area, { transformPerspective: 1300 });   // ảnh in nghiêng 3D trôi chậm + vệt sáng quét
        tl.fromTo(area, { rotationY: 10 }, { rotationY: -8, duration: Math.max(0.3, dur), ease: "sine.inOut", immediateRender: false }, s.t0);
        holder.style.overflow = "hidden"; const sh = el("div", "shine", null, holder); tl.fromTo(sh, { xPercent: -160 }, { xPercent: 260, duration: 1.1, ease: "power2.inOut", immediateRender: false }, s.t0 + 0.5); }
    }
    if (s.label) { const lb = el("div", "boxlbl mono", esc(s.label.text), d); lb.style.top = px(s.label.y || 1120); tl.to(lb, { opacity: 1, duration: 0.25 }, s.label.at); }
    credit(d, s.credit, s.creditY || 1330, s.t0 + 0.2);
    if (s.stamp) { const st = el("div", "stamp", esc(s.stamp.text), d); st.style.fontSize = px(fsz(s.stamp.text, 104, 900 - (s.stamp.x || 330), 0.72)); st.style.left = px(s.stamp.x || 330); st.style.top = px(s.stamp.y || 1180); stamp(st, s.stamp.at, s.stamp.rot || -8); }
  };

  /* ---------- counter: số đếm lớn + nhãn (+ ảnh in) ----------
     sfx: tick theo từng bước (tối đa 28) theo ease power2.out từ at tới until; until -> thud */
  const vn = (n) => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  B.counter = (s, d) => {
    // số thập phân (vd. "to": 3.1) giữ đúng số chữ số sau dấu phẩy; trước 12/10/2026 bị làm tròn thành "3"
    const dp = s.dec ?? Math.max(...[s.to, s.from || 0].map((n) => (String(n).split(".")[1] || "").length));
    const vn = (n) => { const [a, b] = Number(n).toFixed(dp).split("."); return (s.year ? a : a.replace(/\B(?=(\d{3})+(?!\d))/g, ".")) + (b ? "," + b : ""); };   // "year": true -> 1996, không chấm nghìn (26/10/2026: Short Turing hiện "1.996")
    const str = (s.prefix || "") + vn(s.to) + (s.suffix || ""), fs = fsz(str, 300, 1000, /[MWmw]/.test(str) ? 0.72 : 0.66);   // chữ có M/W rộng hơn hẳn: "500 NĂM" từng chạm hai mép khung (14/10/2026)
    const ct = el("div", "count", esc((s.prefix || "") + vn(s.from || 0) + (s.suffix || "")), d); ct.style.fontSize = px(fs); if (s.top) ct.style.top = px(s.top);
    const top = (s.top || 360) + fs + 20;
    const o = { v: s.from || 0 };
    tl.to(o, { v: s.to, duration: Math.max(0.2, s.until - s.at), ease: "power2.out", onUpdate: () => { ct.textContent = (s.prefix || "") + vn(o.v) + (s.suffix || ""); } }, s.at);
    if (s.label) { const lb = el("div", "countlbl", esc(s.label), d); lb.style.top = px(top); lb.style.fontSize = px(fsz(s.label, 52, 980, 0.9));
      tl.fromTo(lb, { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power3.out", immediateRender: false }, s.labelAt ?? s.until - 0.1); }
    if (s.sub) { const sb = el("div", "countsub mono", esc(s.sub.text), d); sb.style.top = px(top + 90); sb.style.fontSize = px(fsz(s.sub.text, 30, 980, 0.86)); tl.to(sb, { opacity: 1, duration: 0.3 }, s.sub.at); }
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
      const c = el("div", "cell", `<b>${k + 1}</b><i>${esc(s.unit || LB.unit || "NGÀY")}</i>`, cal); Object.assign(c.style, { width: px(w), height: px(h) });
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
    el("div", "k", esc(s.k || LB.file || "HỒ SƠ"), cd);
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
      const lbl = q.label || p.label || p.name, lw = [...lbl].length * 22 + 40;
      let side = q.side || (p.x > 700 ? "t" : "r");
      // nhãn không được tràn mép khung (lỗi thật: ANTWERP/QUEBEC bị cắt)
      if (side === "r" && p.x + lw > 1050) side = p.x - lw > 30 ? "l" : "t";
      if (side === "l" && p.x - lw < 30) side = p.x + lw < 1050 ? "r" : "t";
      if (side === "t" && (p.x - lw / 2 < 30 || p.x + lw / 2 > 1050)) side = p.x < 540 ? "r" : "l";
      const t = sv("text", { x: side === "r" ? p.x + 40 : side === "l" ? p.x - 40 : p.x, y: side === "t" ? p.y - 56 : p.y + 12, class: "pinlbl", "text-anchor": side === "r" ? "start" : side === "l" ? "end" : "middle" }, g);
      t.textContent = lbl;
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

  /* ---------- quote karaoke (BUD v2, Shorts Studio port): cả câu hiện mờ, từng chữ sáng đúng lúc được đọc (s.wt từ build.py) ---------- */
  const quoteKaraoke = (s, d) => {
    const pp = el("div", "qkara", null, d);
    Object.assign(pp.style, { position: "absolute", left: "90px", right: "90px", top: "430px", textAlign: "left" });
    const qm = el("div", null, "“", pp); qm.setAttribute("data-layout-allow-overlap", ""); Object.assign(qm.style, { fontFamily: "'Playfair Display',serif", fontSize: "200px", lineHeight: "0.8", color: "var(--red)" });
    const qt = el("div", null, null, pp); const ws = s.text.split(/\s+/), L = s.text.length;
    Object.assign(qt.style, { fontFamily: "'Playfair Display',serif", fontStyle: "italic", fontWeight: "700", fontSize: px(L < 70 ? 78 : L < 110 ? 68 : 58), lineHeight: "1.3", color: "#f4efe3" });
    const sp = ws.map((w) => { const e = el("span", null, esc(w) + " ", qt); e.style.opacity = 0.28; return e; });
    sp.forEach((e, k) => { const t = (s.wt && s.wt[k] != null) ? s.wt[k] : s.t0 + k * 0.25; tl.to(e, { opacity: 1, duration: 0.15, ease: "none" }, Math.max(s.t0, t - 0.03)); });
    if (s.by) { const by = el("div", "mono", "— " + esc(s.by), pp); Object.assign(by.style, { marginTop: "36px", fontSize: "34px", letterSpacing: ".08em", color: "var(--red)", opacity: 0 });
      tl.to(by, { opacity: 1, duration: 0.3 }, s.t0 + 0.3); }
    tl.fromTo(pp, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out", immediateRender: false }, s.t0);
  };
  const quoteType = B.quote;
  B.quote = (s, d) => (s.mode === "karaoke" ? quoteKaraoke(s, d) : quoteType(s, d));

  /* ---------- source: thẻ dẫn kinh (BUD v2, Shorts Studio source_card) -- chữ lớn đọc được, "diễn ý" cùng dòng nguồn ----------
     sfx: sealAt -> thud (con dấu) */
  B.source = (s, d) => {
    const card = el("div", "srccard", null, d); card.setAttribute("data-layout-allow-occlusion", "");   // #scrims phủ mờ có chủ đích
    Object.assign(card.style, { position: "absolute", left: "80px", right: "80px", top: px(s.top || 400), padding: "56px 56px 64px",
      background: "rgba(250,246,236,0.97)", borderLeft: "14px solid var(--red)", borderRadius: "10px", boxShadow: "0 30px 80px rgba(0,0,0,.45)", color: "#1c1a17" });
    const src = el("div", "mono", esc(s.source || "") + (s.paraphrase === false ? "" : ' <span style="color:#7a5c2e">· DIỄN Ý</span>'), card);
    Object.assign(src.style, { fontSize: "36px", fontWeight: "700", letterSpacing: ".06em", color: "#7a3f10", whiteSpace: "nowrap" });   // nâu đậm trên kem: đạt WCAG AA
    if (s.ref) { const rf = el("div", null, esc(s.ref), card); Object.assign(rf.style, { fontFamily: "'Playfair Display',serif", fontWeight: "900", fontSize: px(fsz(s.ref, 92, 880, 0.55)), lineHeight: "1.1", margin: "20px 0 28px" }); }
    const sn = el("div", null, null, card); Object.assign(sn.style, { fontFamily: "'Playfair Display',serif", fontStyle: "italic", fontWeight: "700", fontSize: px(s.size || 64), lineHeight: "1.32" });
    let hl = null; String(s.snippet || "").split(/\[\[|\]\]/).forEach((p, k) => { if (k % 2) { hl = el("span", null, esc(p), sn);
      Object.assign(hl.style, { backgroundImage: "linear-gradient(transparent 58%, rgba(224,159,62,.55) 58%)", backgroundRepeat: "no-repeat", backgroundSize: "0% 100%" }); }
      else sn.appendChild(document.createTextNode(p)); });
    tl.fromTo(card, { opacity: 0, x: 140 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out", immediateRender: false }, s.t0 + 0.02);
    if (hl) tl.to(hl, { backgroundSize: "100% 100%", duration: 0.5, ease: "power2.inOut" }, s.hlAt);
    if (s.seal !== false) { const se = el("div", "mono", esc(s.seal || "ĐÃ ĐỐI CHIẾU"), d);
      Object.assign(se.style, { position: "absolute", right: "110px", top: px((s.top || 400) - 70), padding: "14px 22px", border: "5px solid var(--red)", color: "var(--red)",
        fontSize: "34px", fontWeight: "700", letterSpacing: ".08em", borderRadius: "8px", opacity: 0 });
      stamp(se, s.sealAt, -7); }
  };

  /* ---------- kinetic: chữ lớn xếp tầng, từng dòng đập vào theo lời ----------
     sfx: mỗi item.at -> thud nhẹ */
  const { SLAM, beat } = makeBeat({ tl, el, esc, rnd });   // beat.js: thư viện hiệu ứng chữ dùng chung với casewide
  // "sm": true = dòng phụ nhỏ (như casewide.js: trần 56 thay 130 ở khung 1920 ngang -> 64 thay 150 ở khung dọc),
  // nét 700 + màu giấy (.kin.sm trong casefile.css). Không có "sm" -> cỡ/class y hệt cũ.
  B.kinetic = (s, d) => {
    const term = (q) => TH.prompt && q.fx === "type", cap = (q) => (q.sm ? 64 : 150);
    const it = s.items, sizes = it.map((q) => q.size || (term(q) ? fsz("> " + q.text, cap(q), 900, 0.8) : fsz(q.text, cap(q), 960, 0.8))),
          lh = (k) => (it[k].sm ? 1.4 : 1.08),   // dòng nhỏ: chừa chỗ cho dấu tiếng Việt của dòng lớn kề bên
          total = sizes.reduce((a, b, k) => a + b * lh(k), 0);
    let y = Math.max(300, (s.cy || (s.win ? 1235 : 820)) - total / 2);
    it.forEach((q, k) => { const e = el("div", "kin" + (q.acc ? " acc" : "") + (q.serif ? " serif" : "") + (q.sm ? " sm" : ""), esc(q.text), d); Object.assign(e.style, { fontSize: px(sizes[k]), top: px(y) }); y += sizes[k] * lh(k);
      if (q.c) e.style.color = ccol(q.c);   // màu riêng của dòng (CK: đỏ/xanh theo bảng giá); không ghi -> như cũ
      if (LK.kin === "left" && !s.win) { e.style.textAlign = "left"; e.style.left = px(96); }
      else if (LK.kin === "tilt") gsap.set(e, { rotation: -3.5, transformOrigin: "50% 50%" });
      beat(e, q); });
    if (LK.kin === "left" && !s.win) { const bar = el("div", "kbar", null, d), y0 = Math.max(300, (s.cy || 820) - total / 2);
      Object.assign(bar.style, { top: px(y0 + 8), height: px(Math.max(40, total - 16)) });
      tl.fromTo(bar, { scaleY: 0 }, { scaleY: 1, duration: 0.4, ease: "power3.out", immediateRender: false }, s.t0 + 0.05); }
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
    const lines = s.text.split("\n"), fs = fsz(lines.reduce((a, b) => (a.length > b.length ? a : b)), 170, 960, 0.8);
    const sl = el("div", "slam", lines.map(esc).join("<br/>"), d); Object.assign(sl.style, { fontSize: px(fs), top: px(820 - fs * lines.length / 2), lineHeight: 1.02, color: s.white ? "#fff" : "" });
    if (s.fx && s.fx !== "punch" && SLAM[s.fx]) SLAM[s.fx](sl, s);
    else tl.fromTo(sl, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in", immediateRender: false }, s.at - 0.13);
    if (s.sub) { const sb = el("div", "dsub mono", esc(s.sub), d); sb.style.top = px(840 + fs * lines.length / 2 + 30); sb.style.fontSize = px(fsz(s.sub, 30, 980, 0.84)); tl.to(sb, { opacity: 1, duration: 0.3 }, s.at + 0.3); }
    tl.to("#stage", { x: 12, duration: 0.03, yoyo: true, repeat: 5 }, s.at + 0.05);
  };

  /* ---------- chart: biểu đồ cột / đường (kênh CK "Biểu Đồ Biết Nói"; style ở theme-ck.css) ----------
     kind "bars": bars[{label, v, text, c, at, ghost?, gapAt?, gapText?}] mọc từ đường 0 (âm thì mọc xuống);
       ghost = khung đứt nét tới giá trị cũ, phần hụt tô đỏ lúc gapAt (vd. sức mua 100 -> 95,7).
     kind "line": points[{x?, v, at, tag?, pos?, c?}] vẽ dần từng đoạn tới mốc điểm sau (lên = xanh, xuống = đỏ);
       tag = nhãn cạnh điểm (pos "t"/"b"/"l"/"r"), ticks[{x, label}] = nhãn trục ngang. x theo thời gian thật, không giãn đều.
     Chung: title, unit, grid[] (vạch ngang + số), ref{v, label, at, below?}, badge{text, at, c, y}, note (dòng nguồn).
     Trục dọc tính từ 0 cho cột (không phóng đại chênh lệch); đường thì vừa khít dữ liệu, có grid ghi số.
     sfx: bar.at -> thud nhẹ + tick; point.at -> blip; badge.at -> thud; gapAt -> scratch */
  const nfmt = (v) => String(v).replace(".", ",");
  B.chart = (s, d) => {
    const line = s.kind === "line", X0 = s.left || 150, X1 = s.right || 940, Y0 = s.top || 560, Y1 = s.bottom || 1150, H = Y1 - Y0;
    const vals = line ? s.points.map((p) => p.v) : s.bars.flatMap((b) => [b.v, b.ghost ?? b.v]);
    if (s.ref) vals.push(s.ref.v);
    let lo = Math.min(...vals), hi = Math.max(...vals);
    if (!line) { lo = Math.min(0, lo); hi = Math.max(0, hi); }
    const span = hi - lo || 1, vmin = s.min ?? (line ? lo - span * 0.15 : lo), vmax = s.max ?? hi + span * (line ? 0.2 : 0.16);
    const Y = (v) => Y1 - ((v - vmin) / (vmax - vmin)) * H;
    tl.fromTo(d, { scale: 1.0 }, { scale: 1.03, transformOrigin: "50% 45%", duration: Math.max(0.3, s.t1 - s.t0), ease: "none", immediateRender: false }, s.t0);
    if (s.title) { const t = el("div", "chtitle", esc(s.title), d); t.style.fontSize = px(fsz(s.title, 60, 960, 0.72)); t.style.top = px(s.titleY || Y0 - 210);
      tl.fromTo(t, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, s.t0 + 0.02); }
    if (s.unit) { const u = el("div", "chunit mono", esc(s.unit), d); u.style.fontSize = px(fsz(s.unit, 28, 1000, 0.82)); u.style.top = px(s.titleY ? s.titleY + 84 : Y0 - 122); tl.to(u, { opacity: 1, duration: 0.3 }, s.t0 + 0.15); }
    const svg = sv("svg", { class: "layer", viewBox: "0 0 1080 1920" }, d);
    (s.grid || []).forEach((g) => { const y = Y(g), gl = sv("line", { x1: X0, y1: y, x2: X1, y2: y, class: "chgrid", opacity: 0 }, svg);
      const t = sv("text", { x: X0 - 16, y: y + 9, class: "chgl", "text-anchor": "end", opacity: 0 }, svg); t.textContent = nfmt(g);
      tl.fromTo([gl, t], { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, s.t0 + 0.1); });
    const yb = line ? Y1 : Y(0), axis = sv("line", { x1: X0 - 24, y1: yb, x2: X1 + 24, y2: yb, class: "chaxis" }, svg);
    draw(axis, s.t0 + 0.05, 0.35);
    if (line) {
      const P = s.points, xs = P.map((p, k) => p.x ?? k), xa = Math.min(...xs), xb = Math.max(...xs);
      const X = (x) => X0 + ((x - xa) / ((xb - xa) || 1)) * (X1 - X0);
      (s.ticks || []).forEach((q) => { const t = sv("text", { x: X(q.x), y: Y1 + 52, class: "chtick", "text-anchor": "middle", opacity: 0 }, svg); t.textContent = q.label;
        tl.fromTo(t, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, s.t0 + 0.2); });
      for (let k = 0; k < P.length - 1; k++) {
        const a = P[k], b = P[k + 1], col = ccol(b.c || (b.v >= a.v ? "up" : "down"));
        const seg = sv("line", { x1: X(xs[k]), y1: Y(a.v), x2: X(xs[k + 1]), y2: Y(b.v), stroke: col, "stroke-width": 11, "stroke-linecap": "round", class: "chseg" }, svg);
        const dd = Math.max(0.25, Math.min(0.9, b.at - a.at - 0.05));
        draw(seg, b.at - dd, dd, "power1.inOut");          // đường chạm điểm sau ĐÚNG lúc nó được đọc
      }
      P.forEach((p, k) => { const x = X(xs[k]), y = Y(p.v), g = sv("g", { opacity: 0 }, svg);
        sv("circle", { cx: x, cy: y, r: 30, fill: "var(--red)", opacity: 0.22 }, g); sv("circle", { cx: x, cy: y, r: 14, fill: "#fff", stroke: "var(--red)", "stroke-width": 6 }, g);
        tl.fromTo(g, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, Math.max(s.t0, (k ? p.at : P[0].at) - 0.05));
        if (p.tag) { const pos = p.pos || "t", t = sv("text", { x: pos === "l" ? x - 40 : pos === "r" ? x + 40 : x, y: pos === "b" ? y + 78 : pos === "t" ? y - 46 : y + 14,
            class: "chtag", "text-anchor": pos === "l" ? "end" : pos === "r" ? "start" : "middle", opacity: 0 }, svg); t.textContent = p.tag;
          if (p.c) t.style.fill = ccol(p.c);
          tl.fromTo(t, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, p.at + 0.1); } });
    } else {
      const n = s.bars.length, gap = n > 3 ? 36 : 80, bw = Math.min(260, (X1 - X0 - gap * (n - 1)) / n), L0 = (X0 + X1) / 2 - (n * bw + (n - 1) * gap) / 2, y0 = Y(0);
      s.bars.forEach((b, k) => {
        const x = L0 + k * (bw + gap), up = b.v >= 0, top = up ? Y(b.v) : y0, h = Math.max(6, Math.abs(Y(b.v) - y0)), col = ccol(b.c || (up ? "up" : "down"));
        if (b.ghost != null) { const gt = Y(b.ghost), gh = el("div", "chghost", null, d); Object.assign(gh.style, { left: px(x), width: px(bw), top: px(gt), height: px(y0 - gt) });
          tl.fromTo(gh, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, b.at - 0.2);
          if (b.gapAt != null) { const gp = el("div", "chgap", null, d); Object.assign(gp.style, { left: px(x), width: px(bw), top: px(gt), height: px(Math.max(6, Y(b.v) - gt)) });
            tl.fromTo(gp, { opacity: 0, scaleY: 0 }, { opacity: 1, scaleY: 1, transformOrigin: "50% 100%", duration: 0.35, ease: "power3.out", immediateRender: false }, b.gapAt);
            if (b.gapText) { const gh2 = Y(b.v) - gt, gx = el("div", "chgapt", esc(b.gapText), d);   // chữ giữa phần hụt; phần hụt mỏng -> ngay trên khung
              Object.assign(gx.style, { left: px(x - gap / 2), width: px(bw + gap), top: px(gh2 > 70 ? gt + gh2 / 2 - 26 : gt - 64) });
              tl.fromTo(gx, { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power3.out", immediateRender: false }, b.gapAt + 0.15); } } }
        const bar = el("div", "chbar", null, d);
        Object.assign(bar.style, { left: px(x), width: px(bw), top: px(top), height: px(h), transformOrigin: up ? "50% 100%" : "50% 0%",
          background: `linear-gradient(180deg, ${col} 0%, color-mix(in srgb, ${col} 55%, #050912) 100%)`, boxShadow: `0 0 50px color-mix(in srgb, ${col} 35%, transparent)` });
        tl.fromTo(bar, { scaleY: 0 }, { scaleY: 1, duration: 0.6, ease: "power3.out", immediateRender: false }, b.at - 0.1);
        if (b.text) { const v = el("div", "chval", esc(b.text), d); v.style.fontSize = px(fsz(b.text, 76, bw + gap - 10, 0.6));
          // cột có khung "ghost": số nằm TRONG cột (phía trên là phần hụt + chữ hụt)
          Object.assign(v.style, { left: px(x - gap / 2), width: px(bw + gap), top: px(b.ghost != null ? top + 22 : up ? top - 96 : top + h + 14), color: b.ghost != null ? "#fff" : col });
          tl.fromTo(v, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, b.at + 0.3); }
        if (b.label) { const lb = el("div", "chlbl", esc(b.label).replace(/\n/g, "<br/>"), d);
          Object.assign(lb.style, { left: px(x - gap / 2 + 4), width: px(bw + gap - 8), top: px(up ? y0 + 22 : y0 - 22 - 44 * (b.label.split("\n").length)) });
          tl.fromTo(lb, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, b.at - 0.15); }
      });
    }
    if (s.ref) { const top2 = sv("svg", { class: "layer", viewBox: "0 0 1080 1920" }, d);   // trên các cột (cột là div vẽ sau svg nền)
      const y = Y(s.ref.v), rl = sv("line", { x1: X0 - 10, y1: y, x2: X1 + 10, y2: y, class: "chref" }, top2); draw(rl, s.ref.at, 0.5, "power1.inOut");
      if (s.ref.label) { const t = sv("text", { x: X0 - 10, y: s.ref.below ? y + 44 : y - 18, class: "chreft", "text-anchor": "start", opacity: 0 }, top2); t.textContent = s.ref.label;
        tl.fromTo(t, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, s.ref.at + 0.3); } }
    if (s.badge) { const bg = el("div", "chbadge", esc(s.badge.text), d); bg.style.fontSize = px(fsz(s.badge.text, 92, 960, 0.76)); bg.style.top = px(s.badge.y || 1310);
      if (s.badge.c) bg.style.color = ccol(s.badge.c);
      tl.fromTo(bg, { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in", immediateRender: false }, s.badge.at - 0.12); }
    if (s.note) { const nt = el("div", "chnote mono", esc(s.note), d); nt.style.top = px(s.noteY || 1428); tl.to(nt, { opacity: 1, duration: 0.3 }, s.t0 + 0.4); }
  };

  /* ---------- board: bảng trắng vẽ tay (12/10/2026: Short phải phối chữ / hình / biểu đồ / sơ đồ) ----------
     nodes[{text, x, y, at, shape? "box"|"circle"|"none", c? "acc", cross?: mốc gạch chéo}] -- x, y là tâm, tỉ lệ 0..1 trên bảng;
     arrows[{from, to, at, label?}] -- chỉ số node; nét vẽ dần ĐÚNG lúc at. title, note (dòng nguồn dưới bảng).
     Nét run tay tất định (rnd có hạt). sfx: node.at -> scratch; arrow.at -> whoosh; cross -> scratch */
  B.board = (s, d) => {
    const BS = LK.board || "paper", INK = { paper: "#1f2937", chalk: "#f4f1e8", blueprint: "#bfe9ff", lined: "#1e3a8a", glass: "#e8f7ff" }[BS] || "#1f2937";
    const CW = BS === "blueprint" ? 0.63 : BS === "glass" ? 0.6 : 0.5;   // bề rộng chữ theo phông của kiểu bảng
    const W = 940, H = s.h || 880, X0 = 70, Y0 = s.top || 450;
    const bd = el("div", "board bd-" + BS, null, d); Object.assign(bd.style, { left: px(X0), top: px(Y0), width: px(W), height: px(H) });
    tl.fromTo(bd, { opacity: 0, y: 90, rotation: 2.5 }, { opacity: 1, y: 0, rotation: -0.8, duration: 0.45, ease: "power3.out", immediateRender: false }, s.t0);
    tl.to(bd, { scale: 1.03, duration: Math.max(0.3, s.t1 - s.t0 - 0.45), ease: "none" }, s.t0 + 0.45);
    if (s.title) { const t = el("div", "bdt", esc(s.title), bd); t.style.fontSize = px(fsz(s.title, 76, W - 100, CW)); t.style.color = INK; t.style.borderBottomColor = INK; }
    const svg = sv("svg", { class: "bdsvg", viewBox: `0 0 ${W} ${H}`, width: W, height: H }, bd);
    const j = (a) => (rnd() - 0.5) * a, col = (q) => (q.c === "acc" ? "var(--red)" : q.c ? ccol(q.c) : INK);
    const N = (s.nodes || []).map((q) => { const fs = Math.min(q.size || 68, fsz(q.text, q.size || 68, (q.w || 640) - 40, CW)), w = Math.max(150, [...q.text].length * fs * CW + 64), h = fs + 54;
      return { q, fs, w, h, cx: q.x * W, cy: q.y * H }; });
    N.forEach((n) => { const { q, fs, w, h, cx, cy } = n, x = cx - w / 2, y = cy - h / 2, c = col(q), shape = q.shape || "box";
      if (shape === "box") { const p = sv("path", { d: `M${x + j(8)} ${y + j(8)} L${x + w + j(10)} ${y + j(10)} L${x + w + j(10)} ${y + h + j(8)} L${x + j(10)} ${y + h + j(10)} L${x + j(6)} ${y - 6 + j(6)}`,
        stroke: c, "stroke-width": 6, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, svg); draw(p, q.at - 0.12, 0.42); }
      else if (shape === "circle") { const rx = w / 2 + 8, ry = h / 2 + 10; const p = sv("path", { d: `M${cx + rx} ${cy + j(6)} C${cx + rx} ${cy - ry * 1.25} ${cx - rx} ${cy - ry * 1.2} ${cx - rx} ${cy + j(6)} C${cx - rx} ${cy + ry * 1.25} ${cx + rx + 10} ${cy + ry * 1.15} ${cx + rx - 6} ${cy - 12}`,
        stroke: c, "stroke-width": 6, fill: "none", "stroke-linecap": "round" }, svg); draw(p, q.at - 0.12, 0.42); }
      const t = el("div", "bdn", esc(q.text), bd); Object.assign(t.style, { left: px(x), top: px(y), width: px(w), height: px(h), lineHeight: px(h), fontSize: px(fs), color: c });
      tl.fromTo(t, { opacity: 0, scale: 0.86 }, { opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2)", immediateRender: false }, q.at);
      if (q.cross != null) { [[x + 14, y + 10, x + w - 14, y + h - 10], [x + w - 14, y + 10, x + 14, y + h - 10]].forEach((v, k) => {
        const ln = sv("path", { d: `M${v[0]} ${v[1]} L${v[2] + j(8)} ${v[3] + j(8)}`, stroke: "var(--red)", "stroke-width": 9, fill: "none", "stroke-linecap": "round" }, svg); draw(ln, q.cross + k * 0.14, 0.16, "power2.in"); }); } });
    (s.arrows || []).forEach((a) => { const A = N[a.from], Bn = N[a.to]; if (!A || !Bn) throw new Error("board: arrow trỏ tới node không có");
      const dx = Bn.cx - A.cx, dy = Bn.cy - A.cy, L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L;
      const edge = (n, sx, sy) => Math.min(Math.abs(sx) > 0.001 ? (n.w / 2 + 16) / Math.abs(sx) : 1e9, Math.abs(sy) > 0.001 ? (n.h / 2 + 16) / Math.abs(sy) : 1e9);
      const x1 = A.cx + ux * edge(A, ux, uy), y1 = A.cy + uy * edge(A, ux, uy), x2 = Bn.cx - ux * edge(Bn, ux, uy), y2 = Bn.cy - uy * edge(Bn, ux, uy);
      const bend = (a.bend ?? 0.12) * L, mx = (x1 + x2) / 2 - uy * bend, my = (y1 + y2) / 2 + ux * bend, c = a.c === "acc" ? "var(--red)" : INK;
      const p = sv("path", { d: `M${x1} ${y1} Q${mx} ${my} ${x2} ${y2}`, stroke: c, "stroke-width": 6, fill: "none", "stroke-linecap": "round" }, svg); draw(p, a.at - 0.05, 0.35);
      const tx = x2 - mx, ty = y2 - my, tL = Math.hypot(tx, ty) || 1, hx = tx / tL, hy = tL ? ty / tL : 0;
      [0.5, -0.5].forEach((r) => { const cs = Math.cos(r), sn = Math.sin(r), bx = -(hx * cs - hy * sn), by = -(hx * sn + hy * cs);
        const hd = sv("path", { d: `M${x2} ${y2} L${x2 + bx * 34} ${y2 + by * 34}`, stroke: c, "stroke-width": 6, fill: "none", "stroke-linecap": "round" }, svg); draw(hd, a.at + 0.28, 0.12); });
      if (a.label) { const lb = el("div", "bdl", esc(a.label), bd); const off = Math.abs(bend) < 1 ? -250 : 34;   // mũi tên thẳng: nhãn đứng hẳn sang một bên, không đè lên nét
        Object.assign(lb.style, { left: px(mx - 200 - uy * off), top: px(my - 30 + ux * off), width: px(400), color: c });
        tl.fromTo(lb, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, a.at + 0.2); } });
    if (s.note) { const nt = el("div", "bdnote mono", esc(s.note), d); nt.style.top = px(Y0 + H + 26); tl.to(nt, { opacity: 1, duration: 0.3 }, s.t0 + 0.4); }
  };

  /* ---------- cards3d: 2–3 thẻ kính lật trong không gian 3D (so sánh A / B) ----------
     cards[{k, v, sub?, at, c? "acc"|"up"|"down"|mã màu}] xếp dọc; mỗi thẻ lật lên đúng lúc at rồi nghiêng trôi chậm. title, note.
     sfx: card.at -> whoosh(-0.15) + thud */
  B.cards3d = (s, d) => {
    const n = s.cards.length, Hc = n <= 2 ? 370 : 280, gap = 46, tot = n * Hc + (n - 1) * gap, top = Math.max(430, 900 - tot / 2);
    if (s.title) { const t = el("div", "c3t", esc(s.title), d); t.style.fontSize = px(fsz(s.title, 60, 940, /[MW]/.test(s.title) ? 0.7 : 0.64)); t.style.top = px(top - 130);
      tl.fromTo(t, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, s.t0 + 0.02); }
    s.cards.forEach((c, k) => { const col = c.c === "acc" ? "var(--red)" : c.c ? ccol(c.c) : "#fff", dir = k % 2 ? 1 : -1;
      const CS = LK.cards || "glass";
      const e = el("div", "c3 c3-" + CS, `<div class="c3k">${esc(c.k)}</div><div class="c3v">${esc(c.v)}</div>${c.sub ? `<div class="c3s">${esc(c.sub)}</div>` : ""}`, d);
      Object.assign(e.style, { top: px(top + k * (Hc + gap)), height: px(Hc), borderColor: col });
      const v = e.querySelector(".c3v"); v.style.color = col; v.style.fontSize = px(fsz(c.v, n <= 2 ? 170 : 130, 700, /[MW]/.test(c.v) ? 0.72 : 0.66));
      if (CS === "solid") { e.style.background = c.c ? col : "#e2e8f0"; v.style.color = "#06121a"; }
      else if (CS === "index") { v.style.color = c.c ? col : "#111827"; gsap.set(e, { rotation: dir * 1.6 }); }
      else if (CS === "gradient") { e.style.background = `linear-gradient(135deg, color-mix(in srgb, ${col} 82%, #000) 0%, color-mix(in srgb, ${col} 30%, #0b1220) 100%)`; v.style.color = "#fff"; }
      gsap.set(e, { transformPerspective: 1300, transformOrigin: "50% 100%" });
      tl.fromTo(e, { opacity: 0, rotationX: -92, rotationY: 0, y: 110 }, { opacity: 1, rotationX: 0, rotationY: 11 * dir, y: 0, duration: 0.55, ease: "back.out(1.3)", immediateRender: false }, c.at - 0.15);
      tl.to(e, { rotationY: -7 * dir, rotationX: 3, duration: Math.max(0.4, s.t1 - c.at - 0.4), ease: "sine.inOut" }, c.at + 0.4); });
    if (s.note) { const nt = el("div", "bdnote mono", esc(s.note), d); nt.style.top = px(top + tot + 34); tl.to(nt, { opacity: 1, duration: 0.3 }, s.t0 + 0.4); }
  };

  // ---------- dựng cảnh ----------
  if (window.HFS && window.HFS.mount) window.HFS.mount(tl, C, B);   // BUD v2.1: thiết bị Shorts Studio -> B.hf_* (chỉ khi bridge được nạp)
  C.scenes.forEach((s, i) => {
    const d = el("div", "scene", null, stage); show(d, s.t0, s.t1, s.type === "question" ? 0.06 : 0.1);
    if (!B[s.type]) throw new Error("loại cảnh lạ: " + s.type);
    if (s.vid) {   // nền video: đẩy máy chậm + màn che (chữ phía trên vẫn đọc rõ); thẻ <video> do build.py nướng sẵn
      const v = document.getElementById(s.vid) || (window.__HF_CHECK ? el("div", "clip bv", null, document.getElementById("root")) : null); if (!v) throw new Error("thiếu video " + s.vid);   // __HF_CHECK: bản sao cho `hyperframes check` (BUD v2) -- trình kiểm tách thẻ video
      if (s.win) {   // cửa sổ video (12/10/2026): hình chiếm nửa trên, chữ/số nằm dưới -- hình và chữ cùng lúc, không che nhau
        const WS = LK.win || "top", G = { top: [215, 1010, 56, 1024, 40], tilt: [250, 980, 120, 960, 6], band: [330, 930, 0, 1080, 0], circle: [220, 1000, 150, 930, 390] }[WS] || [215, 1010, 56, 1024, 40];
        const T = G[0], Bt = G[1], L = G[2], R = G[3];
        v.style.clipPath = WS === "circle" ? `circle(${G[4]}px at 540px 610px)` : `inset(${T}px ${1080 - R}px ${1920 - Bt}px ${L}px round ${G[4]}px)`;
        v.style.objectPosition = s.winPos || "50% 35%";
        const fr = el("div", "vwin vw-" + WS, null, d); Object.assign(fr.style, { left: px(L), top: px(T), width: px(R - L), height: px(Bt - T) });
        if (WS === "tilt") { gsap.set(v, { rotation: -3, transformOrigin: "540px 615px" }); gsap.set(fr, { rotation: -3 }); }
        tl.fromTo(fr, { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 0.35, ease: "power3.out", immediateRender: false }, s.t0);
        if (s.winLabel) { const lb = el("div", "vwlbl mono", esc(s.winLabel), fr); tl.fromTo(lb, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.3, immediateRender: false }, s.t0 + 0.25); }
      } else {
      tl.fromTo(v, { scale: 1.08 }, { scale: 1.0, duration: Math.max(0.2, s.t1 - s.t0 + 0.3), ease: "none", immediateRender: false }, s.t0 - 0.2);
      const vl = el("div", "vveil", null, d), a = s.veil ?? 0.55;
      vl.style.background = `linear-gradient(180deg, rgba(4,8,16,${a + 0.15}) 0%, rgba(4,8,16,${a}) 40%, rgba(4,8,16,${a + 0.2}) 100%)`;
      }
    }
    B[s.type](s, d);
    if (i > 0 && C.mix && !s.tr) {   // chuyển cảnh Short phối: lia nhoè / đẩy vào
      const TR = LK.tr || ["whip", "zoom"], tr = TR[(i - 1) % TR.length];
      if (tr === "whip") tl.fromTo(d, { x: i % 4 === 1 ? 110 : -110, filter: "blur(18px)" }, { x: 0, filter: "blur(0px)", duration: 0.26, ease: "power3.out", immediateRender: false }, s.t0);
      else if (tr === "up") tl.fromTo(d, { y: 150 }, { y: 0, duration: 0.32, ease: "power3.out", immediateRender: false }, s.t0);
      else if (tr === "swipe") tl.fromTo(d, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.32, ease: "power3.inOut", immediateRender: false }, s.t0);
      else if (tr === "flash") { flash(s.t0, 0.3); tl.fromTo(d, { scale: 1.06 }, { scale: 1, duration: 0.3, ease: "power2.out", immediateRender: false }, s.t0); }
      else tl.fromTo(d, { scale: 1.14, filter: "blur(14px)" }, { scale: 1, filter: "blur(0px)", duration: 0.28, ease: "power3.out", immediateRender: false }, s.t0);
    } else
    if (i > 0) { const tr = s.tr || ["leak", "flash", "cut"][i % 3]; if (tr === "leak") leak(s.t0 - 0.08); else if (tr === "flash") flash(s.t0, 0.25); }
  });

  // ---------- không khí ----------
  for (let i = 0; i < 38; i++) { const m = el("div", "mote", null, $("#motes")); Object.assign(m.style, { left: px(rnd() * 1080), top: px(rnd() * 1920), transform: `scale(${0.5 + rnd() * 1.4})` });
    tl.to(m, { y: -160 - rnd() * 260, x: (rnd() - 0.5) * 140, opacity: 0.2 + rnd() * 0.6, duration: DUR, ease: "none" }, 0); }
  tl.to("#prog i", { scaleX: 1, duration: DUR, ease: "none" }, 0);
  if (TH.drift) tl.fromTo("#bed", { backgroundPosition: "0px 0px, 0px 0px, 50% 0%" },
    { backgroundPosition: `0px ${Math.round(DUR * 14)}px, ${Math.round(DUR * 6)}px 0px, 50% 0%`, duration: DUR, ease: "none", immediateRender: true }, 0);
  for (let k = 0; k < Math.ceil(DUR * 2); k++) tl.set("#grain", { opacity: 0.08 + ((k * 37) % 7) / 100 }, k * 0.5);
  $("#kicker .t").innerHTML = esc(C.kicker) + `<small>${esc(C.sub || "")}</small>`;

  // ---------- phụ đề: cụm 2–4 từ, một màu nhấn ----------
  const ACC = new Set((C.acc || []).map(norm));
  const caps = $("#caps"), chunks = [], ALLW = C.lines.flatMap((ln) => ln.words);
  C.lines.forEach((ln) => { let cur = []; ln.words.forEach((w, k) => { cur.push(w);
    if (/[.,…?!:;]$/.test(w.w) || cur.length >= 4 || k === ln.words.length - 1) { chunks.push(cur); cur = []; } }); });
  chunks.forEach((c, n) => { const box = el("div", "cap", null, caps);
    c.forEach((w) => { const clean = w.w.replace(/["“”]/g, ""), acc = ACC.has(norm(w.w)) || /\d/.test(w.w);
      const sp = el("span", "cw" + (acc ? " acc" : ""), esc(clean), box); tl.to(sp, { opacity: 1, duration: 0.08 }, w.t);
      if (TH.karaoke && !acc) { tl.set(sp, { color: C.accent }, w.t); const nx = ALLW[ALLW.indexOf(w) + 1]; tl.set(sp, { color: "#f4f7fb" }, nx ? nx.t : w.t + 0.4); }
      // Beat Text MIM: từ nhấn (không phải số) nảy nhẹ ĐÚNG lúc được đọc -- chỉ transform, <=0.12s (Grok: to hơn là
      // kiểu "Hormozi bounce" engine tránh, và cắt dòng 62px).
      if (TH.pop && ACC.has(norm(w.w))) tl.fromTo(sp, { scale: 1 }, { scale: 1.06, duration: 0.06, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, w.t); });
    const t0 = c[0].t - 0.06, nx = chunks[n + 1], t1 = nx ? nx[0].t - 0.06 : DUR;
    tl.set(box, { opacity: 1 }, t0); tl.set(box, { opacity: 0 }, t1); });
  C.scenes.filter((s) => s.type === "question" || (s.type === "quote" && s.mode === "karaoke") || s.loop).forEach((s) => { tl.set("#caps", { opacity: 0 }, s.t0 - 0.01); tl.set("#caps", { opacity: 1 }, s.t1); });

  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = tl;
})();
