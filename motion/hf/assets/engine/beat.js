/* beat.js — thư viện hiệu ứng chữ (beat text) dùng chung cho casewide (Long 16:9) và casefile (Short 9:16).
   Nạp TRƯỚC engine:  const { BEAT, SLAM, beat } = makeBeat({ tl, el, esc, rnd });
   q.fx / s.fx do build_long.assign_beats / stier build.assign_beats chọn (tất định). CSS: beat.css. */
window.makeBeat = ({ tl, el, esc, rnd }) => {
  /* ---------- BEAT: thư viện hiệu ứng chữ (beat text) ----------
     Mỗi dòng chữ (kinetic item / kin phủ) mang q.fx do build_long chọn (tất định, không lặp kiểu liền kề, hợp nội dung):
     pop · rise · blur · slice · drop · marker · redact · stamp · tape · flicker · outline · type · scramble · strike.
     Hàm nhận phần tử .kin đã đặt chữ + vị trí, tự gắn animation vào tl tại q.at. sfx tương ứng ở sfx_long.py. */
  const words = (t) => esc(t).split(" ");
  const inner = (e, cls) => { const s = el("span", "kt" + (cls ? " " + cls : ""), e.innerHTML); e.innerHTML = ""; e.appendChild(s); return s; };
  const GLY = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&$@";
  const BEAT = {
    pop: (e, q) => tl.fromTo(e, { opacity: 0, scale: 1.3, y: -16 }, { opacity: 1, scale: 1, y: 0, duration: 0.2, ease: "power4.in", immediateRender: false }, q.at - 0.08),
    // từng chữ trồi lên từ sau một mép che (kiểu Vox)
    rise: (e, q) => { e.innerHTML = words(q.text).map((w) => `<span class="rw"><span>${w}</span></span>`).join(" ");
      tl.set(e, { opacity: 1 }, q.at - 0.12);
      tl.fromTo(e.querySelectorAll(".rw > span"), { yPercent: 115 }, { yPercent: 0, duration: 0.42, ease: "power3.out", stagger: 0.055, immediateRender: false }, q.at - 0.12); },
    // nhòe + giãn chữ -> nét (tiêu đề điện ảnh)
    blur: (e, q) => tl.fromTo(e, { opacity: 0, filter: "blur(22px)", letterSpacing: "0.35em" }, { opacity: 1, filter: "blur(0px)", letterSpacing: "0em", duration: 0.65, ease: "power3.out", immediateRender: false }, q.at - 0.25),
    // nửa trên lướt từ trái, nửa dưới lướt từ phải, ghép lại
    slice: (e, q) => { const h = e.innerHTML; e.innerHTML = `<span class="sl a">${h}</span><span class="sl b">${h}</span><span class="sl0">${h}</span>`;
      tl.set(e, { opacity: 1 }, q.at - 0.2);
      tl.fromTo(e.querySelector(".sl.a"), { x: -260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.32, ease: "power4.out", immediateRender: false }, q.at - 0.2);
      tl.fromTo(e.querySelector(".sl.b"), { x: 260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.32, ease: "power4.out", immediateRender: false }, q.at - 0.2); },
    // từng chữ rơi xuống, nảy nhẹ
    drop: (e, q) => { e.innerHTML = words(q.text).map((w) => `<span class="dw">${w}</span>`).join(" ");
      tl.set(e, { opacity: 1 }, q.at - 0.15);
      tl.fromTo(e.querySelectorAll(".dw"), { y: -90, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "bounce.out", stagger: 0.07, immediateRender: false }, q.at - 0.15); },
    // bút dạ quang quét phía sau chữ (kiểu Johnny Harris)
    marker: (e, q) => { const s = inner(e, "mk"); tl.fromTo(e, { opacity: 0 }, { opacity: 1, duration: 0.12, immediateRender: false }, q.at - 0.1);
      tl.fromTo(s, { backgroundSize: "0% 78%" }, { backgroundSize: "100% 78%", duration: 0.38, ease: "power2.inOut", immediateRender: false }, q.at); },
    // vạch bôi đen phủ chữ rồi rút đi: hồ sơ được giải mật
    redact: (e, q) => { const s = inner(e, "rd"), bar = el("i", "rdb", null, s); tl.set(e, { opacity: 1 }, q.at - 0.32);
      tl.fromTo(bar, { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.16, ease: "power2.out", immediateRender: false }, q.at - 0.32);
      tl.to(bar, { scaleX: 0, transformOrigin: "100% 50%", duration: 0.3, ease: "power3.inOut" }, q.at); },
    // con dấu đỏ đóng mạnh
    stamp: (e, q) => { const s = inner(e, "stp"), rot = (rnd() - 0.5) * 9; tl.set(e, { opacity: 1 }, q.at - 0.14);
      tl.fromTo(s, { opacity: 0, scale: 2.3, rotation: rot }, { opacity: 1, scale: 1, rotation: rot, duration: 0.15, ease: "power4.in", immediateRender: false }, q.at - 0.14);
      tl.to("#stage", { x: 7, duration: 0.03, yoyo: true, repeat: 3 }, q.at + 0.02); },
    // băng dán vàng kiểu dây phong tỏa hiện trường
    tape: (e, q) => { const s = inner(e, "tp"), rot = -2.5 + rnd() * 1.5; tl.set(e, { opacity: 1 }, q.at - 0.22);
      tl.fromTo(s, { clipPath: "inset(0 100% 0 0)", rotation: rot }, { clipPath: "inset(0 0% 0 0)", rotation: rot, duration: 0.3, ease: "power3.out", immediateRender: false }, q.at - 0.22); },
    // bảng neon chập chờn rồi sáng hẳn
    flicker: (e, q) => { e.classList.add("neo"); const seq = [0, 0.9, 0.1, 0.8, 0, 1, 0.35, 1];
      seq.forEach((o, k) => tl.set(e, { opacity: o }, q.at - 0.2 + k * 0.055)); },
    // viền chữ vẽ ra trước, rồi màu tràn đầy
    outline: (e, q) => { e.classList.add("otl"); const s = inner(e), fill = getComputedStyle(e).color;
      tl.fromTo(e, { opacity: 0, scale: 1.08 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power2.out", immediateRender: false }, q.at - 0.3);
      tl.fromTo(s, { color: "rgba(0,0,0,0)" }, { color: fill, duration: 0.3, ease: "power1.in", immediateRender: false }, q.at + 0.05); },
    // máy đánh chữ + con trỏ nhấp nháy
    type: (e, q) => { e.classList.add("typ"); const chars = [...q.text], n = chars.length, span = Math.min(0.9, 0.045 * n);
      const s = el("span", null, "", null), cur = el("span", "cur", "▌", null); e.innerHTML = ""; e.appendChild(s); e.appendChild(cur);
      tl.set(e, { opacity: 1 }, q.at - 0.05);
      for (let k = 1; k <= n; k++) tl.set(s, { textContent: chars.slice(0, k).join("") }, q.at - 0.05 + span * (k / n));
      for (let k = 0; k < 6; k++) tl.set(cur, { opacity: k % 2 ? 1 : 0 }, q.at + span + 0.25 * k);
      tl.set(cur, { opacity: 0 }, q.at + span + 1.6); },
    // ký tự ngẫu nhiên giải mã dần từ trái sang phải
    scramble: (e, q) => { e.classList.add("scr2"); const chars = [...q.text], n = chars.length, steps = 14;
      tl.set(e, { opacity: 1 }, q.at - 0.35);
      for (let k = 0; k <= steps; k++) { const done = Math.floor(n * k / steps);
        tl.set(e, { textContent: chars.map((c, i) => (i < done || c === " " ? c : GLY[Math.floor(rnd() * GLY.length)])).join("") }, q.at - 0.35 + k * 0.035); } },
    // gạch ngang đè lên chữ (dùng cho "không phải X") — q.strikeAt (mặc định: at + 0.6)
    strike: (e, q) => { const s = inner(e, "stk2"), ln = el("i", "stl", null, s); BEAT.pop(e, q);
      tl.fromTo(ln, { scaleX: 0 }, { scaleX: 1, duration: 0.25, ease: "power2.out", immediateRender: false }, q.strikeAt ?? q.at + 0.6);
      tl.to(s, { opacity: 0.55, duration: 0.25 }, (q.strikeAt ?? q.at + 0.6) + 0.1); },
  };

  /* ---------- SLAM fx: các kiểu đập chữ khác "punch" (mặc định) ----------
     glitch: tách kênh màu, giật hình rồi khớp · slice: 3 dải ngang trượt so le · zoom: từ xa lao tới, nhòe -> nét
     outline: viền chữ hiện trước, màu đổ đầy đúng nhịp. Nếu cú đập đến muộn, chữ hiện mờ trước để khỏi trống màn. */
  const preshow = (sl, s) => { if (s.at - s.t0 > 1.6) tl.fromTo(sl, { opacity: 0 }, { opacity: 0.14, duration: 0.6, immediateRender: false }, s.t0 + 0.2); };
  const SLAM = {
    glitch: (sl, s) => { const h = sl.innerHTML; sl.innerHTML = `<span class="gl r">${h}</span><span class="gl c">${h}</span><span class="gl0">${h}</span>`;
      preshow(sl, s); tl.set(sl, { opacity: 1 }, s.at - 0.05);
      const r = sl.querySelector(".gl.r"), c = sl.querySelector(".gl.c");
      for (let k = 0; k < 9; k++) { const t = s.at - 0.05 + k * 0.04, a = (rnd() - 0.5) * 40, b = (rnd() - 0.5) * 14;
        tl.set(r, { x: a, y: b, opacity: 0.85 }, t); tl.set(c, { x: -a, y: -b, opacity: 0.85 }, t); tl.set(sl, { skewX: (rnd() - 0.5) * 14 }, t); }
      tl.set([r, c], { x: 0, y: 0, opacity: 0 }, s.at + 0.32); tl.set(sl, { skewX: 0 }, s.at + 0.32);
      tl.to("#stage", { x: 10, duration: 0.03, yoyo: true, repeat: 5 }, s.at + 0.05); },
    slice: (sl, s) => { const h = sl.innerHTML; sl.innerHTML = [0, 1, 2].map((k) => `<span class="sx s${k}">${h}</span>`).join("") + `<span class="sx0">${h}</span>`;
      preshow(sl, s); tl.set(sl, { opacity: 1 }, s.at - 0.25);
      sl.querySelectorAll(".sx").forEach((p, k) => tl.fromTo(p, { x: (k % 2 ? 1 : -1) * 900, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: "power4.out", immediateRender: false }, s.at - 0.25 + k * 0.05));
      tl.to("#stage", { x: 8, duration: 0.03, yoyo: true, repeat: 3 }, s.at + 0.08); },
    zoom: (sl, s) => { preshow(sl, s);
      tl.fromTo(sl, { opacity: 0, scale: 0.25, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: "expo.out", immediateRender: false }, s.at - 0.18);
      tl.to(sl, { scale: 1.04, duration: 1.4, ease: "none" }, s.at + 0.14);
      tl.to("#stage", { x: 10, duration: 0.03, yoyo: true, repeat: 5 }, s.at + 0.05); },
    outline: (sl, s) => { sl.classList.add("otl"); const fill = s.white ? "#fff" : getComputedStyle(sl).color; sl.style.color = "rgba(0,0,0,0)"; sl.style.webkitTextStroke = `0.02em ${fill}`;
      tl.fromTo(sl, { opacity: 0, scale: 1.12 }, { opacity: 1, scale: 1, duration: 0.45, ease: "power2.out", immediateRender: false }, Math.max(s.t0 + 0.1, s.at - 0.6));
      tl.to(sl, { color: fill, duration: 0.12, ease: "power4.in" }, s.at - 0.06);
      tl.to("#stage", { x: 8, duration: 0.03, yoyo: true, repeat: 3 }, s.at + 0.06); },
  };

  return { BEAT, SLAM, beat: (e, q) => (BEAT[q.fx] || BEAT.pop)(e, q) };
};
