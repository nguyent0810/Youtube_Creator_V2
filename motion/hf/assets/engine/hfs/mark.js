/* MARK / EVIDENCE devices */
// Chữ lớn + chữ Hán mờ + các dấu son đóng theo mốc lời (cảnh báo, phán định theo truyền thống).
HFS.device("stamp", {
  meta: { purpose: "statement", framing: "edge-band", axis: "X", circle: 0, energy: "H" },
  css: `.st-han{position:absolute;left:0;right:0;top:320px;text-align:center;font-size:880px;line-height:1;color:var(--ghost-accent, rgba(195,47,39,.08));font-family:var(--font-cjk, serif)}
        .st-kick{position:absolute;left:108px;top:330px;font-size:32px;color:var(--accent)}
        .st-big{position:absolute;left:96px;top:400px;font-size:320px;line-height:1.05;white-space:nowrap}`,
  build(c, s, st) {
    if (s.han) c.el("div", "st-han", c.esc(s.han), st);
    c.el("div", "st-kick mono", c.esc(s.kick || ""), st);
    const big = c.el("div", "st-big disp", c.esc(s.big || ""), st);
    const seals = (s.stamps || []).map((p) => { const e = c.el("div", "seal", c.esc(p.text), st); e.style.left = p.x + "px"; e.style.top = p.y + "px"; return e; });
    return { big, seals, st };
  },
  enter(c, h, t0, s) {
    c.reveal(h.big, t0 + .05, { x: -90, y: 0, d: .45 });
    (s.stamps || []).forEach((p, k) => { const ts = c.t(p.at, t0 + 1 + k); c.stamp(h.seals[k], ts, p.rot || -6);
      c.burst(h.st, p.x + 160, p.y + 50, ts + .04, "st" + t0 + k, 10);
      c.tl.fromTo(h.st, { x: 0 }, { x: 8, duration: .05, yoyo: true, repeat: 3, ease: "none", immediateRender: false }, ts + .02); });
  },
});

// Thẻ nguồn: tên kinh/sách + mã + đoạn trích, dải sáng quét cụm then chốt, dấu "ĐÃ ĐỐI CHIẾU" (tạo niềm tin trước phán định).
HFS.device("source_card", {
  meta: { purpose: "evidence", framing: "card-on-field", axis: "Y", circle: 0, energy: "C" },
  css: `.sc-card{position:absolute;left:100px;right:110px;top:420px;padding:56px 54px 60px;background:var(--card, var(--ground2));border:2px solid var(--line);border-left:12px solid var(--accent)}
        .sc-src{font-size:34px;color:var(--accent)}.sc-ref{font-size:96px;line-height:1.08;margin:18px 0 26px}
        .sc-snip{font-family:var(--font-quote, var(--font-display));font-style:italic;font-size:54px;line-height:1.32;color:var(--ink)}
        .sc-hl{position:relative;display:inline}.sc-hl::before{content:"";position:absolute;left:-4px;right:-4px;bottom:2px;height:.5em;background:var(--glow);opacity:.45;z-index:-1;transform:scaleX(var(--hl,0));transform-origin:0 50%}
        .sc-seal{right:120px;top:1170px;left:auto;font-size:44px}`,
  build(c, s, st) {
    const card = c.el("div", "sc-card", null, st);
    c.el("div", "sc-src mono", c.esc(s.source || ""), card);
    c.el("div", "sc-ref disp", c.esc(s.ref || ""), card);
    const snip = c.el("div", "sc-snip", null, card);
    const parts = String(s.snippet || "").split(/\[\[|\]\]/);       // [[cụm then chốt]]
    let hl = null; parts.forEach((p, k) => { if (k % 2) { hl = c.el("span", "sc-hl", c.esc(p), snip); } else snip.appendChild(document.createTextNode(p)); });
    const seal = c.el("div", "seal sc-seal", c.esc(s.seal || "ĐÃ ĐỐI CHIẾU"), st);
    return { card, hl, seal };
  },
  enter(c, h, t0, s) {
    c.reveal(h.card, t0 + .05, { y: 80, d: .5 });
    if (h.hl) { c.tl.set(h.hl, { "--hl": 0 }, 0); c.tl.to(h.hl, { "--hl": 1, duration: c.S(.6), ease: c.E.draw }, c.t(s.hlAt, t0 + 1.4)); }
    if (s.seal !== false) c.stamp(h.seal, c.t(s.sealAt, t0 + 2.2), 6);
  },
});
