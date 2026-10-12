/* lab.js — cảnh motion graphic riêng của kênh Mind in the Machine (theme "lab") cho engine video dài casewide.js.
   Nạp TRƯỚC casewide.js; casewide gọi window.labScenes({...}) để gắn thêm vào bảng cảnh B. Mọi mốc đã quy về giây
   (build_long.plan), tất định (rnd có hạt), mọi tween nằm trên timeline tạm dừng -> tua được (seek-safe).
   Âm thanh tương ứng: sfx_long.py (tick theo thẻ / chữ / mẩu chữ, whoosh theo tín hiệu, tiếng quân cờ).

   punch  : thẻ đục lỗ trượt vào máy, đếm lần thử 1→N, độ chính xác tăng, cuối cùng "TRÁI ✓ PHẢI ✓"
            {trials, startAt, until, accFrom?, label?}  ("at" cấp cảnh = lúc cảnh bắt đầu, build_long không chuyển vào engine)
   guess  : trò đoán chữ của Shannon — chữ hiện từng ô; đoán đúng sáng cyan, đoán sai nháy hổ phách rồi hiện chữ đúng
            {text, startAt, until, right, total, statAt?}  (mẫu đúng/sai là MINH HOẠ, chỉ tỉ lệ là số thật)
   chat   : khung trò chuyện; máy đáp gõ từng ký tự (ELIZA) hoặc chảy từng mẩu chữ (stream: true)
            {head, msgs: [{who: "u"|"m", text, at, dur?}], stream?}
   nn     : mạng nơ-ron vẽ dần; tín hiệu chạy xuôi (fwdAt), lỗi chạy ngược (backAt)
            {layers?, fwdAt?, backAt?, label?}
   go     : bàn cờ vây 19x19, quân đặt dần, một nước sáng lên với nhãn
            {hitAt, move, prob?, stones?}  */
