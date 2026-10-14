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
    // "pos": [[x, y, "B"|"W"], …] = THẾ CỜ THẬT (dựng từ biên bản ván đấu, theo thứ tự đặt quân); thiếu thì quân đặt ngẫu nhiên để minh hoạ.
    const used = new Set(), pos = s.pos, m = pos ? pos.length : (s.stones || 46), t0 = s.t0 + 0.2, span = Math.max(0.6, (s.hitAt ?? s.t1 - 1) - t0 - 0.4);
    for (let k = 0; k < m; k++) { let i, j, wh = k % 2; if (pos) { [i, j] = pos[k]; wh = pos[k][2] === "W"; }
      else do { i = 2 + Math.floor(rnd() * 15); j = 2 + Math.floor(rnd() * 15); } while (used.has(i * N + j)); used.add(i * N + j);
      const st = sv("circle", { cx: cx + i * cell, cy: cy + j * cell, r: cell * 0.45, fill: wh ? "#e6f1ff" : "#0a0f18", stroke: wh ? "#9fb3c8" : "#5b6b80", "stroke-width": 1.5 }, g);
      tl.fromTo(st, { opacity: 0, scale: 1.6, svgOrigin: `${cx + i * cell} ${cy + j * cell}` }, { opacity: 1, scale: 1, duration: 0.12, immediateRender: false }, t0 + span * (k / m)); }
    if (s.hitAt != null) { let i = 9, j = 9; if (s.hit) { i = s.hit[0]; j = s.hit[1]; } else while (used.has(i * N + j)) i++;
      const X = cx + i * cell, Y = cy + j * cell, st = sv("circle", { cx: X, cy: Y, r: cell * 0.45, fill: (s.hit ? s.hit[2] === "B" : s.black) ? "#0a0f18" : "#e6f1ff", stroke: acc, "stroke-width": 3 }, g);
      const ring = sv("circle", { cx: X, cy: Y, r: cell * 0.9, fill: "none", stroke: acc, "stroke-width": 4 }, g);
      tl.fromTo(st, { opacity: 0, scale: 2, svgOrigin: `${X} ${Y}` }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in", immediateRender: false }, s.hitAt - 0.12);
      tl.fromTo(ring, { opacity: 0, scale: 0.5, svgOrigin: `${X} ${Y}` }, { opacity: 1, scale: 1.4, duration: 0.6, ease: "power2.out", immediateRender: false }, s.hitAt);
      const lb = el("div", "golbl", `<b>NƯỚC ${esc(s.move || "")}</b>${s.prob ? `<span>${esc(s.prob)}</span>` : ""}`, d);
      tl.fromTo(lb, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out", immediateRender: false }, s.hitAt + 0.2); }
    common(s, d); };

  /* chess : bàn cờ vua 8x8. {fen (THẾ CỜ THẬT dựng từ biên bản, hoặc thế ban đầu), hit?: "e6" (ô được nhấn), hitAt?, move?: "8", prob?: chú thích,
             flip?: true (nhìn từ phía quân đen)}. Quân vẽ bằng ký tự cờ Unicode (♚♛♜♝♞♟) tô trắng/đen, có viền. (14/10/2026, MIM Deep Blue) */
  B.chess = (s, d) => { bg(s, d, 0.85);
    const S = 720, c = S / 8, cx = W / 2 - S / 2, cy = 110, g = sv("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d);
    sv("rect", { x: cx - 26, y: cy - 26, width: S + 52, height: S + 52, rx: 10, fill: "rgba(15,27,45,.94)", stroke: "rgba(34,211,238,.4)", "stroke-width": 2 }, g);
    for (let r = 0; r < 8; r++) for (let f = 0; f < 8; f++)
      sv("rect", { x: cx + f * c, y: cy + r * c, width: c, height: c, fill: (r + f) % 2 ? "#3b5a7a" : "#c9d6e3" }, g);
    const GL = { k: "♚", q: "♛", r: "♜", b: "♝", n: "♞", p: "♟" }, sq = (name) => { const f = name.charCodeAt(0) - 97, r = 8 - +name[1];
      return s.flip ? [7 - f, 7 - r] : [f, r]; };
    const rows = String(s.fen || "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR").split(" ")[0].split("/"), pcs = [];
    rows.forEach((row, r) => { let f = 0; for (const ch of row) { if (/\d/.test(ch)) { f += +ch; continue; }
      const white = ch === ch.toUpperCase(), name = String.fromCharCode(97 + f) + (8 - r), [x, y] = sq(name);
      const t = sv("text", { x: cx + x * c + c / 2, y: cy + y * c + c * 0.78, "text-anchor": "middle", "font-size": c * 0.82, "font-family": "'Segoe UI Symbol','DejaVu Sans','Noto Sans Symbols 2',serif",
        fill: white ? "#f8fafc" : "#0a0f18", stroke: white ? "#0a0f18" : "#e2e8f0", "stroke-width": 1.6, "paint-order": "stroke" }, g);
      t.textContent = GL[ch.toLowerCase()]; pcs.push(t); f++; } });
    const t0 = s.t0 + 0.15; pcs.forEach((p, k) => tl.fromTo(p, { opacity: 0 }, { opacity: 1, duration: 0.12, immediateRender: false }, t0 + Math.min(0.9, k * 0.03)));
    for (let i = 0; i < 8; i++) { const fl = sv("text", { x: cx + i * c + c / 2, y: cy + S + 20, "text-anchor": "middle", "font-size": 18, fill: "rgba(148,163,184,.9)", "font-family": "'JetBrains Mono',monospace" }, g);
      fl.textContent = String.fromCharCode(97 + (s.flip ? 7 - i : i));
      const rk = sv("text", { x: cx - 14, y: cy + i * c + c / 2 + 6, "text-anchor": "middle", "font-size": 18, fill: "rgba(148,163,184,.9)", "font-family": "'JetBrains Mono',monospace" }, g);
      rk.textContent = String(s.flip ? i + 1 : 8 - i); }
    if (s.hit) { const [x, y] = sq(s.hit), X = cx + x * c + c / 2, Y = cy + y * c + c / 2, at = Math.max(0, s.hitAt ?? s.t0 + 1);
      const ring = sv("rect", { x: X - c / 2 + 3, y: Y - c / 2 + 3, width: c - 6, height: c - 6, fill: "none", stroke: acc, "stroke-width": 6, rx: 6 }, g);
      tl.fromTo(ring, { opacity: 0, scale: 1.8, svgOrigin: `${X} ${Y}` }, { opacity: 1, scale: 1, duration: 0.35, ease: "power3.out", immediateRender: false }, at);
      if (s.move || s.prob) { const lb = el("div", "golbl", `<b>NƯỚC ${esc(s.move || "")}</b>${s.prob ? `<span>${esc(s.prob)}</span>` : ""}`, d);
        tl.fromTo(lb, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out", immediateRender: false }, at + 0.2); } }
    common(s, d); };

  /* qr      : "giải phẫu" một mã QR (MINH HOẠ, không phải mã thật): ô vuông 25x25, ba ô định vị ở góc, tỷ lệ 1:1:3:1:1,
               vết bẩn ~30%, vạch quét. {modulesAt?, modulesUntil?, hl? (lúc ba góc sáng lên), ratio?: {at}, damage?: {at, okAt?, text?},
               scanAt?, side?: {k, v, at} (nhãn bên phải)}
     barcode : n mã vạch 1 chiều hiện dần (n = 1: một mã lớn + dãy 12 số). {n?, until?, digits?} */
  B.qr = (s, d) => { bg(s, d, 0.85);
    // S = 600, cy = 140: đáy khung trắng (cy + S + 36 = 776) nằm TRÊN dải chú thích "HÌNH MINH HOẠ" (~800 px); bản 700 bị dải ấy đè lên ô góc dưới.
    const N = 25, S = 600, cx = W / 2 - S / 2 - (s.side || s.ratio || s.damage ? 300 : 0), cy = 140, c = S / N;
    const g = sv("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d);
    sv("rect", { x: cx - 36, y: cy - 36, width: S + 72, height: S + 72, rx: 14, fill: "#f8fafc" }, g);
    const inF = (i, j) => (i < 8 && j < 8) || (i >= N - 8 && j < 8) || (i < 8 && j >= N - 8);
    const t0 = s.modulesAt ?? s.t0 + 0.25, span = Math.max(0.3, (s.modulesUntil ?? t0 + 1.2) - t0), mods = [];
    for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) { if (inF(i, j) || rnd() > 0.48) continue;
      mods.push(sv("rect", { x: cx + i * c, y: cy + j * c, width: c + 0.6, height: c + 0.6, fill: "#0a0f18", opacity: 0 }, g)); }
    mods.forEach((m, k) => tl.fromTo(m, { opacity: 0 }, { opacity: 1, duration: 0.06, immediateRender: false }, t0 + span * (k / mods.length)));
    [[0, 0], [N - 7, 0], [0, N - 7]].forEach(([a, b], k) => { const x = cx + a * c, y = cy + b * c, f = sv("g", { opacity: 0 }, g);
      sv("rect", { x, y, width: 7 * c, height: 7 * c, fill: "#0a0f18" }, f); sv("rect", { x: x + c, y: y + c, width: 5 * c, height: 5 * c, fill: "#f8fafc" }, f);
      sv("rect", { x: x + 2 * c, y: y + 2 * c, width: 3 * c, height: 3 * c, fill: "#0a0f18" }, f);
      tl.fromTo(f, { opacity: 0, scale: 1.5, svgOrigin: `${x + 3.5 * c} ${y + 3.5 * c}` }, { opacity: 1, scale: 1, duration: 0.2, ease: "power3.out", immediateRender: false }, s.t0 + 0.12 + k * 0.08);
      if (s.hlAt != null) { const r = sv("rect", { x: x - 10, y: y - 10, width: 7 * c + 20, height: 7 * c + 20, rx: 8, fill: "none", stroke: acc, "stroke-width": 9, opacity: 0 }, g);
        tl.fromTo(r, { opacity: 0, scale: 1.35, svgOrigin: `${x + 3.5 * c} ${y + 3.5 * c}` }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }, s.hlAt + k * 0.18); } });
    const RX = cx + S + 90;
    if (s.ratio) { const y = cy + 3.5 * c, ln = sv("line", { x1: cx - 20, y1: y, x2: cx + 7 * c + 20, y2: y, stroke: "#f59e0b", "stroke-width": 8, opacity: 0 }, g);
      tl.fromTo(ln, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, s.ratio.at);
      const t = sv("text", { x: RX, y: cy + 130, fill: "#e6f1ff", "font-size": 92, "font-weight": 900, "font-family": "Be Vietnam Pro, sans-serif", opacity: 0 }, g); t.textContent = "1 : 1 : 3 : 1 : 1";
      const t2 = sv("text", { x: RX, y: cy + 200, fill: "#f59e0b", "font-size": 36, "font-weight": 700, "font-family": "JetBrains Mono, monospace", opacity: 0 }, g); t2.textContent = "ĐEN : TRẮNG : ĐEN : TRẮNG : ĐEN";
      tl.fromTo([t, t2], { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, s.ratio.at + 0.15); }
    if (s.damage) { const bl = sv("ellipse", { cx: cx + 0.66 * S, cy: cy + 0.66 * S, rx: 0.33 * S, ry: 0.29 * S, fill: "rgba(92,58,26,.94)", opacity: 0, transform: `rotate(-18 ${cx + 0.66 * S} ${cy + 0.66 * S})` }, g);
      tl.fromTo(bl, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, s.damage.at);
      const t = sv("text", { x: RX, y: cy + 250, fill: "#fca5a5", "font-size": 58, "font-weight": 900, "font-family": "Be Vietnam Pro, sans-serif", opacity: 0 }, g); t.textContent = s.damage.text || "BẨN ~30%";
      tl.fromTo(t, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.3, immediateRender: false }, s.damage.at + 0.1);
      if (s.damage.okAt != null) { const ok = sv("text", { x: RX, y: cy + 350, fill: acc, "font-size": 72, "font-weight": 900, "font-family": "Be Vietnam Pro, sans-serif", opacity: 0 }, g); ok.textContent = "✓ VẪN ĐỌC ĐƯỢC";
        tl.fromTo(ok, { opacity: 0, scale: 1.3, svgOrigin: `${RX} ${cy + 330}` }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }, s.damage.okAt); } }
    if (s.scanAt != null) { const sc = sv("rect", { x: cx - 36, y: cy - 36, width: S + 72, height: 14, fill: acc, opacity: 0 }, g);
      tl.fromTo(sc, { opacity: 0.95, y: cy - 36 }, { y: cy + S + 22, duration: 0.55, ease: "power1.inOut", immediateRender: false }, s.scanAt);
      tl.to(sc, { opacity: 0, duration: 0.1 }, s.scanAt + 0.55); }
    if (s.side) { const lb = el("div", "golbl", `<b>${esc(s.side.k || "")}</b>${s.side.v ? `<span>${esc(s.side.v)}</span>` : ""}`, d); lb.style.left = px(RX); lb.style.top = px(cy + 400);
      tl.fromTo(lb, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out", immediateRender: false }, s.side.at); }
    common(s, d); };

  B.barcode = (s, d) => { bg(s, d, 0.85);
    const n = s.n || 1, g = sv("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d), cols = n > 1 ? 5 : 1, rows = Math.ceil(n / cols);
    const bw = n > 1 ? 280 : 980, bh = n > 1 ? 170 : 330, gx = 36, gy = 44, X0 = W / 2 - (cols * bw + (cols - 1) * gx) / 2, Y0 = n > 1 ? 250 : 250;
    const t0 = s.t0 + 0.2, span = Math.max(0.3, (s.until ?? s.t1 - 0.6) - t0);
    for (let k = 0; k < n; k++) { const x = X0 + (k % cols) * (bw + gx), y = Y0 + Math.floor(k / cols) * (bh + gy), f = sv("g", { opacity: 0 }, g);
      sv("rect", { x, y, width: bw, height: bh, rx: 8, fill: "#f8fafc" }, f);
      let px0 = x + bw * 0.06; const end = x + bw * 0.94;
      while (px0 < end) { const w = (1 + Math.floor(rnd() * 3)) * (bw / 190); sv("rect", { x: px0, y: y + bh * 0.1, width: w, height: bh * (n > 1 ? 0.8 : 0.66), fill: "#0a0f18" }, f); px0 += w + (1 + Math.floor(rnd() * 3)) * (bw / 190); }
      if (n === 1) { const t = sv("text", { x: x + bw / 2, y: y + bh * 0.93, fill: "#0a0f18", "font-size": 46, "font-weight": 700, "font-family": "JetBrains Mono, monospace", "text-anchor": "middle" }, f); t.textContent = s.digits || "1 2 3 4 5 6 7 8 9 0 1 2"; }
      tl.fromTo(f, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.22, ease: "power3.out", immediateRender: false }, n > 1 ? t0 + span * (k / n) : t0); }
    common(s, d); };

  /* flap : MINH HOẠ cơ chế "một chạm, lách qua khe" bằng hình khối (không dùng hình ảnh, nhân vật của trò chơi thật):
            một chấm tròn lách qua các cặp thanh chắn trôi từ phải sang; điểm tăng dần; crashAt -> chạm thanh, "HẾT VÁN".
            {crashAt?, speed? (px/giây), label?} */
  B.flap = (s, d) => { bg(s, d, 0.85);
    const PW = 1180, PH = 620, PX = W / 2 - PW / 2, PY = 150, g = sv("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d);
    sv("rect", { x: PX, y: PY, width: PW, height: PH, rx: 16, fill: "rgba(15,27,45,.94)", stroke: "rgba(34,211,238,.35)", "stroke-width": 2 }, g);
    const clip = sv("clipPath", { id: "flapc" + Math.round(s.t0 * 100) }, g); sv("rect", { x: PX, y: PY, width: PW, height: PH, rx: 16 }, clip);
    const strip = sv("g", { "clip-path": `url(#${clip.getAttribute("id")})` }, g), mv = sv("g", {}, strip);
    const t0 = s.t0 + 0.3, end = s.crashAt ?? s.t1 - 0.2, sp = s.speed || 260, bx = PX + 300, gapH = 190, step = 330, bw = 96;
    const n = Math.ceil(((end - t0) * sp + PW) / step) + 1, gaps = [];
    for (let k = 0; k < n; k++) { const x = PX + PW * 0.75 + k * step, gc = PY + 150 + rnd() * (PH - 300); gaps.push({ x, gc });
      sv("rect", { x, y: PY, width: bw, height: gc - gapH / 2 - PY, fill: "#1f6f8b" }, mv); sv("rect", { x, y: gc + gapH / 2, width: bw, height: PY + PH - gc - gapH / 2, fill: "#1f6f8b" }, mv); }
    tl.fromTo(mv, { x: 0 }, { x: -(end - t0) * sp, duration: end - t0, ease: "none", immediateRender: false }, t0);
    const dot = sv("circle", { cx: bx, cy: PY + PH / 2, r: 26, fill: acc }, g), sc = sv("text", { x: PX + PW / 2, y: PY + 100, fill: "#e6f1ff", "font-size": 96, "font-weight": 900, "font-family": "Be Vietnam Pro, sans-serif", "text-anchor": "middle" }, g); sc.textContent = "0";
    let prevT = t0, score = 0;
    gaps.forEach((p, k) => { const tp = t0 + (p.x + bw / 2 - bx) / sp; if (tp > end) { if (s.crashAt != null && prevT < end) { tl.to(dot, { attr: { cy: p.gc - gapH / 2 - 60 }, duration: Math.max(0.1, end - prevT), ease: "sine.inOut" }, prevT); prevT = end; } return; }
      tl.to(dot, { attr: { cy: p.gc }, duration: Math.max(0.12, tp - prevT), ease: "sine.inOut" }, prevT); prevT = tp;
      const v = ++score; tl.set(sc, { textContent: String(v) }, tp); });
    if (s.crashAt != null) { tl.set(dot, { attr: { fill: "#ef4444" } }, s.crashAt);
      const over = sv("text", { x: PX + PW / 2, y: PY + PH / 2 + 30, fill: "#ef4444", "font-size": 120, "font-weight": 900, "font-family": "Be Vietnam Pro, sans-serif", "text-anchor": "middle", opacity: 0 }, g); over.textContent = "HẾT VÁN";
      tl.fromTo(over, { opacity: 0, scale: 1.4, svgOrigin: `${PX + PW / 2} ${PY + PH / 2}` }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in", immediateRender: false }, s.crashAt + 0.05); }
    common(s, d); };

  /* captcha : hình MINH HOẠ một ô mã xác nhận do kênh tự vẽ (không phải giao diện của dịch vụ nào).
       mode "tick" : ô vuông + dòng chữ; tickAt = lúc dấu tick hiện
       mode "text" : hai từ méo (words: [a, b]) + ô gõ đáp án từ typeAt tới until; labels: [nhãn a, nhãn b] hiện ở labelAt
       mode "grid" : lưới 3x3, tiêu đề head; các ô trong pick sáng lần lượt từ selAt */
  B.captcha = (s, d) => { bg(s, d, 0.85);
    const g = sv("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d), mode = s.mode || "tick", F = "Be Vietnam Pro, sans-serif", M = "JetBrains Mono, monospace";
    const card = (x, y, w, h) => sv("rect", { x, y, width: w, height: h, rx: 18, fill: "#f8fafc", stroke: "#cbd5e1", "stroke-width": 3 }, g);
    const txt = (x, y, t, o = {}) => { const e = sv("text", { x, y, fill: "#0f172a", "font-size": 54, "font-weight": 800, "font-family": F, ...o }, g); e.textContent = t; return e; };
    const tickPath = (x, y, k) => sv("path", { d: `M${x} ${y + 30 * k} l${26 * k} ${28 * k} l${52 * k} ${-62 * k}`, fill: "none", stroke: "#16a34a", "stroke-width": 14 * k, "stroke-linecap": "round", "stroke-linejoin": "round", opacity: 0 }, g);
    if (mode === "tick") { const w = 1100, h = 230, x = W / 2 - w / 2, y = s.y ?? 330; card(x, y, w, h);
      sv("rect", { x: x + 60, y: y + 60, width: 110, height: 110, rx: 10, fill: "#fff", stroke: "#475569", "stroke-width": 6 }, g);
      txt(x + 220, y + 135, s.text || "Tôi không phải người máy");
      if (s.tickAt != null) { const t = tickPath(x + 78, y + 82, 1.1); tl.fromTo(t, { opacity: 0, scale: 0.4, svgOrigin: `${x + 115} ${y + 115}` }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)", immediateRender: false }, s.tickAt); } }
    if (mode === "text") { const w = 1240, h = 520, x = W / 2 - w / 2, y = 150; card(x, y, w, h);
      (s.words || ["morning", "upon"]).forEach((wd, k) => { const cx = x + (k ? 860 : 330), cy = y + 190, grp = sv("g", {}, g);
        [...wd].forEach((ch, i) => { const e = sv("text", { x: cx + (i - (wd.length - 1) / 2) * 62, y: cy + Math.sin(i * 1.7 + k) * 22, fill: "#0f172a", "font-size": 104, "font-weight": 700, "font-family": "Georgia, serif", "text-anchor": "middle",
          transform: `rotate(${(rnd() - 0.5) * 34} ${cx + (i - (wd.length - 1) / 2) * 62} ${cy})` }, grp); e.textContent = ch; });
        sv("path", { d: `M${cx - 250} ${cy - 30 + k * 26} q125 ${k ? 70 : -70} 250 0 t250 0`, fill: "none", stroke: "#0f172a", "stroke-width": 5, opacity: 0.75 }, grp);
        if (s.labels && s.labels[k]) { const col = k ? "#f59e0b" : acc, r = sv("rect", { x: cx - 290, y: cy - 130, width: 580, height: 210, rx: 14, fill: "none", stroke: col, "stroke-width": 7, opacity: 0 }, g);
          const lb = sv("text", { x: cx, y: y - 30, fill: col, "font-size": 40, "font-weight": 800, "font-family": M, "text-anchor": "middle", opacity: 0 }, g); lb.textContent = s.labels[k];
          tl.fromTo([r, lb], { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, (s.labelAt ?? s.t0 + 1) + k * (s.labelGap ?? 0.5)); } });
      sv("rect", { x: x + 70, y: y + 350, width: w - 140, height: 110, rx: 10, fill: "#fff", stroke: "#475569", "stroke-width": 5 }, g);
      const ans = (s.words || ["morning", "upon"]).join(" "), a0 = s.typeAt ?? s.t0 + 0.8, a1 = Math.max(a0 + 0.4, s.until ?? a0 + 1.6);
      const inp = txt(x + 100, y + 428, "", { "font-family": M, "font-size": 60, "font-weight": 700 }), o = { n: 0 };
      tl.to(o, { n: ans.length, duration: a1 - a0, ease: "none", onUpdate: () => { inp.textContent = ans.slice(0, Math.round(o.n)); } }, a0); }
    if (mode === "grid") { const c = 160, gp = 14, w = 3 * c + 4 * gp, x = W / 2 - w / 2 - (s.side ? 260 : 0), y = 230;   // đáy thẻ = 786 px, trên dải chú thích (~793) card(x - 20, y - 150, w + 40, 3 * c + 4 * gp + 170);
      sv("rect", { x: x - 20, y: y - 150, width: w + 40, height: 130, rx: 18, fill: "#1d4ed8" }, g); txt(x + 6, y - 72, s.head || "Chọn tất cả ô có đèn giao thông", { fill: "#fff", "font-size": 31 });
      const pick = s.pick || [1, 4, 5], a0 = s.selAt ?? s.t0 + 0.8;
      for (let k = 0; k < 9; k++) { const tx = x + gp + (k % 3) * (c + gp), ty = y + gp + Math.floor(k / 3) * (c + gp), on = pick.includes(k);
        sv("rect", { x: tx, y: ty, width: c, height: c, fill: on ? "#94a3b8" : ["#64748b", "#475569", "#7c8aa0"][k % 3] }, g);
        sv("rect", { x: tx, y: ty + c * 0.72, width: c, height: c * 0.28, fill: "#334155" }, g);
        if (on) { sv("rect", { x: tx + c / 2 - 20, y: ty + 16, width: 40, height: 96, rx: 10, fill: "#0f172a" }, g);
          ["#ef4444", "#f59e0b", "#22c55e"].forEach((col, i) => sv("circle", { cx: tx + c / 2, cy: ty + 35 + i * 29, r: 10, fill: col }, g));
          const i = pick.indexOf(k), r = sv("rect", { x: tx + 5, y: ty + 5, width: c - 10, height: c - 10, fill: "none", stroke: "#2563eb", "stroke-width": 12, opacity: 0 }, g), t = tickPath(tx + c - 58, ty + 10, 0.45);
          tl.fromTo([r, t], { opacity: 0 }, { opacity: 1, duration: 0.15, immediateRender: false }, a0 + i * (s.selGap ?? 0.45)); } } }
    if (s.side) { const lb = el("div", "golbl", `<b>${esc(s.side.k || "")}</b>${s.side.v ? `<span>${esc(s.side.v)}</span>` : ""}`, d); lb.style.left = px(s.side.x ?? W / 2 + 200); lb.style.top = px(s.side.y ?? 420);
      tl.fromTo(lb, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out", immediateRender: false }, s.side.at); }
    common(s, d); };

  /* keyboard : bàn phím chữ do kênh tự vẽ. layout "qwerty" | "abc" (hai hàng theo thứ tự chữ cái) | "dvorak" (chỉ phím chữ).
       hl: chuỗi chữ sáng lần lượt từ hlAt (cách nhau hlGap giây); row: chỉ số hàng được tô từ rowAt; dim: chuỗi chữ làm mờ. */
  B.keyboard = (s, d) => { bg(s, d, 0.85);
    const L = { qwerty: ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"], abc: ["ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"], dvorak: ["PYFGCRL", "AOEUIDHTNS", "QJKXBMWVZ"] }[s.layout || "qwerty"];
    const g = sv("svg", { class: "layer", viewBox: `0 0 ${W} ${H}` }, d), n = Math.max(...L.map((r) => r.length)), K = Math.min(132, Math.floor(1500 / n) - 14), gp = 14;
    const y0 = (s.y ?? 250) + (3 - L.length) * (K + gp) / 2, keys = {};
    L.forEach((row, j) => { const off = (s.layout === "abc" ? 0 : j * K * 0.3) + (s.layout === "dvorak" && j === 0 ? 3 * (K + gp) : 0), x0 = W / 2 - (n * (K + gp) - gp) / 2 + off;
      if (s.row === j) { const r = sv("rect", { x: x0 - 14, y: y0 + j * (K + gp) - 14, width: row.length * (K + gp) - gp + 28, height: K + 28, rx: 20, fill: "none", stroke: "#f59e0b", "stroke-width": 7, opacity: 0 }, g);
        tl.fromTo(r, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, s.rowAt ?? s.t0 + 0.6); }
      [...row].forEach((ch, i) => { const x = x0 + i * (K + gp), y = y0 + j * (K + gp), grp = sv("g", { opacity: 0 }, g);
        const r = sv("rect", { x, y, width: K, height: K, rx: 16, fill: "rgba(15,27,45,.96)", stroke: "rgba(148,163,184,.55)", "stroke-width": 3 }, grp);
        const t = sv("text", { x: x + K / 2, y: y + K * 0.66, fill: (s.dim || "").includes(ch) ? "#475569" : "#e6f1ff", "font-size": K * 0.5, "font-weight": 800, "font-family": "Be Vietnam Pro, sans-serif", "text-anchor": "middle" }, grp); t.textContent = ch;
        tl.fromTo(grp, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.18, ease: "power2.out", immediateRender: false }, s.t0 + 0.1 + (j * n + i) * 0.012);
        keys[ch] = { r, t }; }); });
    [...(s.hl || "")].forEach((ch, i) => { const k = keys[ch]; if (!k) return; const at = (s.hlAt ?? s.t0 + 0.8) + i * (s.hlGap ?? 0.16);
      tl.to(k.r, { attr: { fill: acc, stroke: acc }, duration: 0.08 }, at); tl.to(k.t, { attr: { fill: "#04121c" }, duration: 0.08 }, at); });
    common(s, d); };
};
