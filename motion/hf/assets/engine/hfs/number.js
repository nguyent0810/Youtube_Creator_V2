/* NUMBER devices -- mỗi con số đi kèm một hình (vòng, thanh, lưới), đếm power3.out 1.2-1.6s, đơn vị vào SAU khi số chạm đích. */
HFS.device("count_ring", {
  meta: { purpose: "number", framing: "center-hero", axis: "count", circle: 1, energy: "M" },
  css: `.cr-lab{position:absolute;left:100px;right:110px;top:320px;font-size:64px;font-weight:900;line-height:1.15}
        .cr-svg{position:absolute;left:190px;top:470px}
        .cr-num{position:absolute;left:0;right:0;top:760px;text-align:center;font-family:var(--font-display);font-weight:900;font-size:230px;line-height:1;font-variant-numeric:tabular-nums;color:var(--accent)}
        .cr-suf{position:absolute;left:0;right:0;top:1010px;text-align:center;font-size:58px;font-weight:900}
        .cr-note{position:absolute;left:100px;right:110px;top:1260px;font-size:44px;font-weight:700;color:var(--soft-text,#6B6156);text-align:center}`,
  build(c, s, st) {
    c.el("div", "cr-lab", c.esc(s.label || ""), st);
    const svg = c.sv("svg", { width: 700, height: 700, viewBox: "-350 -350 700 700", class: "cr-svg" }, st);
    c.sv("circle", { r: 300, style: "fill:none;stroke:var(--line)", "stroke-width": 26 }, svg);
    const ring = c.sv("circle", { r: 300, style: "fill:none;stroke:var(--accent)", "stroke-width": 26, "stroke-linecap": "round", transform: "rotate(-90)" }, svg);
    const num = c.el("div", "cr-num", "", st), suf = c.el("div", "cr-suf", c.esc(s.suffix || ""), st);
    const note = s.note ? c.el("div", "cr-note", c.esc(s.note), st) : null;
    return { ring, num, suf, note };
  },
  enter(c, h, t0, s) {
    const t = c.t(s.at, t0 + .2), d = s.dur || 1.4, L = 2 * Math.PI * 300, pct = s.pct != null ? s.pct : 1;
    const fmt = (v) => (s.decimals ? v.toFixed(s.decimals).replace(".", ",") : Math.round(v).toLocaleString("vi-VN"));
    h.ring.setAttribute("stroke-dasharray", L); c.tl.set(h.ring, { attr: { "stroke-dashoffset": L } }, 0);
    c.tl.to(h.ring, { attr: { "stroke-dashoffset": L * (1 - pct) }, duration: c.S(d), ease: "power3.out" }, t);
    c.count(h.num, s.from || 0, s.value, t, d, fmt);
    c.tl.fromTo(h.num, { scale: .5 }, { scale: 1, duration: c.S(d), ease: "power3.out", immediateRender: false }, t);
    c.reveal(h.suf, t + c.S(d) - .05, { y: 20, d: .4, ease: c.E.pop() });
    if (h.note) c.reveal(h.note, c.t(s.noteAt, t + c.S(d) + .4), { y: 24, d: .35 });
  },
});

