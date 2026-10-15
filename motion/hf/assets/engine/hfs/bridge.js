/* HFS bridge (BUD v2, 14/10/2026): chạy thiết bị Shorts Studio (motion/hf/assets/engine/hfs/*.js, chép từ feat/shorts-studio
 * engine 1.0) bên trong casefile.js -- CHỈ khi composition nạp file này (build.py chỉ nạp cho theme bud có cảnh hf_*).
 * Thiết bị đăng ký qua HFS.device(name, def); casefile.js gọi HFS.mount(tl, C) -> B["hf_" + name] cho từng thiết bị. */
window.HFS = (function () {
  "use strict";
  const DEV = {}, NS = "http://www.w3.org/2000/svg";
  const device = (name, def) => { DEV[name] = def;
    if (def.css) { const st = document.createElement("style"); st.textContent = def.css; document.head.appendChild(st); } };
  const el = (tag, cls, html, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (parent) parent.appendChild(e); return e; };
  const sv = (tag, a, parent) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); if (parent) parent.appendChild(e); return e; };
  function hash(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function rng(key) { let a = hash(String(key)) || 1; return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const nfc = (s) => String(s).normalize("NFC");
  const esc = (s) => nfc(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
  function tokens(text) { const out = []; let hot = false;
    nfc(text).split(/\s+/).filter(Boolean).forEach((tok) => { let t = tok; if (t.startsWith("**")) { hot = true; t = t.slice(2); }
      const end = t.endsWith("**") || /\*\*[.,:;!?]$/.test(t); t = t.replace(/\*\*/g, ""); out.push({ w: t, hot }); if (end) hot = false; });
    return out; }

  function mount(tl, C, B) {
    const root = document.getElementById("root"), probe = el("div", "hfs", null, root), cs = getComputedStyle(probe);
    const tok = (n, d) => (cs.getPropertyValue("--" + n).trim() || d);
    const T = { ground: tok("ground", "#ECE6D8"), ground2: tok("ground2", "#E1D9C6"), ink: tok("ink", "#1B2566"), soft: tok("ink-soft", "#3A4380"),
                accent: tok("accent", "#B5651D"), accent2: tok("accent2", "#7A2E1E"), glow: tok("glow", "#E09F3E"), mute: tok("mute", "#8A7F72"),
                on2: tok("on-accent2", "#F4EFE3"), line: tok("line", "rgba(27,37,102,.18)") };
    root.removeChild(probe);
    // chuyển động "saffron": êm, không nảy, chậm 1,25x
    const M = { entry: "power3.out", exit: "power2.in", move: "sine.inOut", calm: "sine.inOut", draw: "sine.inOut", accent: "power3.out", speed: 1.25, overshoot: 0, blur: 8 };
    const S = (d) => d * M.speed;
    const E = { entry: M.entry, exit: M.exit, move: M.move, calm: M.calm, draw: M.draw, pop: () => M.entry };
    const fail = (code, d) => { console.error("HFS", code, d); throw new Error("HFS " + code + " " + JSON.stringify(d)); };
    const ctx = { tl, T, E, S, M, el, sv, tokens, esc, rng, dur: C.dur, lines: C.lines, fail,
      t: (x, def) => (typeof x === "number" ? x : (def != null ? def : (fail("anchor", x), 0))),
      words(box, text, { mask = false } = {}) {
        return tokens(text).map((x, i) => { if (i) box.appendChild(document.createTextNode(" "));
          const wd = el("span", "wd" + (mask ? " mask" : ""), null, box), inn = el("span", "in" + (x.hot ? " hot" : ""), null, wd);
          inn.textContent = x.w; return { wd, inn, w: x.w }; }); },
      waterfall(items, times, { y = 46, axis = "y" } = {}) {
        items.forEach((it, i) => { const last = i === items.length - 1, d = S(last ? .2 : .15), off = last ? y * 1.5 : y, t = Math.max(0, times[i]);
          tl.set(it.inn, { opacity: 0 }, 0); tl.set(it.inn, { opacity: 1 }, t);
          tl.fromTo(it.inn, { [axis]: off }, { [axis]: 0, duration: d, ease: "power4.out", immediateRender: false }, t); }); },
      spread: (t0, t1, n) => Array.from({ length: n }, (_, i) => t0 + (t1 - t0) * (n > 1 ? i / (n - 1) : 0)),
      reveal(node, t, { y = 30, x = 0, d = .3, ease } = {}) { t = Math.max(0, t);
        tl.set(node, { autoAlpha: 0 }, 0); tl.set(node, { autoAlpha: 1 }, t);
        tl.fromTo(node, { x, y }, { x: 0, y: 0, duration: S(d), ease: ease || E.entry, immediateRender: false }, t); },
      underline(node, t, { cls = "u-line", d = .5 } = {}) { const u = el("span", cls, null, node); tl.set(u, { scaleX: 0 }, 0);
        tl.to(u, { scaleX: 1, duration: S(d), ease: E.draw }, Math.max(0, t)); return u; },
      draw(path, t, d = .5, ease) { const len = path.getTotalLength ? (path.getTotalLength() || 800) : 800;
        path.setAttribute("stroke-dasharray", len); tl.set(path, { attr: { "stroke-dashoffset": len }, autoAlpha: 1 }, 0);
        tl.to(path, { attr: { "stroke-dashoffset": 0 }, duration: S(d), ease: ease || E.draw }, Math.max(0, t)); },
      stamp(node, t, rot = -6) { t = Math.max(0, t); tl.set(node, { autoAlpha: 0 }, 0); tl.set(node, { autoAlpha: 1 }, t);
        tl.fromTo(node, { scale: 1.7, rotation: rot - 6 }, { scale: 1, rotation: rot, duration: .28, ease: "power4.out", immediateRender: false }, t); },
      burst(parent, cx, cy, t, key, n = 12) { const r = rng(key);
        for (let k = 0; k < n; k++) { const d = el("i", "dot", null, parent); d.style.left = cx + "px"; d.style.top = cy + "px";
          const a = (k / n) * Math.PI * 2 + r() * .4, R = 90 + r() * 90; tl.set(d, { autoAlpha: 0 }, 0);
          tl.fromTo(d, { x: 0, y: 0, autoAlpha: 1, scale: 1 }, { x: Math.cos(a) * R, y: Math.sin(a) * R, autoAlpha: 0, scale: .4, duration: .55, ease: "power3.out", immediateRender: false }, Math.max(0, t)); } },
      count(node, from, to, t, d = 1.2, fmt) { const st = { v: from }; const f = fmt || ((v) => String(Math.round(v)));
        node.textContent = f(from); tl.fromTo(st, { v: from }, { v: to, duration: S(d), ease: "power3.out", immediateRender: false, onUpdate: () => (node.textContent = f(st.v)) }, Math.max(0, t)); },
    };
    Object.keys(DEV).forEach((name) => {
      B["hf_" + name] = (s, d) => {
        const sec = el("div", "hfs hfs-" + name, null, d), stage = el("div", "stage", null, sec);
        tl.fromTo(sec, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: S(.4), ease: E.entry, immediateRender: false }, s.t0);
        const h = DEV[name].build(ctx, s, stage, 0) || {};
        if (DEV[name].enter) DEV[name].enter(ctx, h, s.t0, s);
      };
    });
  }
  return { device, mount, hash, rng, defs: DEV };
})();
