/* beat2.js — bố cục cảnh chữ + từ nhấn (PM 09/10/2026). Chỉ nạp cho video có spec "beat2": true (build_long chèn thẻ script),
   nạp SAU beat.js và TRƯỚC casewide.js: bọc window.makeBeat, giữ nguyên mọi hiệu ứng, thêm 3 việc sau khi hiệu ứng gắn xong:
     q.L {cls, style}   vị trí/cỡ chữ do motion/beatfx.layout_items tính sẵn (bố cục: hero · split · corner · ladder · frame)
     q.D [{kind, style, at}]  trang trí của cả cảnh (vạch nhấn, thanh dọc, vạch chia đôi, khung ngắm) — đặt trên dòng đầu
     q.em  một từ nhấn: màu nhấn + vạch quét dưới chân chữ
   Không có q.L / q.D / q.em -> y hệt beat.js. Tất định: không Math.random, không Date. */
window.makeBeat = ((orig) => (ctx) => {
  const r = orig(ctx), { tl, el, esc } = ctx;
  const deco = (e, q) => (q.D || []).forEach((g) => {
    const n = el("div", "b2" + g.kind, g.kind === "frame" ? "<i></i><i></i><i></i><i></i>" : null, e.parentNode);
    Object.assign(n.style, g.style || {});
    if (g.kind === "frame") tl.fromTo(n, { scale: 1.25, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "expo.out", immediateRender: false }, g.at);
    else if (g.kind === "rule") tl.fromTo(n, { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power3.out", immediateRender: false }, g.at);
    else tl.fromTo(n, { scaleY: 0 }, { scaleY: 1, duration: g.kind === "split" ? 0.5 : 0.4, ease: "power3.out", immediateRender: false }, g.at);
  });
  const emph = (e, q) => {
    const ws = [...e.querySelectorAll(".rw > span, .dw, .sw")];
    let em = ws.find((w) => w.textContent === q.em), k = ws.indexOf(em);
    if (!em) {
      if (e.querySelector(".sl, .gl, .sx") || e.classList.contains("typ") || e.classList.contains("scr2")) return;   // chữ nhân bản / gõ từng ký tự
      const host = e.querySelector(".kt") || e, h = esc(q.em), i = host.innerHTML.indexOf(h);
      if (i < 0) return;
      host.innerHTML = host.innerHTML.slice(0, i) + `<span class="em">${h}</span>` + host.innerHTML.slice(i + h.length);
      em = host.querySelector(".em");
    }
    em.classList.add("em");
    const t = q.wt && k >= 0 && q.wt[k] != null ? q.wt[k] : q.at;
    tl.fromTo(em, { backgroundSize: "0% .09em" }, { backgroundSize: "100% .09em", duration: 0.3, ease: "power2.out", immediateRender: false }, t + 0.18);
  };
  // chốt chặn tràn chữ: dòng (nowrap) rộng hơn khung của nó -> co cỡ chữ tới khi vừa (tối thiểu 40% cỡ đặt). Đo TRƯỚC hiệu ứng
  // (lúc đó e còn đủ chữ), đo lại khi webfont nạp xong. MIM #7 09/10: "KHÔNG THAY ĐỔI" tràn mép phải.
  const fitTo = (e) => { const f0 = parseFloat(e.style.fontSize || getComputedStyle(e).fontSize); if (!f0) return;
    if (!e.dataset.f0) e.dataset.f0 = f0;
    let f = +e.dataset.f0; e.style.fontSize = f + "px";
    while (e.scrollWidth > e.clientWidth + 2 && f > +e.dataset.f0 * 0.4) { f *= 0.95; e.style.fontSize = f + "px"; } };
  const fitted = [];
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => fitted.forEach(fitTo));
  const beat = (e, q) => {
    if (q.L) { (q.L.cls || "").split(" ").filter(Boolean).forEach((c) => e.classList.add(c)); Object.assign(e.style, q.L.style || {}); }
    if (q.L) { fitTo(e); fitted.push(e); }
    r.beat(e, q);
    if (q.em) emph(e, q);
    if (q.D) deco(e, q);
  };
  return { ...r, beat };
})(window.makeBeat);
