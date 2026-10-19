/* COMPARE devices */
// Hai vùng cắt cạnh cứng (coral region split, dọc cho 9:16). static=true -> làm móc, đủ nghĩa ở khung 0.
HFS.device("split", {
  meta: { purpose: "compare", framing: "stacked-split", axis: "mask", circle: 0, energy: "M" },
  css: `.sp-a,.sp-b{position:absolute;left:0;right:0}
        .sp-a{top:250px;height:610px}.sp-b{top:860px;height:600px;background:var(--accent2);color:var(--on-accent2)}
        .sp-lab{position:absolute;left:108px;font-size:30px}.sp-a .sp-lab{top:90px;color:var(--accent)}.sp-b .sp-lab{top:70px;color:var(--glow)}
        .sp-val{position:absolute;left:100px;right:110px;font-size:160px}.sp-a .sp-val{top:140px}.sp-b .sp-val{top:120px}
        .sp-num{position:absolute;left:104px;font-size:220px;line-height:1;transform:rotate(-5deg);transform-origin:0 100%;white-space:nowrap}
        .sp-a .sp-num{top:350px;color:var(--accent)}.sp-b .sp-num{top:330px;color:var(--glow)}
        .sp-rule{position:absolute;left:0;right:0;top:856px;height:8px;background:var(--accent);transform-origin:0 50%}`,
  build(c, s, st) {
    const A = c.el("div", "sp-a", null, st), B = c.el("div", "sp-b", null, st), rule = c.el("div", "sp-rule", null, st);
    [A, B].forEach((x) => x.setAttribute("data-layout-allow-overlap", ""));
    const mk = (box, p) => { c.el("div", "sp-lab mono", c.esc(p.lab || ""), box); const v = c.el("div", "sp-val heavy", null, box);
      const ws = c.words(v, p.val); if (p.num) c.el("div", "sp-num disp", c.esc(p.num), box); return ws; };
    return { A, B, rule, wa: mk(A, s.a), wb: mk(B, s.b) };
  },
  enter(c, h, t0, s) {
    if (s.static) return;
    const ta = Math.max(t0 + .05, c.t(s.a.at, t0)), tb = Math.max(t0 + .6, c.t(s.b.at, t0 + 2));
    c.waterfall(h.wa, c.spread(ta, ta + .3, h.wa.length));
    c.tl.set(h.rule, { scaleX: 0 }, 0); c.tl.to(h.rule, { scaleX: 1, duration: c.S(.5), ease: c.E.entry }, tb - .45);
    c.tl.set(h.B, { clipPath: "inset(100% 0 0 0)" }, 0);
    c.tl.to(h.B, { clipPath: "inset(0% 0 0 0)", duration: c.S(.45), ease: "power4.out" }, tb - .3);
    c.waterfall(h.wb, c.spread(tb, tb + .3, h.wb.length), { y: 60 });
  },
});

// Ngộ nhận bị gạch -> sự thật đến bằng inverse zoom (H6 / myth-strike). BUD: glitch tắt (theme), không crash.
HFS.device("myth_strike", {
  meta: { purpose: "compare", framing: "center-hero", axis: "X", circle: 0, energy: "H" },
  css: `.ms-lab{position:absolute;left:108px;font-size:30px}.ms-myth{position:absolute;left:100px;right:110px;top:420px;font-size:112px;color:var(--ink)}
        .ms-x{position:absolute;left:-10px;right:-10px;top:50%;height:12px;background:var(--accent);transform-origin:0 50%}
        .ms-truth{position:absolute;left:100px;right:110px;top:900px;font-size:136px;color:var(--accent)}`,
  build(c, s, st) {
    c.el("div", "ms-lab mono", c.esc(s.mythLab || "NHIỀU NGƯỜI NGHĨ"), st).style.top = "340px";
    const m = c.el("div", "ms-myth heavy", null, st); c.words(m, s.myth);
    const x1 = c.el("div", "ms-x", null, m), x2 = c.el("div", "ms-x", null, m);
    const tl2 = c.el("div", "ms-lab mono", c.esc(s.truthLab || "THẬT RA"), st); tl2.style.top = "830px"; tl2.style.color = "var(--accent)";
    const t = c.el("div", "ms-truth heavy", null, st); c.words(t, s.truth);
    return { m, x1, x2, t, tl2 };
  },
  enter(c, h, t0, s) {
    c.reveal(h.m, t0 + .05, { x: -320, y: 0, d: .45 });
    const ts = c.t(s.strikeAt, t0 + 1.5);
    c.tl.set([h.x1, h.x2], { scaleX: 0 }, 0);
    c.tl.fromTo(h.x1, { scaleX: 0, rotation: -12 }, { scaleX: 1, rotation: -12, duration: .3, ease: c.E.draw, immediateRender: false }, ts);
    c.tl.fromTo(h.x2, { scaleX: 0, rotation: 12 }, { scaleX: 1, rotation: 12, duration: .3, ease: c.E.draw, immediateRender: false }, ts + .15);
    c.tl.to(h.m, { opacity: .55, duration: .3 }, ts + .15);
    const tt = c.t(s.truthAt, ts + .8);
    [h.tl2, h.t].forEach((n) => { c.tl.set(n, { autoAlpha: 0 }, 0); c.tl.set(n, { autoAlpha: 1 }, tt); });
    c.tl.fromTo(h.t, { scale: 1.25, filter: `blur(${c.M.blur}px)` }, { scale: 1, filter: "blur(0px)", duration: c.S(.5), ease: "expo.out", immediateRender: false }, tt);
    c.tl.set(h.t, { filter: "none" }, tt + c.S(.5));
  },
});