window.labScenes = ({ B, tl, el, sv, esc, px, fsz, rnd, bg, common, W, H, C }) => {
  const acc = C.accent || "#22d3ee";

  B.punch = (s, d) => { bg(s, d, 0.78);
    const n = s.trials || 50, a0 = s.startAt ?? s.t0 + 0.4, a1 = Math.max(a0 + 1.2, s.until ?? s.t1 - 0.8), step = (a1 - a0) / n;
    const slot = el("div", "lbslot", null, d);
    for (let k = 0; k < Math.min(n, 24); k++) {   // thẻ thấy được; nhịp còn lại do bộ đếm thể hiện
      const left = (k * 7 + 3) % 2 === 0, t = a0 + (a1 - a0) * (k / Math.min(n, 24));
      const c = el("div", "pcard", null, d);
      for (let j = 0; j < 12; j++) { const h = el("i", null, null, c); h.style.left = px(18 + j * 23); h.style.opacity = rnd() > 0.6 ? 1 : 0.25; }
      const m = el("b", null, null, c); m.style.left = px(left ? 14 : 268);
      tl.fromTo(c, { x: -520, opacity: 0, rotation: (rnd() - 0.5) * 6 }, { x: 0, opacity: 1, duration: 0.22, ease: "power3.out", immediateRender: false }, t);
      tl.to(c, { x: 420, opacity: 0, duration: 0.2, ease: "power2.in" }, t + Math.max(0.12, step * 0.9));
    }
    const ct = el("div", "pcount", "LẦN THỬ <b>0</b>", d), o = { v: 0 };
    tl.fromTo(ct, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, a0 - 0.2);
    tl.to(o, { v: n, duration: a1 - a0, ease: "none", onUpdate: () => { ct.innerHTML = `LẦN THỬ <b>${Math.round(o.v)}</b>`; } }, a0);
    const bar = el("div", "pbar", "<i></i><span>ĐOÁN ĐÚNG</span>", d), fill = bar.querySelector("i");
    tl.fromTo(bar, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, a0);
    tl.fromTo(fill, { scaleX: (s.accFrom ?? 50) / 100 }, { scaleX: 1, duration: a1 - a0, ease: "power2.in", immediateRender: false }, a0);
    const ok = el("div", "pok", "TRÁI ✓&nbsp;&nbsp;&nbsp;PHẢI ✓", d);
    tl.fromTo(ok, { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.in", immediateRender: false }, a1 + 0.05);
    common(s, d); };

  B.guess = (s, d) => { bg(s, d, 0.85);
    const chars = [...s.text], n = chars.length, a0 = s.startAt ?? s.t0 + 0.3, a1 = Math.max(a0 + 1, s.until ?? s.t1 - 1.2);
    const want = Math.round(n * (s.right || 89) / (s.total || 129));   // số ô "đoán đúng" theo đúng tỉ lệ thật
    const order = chars.map((c, i) => ({ i, r: rnd() })).sort((x, y) => x.r - y.r), good = new Set(order.slice(0, want).map((x) => x.i));
    const fs = Math.min(84, Math.floor(1640 / (n * 0.62)));
    const row = el("div", "gsrow", null, d); row.style.fontSize = px(fs);
    tl.fromTo(row, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, s.t0 + 0.15);
    chars.forEach((ch, i) => { const c = el("span", "gsc" + (ch === " " ? " sp" : ""), ch === " " ? "&nbsp;" : esc(ch), row);
      if (ch === " ") return;
      c.style.opacity = 1; c.style.color = "rgba(230,241,255,0)";
      const t = a0 + (a1 - a0) * (i / n);
      if (good.has(i)) tl.fromTo(c, { y: 18, color: "rgba(34,211,238,0)" }, { y: 0, color: acc, duration: 0.12, immediateRender: false }, t);
      else { tl.fromTo(c, { color: "rgba(255,181,71,0)" }, { color: "#ffb547", duration: 0.08, immediateRender: false }, t);
             tl.to(c, { color: "#e6f1ff", duration: 0.2 }, t + 0.18); } });
    const leg = el("div", "gsleg", `<span style="color:${acc}">■ ĐOÁN ĐÚNG NGAY</span><span style="color:#ffb547">■ PHẢI GỢI Ý</span><em>MINH HỌA CÁCH CHƠI</em>`, d);
    tl.fromTo(leg, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, Math.min(a0, s.t0 + 0.4));
    const st = el("div", "gsstat", `<b>${s.right || 89}</b> / ${s.total || 129} chữ cái<span>${Math.round(100 * (s.right || 89) / (s.total || 129))}%</span>`, d);
    tl.fromTo(st, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out", immediateRender: false }, s.statAt ?? a1 + 0.1);
    common(s, d); };

  B.chat = (s, d) => { bg(s, d, 0.8);
    const win = el("div", "chwin", `<div class="chh"><i></i><i></i><i></i><span>${esc(s.head || "")}</span></div>`, d), body = el("div", "chbody", null, win);
    tl.fromTo(win, { opacity: 0, y: 40, scale: 0.97 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "power3.out", immediateRender: false }, s.t0 + 0.05);
    (s.msgs || []).forEach((m) => { const b = el("div", "chm " + (m.who === "m" ? "mach" : "user"), "", body), txt = [...m.text];
      tl.set(b, { opacity: 1 }, m.at - 0.05);
      const dur = m.dur ?? (m.who === "m" ? Math.min(1.4, 0.045 * txt.length) : Math.min(0.6, 0.02 * txt.length));
      if (s.stream && m.who === "m") {   // chảy từng mẩu chữ (vài ký tự một lần) — minh hoạ "đoán mẩu tiếp theo"
        const toks = m.text.match(/\S+\s*/g) || [m.text];
        toks.forEach((_, k) => tl.set(b, { innerHTML: esc(toks.slice(0, k + 1).join("")) + '<i class="chcur"></i>' }, m.at + dur * (k / toks.length)));
        tl.set(b, { innerHTML: esc(m.text) }, m.at + dur + 0.05);
      } else {
        const steps = Math.min(txt.length, 40);
        for (let k = 1; k <= steps; k++) tl.set(b, { textContent: txt.slice(0, Math.round(txt.length * k / steps)).join("") }, m.at + dur * (k / steps));
      } });
    common(s, d); };

  B.nn = (s, d) => { bg(s, d, 0.85);
    const L = s.layers || [4, 6, 6, 3], x0 = 470, x1 = 1450, y0 = 210, y1 = 790, g = sv("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d);
    const pos = L.map((n, li) => Array.from({ length: n }, (_, k) => [x0 + (x1 - x0) * li / (L.length - 1), y0 + (y1 - y0) * (k + 0.5) / n]));
    const edges = [];
    pos.forEach((col, li) => { if (li === 0) return; pos[li - 1].forEach((a) => col.forEach((b) => {
      const e = sv("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: "rgba(125,211,252,.28)", "stroke-width": 1.2 + rnd() * 2.2 }, g); edges.push([e, li]); })); });
    edges.forEach(([e, li]) => tl.fromTo(e, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, s.t0 + 0.15 + li * 0.12));
    const nodes = pos.flat().map(([x, y], k) => { const c = sv("circle", { cx: x, cy: y, r: 16, fill: "#0b1626", stroke: acc, "stroke-width": 3 }, g);
      tl.fromTo(c, { opacity: 0, scale: 0, svgOrigin: `${x} ${y}` }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)", immediateRender: false }, s.t0 + 0.1 + k * 0.025); return c; });
    const wave = (t, dir, color) => pos.forEach((col, li) => { const k = dir > 0 ? li : L.length - 1 - li;
      pos[k].forEach(([x, y]) => { const p = sv("circle", { cx: x, cy: y, r: 16, fill: color, opacity: 0 }, g);
        tl.fromTo(p, { opacity: 0.9, scale: 1, svgOrigin: `${x} ${y}` }, { opacity: 0, scale: 2.4, duration: 0.5, ease: "power2.out", immediateRender: false }, t + li * 0.16); }); });
    if (s.fwdAt != null) wave(s.fwdAt, 1, acc);
    if (s.backAt != null) { wave(s.backAt, -1, "#ffb547");
      edges.forEach(([e]) => tl.to(e, { attr: { "stroke-width": 1 + rnd() * 4 }, duration: 0.4 }, s.backAt + 0.5)); }
    common(s, d); };

  B.go = (s, d) => { bg(s, d, 0.85);
    const N = 19, S = 760, cx = W / 2 - S / 2, cy = 150, cell = S / (N - 1), g = sv("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d);
    sv("rect", { x: cx - 30, y: cy - 30, width: S + 60, height: S + 60, rx: 10, fill: "rgba(15,27,45,.92)", stroke: "rgba(34,211,238,.35)", "stroke-width": 2 }, g);
    for (let i = 0; i < N; i++) { sv("line", { x1: cx, y1: cy + i * cell, x2: cx + S, y2: cy + i * cell, stroke: "rgba(125,211,252,.35)", "stroke-width": 1.5 }, g);
      sv("line", { x1: cx + i * cell, y1: cy, x2: cx + i * cell, y2: cy + S, stroke: "rgba(125,211,252,.35)", "stroke-width": 1.5 }, g); }
    const used = new Set(), m = s.stones || 46, t0 = s.t0 + 0.2, span = Math.max(0.6, (s.hitAt ?? s.t1 - 1) - t0 - 0.4);
    for (let k = 0; k < m; k++) { let i, j; do { i = 2 + Math.floor(rnd() * 15); j = 2 + Math.floor(rnd() * 15); } while (used.has(i * N + j)); used.add(i * N + j);
      const st = sv("circle", { cx: cx + i * cell, cy: cy + j * cell, r: cell * 0.45, fill: k % 2 ? "#e6f1ff" : "#0a0f18", stroke: k % 2 ? "#9fb3c8" : "#5b6b80", "stroke-width": 1.5 }, g);
      tl.fromTo(st, { opacity: 0, scale: 1.6, svgOrigin: `${cx + i * cell} ${cy + j * cell}` }, { opacity: 1, scale: 1, duration: 0.12, immediateRender: false }, t0 + span * (k / m)); }
    if (s.hitAt != null) { let i = 9, j = 9; while (used.has(i * N + j)) i++;
      const X = cx + i * cell, Y = cy + j * cell, st = sv("circle", { cx: X, cy: Y, r: cell * 0.45, fill: "#e6f1ff", stroke: acc, "stroke-width": 3 }, g);
      const ring = sv("circle", { cx: X, cy: Y, r: cell * 0.9, fill: "none", stroke: acc, "stroke-width": 4 }, g);
      tl.fromTo(st, { opacity: 0, scale: 2, svgOrigin: `${X} ${Y}` }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in", immediateRender: false }, s.hitAt - 0.12);
      tl.fromTo(ring, { opacity: 0, scale: 0.5, svgOrigin: `${X} ${Y}` }, { opacity: 1, scale: 1.4, duration: 0.6, ease: "power2.out", immediateRender: false }, s.hitAt);
      const lb = el("div", "golbl", `<b>NƯỚC ${esc(s.move || "")}</b>${s.prob ? `<span>${esc(s.prob)}</span>` : ""}`, d);
      tl.fromTo(lb, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out", immediateRender: false }, s.hitAt + 0.2); }
    common(s, d); };
};
