/* PROCESS / CYCLE devices (tính vào ngân sách "circle": tối đa 1 / video) */
const HFS_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"];

// Bánh xe N ô (mặc định 12 chi) nghiêng 3D (lớp ngoài nghiêng, lớp trong xoay), quay về ô đích, làm phẳng rồi vẽ đường nối.
HFS.device("wheel", {
  meta: { purpose: "process", framing: "center-hero", axis: "3D", circle: 1, energy: "M" },
  css: `.wh-stage{position:absolute;left:0;top:250px;width:1080px;height:1200px;perspective:1600px}
        .wh-tilt{position:absolute;left:110px;top:150px;width:860px;height:860px;transform-style:preserve-3d}
        .wh-disc{position:absolute;inset:0}.wh-kick{position:absolute;left:108px;top:300px;font-size:30px;color:var(--accent)}
        .wh-tag{position:absolute;left:100px;top:1290px}`,
  build(c, s, st) {
    if (s.kick) c.el("div", "wh-kick mono", c.esc(s.kick), st);
    const labs = s.labels || HFS_CHI, N = labs.length, step = 360 / N;
    const stage = c.el("div", "wh-stage", null, st), tilt = c.el("div", "wh-tilt", null, stage), disc = c.el("div", "wh-disc", null, tilt);
    const svg = c.sv("svg", { width: 860, height: 860, viewBox: "-430 -430 860 860" }, disc);
    const R = 410, r0 = 108, P = (a, r) => [Math.sin(a * Math.PI / 180) * r, -Math.cos(a * Math.PI / 180) * r];
    c.sv("circle", { r: R + 8, style: "fill:none;stroke:var(--ink)", "stroke-width": 4 }, svg);
    const wedges = [], labels = [], nodes = [];
    labs.forEach((lab, i) => {
      const a0 = i * step - step / 2, a1 = i * step + step / 2, [x0, y0] = P(a0, R), [x1, y1] = P(a1, R), [x2, y2] = P(a1, r0), [x3, y3] = P(a0, r0);
      wedges.push(c.sv("path", { d: `M${x0},${y0} A${R},${R} 0 0 1 ${x1},${y1} L${x2},${y2} A${r0},${r0} 0 0 0 ${x3},${y3} Z`,
        style: `fill:${i % 2 ? "var(--ground2)" : "var(--ground)"};stroke:var(--ink)`, "stroke-width": 2 }, svg));
      const [lx, ly] = P(i * step, (R + r0) / 2 + 10), g = c.sv("g", { transform: `translate(${lx},${ly})` }, svg);
      const t = c.sv("text", { "text-anchor": "middle", y: 22, "font-weight": 900, "font-size": N > 12 ? 44 : 62, style: "font-family:var(--font-body);fill:var(--ink)" }, g);
      t.textContent = lab; labels.push({ g, lx, ly, t }); nodes.push(P(i * step, s.linkR || 232));
    });
    c.sv("circle", { r: r0 - 4, style: "fill:var(--ink)" }, svg);
    const lines = (s.links || []).map((pair) => { const [p, q] = pair.map((x) => nodes[labs.indexOf(x)]);
      return c.sv("line", { x1: p[0], y1: p[1], x2: q[0], y2: q[1], style: `stroke:${s.linkTone === "accent" ? "var(--accent)" : "var(--glow)"}`, "stroke-width": 14, "stroke-linecap": "round", opacity: 0 }, svg); });
    const tag = c.el("div", "wh-tag", null, st); c.el("span", "pill", c.esc(s.tag || ""), tag);
    return { tilt, disc, wedges, labels, lines, tag, idx: labs.indexOf(s.target), labs, step };
  },
  enter(c, h, t0, s) {
    const sp = { a: 180 - h.idx * h.step - 900, tilt: 52 }, a1 = 180 - h.idx * h.step - 720;
    const place = () => { gsap.set(h.tilt, { rotationX: sp.tilt }); gsap.set(h.disc, { rotation: sp.a });
      h.labels.forEach((L) => L.g.setAttribute("transform", `translate(${L.lx},${L.ly}) rotate(${-sp.a})`)); };
    place();
    c.tl.fromTo(sp, { a: sp.a, tilt: 52 }, { a: a1, tilt: 52, duration: c.S(2.0), ease: "power4.out", onUpdate: place, immediateRender: false }, t0);
    const tl2 = t0 + c.S(1.7);
    c.tl.set(h.wedges[h.idx], { attr: { style: "fill:var(--accent);stroke:var(--ink)" } }, tl2);
    c.tl.set(h.labels[h.idx].t, { attr: { style: "font-family:var(--font-body);fill:var(--on-accent,#fff)" } }, tl2);
    (s.also || []).forEach((x) => c.tl.set(h.wedges[h.labs.indexOf(x)], { attr: { style: "fill:var(--glow-soft, var(--ground2));stroke:var(--ink)" } }, c.t(s.alsoAt, tl2 + .4)));
    const tf = Math.max(tl2 + .3, c.t(s.linkAt, tl2 + .6));
    c.tl.to(sp, { tilt: 18, duration: c.S(.7), ease: c.E.move, onUpdate: place }, tf - .5);
    h.lines.forEach((ln, k) => { const len = Math.hypot(ln.x2.baseVal.value - ln.x1.baseVal.value, ln.y2.baseVal.value - ln.y1.baseVal.value);
      ln.setAttribute("stroke-dasharray", len); c.tl.set(ln, { attr: { "stroke-dashoffset": len }, opacity: 1 }, tf);
      c.tl.to(ln, { attr: { "stroke-dashoffset": 0 }, duration: c.S(.4), ease: c.E.draw }, tf + k * .28); });
    c.reveal(h.tag, c.t(s.tagAt, tf + .3), { x: -60, y: 0, d: .45 });
  },
});

