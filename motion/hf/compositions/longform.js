/* ===== VIDEO DÀI: bố cục ảnh, sơ đồ dữ liệu, thẻ chương =====
   Nạp SAU engine.js và TRƯỚC HF.build(). engine.js gọi vào window.HF_LONG khi
   một câu có `visual` (sơ đồ), `media.layout` (bố cục ảnh khác ô mặc định của
   style), hoặc `chapter_no` (câu tiêu đề chương của video dài).

   Nguyên tắc (skill hyperframes-animation / faceless-explainer):
   - Không một bố cục cho cả video -- mỗi cảnh một việc, luân phiên bố cục.
   - Thứ gì trên sơ đồ cũng hiện ĐÚNG LÚC giọng đọc nhắc tới (bước `at` = số
     thứ tự câu, `word` = từ trong câu đó), không đổ hết ra ở giây đầu.
   - Mọi chuyển động nằm trên timeline GSAP đã pause -- tất định khi seek.
   - Sơ đồ vẽ từ dữ liệu plan (tên chi, quan hệ, ngũ hành) mà plan đã đối chiếu
     tay; file này không tự suy ra quan hệ nào. */
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const el = (t, c, x) => HF.el(t, c, x);
  function sv(tag, attrs, parent) {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs || {}) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  const CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"];
  const REL = {  // màu + nhãn mặc định của từng quan hệ
    xung: ["--lf-xung", "LỤC XUNG"], tamhinh: ["--lf-hinh", "TAM HÌNH"], tamhop: ["--lf-hop", "TAM HỢP"],
    luchop: ["--lf-luchop", "LỤC HỢP"], hai: ["--lf-hai", "LỤC HẠI"], pha: ["--lf-hinh", "LỤC PHÁ"],
    focus: ["--accent", ""],
  };
  const ELEM = ["Hỏa", "Thổ", "Kim", "Thủy", "Mộc"];  // theo chiều kim đồng hồ = vòng tương sinh
  const ELEM_COLOR = { "Mộc": "#5fae5a", "Hỏa": "#e05a47", "Thổ": "#d0a44c", "Kim": "#e6e1d3", "Thủy": "#4c86e0" };
  const ELEM_INK = { "Mộc": "#0b1130", "Hỏa": "#0b1130", "Thổ": "#0b1130", "Kim": "#0b1130", "Thủy": "#f3f6ff" };
  const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim() || "#d4a93a";
  const clean = (s) => (s || "").replace(/\*\*/g, "").trim();
  // Short dọc (1080x1920) chỉ mượn các cảnh chữ/minh hoạ; chuyển cảnh + không khí
  // giữ của riêng style short (đã chỉnh cho nhịp 30 giây).
  const PORTRAIT = document.documentElement.getAttribute("data-resolution") === "portrait";

  // Thời điểm của một bước: đầu câu `at` (+ lệch), hoặc lúc giọng đọc tới `word`.
  function when(ctx, step, fallback) {
    const L = step && step.at ? ctx.LINES[step.at - 1] : null;
    if (!L) return fallback;
    if (step.word) {
      const key = step.word.toLowerCase();
      const w = (L.words || []).find((x) => clean(x.w).toLowerCase().includes(key));
      if (w) return w.t;
    }
    return L.start + (step.offset != null ? step.offset : 0.3);
  }
  function drawOn(tl, path, at, dur, ease) {
    const len = path.getTotalLength ? path.getTotalLength() : 1000;
    path.style.strokeDasharray = `${len}`;
    tl.fromTo(path, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur, ease: ease || "power2.inOut" }, at);
  }
  /* ---------- Bộ chọn đa dạng (kho hiệu ứng) ----------
     Mỗi họ hiệu ứng (chuyển cảnh, thẻ chương, bố cục, lối vào sơ đồ...) có
     nhiều biến thể. pick() lấy biến thể ÍT DÙNG NHẤT trong video, không bao
     giờ trùng lần ngay trước, hoà thì bốc bằng rng hạt giống theo nội dung
     video -- cùng video render lại ra y hệt, video khác ra tổ hợp khác. */
  let R = () => 0.5, USED = {};
  function begin(LINES) {
    const sig = (LINES || []).slice(0, 3).map((l) => (l.words || []).map((w) => w.w).join(" ")).join("|");
    R = HF.rng(HF.hashSeed(sig + "|" + (LINES || []).length));
    USED = {};
  }
  function pick(family, options) {
    const u = USED[family] || (USED[family] = { c: {}, last: null });
    let pool = options.filter((o) => o !== u.last);
    if (!pool.length) pool = options.slice();
    const lo = Math.min(...pool.map((o) => u.c[o] || 0));
    const cand = pool.filter((o) => (u.c[o] || 0) === lo);
    const ch = cand[Math.floor(R() * cand.length) % cand.length];
    u.c[ch] = (u.c[ch] || 0) + 1; u.last = ch;
    return ch;
  }
  // Biến thể do plan chỉ định (spec.variant) thắng; không có thì để kho chọn.
  const variantOf = (family, spec, options) =>
    (spec && spec.variant && options.includes(spec.variant)) ? spec.variant : pick(family, options);

  function title(parent, text, left, top) {
    if (!text) return null;
    const t = el("div", "lf-title", text);
    t.style.left = left + "px"; t.style.top = top + "px";
    parent.appendChild(t);
    return t;
  }

  /* ---------------- Bố cục ảnh ---------------- */
  const layouts = {
    // Ảnh tràn khung, tối dần xuống đáy để phụ đề đọc được.
    full: {
      // Chữ khoá của câu (cụm **đánh dấu**) bật lên góc trên, đúng lúc được đọc.
      build(inner, ln) {
        inner.appendChild(el("div", "lf-full-shade"));
        const hot = (ln.key_parts || []).filter((p) => p.hot).map((p) => p.t).join(" ");
        if (hot && hot.length <= 34) {
          const c = el("div", "lf-callout");
          c.appendChild(el("div", "bar"));
          const t = el("div", "tx");
          hot.split(/\s+/).forEach((w) => t.appendChild(el("span", "", w)));
          c.appendChild(t); inner.appendChild(c);
        }
      },
      enter(tl, inner, ln) {
        const c = inner.querySelector(".lf-callout"); if (!c) return;
        const first = (ln.key_parts || []).find((p) => p.hot);
        const w = first && (ln.words || []).find((x) => x.hot);
        const t = w ? w.t : ln.start + .4;
        tl.fromTo(c.querySelector(".bar"), { scaleY: 0, transformOrigin: "50% 100%" }, { scaleY: 1, duration: .35, ease: "power3.out" }, t - .1);
        tl.fromTo(c.querySelectorAll(".tx span"), { x: 60, opacity: 0 },
          { x: 0, opacity: 1, duration: .45, ease: "power4.out", stagger: .05 }, t);
      },
      enterCont(tl, inner, ln) { this.enter(tl, inner, ln); },
    },
    // Ảnh bên trái, chữ bên phải -- gương của split.
    split_r: {
      build(inner, ln) {
        const w = el("div", "lf-split lf-split-right card-box");
        const key = el("div", "lf-split-key", (ln.key_parts || []).map((p) => p.t).join(" "));
        if (key.textContent.length > 26) key.classList.add("long");
        w.appendChild(key); w.appendChild(el("div", "lf-split-rule"));
        inner.appendChild(w);
      },
      enter(tl, inner, ln) {
        tl.fromTo(inner.querySelector(".lf-split-key"), { x: 90, opacity: 0 }, { x: 0, opacity: 1, duration: .6, ease: "power4.out" }, ln.start + .15);
        tl.fromTo(inner.querySelector(".lf-split-rule"), { width: 0 }, { width: 200, duration: .7, ease: "power2.out" }, ln.start + .35);
      },
      enterCont(tl, inner, ln) { this.enter(tl, inner, ln); },
      motion(tl, clip, ln, mEnd) {
        tl.fromTo(clip, { rotationY: 10, scale: 1, transformPerspective: 1900 },
          { rotationY: 3, scale: 1.04, duration: Math.max(1, mEnd - ln.start), ease: "sine.inOut" }, ln.start);
        return true;
      },
    },
    // Ảnh in có viền trắng, rơi xuống bàn nghiêng một chút rồi trôi chậm.
    polaroid: {
      build() {},
      motion(tl, clip, ln, mEnd) {
        const s = ln.sentence_id % 2 ? 1 : -1;
        tl.fromTo(clip, { y: -120, rotation: -9 * s, scale: 1.08 }, { y: 0, rotation: -3 * s, scale: 1, duration: .9, ease: "back.out(1.4)" }, ln.start);
        tl.to(clip, { rotation: -1.5 * s, y: -10, duration: Math.max(1, mEnd - ln.start - .9), ease: "sine.inOut" }, ln.start + .9);
        return true;
      },
    },
    // Ảnh là một tấm thẻ nghiêng trong không gian 3D, xoay chậm suốt khoảng giữ.
    card3d: {
      build() {},
      motion(tl, clip, ln, mEnd) {
        const s = ln.sentence_id % 2 ? 1 : -1;
        tl.fromTo(clip, { rotationY: -16 * s, rotationX: 7, scale: .93, transformPerspective: 1900 },
          { rotationY: -4 * s, rotationX: 2, scale: 1, duration: Math.max(1, mEnd - ln.start), ease: "sine.inOut" }, ln.start);
        return true;
      },
    },
    // Ảnh bên phải, ý chính của câu bên trái -- mỗi câu nối tiếp thay chữ.
    split: {
      build(inner, ln) {
        const w = el("div", "lf-split card-box");
        const key = el("div", "lf-split-key", (ln.key_parts || []).map((p) => p.t).join(" "));
        if (key.textContent.length > 26) key.classList.add("long");
        w.appendChild(key);
        w.appendChild(el("div", "lf-split-rule"));
        inner.appendChild(w);
      },
      enter(tl, inner, ln) {
        tl.fromTo(inner.querySelector(".lf-split-key"), { x: -90, opacity: 0 },
          { x: 0, opacity: 1, duration: .6, ease: "power4.out" }, ln.start + .15);
        tl.fromTo(inner.querySelector(".lf-split-rule"), { width: 0 }, { width: 200, duration: .7, ease: "power2.out" }, ln.start + .35);
      },
      enterCont(tl, inner, ln) { this.enter(tl, inner, ln); },
      motion(tl, clip, ln, mEnd) {
        tl.fromTo(clip, { rotationY: -10, scale: 1, transformPerspective: 1900 },
          { rotationY: -3, scale: 1.04, duration: Math.max(1, mEnd - ln.start), ease: "sine.inOut" }, ln.start);
        return true;
      },
    },
  };

  /* ---------------- Thẻ chương (5 biến thể) ---------------- */
  const CHAPTER_VARIANTS = ["zoom", "slam", "split", "roll", "depth"];
  const chapter = {
    build(inner, ln) {
      ln._chap = variantOf("chapter", ln, CHAPTER_VARIANTS);
      const w = el("div", "lf-chap lf-chap-" + ln._chap);
      const no = String(ln.chapter_no).padStart(2, "0");
      w.appendChild(el("div", "lf-chap-ghost", no));
      const lab = el("div", "lf-chap-no");
      if (ln._chap === "roll") {  // số chương lăn như đồng hồ cơ
        lab.appendChild(document.createTextNode("PHẦN "));
        const col = el("span", "lf-roll");
        const strip = el("span", "lf-roll-strip");
        for (let d = 0; d <= Number(no); d++) strip.appendChild(el("span", "", String(d).padStart(2, "0")));
        col.appendChild(strip); lab.appendChild(col);
      } else lab.textContent = "PHẦN " + no;
      w.appendChild(lab);
      const t = clean((ln.key_parts || []).map((p) => p.t).join(" ")).replace(/[.:;,]$/, "");
      const tt = el("div", "lf-chap-title");
      if (t.length > 34) tt.classList.add("long");
      if (ln._chap === "slam" || ln._chap === "roll") t.split(/\s+/).forEach((wd) => { const sp = el("span", "lf-word", wd); tt.appendChild(sp); });
      else tt.textContent = t;
      if (ln._chap === "depth") {  // chữ nổi khối: 6 lớp lùi sau, lớp trước cùng
        const stack = el("div", "lf-depth");
        for (let k = 6; k >= 1; k--) { const b = el("div", "lf-chap-title lf-depth-back", t); if (t.length > 34) b.classList.add("long");
          b.style.transform = `translate(${k * 3}px, ${k * 4}px)`; b.style.opacity = String(0.5 - k * 0.06); stack.appendChild(b); }
        stack.appendChild(tt); w.appendChild(stack);
      } else w.appendChild(tt);
      if (ln._chap === "split") { w.appendChild(el("div", "lf-bar lf-bar-a")); w.appendChild(el("div", "lf-bar lf-bar-b")); }
      w.appendChild(el("div", "lf-chap-rule"));
      inner.appendChild(w);
      inner._lf = { t };
    },
    enter(tl, inner, ln) {
      const t0 = ln.start, span = Math.max(1.5, ln.end - ln.start), v = ln._chap;
      const q = (c) => inner.querySelector(c);
      tl.fromTo(q(".lf-chap-ghost"), { scale: .82, opacity: 0 }, { scale: 1.08, opacity: .5, duration: span + .6, ease: "power1.out" }, t0);
      tl.fromTo(q(".lf-chap-no"), { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: .6, ease: "power4.out" }, t0 + .1);
      const title = inner.querySelector(".lf-depth > .lf-chap-title:last-child") || q(".lf-chap-title");
      if (v === "zoom") {  // zoom-through: chữ lao từ sau ra, nhoè 10px (cut-catalog)
        tl.fromTo(title, { opacity: 0, scale: .75, rotationX: 26, filter: "blur(10px)", transformPerspective: 1200 },
          { opacity: 1, scale: 1, rotationX: 0, filter: "blur(0px)", duration: .95, ease: "expo.out" }, t0 + .05);
      } else if (v === "slam") {  // từng chữ đập xuống, khung rung nhẹ ở chữ cuối
        const ws = inner.querySelectorAll(".lf-word");
        tl.fromTo(ws, { opacity: 0, scale: 1.9, filter: "blur(8px)" },
          { opacity: 1, scale: 1, filter: "blur(0px)", duration: .32, ease: "power4.out", stagger: .1 }, t0 + .05);
        tl.fromTo(q(".lf-chap"), { x: 0 }, { x: 7, duration: .05, yoyo: true, repeat: 3, ease: "none" }, t0 + .05 + ws.length * .1);
      } else if (v === "split") {  // hai thanh vàng tách ra, chữ lộ giữa
        tl.fromTo(title, { clipPath: "inset(50% 0% 50% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: .75, ease: "power3.inOut" }, t0 + .15);
        tl.fromTo(q(".lf-bar-a"), { y: 0, opacity: 1 }, { y: -95, opacity: .0, duration: .9, ease: "power3.inOut" }, t0 + .15);
        tl.fromTo(q(".lf-bar-b"), { y: 0, opacity: 1 }, { y: 95, opacity: .0, duration: .9, ease: "power3.inOut" }, t0 + .15);
      } else if (v === "roll") {  // số lăn, rồi tiêu đề gõ ra từng chữ
        const n = Number(ln.chapter_no) || 1;
        tl.fromTo(q(".lf-roll-strip"), { yPercent: 0 }, { yPercent: -100 * n / (n + 1), duration: .8, ease: "power3.out" }, t0 + .1);
        // Gõ theo TỪNG TỪ: xén ngang cả khối làm tiêu đề hai dòng lộ ra theo cột,
        // giữa chừng thấy mảnh chữ vô nghĩa ("NĂM ĐINI").
        const ws = inner.querySelectorAll(".lf-word");
        tl.fromTo(ws, { opacity: 0 }, { opacity: 1, duration: .01, stagger: Math.min(.14, 1.2 / Math.max(1, ws.length)) }, t0 + .5);
      } else {  // depth: khối chữ xoay vào từ bên, các lớp sau dày dần
        tl.fromTo(q(".lf-depth"), { rotationY: -38, opacity: 0, transformPerspective: 1400 },
          { rotationY: 0, opacity: 1, duration: 1.0, ease: "power3.out" }, t0 + .05);
      }
      tl.fromTo(q(".lf-chap-rule"), { width: 0 }, { width: 360, duration: .8, ease: "power2.out" }, t0 + .45);
    },
  };

  /* ---------------- Sơ đồ ---------------- */
  const visuals = {
    // Vòng 12 con giáp, Tý ở đỉnh như mặt đồng hồ; quan hệ vẽ lần lượt theo lời.
    wheel: {
      build(inner, ln) {
        const v = ln.visual, S = { steps: [] };
        const st = el("div", "lf-stage"); inner.appendChild(st);
        const wrap = el("div", "lf-wheel"); st.appendChild(wrap);
        const svg = sv("svg", { viewBox: "-500 -500 1000 1000" }, wrap);
        const deco = sv("g", {}, svg);
        sv("circle", { r: 462, fill: "none", stroke: "var(--lf-line)", "stroke-width": 3 }, deco);
        for (let k = 0; k < 72; k++) {
          const a = (k / 72) * Math.PI * 2, r1 = 462, r2 = k % 6 ? 448 : 432;
          sv("line", { x1: Math.cos(a) * r1, y1: Math.sin(a) * r1, x2: Math.cos(a) * r2, y2: Math.sin(a) * r2,
            stroke: "var(--lf-line)", "stroke-width": k % 6 ? 1.5 : 3 }, deco);
        }
        sv("circle", { r: 250, fill: "none", stroke: "var(--lf-line)", "stroke-width": 1.5, "stroke-dasharray": "6 12" }, deco);
        const relG = sv("g", {}, svg);
        const pos = {};
        CHI.forEach((c, k) => {
          const a = (-90 + k * 30) * Math.PI / 180;
          pos[c] = [Math.cos(a) * 360, Math.sin(a) * 360];
        });
        const nodes = {};
        CHI.forEach((c) => {
          const g = sv("g", { transform: `translate(${pos[c][0]},${pos[c][1]})` }, svg);
          const inG = sv("g", {}, g);
          const circ = sv("circle", { r: 66, class: "node-c" }, inG);
          const txt = sv("text", { class: "node-t" }, inG); txt.textContent = c;
          nodes[c] = { g: inG, circ, txt };
        });
        (v.steps || []).forEach((step) => {
          const color = css((REL[step.rel] || REL.focus)[0]);
          const pts = (step.chi || []).map((c) => pos[c]).filter(Boolean);
          let path = null;
          if (step.rel !== "focus" && pts.length >= 2) {
            const d = "M" + pts.map((p) => p.join(",")).join(" L") + (pts.length > 2 ? " Z" : "");
            path = sv("path", { d, class: "rel", stroke: color }, relG);
          }
          S.steps.push({ step, color, path });
        });
        S.wrap = wrap; S.deco = deco; S.nodes = nodes; S.st = st;
        S.title = title(st, v.title || "VÒNG 12 CON GIÁP", 1090, 96);
        const legend = el("div", "lf-legend"); st.appendChild(legend);
        let row = 0;
        S.steps.forEach((s) => {
          const label = s.step.label || (REL[s.step.rel] || REL.focus)[1];
          if (!label) return;
          const chip = el("div", "lf-chip");
          chip.style.top = (row++ * 128) + "px";
          const bar = el("div", "bar"); bar.style.background = s.color;
          const box = el("div", "");
          const t1 = el("div", "t1", label); t1.style.color = s.color;
          box.appendChild(t1); box.appendChild(el("div", "t2", (s.step.chi || []).join(" – ")));
          chip.appendChild(bar); chip.appendChild(box);
          legend.appendChild(chip); s.chip = chip;
        });
        inner._lf = S;
      },
      enter(tl, inner, ln, ctx) {
        const S = inner._lf, v = ln.visual, t0 = ln.start, span = Math.max(2, ctx.until - t0);
        const nodeGs = Object.values(S.nodes).map((n) => n.g);
        const how = variantOf("wheel", v, ["tilt", "assemble", "spin"]);
        if (how === "tilt") {  // mặt đồng hồ nằm ngửa trong không gian 3D rồi dựng lên
          tl.fromTo(S.wrap, { rotationX: 62, rotationZ: -24, scale: .72, opacity: 0, transformPerspective: 1600 },
            { rotationX: 0, rotationZ: 0, scale: 1, opacity: 1, duration: 1.5, ease: "power3.out" }, t0);
          tl.fromTo(nodeGs, { scale: 0, transformOrigin: "50% 50%" },
            { scale: 1, duration: .6, ease: "back.out(2.2)", stagger: .045 }, t0 + .35);
        } else if (how === "assemble") {  // mười hai chi bay từ tâm ra đúng vị trí trên vòng
          tl.fromTo(S.wrap, { opacity: 0 }, { opacity: 1, duration: .4 }, t0);
          CHI.forEach((c, k) => {
            const a = (-90 + k * 30) * Math.PI / 180;
            tl.fromTo(S.nodes[c].g, { x: -Math.cos(a) * 360, y: -Math.sin(a) * 360, scale: .3 },
              { x: 0, y: 0, scale: 1, duration: .8, ease: "expo.out" }, t0 + .15 + k * .05);
          });
          tl.fromTo(S.deco, { scale: .6, svgOrigin: "0 0", opacity: 0 }, { scale: 1, opacity: 1, duration: 1.2, ease: "power3.out" }, t0 + .1);
        } else {  // spin: cả vòng xoay vào như bánh la bàn, dừng có đà
          tl.fromTo(S.wrap, { rotation: -150, scale: .55, opacity: 0 },
            { rotation: 0, scale: 1, opacity: 1, duration: 1.4, ease: "back.out(1.3)" }, t0);
          tl.fromTo(nodeGs, { scale: 0, transformOrigin: "50% 50%" },
            { scale: 1, duration: .5, ease: "back.out(2.4)", stagger: { each: .035, from: "random" } }, t0 + .6);
        }
        tl.fromTo(S.deco, { rotation: 0, svgOrigin: "0 0" }, { rotation: 14, duration: span, ease: "none" }, t0);
        tl.fromTo(S.st, { scale: 1 }, { scale: 1.035, duration: span, ease: "none" }, t0);
        if (S.title) tl.fromTo(S.title, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .6 }, t0 + .5);
        if (v.focus && S.nodes[v.focus]) {
          const n = S.nodes[v.focus];
          tl.to(n.circ, { fill: css("--accent"), duration: .5 }, t0 + 1.1);
          tl.to(n.txt, { fill: "#0b1130", duration: .5 }, t0 + 1.1);
          tl.to(n.g, { scale: 1.16, duration: .45, ease: "back.out(3)" }, t0 + 1.1);
        }
        let prev = [];
        S.steps.forEach((s, k) => {
          const t = when(ctx, s.step, t0 + 1.4 + k * 1.2);
          prev.forEach((p) => {
            if (p.path) tl.to(p.path, { opacity: .28, duration: .45 }, t);
            if (p.chip) tl.to(p.chip, { opacity: .45, duration: .45 }, t);
          });
          if (s.path) drawOn(tl, s.path, t, 1.0);
          (s.step.chi || []).forEach((c) => {
            const n = S.nodes[c]; if (!n) return;
            tl.to(n.circ, { fill: s.color, stroke: s.color, duration: .4 }, t + .2);
            tl.to(n.txt, { fill: "#0b1130", duration: .4 }, t + .2);
            tl.fromTo(n.g, { scale: 1 }, { scale: 1.2, duration: .35, ease: "back.out(3)", yoyo: true, repeat: 1 }, t + .2);
          });
          if (s.chip) tl.fromTo(s.chip, { x: 80, opacity: 0 }, { x: 0, opacity: 1, duration: .55, ease: "power4.out" }, t + .1);
          prev.push(s);
        });
      },
    },

    // Ngũ hành: vòng tương sinh + sao tương khắc; mỗi bước là một thẻ năm sinh
    // lật 3D bên trái và mũi tên quan hệ vẽ ra bên phải.
    elements: {
      build(inner, ln) {
        const v = ln.visual, S = { steps: [] };
        const st = el("div", "lf-stage"); inner.appendChild(st);
        const wrap = el("div", "lf-elem"); st.appendChild(wrap);
        const svg = sv("svg", { viewBox: "-420 -420 840 840" }, wrap);
        const pos = {};
        ELEM.forEach((e, k) => {
          const a = (-90 + k * 72) * Math.PI / 180;
          pos[e] = { x: Math.cos(a) * 300, y: Math.sin(a) * 300, a: -90 + k * 72 };
        });
        const base = sv("g", {}, svg);
        S.ring = sv("circle", { r: 300, class: "base", "stroke-dasharray": "4 10" }, base);
        const star = ELEM.map((e, k) => pos[ELEM[(k * 2) % 5]]);
        S.star = sv("path", { d: "M" + star.map((p) => `${p.x},${p.y}`).join(" L") + " Z", class: "base", opacity: .45 }, base);
        const arrows = sv("g", {}, svg);
        const nodes = {};
        ELEM.forEach((e) => {
          const g = sv("g", { transform: `translate(${pos[e].x},${pos[e].y})` }, svg);
          const inG = sv("g", {}, g);
          sv("circle", { r: 86, fill: ELEM_COLOR[e], opacity: .95 }, inG);
          const t = sv("text", { class: "el-t", fill: ELEM_INK[e] }, inG); t.textContent = e;
          nodes[e] = inG;
        });
        if (v.year && pos[v.year.element]) {
          const p = pos[v.year.element];
          S.halo = sv("circle", { cx: p.x, cy: p.y, r: 112, fill: "none", stroke: css("--accent"),
            "stroke-width": 5, "stroke-dasharray": "14 12" }, svg);
          const lab = el("div", "lf-yearlabel", v.year.label || "");
          lab.style.left = (1010 + 420 + p.x - 150) + "px"; lab.style.top = (40 + 420 + p.y + 130) + "px";
          st.appendChild(lab); S.yearLabel = lab;
        }
        (v.steps || []).forEach((step) => {
          const a = pos[step.from], b = pos[step.to];
          const color = ELEM_COLOR[step.from] || css("--accent");
          let path = null, head = null;
          if (step.kind === "hoa" && a) {
            path = sv("circle", { cx: a.x, cy: a.y, r: 118, fill: "none", stroke: color, "stroke-width": 10 }, arrows);
          } else if (a && b) {
            let p1, p2, dir;
            if (step.kind === "sinh") {  // cung tròn theo vòng sinh, chừa chỗ cho hai nút
              const a1 = (a.a + 19) * Math.PI / 180, a2 = (a.a + 72 - 19) * Math.PI / 180;
              p1 = [Math.cos(a1) * 300, Math.sin(a1) * 300]; p2 = [Math.cos(a2) * 300, Math.sin(a2) * 300];
              path = sv("path", { d: `M${p1} A300 300 0 0 1 ${p2}`, class: "arrow", stroke: color }, arrows);
              dir = (a.a + 72 - 19 + 90);
            } else {  // tương khắc: dây cung thẳng
              const dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy), u = [dx / L, dy / L];
              p1 = [a.x + u[0] * 100, a.y + u[1] * 100]; p2 = [b.x - u[0] * 108, b.y - u[1] * 108];
              path = sv("path", { d: `M${p1} L${p2}`, class: "arrow", stroke: color }, arrows);
              dir = Math.atan2(dy, dx) * 180 / Math.PI;
            }
            head = sv("path", { d: "M-2,-16 L26,0 L-2,16 Z", fill: color,
              transform: `translate(${p2[0]},${p2[1]}) rotate(${dir})` }, arrows);
          }
          const card = el("div", "lf-card");
          const c = step.card || {};
          card.appendChild(el("div", "yr", c.yr || ""));
          card.appendChild(el("div", "sub", c.sub || ""));
          card.appendChild(el("div", "note", c.note || ""));
          if (step.pill) { const pl = el("div", "pill", step.pill); pl.style.background = color; card.appendChild(pl); }
          st.appendChild(card);
          S.steps.push({ step, path, head, card, color });
        });
        S.wrap = wrap; S.nodes = nodes; S.st = st;
        S.title = title(st, v.title || "NGŨ HÀNH NẠP ÂM", 150, 124);
        inner._lf = S;
      },
      enter(tl, inner, ln, ctx) {
        const S = inner._lf, t0 = ln.start, span = Math.max(2, ctx.until - t0);
        if (variantOf("elements", ln.visual, ["swing", "rise"]) === "swing") {
          tl.fromTo(S.wrap, { rotationY: -40, scale: .8, opacity: 0, transformPerspective: 1700 },
            { rotationY: 0, scale: 1, opacity: 1, duration: 1.3, ease: "power3.out" }, t0);
        } else {  // ngũ hành trồi lên từ đáy khung, nghiêng về phía người xem
          tl.fromTo(S.wrap, { y: 260, rotationX: 40, opacity: 0, transformPerspective: 1700 },
            { y: 0, rotationX: 0, opacity: 1, duration: 1.2, ease: "expo.out" }, t0);
        }
        tl.fromTo(Object.values(S.nodes), { scale: 0, transformOrigin: "50% 50%" },
          { scale: 1, duration: .6, ease: "back.out(2)", stagger: .08 }, t0 + .3);
        drawOn(tl, S.ring, t0 + .4, 1.2); drawOn(tl, S.star, t0 + .9, 1.4);
        if (S.halo) tl.fromTo(S.halo, { rotation: 0, svgOrigin: `${S.halo.getAttribute("cx")} ${S.halo.getAttribute("cy")}`, opacity: 0 },
          { rotation: 90, opacity: 1, duration: span, ease: "none" }, t0 + .8);
        if (S.yearLabel) tl.fromTo(S.yearLabel, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: .5 }, t0 + 1.0);
        if (S.title) tl.fromTo(S.title, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .6 }, t0 + .4);
        S.steps.forEach((s) => gsap.set(s.card, { opacity: 0 }));
        let prev = null, prevYr = null;
        S.steps.forEach((s, k) => {
          const t = when(ctx, s.step, t0 + 1.5 + k * 1.5);
          if (prev) {
            tl.to(prev.card, { rotationY: 70, opacity: 0, duration: .4, ease: "power2.in", transformPerspective: 1400 }, t - .1);
            if (prev.path) tl.to([prev.path, prev.head].filter(Boolean), { opacity: 0, duration: .4 }, t);
          }
          tl.fromTo(s.card, { rotationY: -80, opacity: 0, transformPerspective: 1400 },
            { rotationY: 0, opacity: 1, duration: .75, ease: "power3.out" }, t + .15);
          const yrEl = s.card.querySelector(".yr"), target = parseInt(s.step.card && s.step.card.yr, 10);
          if (!isNaN(target)) {  // đếm số năm tới giá trị thật
            const o = { v: prevYr != null ? prevYr : target - 24 };
            tl.to(o, { v: target, duration: .9, ease: "power2.out",
              onUpdate: () => { yrEl.textContent = String(Math.round(o.v)); } }, t + .15);
            prevYr = target;
          }
          if (s.path) drawOn(tl, s.path, t + .35, .9);
          if (s.head) tl.fromTo(s.head, { opacity: 0, scale: 0, transformOrigin: "50% 50%" },
            { opacity: 1, scale: 1, duration: .3, ease: "back.out(3)" }, t + 1.15);
          [s.step.from, s.step.to].forEach((e) => {
            if (S.nodes[e]) tl.fromTo(S.nodes[e], { scale: 1 }, { scale: 1.16, duration: .35, yoyo: true, repeat: 1, ease: "back.out(3)" }, t + .5);
          });
          prev = s;
        });
      },
    },

    // Hàng thẻ năm sinh lật vào đúng lúc giọng đọc nói tới năm đó.
    years: {
      build(inner, ln) {
        const row = el("div", "lf-years");
        const cards = (ln.visual.items || []).map((it) => {
          const c = el("div", "lf-ycard");
          c.appendChild(el("div", "yr", it.yr || ""));
          if (it.sub) c.appendChild(el("div", "sub", it.sub));
          if (it.note) c.appendChild(el("div", "note", it.note));
          row.appendChild(c);
          return c;
        });
        if (cards.length > 3) row.classList.add("many");
        inner.appendChild(row);
        inner._lf = { cards };
      },
      enter(tl, inner, ln, ctx) {
        const S = inner._lf, items = ln.visual.items || [];
        const how = variantOf("years", ln.visual, ["flip", "deal", "count"]);
        let last = ln.start;
        S.cards.forEach((c, k) => {
          const it = items[k];
          const t = when(ctx, { at: it.at || ln.sentence_id, word: it.word || it.yr }, ln.start + .3 + k * .45);
          const at = Math.max(ln.start, t - .15);
          last = Math.max(last, t);
          if (how === "flip") {  // lật 3D đúng lúc nghe năm đó
            tl.fromTo(c, { rotationY: -95, opacity: 0, y: 40, transformPerspective: 1400 },
              { rotationY: 0, opacity: 1, y: 0, duration: .8, ease: "power3.out" }, at);
          } else if (how === "deal") {  // chia bài: bay ra từ một xấp ở giữa đáy khung
            tl.fromTo(c, { x: (S.cards.length / 2 - k - .5) * 330, y: 360, rotation: -14 + k * 7, opacity: 0 },
              { x: 0, y: 0, rotation: 0, opacity: 1, duration: .75, ease: "power3.out" }, at);
          } else {  // đếm: thẻ nở ra, con số chạy tới năm thật
            tl.fromTo(c, { scale: .6, opacity: 0 }, { scale: 1, opacity: 1, duration: .5, ease: "back.out(2)" }, at);
            const yrEl = c.querySelector(".yr"), target = parseInt(it.yr, 10);
            if (!isNaN(target)) {
              const o = { v: target - 36 };
              tl.to(o, { v: target, duration: .9, ease: "power3.out", onUpdate: () => { yrEl.textContent = String(Math.round(o.v)); } }, at);
            }
          }
        });
        const idle = Math.max(1, ctx.until - last - .9);
        S.cards.forEach((c, k) => tl.to(c, { y: k % 2 ? 10 : -10, duration: idle, ease: "sine.inOut" }, last + .9));
      },
    },

    // Danh sách đánh số: từng mục bật vào theo câu, mục cũ lùi mờ.
    list: {
      build(inner, ln) {
        const st = el("div", "lf-stage"); inner.appendChild(st);
        const box = el("div", "lf-list"); st.appendChild(box);
        const items = ln.visual.items || [];
        const H = Math.min(130, Math.floor((640 - 22 * (items.length - 1)) / Math.max(1, items.length)));
        const rows = items.map((it, k) => {
          const r = el("div", "lf-item");
          const off = Math.max(0, (640 - (items.length * (H + 22) - 22)) / 2);
          r.style.top = (off + k * (H + 22)) + "px"; r.style.height = H + "px";
          r.appendChild(el("div", "no", String(k + 1)));
          r.appendChild(el("div", "tx", it.text || ""));
          box.appendChild(r);
          return r;
        });
        inner._lf = { rows, title: title(st, ln.visual.title, 260, 124) };
      },
      enter(tl, inner, ln, ctx) {
        const S = inner._lf, items = ln.visual.items || [];
        if (S.title) tl.fromTo(S.title, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .5 }, ln.start + .1);
        const how = variantOf("list", ln.visual, ["cascade", "stack", "spotlight"]);
        if (how === "spotlight")  // cả danh sách hiện mờ sẵn, câu nào nói tới thì mục đó sáng lên
          // Phải xong TRƯỚC lần làm sáng đầu tiên (đầu câu + .3s): tween mờ kết
          // thúc sau sẽ ghi đè mục đang được đọc về lại mờ.
          tl.fromTo(S.rows, { opacity: 0, y: 20 }, { opacity: .32, y: 0, duration: .24, stagger: .02, ease: "power2.out" }, ln.start);
        else S.rows.forEach((r) => gsap.set(r, { opacity: 0 }));
        S.rows.forEach((r, k) => {
          const t = when(ctx, items[k], ln.start + .4 + k * .8);
          if (k) tl.to(S.rows.slice(0, k), { opacity: how === "spotlight" ? .32 : .45, scale: 1, duration: .4 }, t);
          if (how === "cascade") {
            tl.fromTo(r, { x: -120, rotationY: -22, opacity: 0, transformPerspective: 1400 },
              { x: 0, rotationY: 0, opacity: 1, duration: .7, ease: "power4.out" }, t);
          } else if (how === "stack") {  // bật lên từ đáy như lò xo
            tl.fromTo(r, { y: 220, opacity: 0, scale: .9 }, { y: 0, opacity: 1, scale: 1, duration: .6, ease: "back.out(1.8)" }, t);
          } else {
            tl.to(r, { opacity: 1, scale: 1.04, duration: .45, ease: "power2.out" }, t);
          }
          if (how !== "spotlight")  // spotlight: số thứ tự có sẵn, cả danh sách đọc được ngay
            tl.fromTo(r.querySelector(".no"), { scale: 0 }, { scale: 1, duration: .45, ease: "back.out(2.6)" }, t + .12);
        });
      },
    },
  };

  // Dòng thời gian: các mốc năm trên một trục, một điểm sáng chạy tới từng mốc
  // đúng lúc được đọc (spatial-pan-stations, rút gọn một khung).
  visuals.timeline = {
    build(inner, ln) {
      const v = ln.visual, items = v.items || [];
      const st = el("div", "lf-stage"); inner.appendChild(st);
      const box = el("div", "lf-tl"); st.appendChild(box);
      box.appendChild(el("div", "lf-tl-axis"));
      const dot = el("div", "lf-tl-dot"); box.appendChild(dot);
      const W = 1500, gap = items.length > 1 ? W / (items.length - 1) : 0;
      const marks = items.map((it, k) => {
        const m = el("div", "lf-tl-mark" + (it.now ? " now" : ""));
        m.style.left = (k * gap) + "px";
        const up = k % 2 === 0;
        m.appendChild(el("div", "pin"));
        const lab = el("div", "lab " + (up ? "up" : "down"));
        lab.appendChild(el("div", "yr", it.yr || ""));
        if (it.label) lab.appendChild(el("div", "sub", it.label));
        m.appendChild(lab); box.appendChild(m);
        return m;
      });
      inner._lf = { box, dot, marks, gap, title: title(st, v.title, 210, 124) };
    },
    enter(tl, inner, ln, ctx) {
      const S = inner._lf, items = ln.visual.items || [];
      if (S.title) tl.fromTo(S.title, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .5 }, ln.start + .1);
      tl.fromTo(S.box.querySelector(".lf-tl-axis"), { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 1.0, ease: "power3.inOut" }, ln.start);
      tl.fromTo(S.dot, { opacity: 0, x: 0 }, { opacity: 1, duration: .3 }, ln.start + .5);
      S.marks.forEach((m, k) => {
        const t = when(ctx, { at: items[k].at || ln.sentence_id, word: items[k].word || items[k].yr }, ln.start + .6 + k * .6);
        tl.to(S.dot, { x: k * S.gap, duration: .55, ease: "power3.inOut" }, t - .3);
        tl.fromTo(m.querySelector(".pin"), { scaleY: 0 }, { scaleY: 1, duration: .35, ease: "back.out(2)" }, t);
        tl.fromTo(m.querySelector(".lab"), { opacity: 0, y: m.querySelector(".up") ? 30 : -30 },
          { opacity: 1, y: 0, duration: .5, ease: "power3.out" }, t + .05);
      });
    },
  };

  // So sánh hai vế: hai thẻ mở như cuốn sách (split-tilt-cards).
  visuals.compare = {
    build(inner, ln) {
      const v = ln.visual, st = el("div", "lf-stage lf-cmp"); inner.appendChild(st);
      const mk = (side, d) => {
        const c = el("div", "lf-cmp-card " + side);
        if (d.eyebrow) c.appendChild(el("div", "eb", d.eyebrow));
        c.appendChild(el("div", "hd", d.title || ""));
        if (d.body) c.appendChild(el("div", "bd", d.body));
        if (d.badge) c.appendChild(el("div", "badge", d.badge));
        st.appendChild(c); return c;
      };
      inner._lf = { L: mk("left", v.left || {}), Rt: mk("right", v.right || {}), title: title(st, v.title, 210, 124) };
    },
    enter(tl, inner, ln, ctx) {
      const S = inner._lf, v = ln.visual;
      if (S.title) tl.fromTo(S.title, { opacity: 0 }, { opacity: 1, duration: .5 }, ln.start + .1);
      const tL = when(ctx, v.left, ln.start + .2), tR = when(ctx, v.right, ln.start + 1.2);
      tl.fromTo(S.L, { x: -260, rotationY: 34, opacity: 0, transformPerspective: 1600 },
        { x: 0, rotationY: 12, opacity: 1, duration: .8, ease: "power3.out" }, tL);
      tl.fromTo(S.Rt, { x: 260, rotationY: -34, opacity: 0, transformPerspective: 1600 },
        { x: 0, rotationY: -12, opacity: 1, duration: .8, ease: "power3.out" }, tR);
      [S.L, S.Rt].forEach((c, k) => {
        const b = c.querySelector(".badge");
        if (b) tl.fromTo(b, { scale: 0 }, { scale: 1, duration: .45, ease: "back.out(3)" }, (k ? tR : tL) + .7);
      });
      tl.to(S.L, { y: -8, duration: Math.max(1, ctx.until - tR - 1), ease: "sine.inOut" }, tR + .9);
      tl.to(S.Rt, { y: 8, duration: Math.max(1, ctx.until - tR - 1), ease: "sine.inOut" }, tR + .9);
    },
  };

  // Một con số lớn đếm lên cùng vòng tiến độ (dataviz-countup).
  visuals.stat = {
    build(inner, ln) {
      const v = ln.visual, st = el("div", "lf-stage lf-stat"); inner.appendChild(st);
      const svg = sv("svg", { viewBox: "-260 -260 520 520", class: "ring" }, st);
      sv("circle", { r: 230, class: "track" }, svg);
      const arc = sv("circle", { r: 230, class: "arc", transform: "rotate(-90)" }, svg);
      const num = el("div", "num", String(v.value));
      const lab = el("div", "lab", v.label || "");
      st.appendChild(num); st.appendChild(lab);
      if (v.suffix) num.setAttribute("data-suffix", v.suffix);
      inner._lf = { arc, num, lab };
    },
    enter(tl, inner, ln, ctx) {
      // Đếm từ đầu câu và CHẠM đích đúng lúc giọng đọc tới con số -- chờ tới lúc đọc
      // mới bắt đầu thì vòng trống ~2 giây (hook short mất khung đầu).
      const S = inner._lf, v = ln.visual, land = when(ctx, v, ln.start + .3);
      const t = ln.start + .1, cnt = Math.max(1.4, land + .5 - t);
      drawOn(tl, S.arc, t, cnt, "power2.out");
      const o = { v: 0 }, target = Number(v.value) || 0, suf = v.suffix || "";
      tl.to(o, { v: target, duration: cnt, ease: "power2.out", onUpdate: () => { S.num.textContent = String(Math.round(o.v)).replace(/\B(?=(\d{3})+(?!\d))/g, ".") + suf; } }, t);  // 20.000 kiểu Việt
      tl.fromTo(S.num, { scale: .7, opacity: 0 }, { scale: 1, opacity: 1, duration: .6, ease: "back.out(2)" }, t);
      tl.fromTo(S.lab, { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: .5, ease: "power3.out" }, land);
    },
  };

  /* ---------- Chuyển cảnh (6 biến thể) ----------
     Luật chọn: vào thẻ chương = đổi phần -> zoom-through / iris (cut-catalog:
     state change). Cảnh cũ có ảnh bên dưới -> chỉ dùng loại kéo ảnh đi cùng
     (blur trên ảnh sẽ đè filter màu của kênh). Còn lại chọn trong cả kho. */
  function transition(tl, oldS, newS, T, ctx) {
    const kinds = ctx.toChapter ? ["zoom", "iris"]
      : ctx.oldClip ? ["blurfade", "push", "pushup"]
      : ["blurfade", "push", "pushup", "zoom", "wipe", "iris"];
    const k = pick("transition", kinds);
    const clip = ctx.oldClip;
    const fgClip = clip && clip.dataset.fg ? document.getElementById(clip.dataset.fg) : null;  // lớp chủ thể 2.5D
    if (k === "push" || k === "pushup") {  // cut-the-curve: hai bên cùng hướng, cắt ở đỉnh tốc độ
      const ax = k === "push" ? "x" : "y", d = 230;
      tl.to(oldS, { [ax]: -d, duration: .34, ease: "power4.in" }, T);
      if (clip) tl.to(clip, { [ax]: -d, duration: .34, ease: "power4.in" }, T);
      if (fgClip) tl.to(fgClip, { [ax]: -d, duration: .34, ease: "power4.in" }, T);
      tl.to(oldS, { opacity: 0, duration: .22, ease: "power1.in" }, T + .1);
      tl.fromTo(newS, { [ax]: d, opacity: 0 }, { [ax]: 0, opacity: 1, duration: .42, ease: "power4.out" }, T + .32);
    } else if (k === "zoom") {  // zoom-through: cả khung lao về phía người xem
      tl.to(oldS, { scale: 1.2, filter: "blur(18px)", duration: .22, ease: "power3.in" }, T);
      tl.to(oldS, { opacity: 0, duration: .22, ease: "none" }, T);
      tl.fromTo(newS, { opacity: 0, scale: .75, filter: "blur(18px)" },
        { opacity: 1, scale: 1, filter: "blur(0px)", duration: .55, ease: "expo.out" }, T + .22);
    } else if (k === "wipe") {  // quét ngang, mép vàng dẫn đường
      tl.fromTo(newS, { opacity: 1, clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: .6, ease: "power3.inOut" }, T);
      tl.to(oldS, { opacity: 0, duration: .2 }, T + .55);
    } else if (k === "iris") {  // mở từ tâm như ống kính
      tl.fromTo(newS, { opacity: 1, clipPath: "circle(0% at 50% 45%)" }, { clipPath: "circle(78% at 50% 45%)", duration: .7, ease: "power2.inOut" }, T);
      tl.to(oldS, { opacity: 0, duration: .2 }, T + .6);
    } else {
      return false;  // blurfade: để style tự chuyển (mỗi style một chất riêng)
    }
    return true;
  }

  /* ================= PHASE A (29/09/2026) =================
     Xu hướng motion 2026 cho video tài liệu/giải thích: nét vẽ tay "on twos"
     (Vox / Johnny Harris), kính lỏng, hạt chuyển động theo thuật toán, vệt
     sáng analog, chữ động theo lời. Tất cả tất định: rng hạt giống, không
     Math.random, mọi chuyển động nằm trên timeline đã pause. */
  const theme = () => (css("--lf-theme") || "night").replace(/["']/g, "");
  // "On twos": nét vẽ tay nhảy theo nấc 12 hình/giây trong video 30 hình/giây --
  // trông như được đặt tay lên khung, không trượt mượt như máy.
  const twos = (dur) => `steps(${Math.max(2, Math.round(dur * 12))})`;
  function jitter(seed) { const r = HF.rng(HF.hashSeed(String(seed))); return () => r() - 0.5; }
  // Vòng tròn vẽ tay: hơi méo, vẽ quá một chút (1.12 vòng) như bút lướt.
  function sketchLoop(cx, cy, rx, ry, seed) {
    const j = jitter(seed), N = 30, pts = [];
    for (let k = 0; k <= N; k++) {
      const a = -Math.PI * 0.62 + (k / N) * Math.PI * 2 * 1.12, w = 1 + j() * 0.09;
      pts.push(`${(cx + Math.cos(a) * rx * w).toFixed(1)},${(cy + Math.sin(a) * ry * w).toFixed(1)}`);
    }
    return "M" + pts.join(" L");
  }
  function sketchUnder(x1, x2, y, seed) {
    const j = jitter(seed), mid = (x1 + x2) / 2;
    return `M${x1},${y + j() * 6} Q${mid},${y + 10 + j() * 8} ${x2},${y - 4 + j() * 6}`;
  }
  // Nét vẽ tay / dạ quang là PHẦN TỬ CON của thứ nó đánh dấu, đặt bằng CSS
  // inset + SVG toạ độ chuẩn hoá 0..100: không đo toạ độ lúc dựng. Đo lúc dựng
  // từng lệch vì font (Lora) nạp xong SAU khi dựng -> chữ đổi bề rộng, dải dạ
  // quang nằm lệch sang chữ khác.
  function sketchOn(target, cls, d) {
    const s = sv("svg", { class: "lf-sketch " + cls, viewBox: "0 0 100 100", preserveAspectRatio: "none" });
    const p = sv("path", { d, class: "lf-ink", "vector-effect": "non-scaling-stroke" }, s);
    target.appendChild(s);
    return p;
  }
  // Vẽ ra bằng cách LỘ dần (không dùng stroke-dash): với non-scaling-stroke,
  // dash tính theo pixel nên pathLength=1 hết tác dụng -> nét thành chấm 1px.
  // Gạch chân: quét trái -> phải. Vòng tròn: mặt nạ hình nón quay một vòng.
  function drawSketch(tl, p, at, dur) {
    const s = p.ownerSVGElement;
    if (s.classList.contains("loop"))
      tl.fromTo(s, { "--sweep": "0deg" }, { "--sweep": "400deg", duration: dur, ease: twos(dur) }, at);
    else
      tl.fromTo(s, { clipPath: "inset(-20% 100% -20% 0%)" }, { clipPath: "inset(-20% 0% -20% 0%)", duration: dur, ease: twos(dur) }, at);
  }
  // Bút dạ quang (Vox): dải màu nghiêng quét qua SAU chữ.
  function marker(target, color) {
    const m = el("div", "lf-marker");
    if (color) m.style.background = color;
    target.insertBefore(m, target.firstChild);
    return m;
  }
  function sweep(tl, m, at, dur) {
    tl.fromTo(m, { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: dur || .5, ease: twos(dur || .5) }, at);
  }
  // Vệt sáng kính: dải trắng mờ trượt chéo qua tấm panel một lần khi nó vào.
  function sheen(tl, panel, at) {
    if (!panel) return;
    const wrap = el("div", "lf-sheen-wrap"), g = el("div", "lf-sheen");
    wrap.appendChild(g); panel.appendChild(wrap);
    tl.fromTo(g, { xPercent: -160 }, { xPercent: 260, duration: 1.1, ease: "power2.inOut" }, at);
  }

  // ---- 1) Trích dẫn: trang sách xưa / chữ động / kính ----
  visuals.quote = {
    build(inner, ln) {
      const v = ln.visual, how = variantOf("quote", v, ["page", "kinetic", "glass"]);
      ln._q = how;
      const st = el("div", "lf-stage lf-q lf-q-" + how); inner.appendChild(st);
      const card = el("div", "lf-q-card"); st.appendChild(card);
      if (how === "page") { card.appendChild(el("div", "tape a")); card.appendChild(el("div", "tape b")); }
      const body = el("div", "lf-q-text"); card.appendChild(body);
      // Chữ lấy đúng câu đang đọc (bỏ dấu **), cụm đánh dấu là cụm được tô.
      let words = (ln.words || []).map((w) => ({ t: clean(w.w), hot: !!w.hot, at: w.t }));
      // "Trong kinh X, Đức Phật dạy: <lời kinh>" -> thẻ chỉ mang lời kinh (nguồn đã ghi
      // ở dòng dưới thẻ). Phần dẫn ngắn thì giữ nguyên cả câu.
      const colon = words.findIndex((w) => /:$/.test(w.t));
      if (v.source && colon >= 0 && words.length - colon > 3) {
        words = words.slice(colon + 1);
        words[0] = { ...words[0], t: words[0].t.charAt(0).toUpperCase() + words[0].t.slice(1) };
      }
      // class "qw", KHÔNG "w": .w là chữ phụ đề trong base.css (trắng, gạch chân)
      const spans = words.map((w) => { const sp = el("span", "qw" + (w.hot ? " hot" : "")); sp.appendChild(document.createTextNode(w.t)); body.appendChild(sp); return sp; });
      if (v.source) card.appendChild(el("div", "lf-q-src", "— " + v.source));
      inner._lf = { st, card, spans, words, markers: [] };
      if (how === "page")  // bút dạ quang dưới từng từ được đánh dấu
        spans.forEach((sp, k) => { if (words[k].hot) inner._lf.markers.push({ m: marker(sp), at: words[k].at }); });
    },
    enter(tl, inner, ln) {
      const S = inner._lf, how = ln._q, t0 = ln.start;
      if (how === "page") {  // tờ giấy rơi xuống, nghiêng, nhảy nấc như ảnh chụp từng khung
        tl.fromTo(S.card, { y: -220, rotation: -9, opacity: 0 }, { y: 0, rotation: -2.2, opacity: 1, duration: .6, ease: twos(.6) }, t0);
        tl.fromTo(S.card.querySelectorAll(".tape"), { scale: 0 }, { scale: 1, duration: .25, ease: twos(.25), stagger: .1 }, t0 + .55);
        tl.fromTo(S.spans, { opacity: 0 }, { opacity: 1, duration: .3, stagger: .015 }, t0 + .3);
        S.markers.forEach((mk) => sweep(tl, mk.m, mk.at, .3));
        tl.to(S.card, { rotation: -1.4, duration: Math.max(1, ln.end - t0 - 1), ease: twos(Math.max(1, ln.end - t0 - 1)) }, t0 + 1);
      } else if (how === "kinetic") {  // từng từ hiện đúng lúc được đọc
        S.spans.forEach((sp, k) => {
          const hot = S.words[k].hot;
          tl.fromTo(sp, { opacity: 0, y: 30, scale: hot ? 1.5 : 1 },
            { opacity: 1, y: 0, scale: 1, duration: hot ? .4 : .28, ease: hot ? "back.out(2.5)" : "power3.out" }, S.words[k].at - .05);
        });
      } else {  // glass: tấm kính trồi lên, vệt sáng lướt qua, chữ hiện theo cụm
        tl.fromTo(S.card, { y: 60, opacity: 0, scale: .96 }, { y: 0, opacity: 1, scale: 1, duration: .8, ease: "expo.out" }, t0);
        sheen(tl, S.card, t0 + .5);
        S.spans.forEach((sp, k) => tl.fromTo(sp, { opacity: .18 }, { opacity: 1, duration: .25 }, S.words[k].at - .05));
      }
    },
  };

  // ---- 2) Bố cục "ghim bảng": ảnh dán băng keo, rơi xuống từng nấc ----
  layouts.pinned = {
    build(inner, ln) {
      const s = ln.sentence_id % 2 ? 1 : -1;
      const g = el("div", "lf-pin"); g.style.transform = `rotate(${-2.4 * s}deg)`;
      g.appendChild(el("div", "tape a")); g.appendChild(el("div", "tape b"));
      inner.appendChild(g);
    },
    enter(tl, inner, ln) {
      const g = inner.querySelector(".lf-pin"); if (!g) return;
      tl.fromTo(g, { y: -160 }, { y: 0, duration: .5, ease: twos(.5) }, ln.start);
      tl.fromTo(g.querySelectorAll(".tape"), { scale: 0 }, { scale: 1, duration: .2, ease: twos(.2), stagger: .08 }, ln.start + .45);
    },
    enterCont() {},
    motion(tl, clip, ln, mEnd) {
      const s = ln.sentence_id % 2 ? 1 : -1;
      gsap.set(clip, { rotation: -2.4 * s });
      tl.fromTo(clip, { y: -160 }, { y: 0, duration: .5, ease: twos(.5) }, ln.start);
      tl.fromTo(clip, { scale: 1 }, { scale: 1.035, duration: Math.max(1, mEnd - ln.start), ease: "none" }, ln.start);
      return true;
    },
  };

  /* ================= PHASE B ================= */
  // ---- 2.5D: nền trôi chậm, chủ thể (tách bằng Vision) đẩy nhanh hơn ----
  layouts.depth = {
    build(inner) { inner.appendChild(el("div", "lf-full-shade")); },
    motion(tl, clip, ln, mEnd) {
      const fg = clip.dataset.fg ? document.getElementById(clip.dataset.fg) : null;
      const d = Math.max(1, mEnd - ln.start), s = ln.sentence_id % 2 ? 1 : -1;
      // Chênh tốc độ giữa hai lớp là thứ tạo chiều sâu: nền 1.06 -> 1.11,
      // chủ thể 1.07 -> 1.20 và dạt ngang gấp gần ba lần.
      tl.fromTo(clip, { scale: 1.06, x: 0 }, { scale: 1.11, x: -18 * s, duration: d, ease: "none" }, ln.start);
      if (fg) {
        tl.fromTo(fg, { opacity: 0 }, { opacity: 1, duration: .55, ease: "sine.out" }, ln.start);
        tl.to(fg, { opacity: 0, duration: .45, ease: "sine.in" }, Math.max(ln.start + .6, mEnd - .45));
        tl.fromTo(fg, { scale: 1.07, x: 0, y: 0 }, { scale: 1.2, x: -48 * s, y: -10, duration: d, ease: "none" }, ln.start);
      }
      return true;
    },
  };

  // ---- Bản đồ (vector lane): biên giới vẽ ra, ghim rơi đúng lúc được nhắc,
  // tuyến nối các ghim. Toạ độ đã nướng sẵn trong spec._geo (hf_geo.py). ----
  visuals.map = {
    build(inner, ln) {
      const v = ln.visual, G = v._geo || { countries: [], pins: [] };
      const st = el("div", "lf-stage lf-map"); inner.appendChild(st);
      const svg = sv("svg", { viewBox: "0 0 1920 1080", class: "lf-map-svg" }, st);
      const world = sv("g", { class: "world" }, svg);
      const S = { st, world, borders: [], fills: [], labels: [], pins: [], routes: [] };
      G.countries.forEach((c) => {
        const f = sv("path", { d: c.d, class: c.focus ? "cty focus" : "cty ctx" }, world);
        if (c.focus) { S.fills.push(f); S.borders.push(sv("path", { d: c.d, class: "border" }, world)); }
        if (c.label && c.lx > 0) {
          const t = sv("text", { x: c.lx, y: c.ly, class: "cty-label" }, world); t.textContent = c.label; S.labels.push(t);
        }
      });
      const routeG = sv("g", {}, world);
      G.pins.forEach((p, k) => {
        if (v.route && k > 0) {  // cung cong nhẹ giữa hai ghim liền nhau
          const a = G.pins[k - 1], mx = (a.x + p.x) / 2, my = (a.y + p.y) / 2 - Math.hypot(p.x - a.x, p.y - a.y) * .18;
          S.routes[k] = sv("path", { d: `M${a.x},${a.y} Q${mx},${my} ${p.x},${p.y}`, class: "route" }, routeG);
        }
        const g = sv("g", { transform: `translate(${p.x},${p.y})` }, world);
        const inG = sv("g", {}, g);
        const ring = sv("circle", { r: 12, class: "pulse" }, inG);
        sv("circle", { r: 11, class: "pin" }, inG);
        const card = el("div", "lf-pin-card " + (p.side || (k % 2 ? "left" : "right")));
        card.style.left = p.x + "px"; card.style.top = p.y + "px";
        card.appendChild(el("div", "nm", p.name || ""));
        if (p.sub) card.appendChild(el("div", "sb", p.sub));
        st.appendChild(card);
        S.pins.push({ g: inG, ring, card, p });
      });
      S.title = title(st, v.title, 150, 124);
      inner._lf = S;
    },
    enter(tl, inner, ln, ctx) {
      const S = inner._lf, t0 = ln.start, span = Math.max(2, ctx.until - t0);
      // Thu phóng CẢ sân khấu (bản đồ SVG + thẻ tên HTML) -- thu riêng SVG thì thẻ
      // tên trôi lệch khỏi ghim tới ~40px ở mép khung.
      tl.fromTo(S.world, { opacity: 0 }, { opacity: 1, duration: 1.1, ease: "power2.out" }, t0);
      tl.fromTo(S.st, { scale: .95 }, { scale: 1.04, duration: span, ease: "sine.out" }, t0);
      S.borders.forEach((b, k) => drawOn(tl, b, t0 + .3 + k * .25, 1.6, "power2.inOut"));
      tl.fromTo(S.fills, { opacity: 0 }, { opacity: 1, duration: .8, stagger: .2 }, t0 + 1.2);
      if (S.labels.length) tl.fromTo(S.labels, { opacity: 0 }, { opacity: 1, duration: .5, stagger: .1 }, t0 + 1.5);
      if (S.title) tl.fromTo(S.title, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .5 }, t0 + .2);
      S.pins.forEach((P, k) => {
        const t = when(ctx, P.p, t0 + 1.6 + k * 1.2);
        if (S.routes[k]) drawOn(tl, S.routes[k], t - .7, .8, "power2.inOut");
        tl.fromTo(P.g, { y: -60, opacity: 0 }, { y: 0, opacity: 1, duration: .5, ease: "back.out(2.4)" }, t);
        tl.fromTo(P.ring, { attr: { r: 12 }, opacity: .9 }, { attr: { r: 46 }, opacity: 0, duration: 1.1, ease: "power2.out", repeat: 1 }, t + .3);
        // Thẻ tên đặt bằng transform translate(-50%) -> chỉ tween opacity; tween x
        // sẽ ghi đè transform, thẻ nhảy khỏi ghim (skill maps: centered overlays).
        tl.fromTo(P.card, { opacity: 0 }, { opacity: 1, duration: .45, ease: "power2.out" }, t + .2);
        tl.fromTo(P.card.querySelector(".nm"), { x: P.card.classList.contains("left") ? 24 : -24 },
          { x: 0, duration: .5, ease: "power3.out" }, t + .2);
      });
    },
  };

  // ---- 3) Kính lỏng trên ảnh tràn khung: thẻ chữ khoá bằng kính thay chữ trần ----
  const fullBase = layouts.full;
  layouts.full = {
    build(inner, ln) {
      ln._fullSkin = ln._fullSkin || pick("fullskin", ["text", "glass"]);
      fullBase.build(inner, ln);
      const c = inner.querySelector(".lf-callout");
      if (c && ln._fullSkin === "glass") c.classList.add("lf-glass");
    },
    enter(tl, inner, ln) {
      fullBase.enter(tl, inner, ln);
      const c = inner.querySelector(".lf-callout.lf-glass");
      if (c) {  // tấm kính vào CÙNG lúc chữ khoá được đọc, không để kính rỗng chờ chữ
        const w = (ln.words || []).find((x) => x.hot), t = (w ? w.t : ln.start + .4) - .15;
        tl.fromTo(c, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: .4, ease: "power3.out" }, t);
        sheen(tl, c, t + .4);
      }
    },
    enterCont(tl, inner, ln) { this.enter(tl, inner, ln); },
  };

  // ---- 4) Bút dạ quang / nét vẽ tay gắn vào các sơ đồ có sẵn ----
  // Gắn thêm vào một sơ đồ có sẵn: `measure` chạy NGAY SAU khi dựng (lúc chưa có
  // tween nào dịch/nghiêng phần tử -- đo vị trí mới đúng), `extra` chạy sau lối vào.
  const withInk = (base, extra, measure) => ({
    build(inner, ln, i, ctx) { base.build(inner, ln, i, ctx); if (measure) measure(inner, ln); },
    enter(tl, inner, ln, ctx) { base.enter(tl, inner, ln, ctx); extra(tl, inner, ln, ctx); },
  });
  // Danh sách: mục đang đọc được tô dạ quang.
  visuals.list = withInk(visuals.list, (tl, inner, ln, ctx) => {
    const items = ln.visual.items || [];
    (inner._marks || []).forEach((m, k) => sweep(tl, m, when(ctx, items[k], ln.start + .4 + k * .8) + .25, .45));
  }, (inner) => {
    inner._marks = inner._lf.rows.map((r) => marker(r.querySelector(".tx"), "var(--lf-marker)"));
  });
  // Thẻ năm: vòng tròn vẽ tay quanh năm được `mark` (hoặc thẻ cuối nếu không đánh dấu).
  visuals.years = withInk(visuals.years, (tl, inner, ln, ctx) => {
    const items = ln.visual.items || [], k = inner._circleAt, p = inner._circle;
    if (!p) return;
    const t = when(ctx, { at: items[k].at || ln.sentence_id, word: items[k].word || items[k].yr }, ln.start + 1) + .6;
    drawSketch(tl, p, t, .6);
  }, (inner, ln) => {
    const items = ln.visual.items || [];
    let k = items.findIndex((it) => it.mark);
    if (k < 0) k = items.length - 1;
    const card = inner._lf.cards[k]; if (!card) return;
    // Vòng vẽ tay là con của con số -> đi theo thẻ khi thẻ lật/bay vào.
    inner._circle = sketchOn(card.querySelector(".yr"), "loop", sketchLoop(50, 50, 47, 45, ln.sentence_id));
    inner._circleAt = k;
  });

  // ---- 5) Thẻ chương thêm biến thể "ink": gạch chân vẽ tay + chữ nhảy nấc ----
  CHAPTER_VARIANTS.push("ink");
  const chapBase = { build: chapter.build, enter: chapter.enter };
  chapter.build = function (inner, ln) {
    chapBase.build(inner, ln);
    // hạt bung ra khi thẻ chương vào (particle-burst)
    const b = el("div", "lf-burst");
    const r = HF.rng(HF.hashSeed("burst" + ln.sentence_id));
    for (let k = 0; k < 26; k++) {
      const d = el("i", ""); const a = (k / 26) * Math.PI * 2 + r() * .3, dist = 220 + r() * 360;
      d.dataset.x = String(Math.cos(a) * dist); d.dataset.y = String(Math.sin(a) * dist * .6);
      d.style.width = d.style.height = (3 + r() * 6).toFixed(1) + "px"; b.appendChild(d);
    }
    inner.querySelector(".lf-chap").appendChild(b);
    if (ln._chap === "ink") {
      inner._ink = sketchOn(inner.querySelector(".lf-chap-title"), "under", sketchUnder(2, 98, 45, ln.sentence_id));
      inner.querySelector(".lf-chap-rule").style.display = "none";
    }
  };
  chapter.enter = function (tl, inner, ln) {
    if (ln._chap === "ink") {
      const t0 = ln.start, q = (c) => inner.querySelector(c);
      tl.fromTo(q(".lf-chap-ghost"), { opacity: 0 }, { opacity: .5, duration: .6 }, t0);
      tl.fromTo(q(".lf-chap-no"), { opacity: 0 }, { opacity: 1, duration: .3, ease: twos(.3) }, t0 + .1);
      tl.fromTo(q(".lf-chap-title"), { opacity: 0, y: 40, rotation: -2 }, { opacity: 1, y: 0, rotation: 0, duration: .5, ease: twos(.5) }, t0 + .1);
      drawSketch(tl, inner._ink, t0 + .6, .5);
    } else chapBase.enter(tl, inner, ln);
    // set + to chứ không fromTo: fromTo vẽ trạng thái đầu ngay lúc dựng, hạt sẽ
    // lơ lửng giữa khung từ giây 0.
    const ps = inner.querySelectorAll(".lf-burst i"), tb = ln.start + .1;
    tl.set(ps, { x: 0, y: 0, opacity: 1, scale: 1 }, tb);
    tl.to(ps, { x: (k, e) => Number(e.dataset.x), y: (k, e) => Number(e.dataset.y), scale: .3,
      duration: 1.4, ease: "expo.out" }, tb);
    tl.to(ps, { opacity: 0, duration: 1.1, ease: "power2.in" }, tb + .3);
  };

  // Vệt sáng kính khi panel của sơ đồ vào (thẻ ngũ hành, thẻ so sánh, chip vòng con giáp).
  ["elements", "compare", "wheel"].forEach((k) => {
    visuals[k] = withInk(visuals[k], (tl, inner, ln) => {
      const S = inner._lf;
      const panels = k === "elements" ? S.steps.map((s) => s.card) : k === "compare" ? [S.L, S.Rt] : S.steps.map((s) => s.chip).filter(Boolean);
      panels.forEach((p, i) => sheen(tl, p, ln.start + 1 + i * .4));
    });
  });

  // ---- 6) Không khí: hạt bay + vệt sáng analog theo chủ đề style ----
  function ambient(tl, DUR, ctx) {
    const root = ctx.root, stage = document.getElementById("stage");
    const layer = el("div", "lf-ambient"); root.insertBefore(layer, stage);
    const night = theme() === "night", r = HF.rng(HF.hashSeed("ambient|" + Math.round(DUR)));
    const N = night ? 34 : 12, parts = [];
    for (let k = 0; k < N; k++) {
      const p = el("i", night ? "mote" : "petal");
      const size = night ? 2 + r() * 5 : 14 + r() * 12;
      p.style.width = size + "px"; p.style.height = (night ? size : size * .62) + "px";
      p.style.left = (r() * 1920).toFixed(0) + "px";
      layer.appendChild(p);
      parts.push({ p, period: night ? 14 + r() * 16 : 11 + r() * 9, phase: r(), sway: (night ? 22 : 90) * (.5 + r()),
        spin: night ? 0 : 180 + r() * 240, peak: night ? .2 + r() * .5 : .55 });
    }
    // Một tween tiến trình duy nhất: vị trí mỗi hạt là hàm của t -> tất định khi
    // seek bất kỳ, không cần đặt tween ở thời điểm âm.
    const clock = { t: 0 }, y0 = night ? 1120 : -60, y1 = night ? -60 : 1140;
    const place = () => parts.forEach((q) => {
      const f = ((clock.t / q.period) + q.phase) % 1;
      q.p.style.transform = `translate(${(Math.sin(f * Math.PI * 4) * q.sway).toFixed(1)}px, ${(y0 + (y1 - y0) * f).toFixed(1)}px) rotate(${(f * q.spin).toFixed(0)}deg)`;
      q.p.style.opacity = (q.peak * Math.sin(f * Math.PI)).toFixed(3);
    });
    place();
    tl.to(clock, { t: DUR, duration: DUR, ease: "none", onUpdate: place }, 0);
    // Vệt sáng ấm quét qua mỗi lần sang chương (analog light leak).
    const leak = el("div", "lf-leak " + (night ? "night" : "paper")); root.insertBefore(leak, stage);
    (ctx.LINES || []).forEach((ln) => {
      if (!ln.chapter_no) return;
      const t = Math.max(0, ln.start - .4);
      tl.set(leak, { xPercent: -120, opacity: 0 }, t);
      tl.to(leak, { xPercent: 130, duration: 2.6, ease: "sine.inOut" }, t);
      tl.to(leak, { opacity: night ? .35 : .55, duration: 1.3, ease: "sine.out" }, t);
      tl.to(leak, { opacity: 0, duration: 1.3, ease: "sine.in" }, t + 1.3);
    });
  }

  /* ================= PHASE C (29/09/2026) =================
     Theo quy trình motion graphic "thuần code" (không footage): chữ động theo
     NGHĨA của từ, minh hoạ SVG tự vẽ nét, nền shader WebGL cho thẻ kết. */

  // ---- C2: chữ lớn với hiệu ứng theo nghĩa ----
  const FX_LEXICON = [
    ["dissolve", ["vô thường", "buông", "tan ", "qua đi", "biến mất", "không còn"]],
    ["rays", ["tỉnh thức", "bình an", "giác ngộ", "thành đạo", "ánh sáng", "thuận", "an lạc", "tỏa sáng"]],
    ["split", ["xung", "chia", "đối diện", "tách", "hai cực"]],
    ["crack", ["phá", "hại", "vỡ", "gián đoạn", "nứt", "hình "]],
    ["ripple", ["nước", "thủy", "sóng", "sông", "suối", "biển"]],
    ["wave", ["khổ", "buồn", "khóc", "lo ", "đau", "hận thù"]],
    ["flicker", ["lửa", "hỏa", "giận", "nóng"]],
    ["grow", ["mộc", "cây", "sinh ra", "lớn lên", "nảy mầm", "bắt đầu"]],
  ];
  function fxFor(text) {
    const t = " " + text.toLowerCase() + " ";
    for (const [fx, keys] of FX_LEXICON) if (keys.some((k) => t.includes(k))) return fx;
    return "slam";
  }
  const glyphs = (s) => Array.from((s || "").normalize("NFC"));

  visuals.word = {
    build(inner, ln) {
      const v = ln.visual;
      const hot = (ln.words || []).filter((w) => w.hot).map((w) => clean(w.w).replace(/[.,:;!?]+$/, "")).join(" ");
      const text = (v.text || hot || clean((ln.key_parts || []).map((p) => p.t).join(" "))).toUpperCase();
      const fx = v.fx || fxFor(text);
      ln._fx = fx;
      const st = el("div", "lf-stage lf-word-stage lf-fx-" + fx); inner.appendChild(st);
      if (fx === "rays") {
        const s = sv("svg", { class: "lf-rays", viewBox: "-500 -500 1000 1000" }, st);
        for (let k = 0; k < 24; k++) {
          const a = (k / 24) * Math.PI * 2, w = k % 2 ? 0.035 : 0.06;
          sv("path", { d: `M0,0 L${Math.cos(a - w) * 520},${Math.sin(a - w) * 520} L${Math.cos(a + w) * 520},${Math.sin(a + w) * 520} Z` }, s);
        }
      }
      if (fx === "ripple") {
        const s = sv("svg", { width: 0, height: 0, style: "position:absolute" }, st);
        const f = sv("filter", { id: "lfRipple" + ln.sentence_id, x: "-20%", y: "-40%", width: "140%", height: "180%" }, s);
        sv("feTurbulence", { type: "fractalNoise", baseFrequency: "0.012 0.06", numOctaves: "2", seed: "3", result: "n" }, f);
        sv("feDisplacementMap", { in: "SourceGraphic", in2: "n", scale: "0", xChannelSelector: "R", yChannelSelector: "G" }, f);
      }
      const box = el("div", "lf-bigword");
      if (fx === "split" || fx === "crack") {  // hai bản chồng khít, mỗi bản giữ một nửa
        box.appendChild(el("div", "half top", text)); box.appendChild(el("div", "half bot", text));
        if (fx === "crack") {
          const s = sv("svg", { class: "lf-crack", viewBox: "0 0 100 40", preserveAspectRatio: "none" }, box);
          const j = jitter(ln.sentence_id); let d = "M0,20";
          for (let x = 8; x <= 100; x += 8) d += ` L${x},${(20 + j() * 14).toFixed(1)}`;
          sv("path", { d, "vector-effect": "non-scaling-stroke" }, s);
        }
      } else {
        // Ký tự gom theo TỪ (không ngắt giữa từ): mỗi ký tự là một inline-block
        // nên trình duyệt được phép xuống dòng giữa hai ký tự bất kỳ -- ra
        // "NƯỚC CHỈ ĐANG BỊ KHU / ẤY" (L_bud_04 bản đầu).
        text.split(/\s+/).forEach((word, wi) => {
          if (wi) box.appendChild(document.createTextNode(" "));
          const wd = el("span", "wd");
          glyphs(word).forEach((g) => wd.appendChild(el("span", "ch", g)));
          box.appendChild(wd);
        });
      }
      if (fx === "ripple") box.style.filter = `url(#lfRipple${ln.sentence_id})`;
      st.appendChild(box);
      if (text.length > 14) box.classList.add("long");
      if (text.length > 22) box.classList.add("xlong");
      inner._lf = { st, box, text, fx };
    },
    enter(tl, inner, ln) {
      const S = inner._lf, fx = S.fx, t0 = ln.start + .1, span = Math.max(1.5, ln.end - ln.start);
      const chs = S.box.querySelectorAll(".ch");
      const r = HF.rng(HF.hashSeed("fx" + ln.sentence_id));
      if (fx === "split" || fx === "crack") {
        const top = S.box.querySelector(".top"), bot = S.box.querySelector(".bot");
        tl.fromTo(S.box, { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: .45, ease: "power4.out" }, t0);
        if (fx === "split") {
          tl.to(top, { y: -46, x: -18, duration: .7, ease: "expo.out" }, t0 + .6);
          tl.to(bot, { y: 46, x: 18, duration: .7, ease: "expo.out" }, t0 + .6);
        } else {
          const p = S.box.querySelector(".lf-crack path");
          tl.fromTo(S.box.querySelector(".lf-crack"), { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: .35, ease: twos(.35) }, t0 + .5);
          tl.to(top, { y: -8, x: -10, rotation: -1.5, duration: .18, ease: "power4.out" }, t0 + .85);
          tl.to(bot, { y: 10, x: 12, rotation: 1.2, duration: .18, ease: "power4.out" }, t0 + .85);
          tl.fromTo(S.st, { x: 0 }, { x: 8, duration: .04, yoyo: true, repeat: 5, ease: "none" }, t0 + .85);
        }
      } else if (fx === "dissolve") {  // hiện rồi tan: từng chữ bay lên, nhoè, mờ
        tl.fromTo(chs, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .5, stagger: .04, ease: "power3.out" }, t0);
        const at = t0 + Math.min(span * .55, 2.2);
        chs.forEach((c) => tl.to(c, { y: -(60 + r() * 140), x: (r() - .5) * 120, rotation: (r() - .5) * 60, opacity: 0,
          filter: "blur(6px)", duration: 1.4 + r() * .6, ease: "power2.in" }, at + r() * .5));
      } else if (fx === "rays") {
        tl.fromTo(chs, { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: .6, stagger: .03 }, t0);
        const rays = S.st.querySelector(".lf-rays");
        tl.fromTo(rays, { opacity: 0, scale: .6, rotation: 0 }, { opacity: 1, scale: 1, duration: 1.2, ease: "power2.out" }, t0 + .3);
        tl.to(rays, { rotation: 25, duration: span + .5, ease: "none" }, t0 + .3);
        tl.fromTo(S.box, { textShadow: "0 0 0px rgba(255,220,140,0)" }, { textShadow: "0 0 60px rgba(255,220,140,.9)", duration: 1 }, t0 + .4);
      } else if (fx === "ripple") {
        const dm = S.st.querySelector("feDisplacementMap"), tb = S.st.querySelector("feTurbulence");
        tl.fromTo(chs, { opacity: 0 }, { opacity: 1, duration: .5, stagger: .03 }, t0);
        tl.fromTo(dm, { attr: { scale: 60 } }, { attr: { scale: 6 }, duration: 1.4, ease: "power2.out" }, t0);
        tl.fromTo(tb, { attr: { baseFrequency: "0.012 0.06" } }, { attr: { baseFrequency: "0.02 0.09" }, duration: span, ease: "sine.inOut" }, t0);
      } else if (fx === "wave") {
        tl.fromTo(chs, { opacity: 0 }, { opacity: 1, duration: .4, stagger: .03 }, t0);
        chs.forEach((c, k) => tl.fromTo(c, { y: 0 }, { y: 16, duration: .5, ease: "sine.inOut", yoyo: true,
          repeat: Math.max(1, Math.floor(span / .5)), delay: 0 }, t0 + .3 + k * .06));
      } else if (fx === "flicker") {  // lửa: sáng tối chập chờn theo chuỗi tất định
        tl.fromTo(chs, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .35, stagger: .03 }, t0);
        let t = t0 + .5;
        while (t < t0 + span) { const d = .06 + r() * .12;
          tl.to(S.box, { opacity: .55 + r() * .45, textShadow: `0 0 ${20 + r() * 50}px rgba(255,120,40,.9)`, duration: d, ease: "none" }, t); t += d; }
      } else if (fx === "grow") {  // chữ nhú lên từ mặt đất
        tl.fromTo(chs, { scaleY: 0, transformOrigin: "50% 100%", opacity: 0 }, { scaleY: 1, opacity: 1, duration: .6, stagger: .07, ease: "back.out(2)" }, t0);
      } else {
        tl.fromTo(chs, { opacity: 0, scale: 1.8, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .32, stagger: .05, ease: "power4.out" }, t0);
      }
    },
  };

  // ---- C3: minh hoạ SVG tự vẽ nét ----
  const ILLUS = {
    // Con đường một điểm tụ, máy quay dolly tiến về chân trời.
    road(s) {
      const g = sv("g", {}, s), hz = 380;
      sv("path", { d: `M0,${hz} L1920,${hz}`, class: "il-line thin" }, g);
      [[-900, 0], [900, 0], [-420, 0], [420, 0]].forEach(([x]) => sv("path", { d: `M${960 + x * 1.6},1080 L960,${hz}`, class: "il-line" + (Math.abs(x) < 500 ? " thin" : "") }, g));
      const dash = sv("path", { d: `M960,1080 L960,${hz}`, class: "il-dash" }, g);
      [[300, 250, 120], [1560, 240, 140], [620, 300, 70], [1320, 305, 60]].forEach(([x, w, h]) =>
        sv("path", { d: `M${x - w / 2},${hz} L${x},${hz - h} L${x + w / 2},${hz}`, class: "il-line thin" }, g));
      const sun = sv("circle", { cx: 960, cy: hz - 10, r: 70, class: "il-sun" }, g);
      return { g, dash, sun, cam: g };
    },
    // Núi nhiều lớp, mặt trời lên kèm tia sáng.
    sunrise(s) {
      const g = sv("g", {}, s);
      const sun = sv("circle", { cx: 960, cy: 700, r: 110, class: "il-sun" }, g);
      const rays = sv("g", { class: "il-rays" }, g);
      for (let k = 0; k < 16; k++) { const a = Math.PI + (k / 15) * Math.PI;
        sv("path", { d: `M${960 + Math.cos(a) * 150},${700 + Math.sin(a) * 150} L${960 + Math.cos(a) * 260},${700 + Math.sin(a) * 260}`, class: "il-line thin" }, rays); }
      const far = sv("path", { d: "M0,760 L240,600 L420,690 L640,540 L900,720 L1150,560 L1380,700 L1600,590 L1920,720 L1920,1080 L0,1080 Z", class: "il-fill far" }, g);
      const near = sv("path", { d: "M0,860 L300,740 L560,830 L820,700 L1100,860 L1400,730 L1700,850 L1920,780 L1920,1080 L0,1080 Z", class: "il-fill near" }, g);
      return { g, sun, rays, far, near, cam: g };
    },
    // Hoa sen nở trên mặt nước, gợn sóng lan ra.
    lotus(s) {
      const g = sv("g", { transform: "translate(960,620)" }, s);
      const ripples = [1, 2, 3].map((k) => sv("ellipse", { cx: 0, cy: 150, rx: 120 * k, ry: 26 * k, class: "il-line thin" }, g));
      const petals = [];
      [[-70, 1.0], [-35, 1.08], [0, 1.15], [35, 1.08], [70, 1.0], [-110, .85], [110, .85]].forEach(([a, k]) => {
        const p = sv("path", { d: `M0,120 C${-60 * k},40 ${-40 * k},${-120 * k} 0,${-190 * k} C${40 * k},${-120 * k} ${60 * k},40 0,120 Z`,
          class: "il-line petal", transform: `rotate(${a} 0 120)` }, g);
        petals.push(p);
      });
      return { g, petals, ripples, cam: g };
    },
    // Trăng khuyết, mây trôi, sao nhấp nháy.
    moon(s) {
      const g = sv("g", {}, s);
      const moon = sv("path", { d: "M1040,260 A150,150 0 1 0 1040,560 A118,118 0 1 1 1040,260 Z", class: "il-line il-moon" }, g);
      const clouds = [[520, 520, 1], [1320, 640, 1.3], [880, 780, .9]].map(([x, y, k]) =>
        sv("path", { d: `M${x - 180 * k},${y} q${40 * k},-60 ${100 * k},-30 q${40 * k},-70 ${120 * k},-20 q${60 * k},-30 ${90 * k},20 q${50 * k},10 ${50 * k},30 Z`, class: "il-line thin" }, g));
      const r = HF.rng(HF.hashSeed("stars"));
      const stars = Array.from({ length: 26 }, () => sv("circle", { cx: r() * 1920, cy: r() * 520, r: 1.5 + r() * 2.5, class: "il-star" }, g));
      return { g, moon, clouds, stars, cam: g };
    },
    // Ngôi nhà nét vẽ, cửa chính, la bàn hướng (phong thuỷ nhà ở).
    house(s) {
      const g = sv("g", { transform: "translate(960,560)" }, s);
      const parts = [
        "M-300,120 L-300,-60 L0,-260 L300,-60 L300,120 Z", "M-360,-40 L0,-300 L360,-40",
        "M-60,120 L-60,-20 L60,-20 L60,120", "M-230,0 L-130,0 L-130,70 L-230,70 Z", "M130,0 L230,0 L230,70 L130,70 Z",
        "M-420,120 L420,120"].map((d) => sv("path", { d, class: "il-line" }, g));
      const comp = sv("g", { transform: "translate(470,-190)" }, g);
      sv("circle", { r: 90, class: "il-line thin" }, comp);
      const needle = sv("path", { d: "M0,-78 L14,0 L0,78 L-14,0 Z", class: "il-fill needle" }, comp);
      [["B", 0, -112], ["N", 0, 128], ["Đ", 118, 10], ["T", -118, 10]].forEach(([t, x, y]) => {
        const e = sv("text", { x, y, class: "il-label" }, comp); e.textContent = t; });
      return { g, parts, comp, needle, cam: g };
    },
  };
  visuals.illus = {
    build(inner, ln) {
      const v = ln.visual, st = el("div", "lf-stage lf-illus"); inner.appendChild(st);
      const s = sv("svg", { viewBox: "0 0 1920 1080", class: "lf-illus-svg", preserveAspectRatio: PORTRAIT ? "xMidYMid slice" : "xMidYMid meet" }, st);
      const make = ILLUS[v.scene] || ILLUS.sunrise;
      inner._lf = { st, s, scene: v.scene in ILLUS ? v.scene : "sunrise", P: make(s), title: title(st, v.title, 150, 124) };
    },
    enter(tl, inner, ln, ctx) {
      const S = inner._lf, P = S.P, t0 = ln.start, span = Math.max(2, ctx.until - t0);
      const draw = (els, at, dur, each) => [].concat(els).forEach((p, k) => drawOn(tl, p, at + k * (each || 0), dur, "power2.inOut"));
      if (S.title) tl.fromTo(S.title, { opacity: 0 }, { opacity: 1, duration: .5 }, t0 + .2);
      if (S.scene === "road") {
        draw(Array.from(P.g.querySelectorAll(".il-line")), t0, 1.2, .08);
        tl.fromTo(P.sun, { attr: { cy: 470 }, opacity: 0 }, { attr: { cy: 300 }, opacity: 1, duration: span, ease: "sine.out" }, t0 + .6);
        tl.fromTo(P.dash, { strokeDashoffset: 0 }, { strokeDashoffset: -600, duration: span, ease: "none" }, t0);
        tl.fromTo(P.cam, { scale: 1, svgOrigin: "960 380" }, { scale: 1.35, duration: span, ease: "power1.in" }, t0 + .8);  // dolly
      } else if (S.scene === "sunrise") {
        tl.fromTo(P.far, { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 1.2, ease: "power3.out" }, t0);
        tl.fromTo(P.near, { y: 120, opacity: 0 }, { y: 0, opacity: 1, duration: 1.2, ease: "power3.out" }, t0 + .2);
        tl.fromTo(P.sun, { attr: { cy: 900 } }, { attr: { cy: 560 }, duration: span, ease: "sine.out" }, t0 + .3);
        tl.fromTo(P.rays, { opacity: 0, y: 340 }, { opacity: 1, y: 0, duration: span, ease: "sine.out" }, t0 + .3);
        draw(Array.from(P.rays.children), t0 + 1.2, .6, .05);
        tl.fromTo(P.near, { x: 0 }, { x: -40, duration: span, ease: "none", immediateRender: false }, t0 + 1.4);   // parallax
        tl.fromTo(P.far, { x: 0 }, { x: -14, duration: span, ease: "none", immediateRender: false }, t0 + 1.4);
      } else if (S.scene === "lotus") {
        draw(P.ripples, t0, 1.0, .2);
        P.petals.forEach((p, k) => { drawOn(tl, p, t0 + .5 + k * .12, .9, "power2.inOut");
          tl.fromTo(p, { scale: .2, svgOrigin: "0 120" }, { scale: 1, duration: 1.1, ease: "back.out(1.6)" }, t0 + .5 + k * .12); });
        P.ripples.forEach((rp, k) => tl.to(rp, { scale: 1.12, opacity: .3, svgOrigin: "0 150", duration: 2, yoyo: true, repeat: Math.ceil(span / 4), ease: "sine.inOut" }, t0 + 1 + k * .5));
      } else if (S.scene === "moon") {
        drawOn(tl, P.moon, t0, 1.4, "power2.inOut");
        tl.fromTo(P.moon, { fillOpacity: 0 }, { fillOpacity: 1, duration: 1 }, t0 + 1.2);
        P.clouds.forEach((c, k) => { drawOn(tl, c, t0 + .4 + k * .2, 1.0);
          tl.to(c, { x: (k % 2 ? -1 : 1) * 90, duration: span, ease: "none" }, t0 + .4); });
        P.stars.forEach((st, k) => tl.fromTo(st, { opacity: 0 }, { opacity: 1, duration: .6, yoyo: true, repeat: Math.ceil(span / 1.2), ease: "sine.inOut" }, t0 + .2 + (k % 7) * .17));
      } else if (S.scene === "house") {
        draw(P.parts, t0, .9, .18);
        tl.fromTo(P.comp, { opacity: 0, scale: .6, svgOrigin: "0 0" }, { opacity: 1, scale: 1, duration: .6, ease: "back.out(2)" }, t0 + 1.2);
        tl.fromTo(P.needle, { rotation: -140, svgOrigin: "0 0" }, { rotation: 0, duration: 1.6, ease: "elastic.out(1, .5)" }, t0 + 1.4);
      }
      tl.fromTo(S.st, { scale: 1 }, { scale: 1.04, duration: span, ease: "none" }, t0);
    },
  };

  // ---- C4: thẻ kết nền shader WebGL (mây/mực chuyển động) ----
  // Thời gian shader lấy từ timeline (tween tiến trình), vẽ lại trong onUpdate:
  // seek tới đâu vẽ đúng khung đó. Không có WebGL -> nền gradient tĩnh.
  visuals.endcard = {
    build(inner, ln) {
      const v = ln.visual, st = el("div", "lf-stage lf-end"); inner.appendChild(st);
      const cv = el("canvas", "lf-end-gl"); cv.width = 960; cv.height = 540; st.appendChild(cv);
      const night = theme() === "night";
      const gl = cv.getContext("webgl", { preserveDrawingBuffer: true, antialias: false });
      let draw = null;
      if (gl) {
        const vs = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
        const fs = `precision mediump float;uniform float t;uniform vec2 r;
          float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
          float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
            return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
          float fbm(vec2 p){float v=0.,a=.5;for(int k=0;k<5;k++){v+=a*n(p);p*=2.03;a*=.5;}return v;}
          void main(){vec2 uv=gl_FragCoord.xy/r;vec2 q=uv*vec2(3.2,1.8);
            float c=fbm(q+vec2(t*.06,t*.02)+fbm(q*1.6-vec2(t*.04,0.)));
            vec3 a=${night ? "vec3(.03,.05,.14)" : "vec3(.94,.91,.84)"}, b=${night ? "vec3(.55,.42,.16)" : "vec3(.62,.30,.20)"};
            gl_FragColor=vec4(mix(a,b,smoothstep(.45,.95,c)*${night ? ".85" : ".55"}),1.);}`;
        const sh = (type, src) => { const s2 = gl.createShader(type); gl.shaderSource(s2, src); gl.compileShader(s2); return s2; };
        const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs));
        gl.linkProgram(pr);
        if (gl.getProgramParameter(pr, gl.LINK_STATUS)) {
          gl.useProgram(pr);
          const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
          gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
          const loc = gl.getAttribLocation(pr, "p"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
          const ut = gl.getUniformLocation(pr, "t"); gl.uniform2f(gl.getUniformLocation(pr, "r"), cv.width, cv.height);
          draw = (tt) => { gl.uniform1f(ut, tt); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); };
          draw(0);
        }
      }
      if (!draw) cv.classList.add("nogl");
      const box = el("div", "lf-end-box");
      box.appendChild(el("div", "lf-end-main", v.text || "Đăng ký kênh"));
      if (v.sub) box.appendChild(el("div", "lf-end-sub", v.sub));
      st.appendChild(box);
      inner._lf = { st, cv, draw, box };
    },
    enter(tl, inner, ln, ctx) {
      const S = inner._lf, t0 = ln.start, span = Math.max(2, ctx.until - t0);
      tl.fromTo(S.cv, { opacity: 0 }, { opacity: 1, duration: 1.0 }, t0);
      if (S.draw) { const clock = { t: 0 }; tl.to(clock, { t: span * 1.0 + 1, duration: span + 1, ease: "none", onUpdate: () => S.draw(clock.t) }, t0); }
      tl.fromTo(S.box.children, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .7, stagger: .25, ease: "expo.out" }, t0 + .4);
      sheen(tl, S.box, t0 + 1.1);
    },
  };

  window.HF_LONG = PORTRAIT
    ? { layouts: {}, visuals, chapter, begin, pick, transition: null, ambient: null }
    : { layouts, visuals, chapter, begin, pick, transition, ambient };
})();
