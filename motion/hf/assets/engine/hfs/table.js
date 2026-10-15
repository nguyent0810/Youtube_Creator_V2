/* LIST / TABLE devices */
// Bảng tra: mỗi hàng (năm sinh + số đếm) hiện theo mốc, ô bên phải hiện + dải sáng theo từng mốc.
HFS.device("ledger", {
  meta: { purpose: "list", framing: "grid", axis: "Y", circle: 0, energy: "M" },
  css: `.lg-title{position:absolute;left:108px;top:330px;font-size:32px}
        .lg{position:absolute;left:100px;right:110px;top:420px}
        .lg-h,.lg-r{display:grid;grid-template-columns:300px 1fr;align-items:center;column-gap:30px}
        .lg-h{font-size:24px;color:var(--accent);padding-bottom:16px;border-bottom:4px solid var(--ink)}
        .lg-r{padding:56px 0 50px;border-bottom:2px solid var(--line)}
        .lg-y{font-size:128px;line-height:1;color:var(--accent)}
        .lg-a{font-family:var(--font-mono);font-weight:800;font-size:100px;line-height:1;font-variant-numeric:tabular-nums;transform-origin:0 50%}
        .lg-a small{font-size:30px;color:var(--soft-text,#6B6156);margin-left:8px}
        .lg-s{font-size:58px;font-weight:900;line-height:1.15;position:relative;margin:10px 0;white-space:nowrap}
        .lg-s small{display:inline-block;width:96px;font-family:var(--font-mono);font-size:26px;color:var(--accent);font-weight:800;letter-spacing:.1em;vertical-align:middle}`,
  build(c, s, st) {
    c.el("div", "lg-title mono", c.esc(s.title || ""), st);
    const box = c.el("div", "lg", null, st), hd = c.el("div", "lg-h mono", null, box);
    (s.head || []).forEach((x) => c.el("div", "", c.esc(x), hd));
    const rows = (s.rows || []).map((r) => { const row = c.el("div", "lg-r", null, box), yc = c.el("div", "", null, row);
      c.el("div", "lg-y disp", c.esc(r.y), yc); const aw = c.el("div", "lg-a", null, yc), a = c.el("span", "", "", aw); if (r.unit) c.el("small", "", c.esc(r.unit), aw);
      const sc = c.el("div", "", null, row);
      const cells = (r.cells || []).map((x) => { const e = c.el("div", "lg-s", `<small>${c.esc(x.k)}</small>${c.esc(x.v)}`, sc); return e; });
      return { row, a, aw, cells }; });
    return { hd, rows };
  },
  enter(c, h, t0, s) {
    c.reveal(h.hd, t0 + .05, { y: 30, d: .4 });
    h.rows.forEach((R, i) => { const r = s.rows[i], tr = c.t(r.at, t0 + .4 + i);
      c.reveal(R.row, tr, { y: 50, d: .2, ease: "power4.out" });
      if (r.value != null) { const ta = c.t(r.valueAt, tr + .3), from = r.from != null ? r.from : r.value - 8;
        c.count(R.a, from, r.value, ta, 1.0); c.tl.fromTo(R.aw, { scale: .6 }, { scale: 1, duration: c.S(1), ease: "power3.out", immediateRender: false }, ta); }
      R.cells.forEach((cell, k) => { const tc = c.t(r.cells[k].at, tr + .6 + k * .5); c.reveal(cell, tc, { y: 26, d: .16, ease: "power4.out" }); c.underline(cell, tc + .15, { d: .4 }); }); });
  },
});

// Danh sách tích lũy: mỗi mục một dòng theo mốc (dấu + chữ trượt), mục cũ mờ dần theo vị trí.
HFS.device("list_build", {
  meta: { purpose: "list", framing: "grid", axis: "X", circle: 0, energy: "M" },
  css: `.lb-title{position:absolute;left:108px;top:330px;font-size:32px;color:var(--accent)}
        .lb{position:absolute;left:100px;right:110px;top:390px;display:flex;flex-direction:column;gap:30px}
        .lb-i{display:grid;grid-template-columns:110px 1fr;align-items:center;column-gap:24px}
        .lb-k{width:96px;height:96px;border-radius:var(--radius,8px);background:var(--accent);color:var(--on-accent,#fff);display:flex;align-items:center;justify-content:center;
              font-family:var(--font-mono);font-weight:800;font-size:44px}
        .lb-t{font-size:66px;font-weight:900;line-height:1.16}.lb-t small{display:block;font-size:34px;font-weight:600;color:var(--soft-text,#6B6156);margin-top:4px}
        .lb-g{font-family:var(--font-mono);font-size:34px;letter-spacing:.14em;color:var(--accent);margin-top:14px;border-top:2px solid var(--line);padding-top:16px}`,
  build(c, s, st) {
    if (s.title) c.el("div", "lb-title mono", c.esc(s.title), st);
    const box = c.el("div", "lb", null, st);
    const items = s.items.map((it, i) => { if (it.group) { const g = c.el("div", "lb-g", c.esc(it.group), box); return { g, it }; }
      const row = c.el("div", "lb-i", null, box);
      c.el("div", "lb-k", c.esc(it.key != null ? it.key : String(i + 1)), row);
      c.el("div", "lb-t", `${c.esc(it.text).replace(/ · /g, "\u00a0· ")}${it.sub ? `<small>${c.esc(it.sub)}</small>` : ""}`, row); return { row, it }; });
    return { items };
  },
  enter(c, h, t0, s) {
    const shown = [];
    h.items.forEach((x, i) => { const t = c.t(x.it.at, t0 + .3 + i * .5);
      if (x.g) { c.reveal(x.g, t, { y: 20, d: .3 }); return; }
      c.reveal(x.row, t, { x: -40, y: 0, d: .3 });
      shown.forEach((p, k) => c.tl.to(p, { opacity: Math.max(.45, 1 - .18 * (shown.length - k)), duration: .3 }, t));
      shown.push(x.row); });
  },
});