// Thanh ngang so sánh (9:16: nhãn bên trái), thanh nhấn đếm số cùng ease, thanh khác mờ.
HFS.device("bars", {
  meta: { purpose: "number", framing: "grid", axis: "X", circle: 0, energy: "M" },
  css: `.br-title{position:absolute;left:108px;top:330px;font-size:32px;color:var(--accent)}
        .br{position:absolute;left:100px;right:110px;top:440px;display:flex;flex-direction:column;gap:70px}
        .br-lab{font-size:50px;font-weight:900;margin-bottom:16px;display:flex;justify-content:space-between}
        .br-lab b{font-family:var(--font-mono);font-variant-numeric:tabular-nums}
        .br-track{height:84px;background:var(--line);border-radius:var(--radius,6px);overflow:hidden}
        .br-fill{height:100%;width:100%;background:var(--ink);transform-origin:0 50%}.br-fill.hot{background:var(--accent)}
        .br-diff{position:absolute;left:100px;right:110px;top:1150px;font-size:76px;font-weight:900;color:var(--accent)}`,
  build(c, s, st) {
    if (s.title) c.el("div", "br-title mono", c.esc(s.title), st);
    const box = c.el("div", "br", null, st), max = Math.max(...s.bars.map((b) => b.value));
    const bars = s.bars.map((b) => { const w = c.el("div", "", null, box), lab = c.el("div", "br-lab", `<span>${c.esc(b.label)}</span>`, w);
      const num = c.el("b", "", "0", lab); const tr = c.el("div", "br-track", null, w), f = c.el("div", "br-fill" + (b.hot ? " hot" : ""), null, tr);
      return { w, num, f, pct: b.value / max, b }; });
    const diff = s.diff ? c.el("div", "br-diff", c.esc(s.diff), st) : null;
    return { bars, diff };
  },
  enter(c, h, t0, s) {
    h.bars.forEach((B, i) => { const t = c.t(B.b.at, t0 + .3 + i * .8);
      c.reveal(B.w, t, { y: 30, d: .3 });
      c.tl.set(B.f, { scaleX: 0 }, 0); c.tl.to(B.f, { scaleX: B.pct, duration: c.S(1.2), ease: "power3.out" }, t);
      c.count(B.num, 0, B.b.value, t, 1.2, (v) => Math.round(v) + (s.unit ? " " + s.unit : "")); });
    if (h.diff) c.reveal(h.diff, c.t(s.diffAt, t0 + 3), { y: 30, d: .4, ease: c.E.pop() });
  },
});

// Lưới đơn vị "k trong N": N ô bật nhanh (<=0.5s), các ô được chọn sáng màu nhấn theo mốc, nhãn đếm.
HFS.device("unit_grid", {
  meta: { purpose: "number", framing: "grid", axis: "Z", circle: 0, energy: "M" },
  css: `.ug-title{position:absolute;left:100px;right:110px;top:320px;font-size:64px;font-weight:900;line-height:1.15}
        .ug{position:absolute;left:100px;right:110px;top:560px;display:grid;gap:18px}
        .ug-c{aspect-ratio:1/1;border:4px solid var(--ink);border-radius:var(--radius,8px);display:flex;align-items:center;justify-content:center;
              font-family:var(--font-mono);font-weight:800;font-size:40px;color:var(--soft-text,#6B6156);background:var(--ground)}
        .ug-c.lit{background:var(--accent);color:var(--on-accent,#fff);border-color:var(--accent)}
        .ug-lab{position:absolute;left:100px;right:110px;top:1240px;font-size:70px;font-weight:900}.ug-lab b{color:var(--accent);font-family:var(--font-mono)}`,
  build(c, s, st) {
    c.el("div", "ug-title", c.esc(s.title || ""), st);
    const g = c.el("div", "ug", null, st), cols = s.cols || 5; g.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    const cells = Array.from({ length: s.total }, (_, i) => c.el("div", "ug-c", String(i + 1), g));
    const lab = c.el("div", "ug-lab", `<b>0</b> ${c.esc(s.unitLabel || "")}`, st);
    return { cells, lab, n: lab.querySelector("b") };
  },
  enter(c, h, t0, s) {
    const n = h.cells.length, step = Math.min(.04, .5 / n);
    h.cells.forEach((e, i) => { c.tl.set(e, { autoAlpha: 0 }, 0); c.tl.set(e, { autoAlpha: 1 }, t0 + .15 + i * step);
      c.tl.fromTo(e, { scale: .5 }, { scale: 1, duration: .3, ease: c.E.entry, immediateRender: false }, t0 + .15 + i * step); });
    const tl0 = c.t(s.litAt, t0 + 1.2), lit = s.lit || [];
    lit.forEach((k, j) => { const e = h.cells[k - 1], t = tl0 + j * .18;
      c.tl.set(e, { attr: { class: "ug-c lit" } }, t);
      c.tl.fromTo(e, { scale: 1.15 }, { scale: 1, duration: .25, ease: c.E.entry, immediateRender: false }, t); });
    c.reveal(h.lab, tl0, { y: 24, d: .35 });
    c.count(h.n, 0, lit.length, tl0, .18 * lit.length + .2);
  },
});