// Chu trình tự vẽ: các nút trên vòng/ngũ giác, mỗi mũi tên vẽ theo mốc lời, nút đích bật khi mũi tên tới.
HFS.device("cycle_draw", {
  meta: { purpose: "process", framing: "center-hero", axis: "draw", circle: 1, energy: "M" },
  css: `.cy-kick{position:absolute;left:108px;top:300px;font-size:30px;color:var(--accent)}
        .cy-svg{position:absolute;left:90px;top:400px}`,
  build(c, s, st) {
    if (s.kick) c.el("div", "cy-kick mono", c.esc(s.kick), st);
    const N = s.nodes.length, R = 330, cx = 450, cy = 450;
    const svg = c.sv("svg", { width: 900, height: 900, viewBox: "0 0 900 900", class: "cy-svg" }, st);
    const pos = s.nodes.map((_, i) => { const a = (i / N) * Math.PI * 2 - Math.PI / 2; return [cx + Math.cos(a) * R, cy + Math.sin(a) * R]; });
    const edges = (s.edges || []).map((e) => { const a = pos[s.nodes.findIndex((n) => n.id === e.from)], b = pos[s.nodes.findIndex((n) => n.id === e.to)];
      const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, k = e.kind === "inner" ? 0 : .35;
      const qx = mx + (mx - cx) * k, qy = my + (my - cy) * k, sh = 92 / Math.hypot(b[0] - a[0], b[1] - a[1]);
      const ax = a[0] + (qx - a[0]) * sh * 1.2, ay = a[1] + (qy - a[1]) * sh * 1.2, bx = b[0] + (qx - b[0]) * sh * 1.2, by = b[1] + (qy - b[1]) * sh * 1.2;
      return { e, p: c.sv("path", { d: `M${ax},${ay} Q${qx},${qy} ${bx},${by}`, style: `fill:none;stroke:${e.kind === "inner" ? "var(--accent)" : "var(--ink)"}`,
        "stroke-width": e.kind === "inner" ? 6 : 9, "stroke-linecap": "round", "stroke-dasharray": e.kind === "inner" ? "" : "", opacity: 0 }, svg), to: b }; });
    const nodes = s.nodes.map((n, i) => { const g0 = c.sv("g", { transform: `translate(${pos[i][0]},${pos[i][1]})` }, svg), g = c.sv("g", {}, g0);
      c.sv("circle", { r: 88, style: `fill:${n.tone === "accent" ? "var(--accent)" : "var(--ground2)"};stroke:var(--ink)`, "stroke-width": 4 }, g);
      const t = c.sv("text", { "text-anchor": "middle", y: 20, "font-weight": 900, "font-size": n.label.length > 4 ? 46 : 58,
        style: `font-family:var(--font-body);fill:${n.tone === "accent" ? "var(--on-accent,#fff)" : "var(--ink)"}` }, g); t.textContent = n.label; return g; });
    return { edges, nodes };
  },
  enter(c, h, t0, s) {
    h.nodes.forEach((g, i) => { const at = c.t(s.nodes[i].at, t0 + .1 + i * .08);
      c.tl.set(g, { autoAlpha: 0 }, 0); c.tl.set(g, { autoAlpha: 1 }, at);
      c.tl.fromTo(g, { scale: .6, transformOrigin: "50% 50%" }, { scale: 1, duration: c.S(.35), ease: c.E.entry, immediateRender: false }, at); });
    h.edges.forEach((ed) => c.draw(ed.p, c.t(ed.e.at, t0 + 1), .55));
  },
});
