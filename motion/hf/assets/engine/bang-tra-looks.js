/* BẢNG TRA -- 8 "giao diện" (22/10/2026): thay B.table của casefile.js bằng bộ vẽ riêng cho từng look, KHÔNG sửa engine dùng chung.
   Nạp qua spec.extra_css (xem docs/pm/2026-10-22-bang-tra-looks.md). Chỉ có tác dụng khi #root có class "btl-<khoá>".
   Dữ liệu cảnh y hệt B.table: title, rowHead, colHead, cols[], rows[{k,sub?,v[],at?}], hl[{r?,c?,at,until?}], foot, note.
   Tất định: không Math.random / Date / fetch; chỉ tween GSAP trên timeline chung. Mốc row.at / hl.at giữ nguyên để sfx.py khớp.
   Khung cuối: mọi chuyển động nền dừng trước t1-3,0 s (hl cuối tắt -> mọi ô sáng, bảng đứng yên). */
(function () {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const px = (v) => v + "px";
  const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;");
  const fsz = (text, max, width, k) => Math.min(max, Math.floor(width / (Math.max(1, [...String(text)].length) * k)));
  const el = (tag, cls, html, p) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (p) p.appendChild(e); return e; };
  const css = (e, o) => { Object.assign(e.style, o); return e; };
  const sv = (tag, attrs, p) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (p) p.appendChild(e); return e; };
  const num = (v) => { const n = parseFloat(String(v).replace(",", ".")); return /^[\d.,]+$/.test(String(v).trim()) && !isNaN(n) ? n : null; };
  const dpOf = (v) => (String(v).split(",")[1] || "").length;
  const fmt = (n, dp) => n.toFixed(dp).replace(".", ",");
  const lerp = (a, b, t) => a + (b - a) * t;
  const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const mixHex = (stops, p) => { const n = stops.length - 1, x = Math.min(0.9999, Math.max(0, p)) * n, i = Math.floor(x), t = x - i, a = hex(stops[i]), b = hex(stops[i + 1]);
    return "#" + a.map((v, k) => Math.round(lerp(v, b[k], t)).toString(16).padStart(2, "0")).join(""); };
  const lum = (h) => { const [r, g, b] = hex(h); return (0.299 * r + 0.587 * g + 0.114 * b) / 255; };

  function ctx(s, d, tl, C, root) {
    const rows = s.rows, cols = s.cols, nr = rows.length, nc = cols.length;
    const K = { s, d, tl, C, nr, nc, rows, cols, el, css, px, esc, fsz, sv, num, mixHex, lum,
      brand: /theme-ck/.test(root.className) ? "BIỂU ĐỒ BIẾT NÓI" : "MIND IN THE MACHINE",
      still: Math.max(s.t0 + 1, s.t1 - 3.0) };
    K.rowAt = (i) => rows[i].at ?? s.t0 + 0.25 + i * 0.08;
    K.hls = (s.hl || []).map((h, j, a) => ({ ...h, j, end: j + 1 < a.length ? a[j + 1].at : (h.until ?? s.t1 - 0.5), last: j + 1 === a.length }));
    // chia chiều cao: before + nr*RH + after nằm gọn trong [top, bot], căn giữa phần dư (không để nửa dưới trống)
    K.layout = (before, after, top, bot, maxRH = 190, minRH = 96) => {
      const RH = Math.max(minRH, Math.min(maxRH, Math.floor((bot - top - before - after) / nr)));
      const used = before + nr * RH + after;
      return { RH, y0: top + Math.max(0, Math.floor((bot - top - used) / 2)) };
    };
    // số đếm KHÔNG dùng onUpdate (tua/seek có thể bỏ qua callback): xếp chồng vài khung số trung gian, bật/tắt bằng tl.set.
    // Trạng thái mặc định của DOM = số cuối (đúng khi tua thẳng tới cuối).
    K.count = (node, v, at, dur) => { const n = num(v); if (n == null) return; const dp = dpOf(v), P = [0.08, 0.3, 0.55, 0.78, 0.93];
      const fin = node.textContent; node.innerHTML = ""; node.classList.add("cnt");
      const f = el("span", "cf", esc(fin), node), st = P.map((p) => { const e = el("span", "cs", fmt(n * p, dp), node); e.style.opacity = 0; return e; });
      const step = dur / (P.length + 1);
      tl.set(f, { opacity: 0 }, at);
      st.forEach((e, i) => { tl.set(e, { opacity: 1 }, at + i * step); tl.set(e, { opacity: 0 }, at + (i + 1) * step); });
      tl.set(f, { opacity: 1 }, at + P.length * step); };
    // gõ chữ từng ký tự bằng tl.set (tất định)
    K.type = (node, text, at, dur) => { node.innerHTML = ""; const cs = [...text].map((ch) => { const e = el("span", null, esc(ch), node); e.style.opacity = 0; return e; });
      cs.forEach((e, i) => tl.set(e, { opacity: 1 }, at + (i + 1) * dur / cs.length)); return cs; };
    // nhấp nháy bằng chuỗi set: tất định, dừng hẳn (sáng cố định hoặc tắt) khi hết [from, to]
    K.blink = (targets, from, to, endOn, period = 0.5) => {
      for (let k = 0, t = from; t < to - 0.01; k++, t += period) tl.set(targets, { opacity: k % 2 ? 0 : 1 }, t);
      tl.set(targets, { opacity: endOn ? 1 : 0 }, to); };
    K.sel = (h, cells) => h.r != null && h.c != null ? [cells[h.r][h.c]] : h.r != null ? cells[h.r] : cells.map((row) => row[h.c]);
    // hộp bao của hl theo hình học G {X0,W,LW,CW,hdrY,hdrH,rowY(i),RH,pad}
    K.bbox = (h, G) => { const p = G.pad ?? 0;
      if (h.r != null && h.c != null) return { x: G.X0 + G.LW + h.c * G.CW - p, y: G.rowY(h.r) - p, w: G.CW + 2 * p, h: G.RH - (G.gap ?? 8) + 2 * p };
      if (h.r != null) return { x: G.X0 - p, y: G.rowY(h.r) - p, w: G.W + 2 * p, h: G.RH - (G.gap ?? 8) + 2 * p };
      return { x: G.X0 + G.LW + h.c * G.CW - p, y: G.hdrY - p, w: G.CW + 2 * p, h: G.rowY(nr - 1) + G.RH - (G.gap ?? 8) - G.hdrY + 2 * p }; };
    K.dim = (all, getOn, op = 0.28) => K.hls.forEach((h) => { const on = getOn(h);
      tl.to(all.filter((x) => !on.includes(x)), { opacity: op, duration: 0.18 }, h.at);
      tl.to(on, { opacity: 1, duration: 0.12 }, h.at);
      if (h.last) tl.to(all, { opacity: 1, duration: 0.3 }, h.end); });
    // thanh sáng một phần tử di chuyển giữa các hl (đặt vị trí tức thời, tắt khi hl cuối hết)
    K.bar = (bar, G, extra) => K.hls.forEach((h) => { const b = K.bbox(h, G);
      tl.set(bar, { left: b.x, top: b.y, width: b.w, height: b.h, opacity: 1 }, h.at);
      tl.fromTo(bar, { opacity: 0.25 }, { opacity: 1, duration: 0.14, immediateRender: false }, h.at);
      if (extra) extra(h, b);
      if (h.last) tl.to(bar, { opacity: 0, duration: 0.25 }, h.end); });
    return K;
  }

  const L = {};

  /* ============ MIM · mim-crt: terminal CRT phosphor xanh lá, con trỏ quét hàng, đảo màu ô ============ */
  L["mim-crt"] = (K) => {
    const { s, d, tl, el, css, px, esc, fsz } = K, X0 = 54, W = 872, LW = 272, CW = (W - LW) / K.nc, TOP = 240, BOT = 1410, G = "#62ff8e";
    const clip = el("div", "crt-clip", null, d); css(clip, { left: px(40), top: px(TOP), width: px(900), height: px(BOT - TOP) });
    const { RH, y0 } = K.layout(278, 156, TOP + 16, BOT - 10, 190, 100);
    const roll = el("div", "crt-roll", null, clip); css(roll, { height: px(150) });
    const cycles = Math.max(1, Math.floor((K.still - s.t0) / 3.2));
    tl.fromTo(roll, { y: -160 }, { y: BOT - TOP + 10, duration: 3.2, ease: "none", repeat: cycles - 1, immediateRender: true }, s.t0);
    el("div", "crt-scan", null, clip); el("div", "crt-vig", null, clip);
    // tiêu đề = dòng lệnh gõ từng chữ (nằm trên cùng trong màn hình, không băng vàng)
    const full = "> " + s.title, tfs = fsz(full, 104, W - 20, 0.43);
    const ti = el("div", "crt-title", esc(full), d); css(ti, { left: px(X0), top: px(y0), width: px(W), height: px(112), fontSize: px(tfs), lineHeight: px(112) });
    K.type(ti, full, s.t0 + 0.05, 0.65);
    const sep = el("div", "crt-sep", null, d); css(sep, { left: px(X0), top: px(y0 + 114), width: px(W) });
    const ch = el("div", "crt-ch", esc(s.colHead || ""), d); css(ch, { left: px(X0), top: px(y0 + 124), width: px(W), height: px(62), fontSize: px(Math.max(52, fsz(s.colHead || "x", 56, W, 0.42))), lineHeight: px(62) });
    const hdrY = y0 + 190, hdr = el("div", "crt-hdr", null, d); css(hdr, { left: px(X0), top: px(hdrY), width: px(W), height: px(86) });
    const rh = el("div", "crt-rh", esc(s.rowHead || ""), hdr); css(rh, { width: px(LW), fontSize: px(Math.max(56, fsz(s.rowHead || "x", 64, LW - 40, 0.42))) });
    const colEl = K.cols.map((c) => { const e = el("div", "crt-c", esc(c), hdr); css(e, { width: px(CW), fontSize: px(Math.max(60, fsz(c, 76, CW - 12, 0.42))) }); return e; });
    tl.fromTo([sep, ch, hdr], { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, s.t0 + 0.2);
    const rowsTop = y0 + 278, rowY = (i) => rowsTop + i * RH, cells = [], keys = [];
    const hb = el("div", "crt-hb", null, d);
    K.rows.forEach((r, i) => {
      const re = el("div", "crt-row", null, d); css(re, { left: px(X0), top: px(rowY(i)), width: px(W), height: px(RH - 8) });
      const k = el("div", "crt-k", `<b>${esc(r.k)}</b>${r.sub ? `<small>${esc(r.sub)}</small>` : ""}`, re); css(k, { width: px(LW) });
      k.querySelector("b").style.fontSize = px(Math.max(56, fsz(r.k, Math.min(80, RH * 0.6), LW - 50, 0.42)));
      if (r.sub) k.querySelector("small").style.fontSize = px(Math.max(40, Math.min(48, (RH - 8) * 0.36)));
      keys.push(k);
      cells.push(r.v.map((v) => { const c = el("div", "crt-v", esc(v), re); css(c, { width: px(CW), fontSize: px(Math.max(64, fsz(String(v), Math.min(140, RH * 0.82), CW - 24, 0.43))) }); return c; }));
      tl.fromTo(re, { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.24, ease: "steps(14)", immediateRender: true }, K.rowAt(i) - 0.05);
    });
    const cur = el("div", "crt-cur", null, d); css(cur, { left: px(X0 + 6), width: px(26), height: px(Math.round(RH * 0.55)), opacity: 0 });
    const curY = (i) => rowY(i) + Math.round(RH * 0.12);
    for (let i = 0; i < K.nr; i++) tl.set(cur, { top: curY(i) }, K.rowAt(i));
    const lastEnd = K.hls.length ? K.hls[K.hls.length - 1].end : K.still;
    K.hls.forEach((h) => tl.set(cur, { top: h.r != null ? curY(h.r) : hdrY + 14 }, h.at));
    K.blink(cur, K.rowAt(0), lastEnd, false);
    // foot = dòng nhắc lệnh cuối, con trỏ nháy rồi đứng yên
    const footTop = rowsTop + K.nr * RH + 10;
    if (s.foot) { const f = el("div", "crt-foot", "&gt; " + esc(s.foot) + '<i class="crt-blk"></i>', d);
      css(f, { left: px(X0), top: px(footTop), width: px(W), height: px(72), fontSize: px(Math.max(56, fsz("> " + s.foot, 72, W - 60, 0.43))), lineHeight: px(72) });
      const blk = f.querySelector(".crt-blk"); css(blk, { height: px(46) });
      tl.fromTo(f, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, s.footAt ?? s.t0 + 1.2);
      K.blink(blk, lastEnd, K.still, true); tl.set(blk, { opacity: 0 }, 0); }
    if (s.note) { const n = el("div", "crt-note", esc(s.note), d); css(n, { left: px(X0), top: px(footTop + 78), width: px(W), fontSize: px(52) }); tl.to(n, { opacity: 1, duration: 0.3 }, s.t0 + 1.2); }
    const Gm = { X0, W, LW, CW, hdrY, rowY, RH, pad: 0, gap: 8 };
    K.bar(hb, Gm, (h, b) => { if (h.r != null && h.c != null) { const cell = cells[h.r][h.c];
      tl.to(cell, { backgroundColor: G, color: "#02140a", textShadow: "none", duration: 0.06 }, h.at);
      tl.to(cell, { backgroundColor: "rgba(0,0,0,0)", color: G, duration: 0.15 }, h.end); } });
    K.dim(cells.flat(), (h) => K.sel(h, cells), 0.3);
  };

  /* ============ MIM · mim-blueprint: bản vẽ xanh đậm, nét trắng vẽ dần, khung tên ở dưới, khoanh cyan ============ */
  L["mim-blueprint"] = (K) => {
    const { s, d, tl, el, css, px, esc, fsz, sv } = K, X0 = 46, W = 880, LW = 300, CW = (W - LW) / K.nc, TOP = 240, BOT = 1410, CY = "#67e8f9";
    const HH = 96, TB = 296, NH = 84, DIM = 70;
    const { RH, y0 } = K.layout(DIM + HH, 30 + TB + NH, TOP + 8, BOT, 180, 100);
    const dimY = y0 + 30, hdrY = y0 + DIM, rowsTop = hdrY + HH, rowY = (i) => rowsTop + i * RH, tabY = rowsTop + K.nr * RH, tbY = tabY + 30;
    const svg = sv("svg", { width: 1080, height: 1920, viewBox: "0 0 1080 1920", class: "bp-svg" }, d);
    const lines = [];
    const ln = (x1, y1, x2, y2, w = 2.5, a = 0.9) => { const e = sv("line", { x1, y1, x2, y2, stroke: "#fff", "stroke-width": w, "stroke-opacity": a, "stroke-linecap": "square" }, svg); lines.push(e); return e; };
    // đường kích thước (dimension line) = nhãn colHead, hai đầu có mũi tên + vạch gióng
    ln(X0, dimY, X0 + W, dimY, 2.5, 0.95);
    [[X0, 1], [X0 + W, -1]].forEach(([x, sg]) => { ln(x, dimY - 24, x, dimY + 44, 2.5, 0.95); ln(x, dimY, x + sg * 34, dimY - 13, 3, 1); ln(x, dimY, x + sg * 34, dimY + 13, 3, 1); });
    // khung bảng
    const tbH = HH + K.nr * RH;
    ln(X0, hdrY, X0 + W, hdrY, 4); ln(X0, hdrY + tbH, X0 + W, hdrY + tbH, 4); ln(X0, hdrY, X0, hdrY + tbH, 4); ln(X0 + W, hdrY, X0 + W, hdrY + tbH, 4);
    ln(X0, rowsTop, X0 + W, rowsTop, 4.5, 1);
    for (let i = 1; i < K.nr; i++) ln(X0, rowY(i), X0 + W, rowY(i), 2, 0.55);
    for (let k = 0; k < K.nc; k++) ln(X0 + LW + k * CW, hdrY, X0 + LW + k * CW, hdrY + tbH, k ? 2 : 4, k ? 0.55 : 1);
    // dấu góc (crosshair) ở 4 góc bảng
    [[X0, hdrY], [X0 + W, hdrY], [X0, hdrY + tbH], [X0 + W, hdrY + tbH]].forEach(([x, y]) => { ln(x - 14, y, x + 14, y, 2, 0.8); ln(x, y - 14, x, y + 14, 2, 0.8); });
    // khung tên
    ln(X0, tbY, X0 + W, tbY, 4.5, 1); ln(X0, tbY + TB, X0 + W, tbY + TB, 4.5, 1); ln(X0, tbY, X0, tbY + TB, 4.5, 1); ln(X0 + W, tbY, X0 + W, tbY + TB, 4.5, 1);
    const sx = X0 + Math.round(W * 0.66); ln(sx, tbY, sx, tbY + TB - 82, 3, 0.9); ln(X0, tbY + TB - 82, X0 + W, tbY + TB - 82, 3, 0.9);
    lines.forEach((e, i) => { const len = e.getTotalLength(); e.style.strokeDasharray = len; e.style.strokeDashoffset = len;
      tl.to(e, { strokeDashoffset: 0, duration: 0.45, ease: "power2.out" }, s.t0 + 0.04 + (i % 14) * 0.025); });
    const dl = el("div", "bp-dim", esc(s.colHead || ""), d); css(dl, { left: px(X0 + 60), width: px(W - 120), top: px(dimY - 24), height: px(48), fontSize: px(Math.max(36, fsz(s.colHead || "x", 42, W - 200, 0.6))), lineHeight: px(48) });
    const hdr = el("div", "bp-hdr", null, d); css(hdr, { left: px(X0), top: px(hdrY), width: px(W), height: px(HH - 4) });
    const rh = el("div", "bp-rh", esc(s.rowHead || ""), hdr); css(rh, { width: px(LW), fontSize: px(Math.max(36, fsz(s.rowHead || "x", 44, LW - 30, 0.9))) });
    const colEl = K.cols.map((c) => { const e = el("div", "bp-c", esc(c), hdr); css(e, { width: px(CW), fontSize: px(Math.max(40, fsz(c, 56, CW - 14, 0.6))) }); return e; });
    tl.fromTo([dl, hdr], { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, s.t0 + 0.3);
    const cells = [], keys = [];
    K.rows.forEach((r, i) => {
      const re = el("div", "bp-row", null, d); css(re, { left: px(X0), top: px(rowY(i)), width: px(W), height: px(RH) });
      const k = el("div", "bp-k", `<b>${esc(r.k)}</b>${r.sub ? `<small>${esc(r.sub)}</small>` : ""}`, re); css(k, { width: px(LW) });
      k.querySelector("b").style.fontSize = px(Math.max(40, fsz(r.k, Math.min(54, RH * 0.42), LW - 40, 0.74)));
      if (r.sub) k.querySelector("small").style.fontSize = px(36);
      keys.push(k);
      cells.push(r.v.map((v) => { const c = el("div", "bp-v", esc(v), re); css(c, { width: px(CW), fontSize: px(Math.max(64, fsz(String(v), Math.min(100, RH * 0.66), CW - 24, 0.6))) }); return c; }));
      tl.fromTo(re, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.28, ease: "power3.out", immediateRender: false }, K.rowAt(i) - 0.05);
    });
    // khung tên: tiêu đề (trái), thương hiệu (phải), dải dưới = foot
    const tb = el("div", "bp-tb", null, d); css(tb, { left: px(X0), top: px(tbY), width: px(W), height: px(TB) });
    const tl1 = el("div", "bp-tbl", `<small>TIÊU ĐỀ BẢN VẼ</small><b>${esc(s.title || "")}</b>`, tb); css(tl1, { width: px(sx - X0), height: px(TB - 82) });
    tl1.querySelector("b").style.fontSize = px(Math.max(44, Math.min(60, fsz(s.title || "x", 60, (sx - X0 - 44) * 1.85, 0.64))));
    const tr1 = el("div", "bp-tbr", `<small>KÊNH</small><b>${esc(K.brand)}</b>`, tb); css(tr1, { left: px(sx - X0), width: px(X0 + W - sx), height: px(TB - 82) });
    const ft = el("div", "bp-tbf", esc(s.foot || ""), tb); css(ft, { top: px(TB - 82), height: px(82), width: px(W), fontSize: px(Math.max(40, fsz(s.foot || "x", 48, W - 40, 0.62))) });
    tl.fromTo(tb, { opacity: 0 }, { opacity: 1, duration: 0.35, immediateRender: false }, s.t0 + 0.35);
    if (s.note) { const n = el("div", "bp-note", esc(s.note), d); css(n, { left: px(X0), width: px(W), top: px(tbY + TB + 14), fontSize: px(36) }); tl.to(n, { opacity: 1, duration: 0.3 }, s.t0 + 1.0); }
    // khoanh cyan vẽ dần quanh ô / hàng / cột đang tra
    const Gm = { X0, W, LW, CW, hdrY, rowY, RH, pad: 7, gap: 0 };
    K.hls.forEach((h) => { const b = K.bbox(h, Gm);
      const rc = sv("rect", { x: b.x, y: b.y, width: b.w, height: b.h, rx: 18, fill: "rgba(103,232,249,.13)", "stroke": CY, "stroke-width": 7 }, svg);
      const len = rc.getTotalLength(); rc.style.strokeDasharray = len; rc.style.strokeDashoffset = len; rc.style.opacity = 0; rc.style.filter = "drop-shadow(0 0 10px rgba(103,232,249,.9))";
      tl.set(rc, { opacity: 1 }, h.at);
      tl.to(rc, { strokeDashoffset: 0, duration: 0.3, ease: "power2.out" }, h.at);
      tl.to(rc, { opacity: 0, duration: 0.22 }, h.end);
      const on = K.sel(h, cells);
      tl.to(on, { color: CY, duration: 0.12 }, h.at); tl.to(on, { color: "#ffffff", duration: 0.2 }, h.end);
      if (on.length === 1) { tl.fromTo(on, { scale: 1 }, { scale: 1.12, duration: 0.22, ease: "back.out(2)", immediateRender: false }, h.at); tl.to(on, { scale: 1, duration: 0.2 }, h.end); } });
    K.dim(cells.flat(), (h) => K.sel(h, cells), 0.4);
  };

  /* ============ MIM · mim-thermal: giấy in nhiệt kem, chữ đơn cách đen, "in" từng dòng từ khe cyan, đảo đen ô ============ */
  L["mim-thermal"] = (K) => {
    const { s, d, tl, el, css, px, esc, fsz } = K, X0 = 40, W = 900, PAD = 28, IW = W - 2 * PAD, LW = 232, CW = (IW - LW) / K.nc, TOP = 262, BOT = 1410, INK = "#1c2127", PAPER = "#f6f1df";
    const HDR = 70, BR = 44, TT = 82, SEP = 26, CH = 56, FT = 62, BC = 72, NT = 112;
    const before = 22 + BR + SEP + TT + SEP + CH + HDR + SEP, after = SEP + FT + BC + NT + 24;
    const { RH, y0 } = K.layout(before, after, TOP, BOT, 170, 92);
    const H = before + K.nr * RH + after;
    const slot = el("div", "th-slot", null, d); css(slot, { left: px(40), top: px(y0 - 26), width: px(900), height: px(30) });
    const paper = el("div", "th-paper", null, d); css(paper, { left: px(X0), top: px(y0), width: px(W), height: px(H) });
    const teeth = 38, tw = W / teeth, pts = [];
    for (let i = 0; i <= teeth; i++) pts.push(`${(i * tw).toFixed(1)}px ${i % 2 ? 0 : 12}px`);
    for (let i = teeth; i >= 0; i--) pts.push(`${(i * tw).toFixed(1)}px ${H - (i % 2 ? 0 : 12)}px`);
    paper.style.clipPath = `polygon(${pts.join(",")})`;
    const P = (cls, html, top, h, extra) => { const e = el("div", cls, html, paper); css(e, Object.assign({ left: px(PAD), width: px(IW), top: px(top), height: px(h) }, extra || {})); return e; };
    let y = 22;
    const br = P("th-brand", "✦ " + esc(K.brand) + " ✦", y, BR, { fontSize: px(36), lineHeight: px(BR) }); y += BR;
    P("th-dash", "", y + SEP / 2, 0); y += SEP;
    const tt = P("th-title", esc(s.title || ""), y, TT, { fontSize: px(Math.max(48, fsz(s.title || "x", 66, IW, 0.62))), lineHeight: px(TT) }); y += TT;
    P("th-dash", "", y + SEP / 2, 0); y += SEP;
    P("th-ch", esc(s.colHead || ""), y, CH, { fontSize: px(Math.max(36, fsz(s.colHead || "x", 40, IW, 0.6))), lineHeight: px(CH) }); y += CH;
    const hdr = P("th-hdr", "", y, HDR); const rh = el("div", "th-rh", esc(s.rowHead || ""), hdr); css(rh, { width: px(LW), fontSize: px(Math.max(36, fsz(s.rowHead || "x", 42, LW - 8, 0.62))) });
    const colEl = K.cols.map((c) => { const e = el("div", "th-c", esc(c), hdr); css(e, { width: px(CW), fontSize: px(Math.max(38, fsz(c, 52, CW - 10, 0.62))) }); return e; }); y += HDR;
    P("th-dash th-dbl", "", y + SEP / 2, 0); y += SEP;
    const rowsTop = y, rowY = (i) => rowsTop + i * RH, cells = [], keys = [], absY = (v) => y0 + v;
    const hbars = K.hls.map(() => { const b = el("div", "th-hb", null, paper); return b; });
    K.rows.forEach((r, i) => {
      const re = P("th-row", "", rowY(i), RH - 4); if (i < K.nr - 1) re.style.borderBottom = "3px dashed rgba(28,33,39,.35)";
      const k = el("div", "th-k", `<b>${esc(r.k)}</b>${r.sub ? `<small>${esc(r.sub)}</small>` : ""}`, re); css(k, { width: px(LW) });
      k.querySelector("b").style.fontSize = px(Math.max(40, fsz(r.k, Math.min(50, RH * 0.42), LW - 10, 0.62)));
      if (r.sub) k.querySelector("small").style.fontSize = px(36);
      keys.push(k);
      cells.push(r.v.map((v) => { const c = el("div", "th-v", esc(v), re); css(c, { width: px(CW), fontSize: px(Math.max(60, fsz(String(v), Math.min(92, RH * 0.66), CW - 14, 0.62))) }); return c; }));
      tl.fromTo(re, { clipPath: "inset(0 0 100% 0)", y: -18 }, { clipPath: "inset(0 0 0% 0)", y: 0, duration: 0.2, ease: "none", immediateRender: true }, K.rowAt(i) - 0.05);
    });
    y = rowsTop + K.nr * RH;
    P("th-dash", "", y + SEP / 2, 0); y += SEP;
    const ft = P("th-foot", s.foot ? "*** " + esc(s.foot) + " ***" : "", y, FT, { fontSize: px(Math.max(36, fsz("*** " + (s.foot || "x") + " ***", 44, IW, 0.74))), lineHeight: px(FT) }); y += FT;
    const bc = P("th-bc", "", y + 6, BC - 12);
    let sd = 11; for (let i = 0; i < 64; i++) { sd = (sd * 1103515245 + 12345) % 2147483648; el("i", null, null, bc).style.width = px(2 + (sd >> 8) % 7); }
    y += BC; const nt = P("th-note", esc(s.note || ""), y + 4, NT - 24, { fontSize: px(36) });
    // khe in: giấy trượt ra từ khe, đèn cyan; paper hiện dần từ trên xuống
    tl.fromTo(paper, { clipPath: paper.style.clipPath }, { duration: 0.01, immediateRender: false }, 0);
    tl.fromTo(slot, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, s.t0);
    tl.fromTo([br, tt], { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, s.t0 + 0.05);
    tl.fromTo(hdr, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, s.t0 + 0.2);
    paper.querySelectorAll(".th-dash,.th-ch,.th-foot,.th-bc,.th-note").forEach((e, i) => tl.fromTo(e, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, s.t0 + 0.15 + i * 0.04));
    // đảo đen: thanh đen quét từ trái sang, chữ trong vùng đổi kem; kèm mũi tên khi là cả hàng
    const Gm = { X0: PAD, W: IW, LW, CW, hdrY: rowsTop - SEP - HDR, rowY, RH, pad: 0, gap: 4 };
    K.hls.forEach((h, j) => { const b = K.bbox(h, Gm), bar = hbars[j];
      css(bar, { left: px(b.x), top: px(b.y), width: px(b.w), height: px(b.h) });
      tl.fromTo(bar, { scaleX: 0, opacity: 1 }, { scaleX: 1, duration: 0.26, ease: "power2.out", immediateRender: true }, h.at);
      tl.to(bar, { opacity: 0, duration: 0.2 }, h.end);
      const on = K.sel(h, cells); tl.to(on, { color: PAPER, duration: 0.1 }, h.at + 0.08); tl.to(on, { color: INK, duration: 0.2 }, h.end);
      if (h.r != null && h.c == null) { tl.to(keys[h.r], { color: PAPER, duration: 0.1 }, h.at + 0.08); tl.to(keys[h.r], { color: INK, duration: 0.2 }, h.end); } });
    K.dim(cells.flat(), (h) => K.sel(h, cells), 0.32);
  };

  /* ============ MIM · mim-heat: bảng nhiệt neon, ô đổi màu lạnh->nóng theo giá trị từng cột, sóng chéo ============ */
  L["mim-heat"] = (K) => {
    const { s, d, tl, el, css, px, esc, fsz, num, mixHex, lum } = K, X0 = 46, W = 880, LW = 304, CW = (W - LW) / K.nc, TOP = 240, BOT = 1410, GAP = 12;
    const STOPS = ["#4f46e5", "#0ea5e9", "#34d399", "#fbbf24", "#f43f5e"];
    const TT = 150, CH = 56, HH = 84, LG = 150;
    const { RH, y0 } = K.layout(TT + CH + HH + 10, LG + 70, TOP, BOT, 188, 98);
    const tfs = Math.max(56, fsz(s.title || "x", 96, W, 0.64));
    const tt = el("div", "ht-title", esc(s.title || ""), d); css(tt, { left: px(X0), top: px(y0), width: px(W), height: px(TT), fontSize: px(tfs), lineHeight: px(TT) });
    const ch = el("div", "ht-ch", esc(s.colHead || ""), d); css(ch, { left: px(X0), top: px(y0 + TT), width: px(W), height: px(CH), fontSize: px(Math.max(36, fsz(s.colHead || "x", 40, W, 0.62))), lineHeight: px(CH) });
    const hdrY = y0 + TT + CH + 6, hdr = el("div", "ht-hdr", null, d); css(hdr, { left: px(X0), top: px(hdrY), width: px(W), height: px(HH) });
    const rh = el("div", "ht-rh", esc(s.rowHead || ""), hdr); css(rh, { width: px(LW), fontSize: px(Math.max(36, fsz(s.rowHead || "x", 42, LW - 14, 0.8))) });
    K.cols.forEach((c) => { const e = el("div", "ht-c", esc(c), hdr); css(e, { width: px(CW), fontSize: px(Math.max(40, fsz(c, 54, CW - 10, 0.64))) }); });
    tl.fromTo([tt, ch, hdr], { opacity: 0, y: -22 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, s.t0 + 0.05);
    const rowsTop = hdrY + HH + 4, rowY = (i) => rowsTop + i * RH;
    const colMin = [], colMax = [];
    for (let c = 0; c < K.nc; c++) { const v = K.rows.map((r) => num(r.v[c])).filter((x) => x != null); colMin[c] = Math.min(...v); colMax[c] = Math.max(...v); }
    const cells = [], keys = [], COLD = "#16234a";
    K.rows.forEach((r, i) => {
      const k = el("div", "ht-k", `<b>${esc(r.k)}</b>${r.sub ? `<small>${esc(r.sub)}</small>` : ""}`, d); css(k, { left: px(X0), top: px(rowY(i)), width: px(LW), height: px(RH - GAP) });
      k.querySelector("b").style.fontSize = px(Math.max(38, fsz(r.k, Math.min(52, RH * 0.42), LW - 18, 0.8)));
      if (r.sub) k.querySelector("small").style.fontSize = px(36);
      keys.push(k); tl.fromTo(k, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.26, ease: "power3.out", immediateRender: false }, K.rowAt(i) - 0.05);
      cells.push(r.v.map((v, c) => {
        const n = num(v), p = n == null ? null : colMax[c] === colMin[c] ? 0.5 : (n - colMin[c]) / (colMax[c] - colMin[c]);
        const col = p == null ? "#27324d" : mixHex(STOPS, p), tx = lum(col) > 0.5 ? "#06101c" : "#ffffff";
        const e = el("div", "ht-v", esc(v), d); css(e, { left: px(X0 + LW + c * CW + GAP / 2), top: px(rowY(i)), width: px(CW - GAP), height: px(RH - GAP), fontSize: px(Math.max(64, fsz(String(v), Math.min(100, RH * 0.66), CW - GAP - 16, 0.64))), backgroundColor: col, color: tx });
        e.dataset.col = col;
        const at = K.rowAt(i) + c * 0.05;
        tl.fromTo(e, { opacity: 0, scale: 0.55, backgroundColor: COLD, color: "#7f93ad" }, { opacity: 1, scale: 1, backgroundColor: col, color: tx, duration: 0.42, ease: "back.out(1.5)", immediateRender: false }, at - 0.05);
        return e; }));
    });
    // chú giải lạnh -> nóng
    const lgY = rowsTop + K.nr * RH + 18, lg = el("div", "ht-leg", null, d); css(lg, { left: px(X0), top: px(lgY), width: px(W), height: px(LG) });
    lg.innerHTML = `<div class="ht-bar" style="background:linear-gradient(90deg,${STOPS.join(",")})"></div><div class="ht-lab"><span>ÍT</span><span>THEO TỪNG CỘT</span><span>NHIỀU</span></div>`;
    if (s.foot) { const f = el("div", "ht-foot", esc(s.foot), lg); css(f, { fontSize: px(Math.max(40, fsz(s.foot, 48, W, 0.64))) }); }
    tl.fromTo(lg, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, s.footAt ?? s.t0 + 1.0);
    if (s.note) { const n = el("div", "ht-note", esc(s.note), d); css(n, { left: px(X0), width: px(W), top: px(lgY + LG + 8), fontSize: px(36) }); tl.to(n, { opacity: 1, duration: 0.3 }, s.t0 + 1.2); }
    // sáng trắng + phồng ô; hàng/cột thì cả dải sáng viền
    K.hls.forEach((h) => { const on = K.sel(h, cells), single = on.length === 1;
      tl.to(on, { boxShadow: "0 0 0 6px #ffffff, 0 0 46px 12px rgba(255,255,255,.55)", zIndex: 5, duration: 0.14 }, h.at);
      tl.fromTo(on, { scale: 1 }, { scale: single ? 1.08 : 1.03, duration: 0.2, ease: "back.out(2)", immediateRender: false }, h.at);
      tl.to(on, { boxShadow: "0 0 0 0px rgba(255,255,255,0), 0 0 0px 0px rgba(255,255,255,0)", zIndex: 1, scale: 1, duration: 0.2 }, h.end);
      if (h.r != null) { tl.to(keys[h.r], { color: "#22d3ee", duration: 0.12 }, h.at); tl.to(keys[h.r], { color: "#e6f1ff", duration: 0.2 }, h.end); } });
    K.dim(cells.flat(), (h) => K.sel(h, cells), 0.3);
  };

  /* ============ CK · ck-led: bảng điện tử LED hổ phách, số lật đếm lên, ô nháy trắng-nóng, dải chạy dưới ============ */
  L["ck-led"] = (K) => {
    const { s, d, tl, el, css, px, esc, fsz } = K, X0 = 54, W = 872, LW = 200, CW = (W - LW) / K.nc, TOP = 240, BOT = 1410, AM = "#ffb000";
    const board = el("div", "led-board", null, d); css(board, { left: px(40), top: px(TOP), width: px(900), height: px(BOT - TOP) });
    const TT = 150, CH = 56, HH = 84, TK = 80, NT = 70;
    const { RH, y0 } = K.layout(TT + CH + HH + 16, TK + NT + 40, TOP + 18, BOT - 18, 176, 98);
    const tb = el("div", "led-tt", `<span>${esc(s.title || "")}</span>`, d); css(tb, { left: px(X0), top: px(y0), width: px(W), height: px(TT - 14) });
    tb.firstChild.style.fontSize = px(Math.max(56, fsz(s.title || "x", 92, W - 60, 0.5)));
    const ch = el("div", "led-ch", esc(s.colHead || ""), d); css(ch, { left: px(X0), top: px(y0 + TT), width: px(W), height: px(CH), fontSize: px(Math.max(40, fsz(s.colHead || "x", 46, W, 0.5))), lineHeight: px(CH) });
    const hdrY = y0 + TT + CH + 6, hdr = el("div", "led-hdr", null, d); css(hdr, { left: px(X0), top: px(hdrY), width: px(W), height: px(HH) });
    const rh = el("div", "led-rh", esc(s.rowHead || ""), hdr); css(rh, { width: px(LW), fontSize: px(Math.max(40, fsz(s.rowHead || "x", 52, LW - 14, 0.5))) });
    K.cols.forEach((c) => { const e = el("div", "led-c", esc(c), hdr); css(e, { width: px(CW), fontSize: px(Math.max(48, fsz(c, 66, CW - 10, 0.5))) }); });
    tl.fromTo([tb], { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "steps(18)", immediateRender: true }, s.t0 + 0.05);
    tl.fromTo([ch, hdr], { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, s.t0 + 0.25);
    const rowsTop = hdrY + HH + 8, rowY = (i) => rowsTop + i * RH, cells = [], keys = [];
    const hb = el("div", "led-hb", null, d);
    K.rows.forEach((r, i) => {
      const re = el("div", "led-row" + (i % 2 ? " odd" : ""), null, d); css(re, { left: px(X0), top: px(rowY(i)), width: px(W), height: px(RH - 8) });
      const k = el("div", "led-k", `<b>${esc(r.k)}</b>${r.sub ? `<small>${esc(r.sub)}</small>` : ""}`, re); css(k, { width: px(LW) });
      k.querySelector("b").style.fontSize = px(Math.max(44, fsz(r.k, Math.min(76, RH * 0.55), LW - 20, 0.5)));
      if (r.sub) k.querySelector("small").style.fontSize = px(38);
      keys.push(k);
      cells.push(r.v.map((v, c) => { const e = el("div", "led-v", esc(v), re); css(e, { width: px(CW), fontSize: px(Math.max(64, fsz(String(v), Math.min(118, RH * 0.82), CW - 16, 0.6))) });
        K.count(e, v, K.rowAt(i) + c * 0.06, 0.7); return e; }));
      // lật như bảng cơ khí: gập từ trục trên xuống
      tl.fromTo(re, { opacity: 0, rotationX: -88, transformPerspective: 900, transformOrigin: "50% 0%" }, { opacity: 1, rotationX: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, K.rowAt(i) - 0.05);
    });
    const tkY = rowsTop + K.nr * RH + 8, tk = el("div", "led-tick", null, d); css(tk, { left: px(X0), top: px(tkY), width: px(W), height: px(TK) });
    const txt = (s.foot || "") ? `<span>${esc(s.foot)}</span>` : "";
    const run = el("div", "led-run", txt, tk); css(run, { fontSize: px(Math.max(44, Math.min(56, fsz(s.foot || "x", 56, W, 0.5)))), lineHeight: px(TK - 10) });
    tl.fromTo(tk, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, s.footAt ?? s.t0 + 1.0);
    // dải chữ chạy từ phải vào, rồi DỪNG ở mép trái (khung cuối đứng yên)
    const T1 = Math.max(s.t0 + 1.4, K.still - 0.3);
    css(run, { left: px(0), width: px(W) }); tl.fromTo(run, { x: W }, { x: 0, duration: Math.max(0.5, T1 - (s.t0 + 1.0)), ease: "power1.out", immediateRender: true }, s.t0 + 1.0);
    if (s.note) { const n = el("div", "led-note", esc(s.note), d); css(n, { left: px(X0), width: px(W), top: px(tkY + TK + 6), fontSize: px(38) }); tl.to(n, { opacity: 1, duration: 0.3 }, s.t0 + 1.2); }
    const Gm = { X0, W, LW, CW, hdrY, rowY, RH, pad: 0, gap: 8 };
    K.bar(hb, Gm, (h) => { const on = K.sel(h, cells);
      tl.to(on, { color: "#fff3cf", textShadow: "0 0 26px #ffb000, 0 0 60px rgba(255,176,0,.9)", duration: 0.08 }, h.at);
      for (let k = 0; k < 3; k++) { tl.set(on, { opacity: 0.25 }, h.at + 0.1 + k * 0.16); tl.set(on, { opacity: 1 }, h.at + 0.18 + k * 0.16); }
      tl.to(on, { color: AM, textShadow: "0 0 14px rgba(255,176,0,.75)", duration: 0.2 }, h.end); });
    K.dim(cells.flat(), (h) => K.sel(h, cells), 0.3);
  };

  /* ============ CK · ck-ledger: sổ kế toán kem, bút highlight vàng quét, số viết tay, tem vàng dưới ============ */
  L["ck-ledger"] = (K) => {
    const { s, d, tl, el, css, px, esc, fsz } = K, X0 = 54, W = 872, LW = 230, CW = (W - LW) / K.nc, TOP = 240, BOT = 1410, INK = "#1d3a8a", NAVY = "#14213d";
    const sheet = el("div", "lg-sheet", null, d); css(sheet, { left: px(40), top: px(TOP), width: px(900), height: px(BOT - TOP) });
    const TT = 160, HH = 92, FT = 108, NT = 62;
    const { RH, y0 } = K.layout(TT + 58 + HH + 14, FT + NT + 22, TOP + 22, BOT - 18, 204, 100);
    el("div", "lg-margin", null, d).style.cssText = `left:${X0 + LW - 8}px;top:${TOP}px;height:${BOT - TOP}px`;
    const tt = el("div", "lg-title", `<span>${esc(s.title || "")}</span>`, d); css(tt, { left: px(X0), top: px(y0), width: px(W), height: px(TT - 20) });
    tt.firstChild.style.fontSize = px(Math.max(48, fsz(s.title || "x", 76, W - 10, 0.62)));
    const ul = el("div", "lg-ul", null, d); css(ul, { left: px(X0), top: px(y0 + TT - 14), width: px(W) });
    const hdrY = y0 + TT + 62, hdr = el("div", "lg-hdr", null, d); css(hdr, { left: px(X0), top: px(hdrY), width: px(W), height: px(HH - 6) });
    const rh = el("div", "lg-rh", esc(s.rowHead || ""), hdr); css(rh, { width: px(LW), fontSize: px(Math.max(36, fsz(s.rowHead || "x", 44, LW - 16, 0.62))) });
    K.cols.forEach((c) => { const e = el("div", "lg-c", esc(c), hdr); css(e, { width: px(CW), fontSize: px(Math.max(48, fsz(c, 68, CW - 10, 0.62))) }); });
    if (s.colHead) { const ch = el("div", "lg-ch", esc(s.colHead), d); css(ch, { left: px(X0), width: px(W), top: px(y0 + TT + 2), height: px(52), lineHeight: px(52), fontSize: px(Math.max(36, fsz(s.colHead, 40, W, 0.6))) }); tl.fromTo(ch, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, s.t0 + 0.3); }
    tl.fromTo(tt, { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.55, ease: "power1.inOut", immediateRender: true }, s.t0 + 0.05);
    tl.fromTo(ul, { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.out", immediateRender: true }, s.t0 + 0.4);
    tl.fromTo(hdr, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, s.t0 + 0.2);
    const rowsTop = hdrY + HH, rowY = (i) => rowsTop + i * RH, cells = [], keys = [];
    const hbs = K.hls.map(() => el("div", "lg-hl", null, d)), pen = el("div", "lg-pen", null, d);
    K.rows.forEach((r, i) => {
      const re = el("div", "lg-row", null, d); css(re, { left: px(X0), top: px(rowY(i)), width: px(W), height: px(RH - 8) });
      const k = el("div", "lg-k", `<b>${esc(r.k)}</b>${r.sub ? `<small>${esc(r.sub)}</small>` : ""}`, re); css(k, { width: px(LW) });
      k.querySelector("b").style.fontSize = px(Math.max(48, fsz(r.k, Math.min(78, RH * 0.56), LW - 30, 0.5)));
      if (r.sub) k.querySelector("small").style.fontSize = px(38);
      keys.push(k);
      cells.push(r.v.map((v) => { const c = el("div", "lg-v", esc(v), re); css(c, { width: px(CW), fontSize: px(Math.max(64, fsz(String(v), Math.min(122, RH * 0.8), CW - 20, 0.46))) }); return c; }));
      tl.fromTo(re, { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.34, ease: "power1.inOut", immediateRender: true }, K.rowAt(i) - 0.05);
    });
    const ftY = rowsTop + K.nr * RH + 8;
    if (s.foot) { const f = el("div", "lg-stamp", esc(s.foot), d); css(f, { left: px(X0 + 20), width: px(W - 40), top: px(ftY + 6), height: px(FT - 28), fontSize: px(Math.max(44, fsz(s.foot, 56, W - 100, 0.66))), lineHeight: px(FT - 28) });
      tl.fromTo(f, { opacity: 0, scale: 1.6, rotation: -6 }, { opacity: 1, scale: 1, rotation: -1.6, duration: 0.2, ease: "power4.in", immediateRender: true }, s.footAt ?? s.t0 + 1.2); }
    if (s.note) { const n = el("div", "lg-note", esc(s.note), d); css(n, { left: px(X0), width: px(W), top: px(ftY + FT), fontSize: px(42) }); tl.to(n, { opacity: 1, duration: 0.3 }, s.t0 + 1.2); }
    // bút highlight quét: vệt vàng mở dần từ trái, đầu bút chạy theo mép
    const Gm = { X0, W, LW, CW, hdrY, rowY, RH, pad: 6, gap: 8 };
    K.hls.forEach((h, j) => { const b = K.bbox(h, Gm), bar = hbs[j], dur = h.r != null && h.c == null ? 0.55 : 0.36;
      css(bar, { left: px(b.x), top: px(b.y), width: px(b.w), height: px(b.h) });
      tl.fromTo(bar, { scaleX: 0, opacity: 1 }, { scaleX: 1, duration: dur, ease: "power1.inOut", immediateRender: true }, h.at);
      tl.fromTo(pen, { left: b.x, top: b.y + b.h * 0.5 - 14, opacity: 1 }, { left: b.x + b.w - 6, duration: dur, ease: "power1.inOut", immediateRender: false }, h.at);
      tl.to(bar, { opacity: 0, duration: 0.25 }, h.end);
      if (h.last) tl.to(pen, { opacity: 0, duration: 0.2 }, Math.min(h.end, h.at + dur + 0.05)); });
    tl.set(pen, { opacity: 0 }, 0.001);
    K.hls.forEach((h) => { tl.to(K.sel(h, cells), { color: "#0b2a7a", duration: 0.1 }, h.at + 0.1); tl.to(K.sel(h, cells), { color: INK, duration: 0.2 }, h.end); });
    K.dim(cells.flat(), (h) => K.sel(h, cells), 0.38);
  };

  /* ============ CK · ck-graph: giấy kẻ ô đồ thị xanh đêm, nến mờ, thước đo bên trái, kính lúp vàng chạy theo ô ============ */
  L["ck-graph"] = (K) => {
    const { s, d, tl, el, css, px, esc, fsz, sv } = K, X0 = 48, W = 860, LW = 216, CW = (W - LW) / K.nc, TOP = 240, BOT = 1410, GD = "#fbbf24";
    // nến mờ phía sau (chuỗi tất định)
    const bg = sv("svg", { width: 1080, height: 1920, viewBox: "0 0 1080 1920", class: "gr-bg" }, d);
    let sd = 7, close = 700; const nC = 22, cw = 860 / nC;
    for (let i = 0; i < nC; i++) { sd = (sd * 1103515245 + 12345) % 2147483648; const mv = ((sd >> 10) % 200) - 85, open = close; close = Math.max(420, Math.min(1180, close + mv));
      const hi = Math.min(open, close) - 24 - ((sd >> 6) % 50), lo = Math.max(open, close) + 24 + ((sd >> 4) % 50), up = close < open, x = X0 + i * cw + cw / 2, col = up ? "#fbbf24" : "#cbd5e1";
      sv("line", { x1: x, x2: x, y1: hi, y2: lo, stroke: col, "stroke-width": 3, "stroke-opacity": 0.26 }, bg);
      sv("rect", { x: x - 12, y: Math.min(open, close), width: 24, height: Math.max(8, Math.abs(close - open)), fill: col, "fill-opacity": 0.22 }, bg); }
    // thước đo dọc bên trái
    const rl = sv("svg", { width: 1080, height: 1920, viewBox: "0 0 1080 1920", class: "gr-bg" }, d);
    sv("rect", { x: 4, y: TOP, width: 34, height: BOT - TOP, rx: 6, fill: "rgba(251,191,36,.14)", stroke: "rgba(251,191,36,.55)", "stroke-width": 2 }, rl);
    for (let y = TOP + 12, k = 0; y < BOT - 6; y += 15, k++) sv("line", { x1: 38, x2: 38 - (k % 5 === 0 ? 24 : 12), y1: y, y2: y, stroke: "rgba(253,230,138,.8)", "stroke-width": k % 5 === 0 ? 3 : 2 }, rl);
    const TT = 150, CH = 60, HH = 84, FT = 84, NT = 66;
    const { RH, y0 } = K.layout(TT + CH + HH + 12, FT + NT + 24, TOP + 8, BOT - 8, 178, 98);
    const tt = el("div", "gr-title", esc(s.title || ""), d); css(tt, { left: px(X0), top: px(y0), width: px(W), height: px(TT), fontSize: px(Math.max(56, fsz(s.title || "x", 90, W, 0.5))), lineHeight: px(TT) });
    const ch = el("div", "gr-ch", esc(s.colHead || ""), d); css(ch, { left: px(X0), top: px(y0 + TT - 6), width: px(W), height: px(CH), fontSize: px(Math.max(36, fsz(s.colHead || "x", 42, W, 0.5))), lineHeight: px(CH) });
    const hdrY = y0 + TT + CH + 4, hdr = el("div", "gr-hdr", null, d); css(hdr, { left: px(X0), top: px(hdrY), width: px(W), height: px(HH) });
    const rh = el("div", "gr-rh", esc(s.rowHead || ""), hdr); css(rh, { width: px(LW), fontSize: px(Math.max(38, fsz(s.rowHead || "x", 46, LW - 14, 0.5))) });
    K.cols.forEach((c) => { const e = el("div", "gr-c", esc(c), hdr); css(e, { width: px(CW), fontSize: px(Math.max(48, fsz(c, 64, CW - 10, 0.5))) }); });
    tl.fromTo([tt, ch, hdr], { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out", immediateRender: false }, s.t0 + 0.05);
    const rowsTop = hdrY + HH + 6, rowY = (i) => rowsTop + i * RH, cells = [], keys = [];
    K.rows.forEach((r, i) => {
      const re = el("div", "gr-row", null, d); css(re, { left: px(X0), top: px(rowY(i)), width: px(W), height: px(RH - 8) });
      const k = el("div", "gr-k", `<b>${esc(r.k)}</b>${r.sub ? `<small>${esc(r.sub)}</small>` : ""}`, re); css(k, { width: px(LW - 8) });
      k.querySelector("b").style.fontSize = px(Math.max(44, fsz(r.k, Math.min(72, RH * 0.52), LW - 30, 0.5)));
      if (r.sub) k.querySelector("small").style.fontSize = px(38);
      keys.push(k);
      cells.push(r.v.map((v) => { const c = el("div", "gr-v", esc(v), re); css(c, { width: px(CW - 8), fontSize: px(Math.max(64, fsz(String(v), Math.min(112, RH * 0.78), CW - 30, 0.5))) }); return c; }));
      tl.fromTo(re, { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, K.rowAt(i) - 0.05);
    });
    const ftY = rowsTop + K.nr * RH + 6;
    if (s.foot) { const f = el("div", "gr-foot", "▼ " + esc(s.foot) + " ▼", d); css(f, { left: px(X0), width: px(W), top: px(ftY), height: px(FT), fontSize: px(Math.max(40, fsz("▼ " + s.foot + " ▼", 52, W, 0.64))), lineHeight: px(FT) }); tl.fromTo(f, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.3, immediateRender: false }, s.footAt ?? s.t0 + 1.2); }
    if (s.note) { const n = el("div", "gr-note", esc(s.note), d); css(n, { left: px(X0), width: px(W), top: px(ftY + FT), fontSize: px(38) }); tl.to(n, { opacity: 1, duration: 0.3 }, s.t0 + 1.2); }
    // kính lúp: vòng vàng kính mờ, trượt từ hl này sang hl kế; tay cầm khi tra một ô
    const lens = el("div", "gr-lens", '<i class="gr-handle"></i>', d), handle = lens.firstChild;
    const Gm = { X0, W, LW, CW, hdrY, rowY, RH, pad: 10, gap: 8 };
    K.hls.forEach((h, j) => { const b = K.bbox(h, Gm), single = h.r != null && h.c != null, set = { left: b.x, top: b.y, width: b.w, height: b.h };
      if (j === 0) { tl.set(lens, { ...set, opacity: 1 }, h.at); tl.fromTo(lens, { scale: 1.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.25, ease: "power3.out", immediateRender: false }, h.at); }
      else tl.to(lens, { ...set, duration: 0.3, ease: "power2.inOut" }, h.at);
      tl.set(handle, { opacity: single ? 1 : 0 }, h.at);
      const on = K.sel(h, cells);
      tl.fromTo(on, { scale: 1 }, { scale: single ? 1.18 : 1.06, duration: 0.25, ease: "back.out(2)", immediateRender: false }, h.at + 0.1);
      tl.to(on, { scale: 1, duration: 0.2 }, h.end);
      tl.to(on, { color: "#fde68a", duration: 0.12 }, h.at + 0.1); tl.to(on, { color: "#ffffff", duration: 0.2 }, h.end);
      if (h.last) tl.to(lens, { opacity: 0, duration: 0.25 }, h.end); });
    tl.set(lens, { opacity: 0 }, 0.001);
    K.dim(cells.flat(), (h) => K.sel(h, cells), 0.33);
  };

  /* ============ CK · ck-bars: mỗi ô có thanh nhiệt kế mini theo giá trị, số đếm lên, tiêu đề hai dòng canh trái ============ */
  L["ck-bars"] = (K) => {
    const { s, d, tl, el, css, px, esc, fsz, num } = K, X0 = 46, W = 880, LW = 200, CW = (W - LW) / K.nc, TOP = 240, BOT = 1410, GAP = 12;
    const TT = 196, CH = 56, HH = 84, FT = 80, NT = 66;
    const { RH, y0 } = K.layout(TT + CH + HH + 8, FT + NT + 20, TOP, BOT, 188, 104);
    // tiêu đề hai dòng canh trái: dòng đầu trắng, dòng sau vàng
    const words = String(s.title || "").split(" "); let a = [], bestI = Math.floor(words.length / 2), best = 1e9;
    for (let i = 1; i < words.length; i++) { const x = words.slice(0, i).join(" ").length, y = words.slice(i).join(" ").length; if (Math.abs(x - y) < best) { best = Math.abs(x - y); bestI = i; } }
    const l1 = words.slice(0, bestI).join(" "), l2 = words.slice(bestI).join(" ");
    const tt = el("div", "br-title", `<span>${esc(l1)}</span><span class="g">${esc(l2)}</span>`, d); css(tt, { left: px(X0), top: px(y0), width: px(W), height: px(TT) });
    tt.style.fontSize = px(Math.max(56, fsz(l1.length > l2.length ? l1 : l2, 92, W, 0.7)));
    const ch = el("div", "br-ch", esc(s.colHead || ""), d); css(ch, { left: px(X0), top: px(y0 + TT), width: px(W), height: px(CH), fontSize: px(Math.max(36, fsz(s.colHead || "x", 40, W, 0.62))), lineHeight: px(CH) });
    const hdrY = y0 + TT + CH + 4, hdr = el("div", "br-hdr", null, d); css(hdr, { left: px(X0), top: px(hdrY), width: px(W), height: px(HH) });
    const rh = el("div", "br-rh", esc(s.rowHead || ""), hdr); css(rh, { width: px(LW), fontSize: px(Math.max(36, fsz(s.rowHead || "x", 42, LW - 10, 0.64))) });
    K.cols.forEach((c) => { const e = el("div", "br-c", `<span>${esc(c)}</span>`, hdr); css(e, { width: px(CW) }); e.firstChild.style.fontSize = px(Math.max(44, fsz(c, 56, CW - 40, 0.64))); });
    tl.fromTo([tt, ch, hdr], { opacity: 0, y: -22 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, s.t0 + 0.05);
    const rowsTop = hdrY + HH + 4, rowY = (i) => rowsTop + i * RH, cells = [], keys = [], fills = [];
    let gmax = 0; K.rows.forEach((r) => r.v.forEach((v) => { const n = num(v); if (n != null && n > gmax) gmax = n; }));
    K.rows.forEach((r, i) => {
      const k = el("div", "br-k", `<b>${esc(r.k)}</b>${r.sub ? `<small>${esc(r.sub)}</small>` : ""}`, d); css(k, { left: px(X0), top: px(rowY(i)), width: px(LW), height: px(RH - GAP) });
      k.querySelector("b").style.fontSize = px(Math.max(44, fsz(r.k, Math.min(64, RH * 0.46), LW - 20, 0.64)));
      if (r.sub) k.querySelector("small").style.fontSize = px(36);
      keys.push(k); tl.fromTo(k, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.26, ease: "power3.out", immediateRender: false }, K.rowAt(i) - 0.05);
      const nh = Math.max(64, Math.min(104, RH * 0.56)), bh = 26;
      cells.push(r.v.map((v, c) => { const n = num(v), pct = n == null ? 0 : n / gmax;
        const e = el("div", "br-cell", `<div class="br-n" style="font-size:${px(Math.max(64, fsz(String(v), nh, CW - GAP - 20, 0.64)))}">${esc(v)}</div><div class="br-tr"><i class="br-fill"></i></div>`, d);
        css(e, { left: px(X0 + LW + c * CW + GAP / 2), top: px(rowY(i)), width: px(CW - GAP), height: px(RH - GAP) });
        const fill = e.querySelector(".br-fill"), nn = e.querySelector(".br-n"); fills.push(fill);
        const at = K.rowAt(i) + c * 0.06;
        tl.fromTo(e, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, at - 0.05);
        tl.fromTo(fill, { width: "0%" }, { width: (pct * 100).toFixed(1) + "%", duration: 0.8, ease: "power2.out", immediateRender: true }, at);
        K.count(nn, v, at, 0.8); e.style.setProperty("--bh", px(bh)); return e; }));
    });
    const ftY = rowsTop + K.nr * RH + 4;
    if (s.foot) { const f = el("div", "br-foot", esc(s.foot), d); css(f, { left: px(X0), width: px(W), top: px(ftY), height: px(FT), fontSize: px(Math.max(40, fsz(s.foot, 50, W, 0.64))), lineHeight: px(FT) }); tl.fromTo(f, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.3, immediateRender: false }, s.footAt ?? s.t0 + 1.2); }
    if (s.note) { const n = el("div", "br-note", esc(s.note), d); css(n, { left: px(X0), width: px(W), top: px(ftY + FT), fontSize: px(36) }); tl.to(n, { opacity: 1, duration: 0.3 }, s.t0 + 1.2); }
    K.hls.forEach((h) => { const on = K.sel(h, cells), single = on.length === 1;
      tl.to(on, { borderColor: "#fde68a", backgroundColor: "rgba(251,191,36,.22)", boxShadow: "0 0 36px rgba(251,191,36,.55)", duration: 0.14 }, h.at);
      tl.fromTo(on, { scale: 1 }, { scale: single ? 1.06 : 1.03, duration: 0.2, ease: "back.out(2)", immediateRender: false }, h.at);
      tl.to(on, { borderColor: "rgba(251,191,36,.28)", backgroundColor: "rgba(255,255,255,.06)", boxShadow: "0 0 0px rgba(251,191,36,0)", scale: 1, duration: 0.2 }, h.end);
      if (h.r != null) { tl.to(keys[h.r], { color: "#fde68a", duration: 0.12 }, h.at); tl.to(keys[h.r], { color: "#fbbf24", duration: 0.2 }, h.end); } });
    K.dim(cells.flat(), (h) => K.sel(h, cells), 0.32);
  };

  window.HFS = { mount(tl, C, B) {
    const root = document.getElementById("root"), m = (root.className.match(/\bbtl-([a-z-]+)/) || [])[1];
    if (!m || !L[m]) return;
    B.table = (s, d) => L[m](ctx(s, d, tl, C, root));
  } };
})();
