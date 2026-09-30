/* Engine dùng chung cho mọi style "cinematic" của kênh Hình Sự.
 *
 * Mỗi style chỉ cần khai báo window.HF_STYLE = { buildScene, transition,
 * ambient } rồi gọi HF.build(). Engine lo phần bất biến giữa các style:
 * đọc biến, dựng scene theo từng câu narration, dựng phụ đề karaoke theo
 * timing THẬT của TTS, gắn audio, đăng ký timeline.
 *
 * Ràng buộc bất biến (xem hyperframes-core/determinism-rules):
 *  - mọi trạng thái hình ảnh phải suy ra được từ thời gian -> không
 *    Date.now/Math.random (dùng PRNG có seed), không repeat:-1.
 *  - scene KHÔNG phải .clip: composition nhiều cảnh có transition thì
 *    GSAP tự quản opacity, framework không được tranh quyền ẩn/hiện.
 *  - luôn fromTo (không from) để trạng thái đầu là tường minh.
 */
window.HF = (function () {
  function rng(seed) {                     // mulberry32 -- ngẫu nhiên nhưng tất định
    let a = seed >>> 0;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function el(tag, cls, txt) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt != null) e.textContent = txt;
    return e;
  }

  function hexA(hex, a) {
    const h = (hex || "#e5484d").replace("#", "");
    const n = parseInt(h.length === 3 ? h.split("").map(c => c + c).join("") : h, 16);
    return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
  }


  /* ---- Đồ hoạ thông tin -------------------------------------------------
   * Nhận SEMANTIC figure theo hf_figure_schema.json ({type, data, ...}) và tự
   * quyết định toàn bộ hình học + chữ định dạng (ADR-0001). Python không tính
   * sẵn gì cả.
   *
   * ADR-0002: ở đây CHỈ được sinh chữ thuần định dạng từ số (2000000 ->
   * "2 TRIỆU"). Mọi nhãn mang khẳng định pháp lý phải đến từ `labels` — chữ
   * người viết đặt tay trong plan. Không bao giờ tự chế ra mệnh đề pháp lý.
   */
  const THRESHOLD_SPLIT = 42;          // % chiều ngang — lựa chọn bố cục, không phải dữ liệu

  function viNumber(n) {
    const rounded = Math.round(n * 10) / 10;
    return Number.isInteger(rounded) ? String(rounded) : String(rounded).replace(".", ",");
  }

  function formatQuantity(value, unit) {
    const u = (unit || "").toLowerCase();
    if (u === "đồng") {
      if (value >= 1e9) return viNumber(value / 1e9) + " TỶ";
      if (value >= 1e6) return viNumber(value / 1e6) + " TRIỆU";
      if (value >= 1e3) return viNumber(value / 1e3) + " NGHÌN";
      return viNumber(value) + " ĐỒNG";
    }
    return viNumber(value) + " " + (unit || "").toUpperCase();
  }

  function buildFigure(fig, labels) {
    const L = labels || {};
    const d = fig.data || {};
    const box = el("div", "fig fig-" + fig.type);

    if (fig.type === "threshold") {
      const q = formatQuantity(d.value, d.unit);
      const at = THRESHOLD_SPLIT + "%";
      const axis = el("div", "axis");
      const lo = el("div", "lo"), hi = el("div", "hi"), mark = el("div", "mark"), pin = el("div", "pin", q);
      lo.style.width = at; hi.style.left = at; mark.style.left = at; pin.style.left = at;
      axis.appendChild(lo); axis.appendChild(hi); axis.appendChild(mark); axis.appendChild(pin);
      box.appendChild(axis);
      const labelRow = el("div", "labels");
      labelRow.appendChild(el("div", "l", L.left || ("Dưới " + q.toLowerCase())));
      labelRow.appendChild(el("div", "r", L.right || ((d.direction === "above" ? "Trên " : "Từ ") + q.toLowerCase())));
      box.appendChild(labelRow);
      if (L.note) box.appendChild(el("div", "note", L.note));

    } else if (fig.type === "range") {
      const a = formatQuantity(d.from.value, d.from.unit);
      const b = formatQuantity(d.to.value, d.to.unit);
      const rail = el("div", "rail");
      rail.appendChild(el("div", "bar"));
      rail.appendChild(el("div", "edge start", a));
      rail.appendChild(el("div", "edge stop", b));
      box.appendChild(rail);
      if (L.note) box.appendChild(el("div", "note", L.note));

    } else if (fig.type === "flow") {
      (d.steps || []).forEach((st, i) => {
        if (i) box.appendChild(el("div", "arrow", "→"));
        const cls = "step" + (st.terminal ? " end" : "") + (st.text.length > 34 ? " long" : "");
        box.appendChild(el("div", cls, st.text));
      });

    } else if (fig.type === "timeline") {
      const points = (d.points || []).slice().sort((a, b) => a.year - b.year);
      const rail = el("div", "rail");
      const line = el("div", "line");
      rail.appendChild(line);
      const span = Math.max(1, points.length - 1);
      points.forEach((pt, i) => {
        const tick = el("div", "tick");
        tick.style.left = (span ? (i / span) * 100 : 50) + "%";
        tick.appendChild(el("div", "dot"));
        tick.appendChild(el("div", "year", String(pt.year)));
        if (pt.text) tick.appendChild(el("div", "what", pt.text));
        rail.appendChild(tick);
      });
      box.appendChild(rail);
      if (L.note) box.appendChild(el("div", "note", L.note));

    } else if (fig.type === "stat") {
      const big = el("div", "big");
      big.dataset.target = String(d.value);
      big.dataset.unit = d.unit || "";
      big.textContent = formatQuantity(0, d.unit);
      box.appendChild(big);
      if (d.of != null) {
        const track = el("div", "track");
        const fill = el("div", "fill");
        fill.style.width = Math.max(0, Math.min(100, (d.value / d.of) * 100)) + "%";
        track.appendChild(fill);
        box.appendChild(track);
      }
      if (L.note) box.appendChild(el("div", "note", L.note));
    }
    return box;
  }

  function animateFigure(tl, box, fig, at) {
    tl.fromTo(box, { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: .42, ease: "power3.out" }, at);

    if (fig.type === "threshold") {
      tl.fromTo(box.querySelector(".lo"), { scaleX: 0 }, { scaleX: 1, duration: .5, ease: "power2.out" }, at + .1);
      tl.fromTo(box.querySelector(".hi"), { scaleX: 0 }, { scaleX: 1, duration: .6, ease: "power3.out" }, at + .34);
      tl.fromTo(box.querySelector(".mark"), { scaleY: 0 }, { scaleY: 1, duration: .34, ease: "back.out(2)" }, at + .5);
      tl.fromTo(box.querySelector(".pin"), { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .34 }, at + .58);
      tl.fromTo(box.querySelectorAll(".labels div"), { opacity: 0 }, { opacity: 1, duration: .34, stagger: .1 }, at + .66);

    } else if (fig.type === "range") {
      tl.fromTo(box.querySelector(".bar"), { scaleX: 0 }, { scaleX: 1, duration: .68, ease: "power3.out" }, at + .12);
      tl.fromTo(box.querySelector(".edge.start"), { opacity: 0, x: -14 }, { opacity: 1, x: 0, duration: .34 }, at + .3);
      tl.fromTo(box.querySelector(".edge.stop"), { opacity: 0, x: 14 }, { opacity: 1, x: 0, duration: .34 }, at + .52);

    } else if (fig.type === "flow") {
      box.querySelectorAll(".step").forEach((st, i) => {
        tl.fromTo(st, { opacity: 0, y: 24, scale: .95 },
          { opacity: 1, y: 0, scale: 1, duration: .4, ease: "power3.out" }, at + .08 + i * .22);
      });
      box.querySelectorAll(".arrow").forEach((ar, i) => {
        tl.fromTo(ar, { opacity: 0, x: -10 }, { opacity: 1, x: 0, duration: .26 }, at + .3 + i * .22);
      });

    } else if (fig.type === "timeline") {
      tl.fromTo(box.querySelector(".line"), { scaleX: 0 }, { scaleX: 1, duration: .7, ease: "power2.out" }, at + .1);
      box.querySelectorAll(".tick").forEach((tk, i) => {
        tl.fromTo(tk, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .32, ease: "power3.out" }, at + .3 + i * .18);
      });

    } else if (fig.type === "stat") {
      const big = box.querySelector(".big");
      if (big) {
        const state = { v: 0 }, target = Number(big.dataset.target) || 0, unit = big.dataset.unit;
        tl.to(state, { v: target, duration: .9, ease: "power2.out",
                       onUpdate: () => { big.textContent = formatQuantity(state.v, unit); } }, at + .12);
      }
      const fill = box.querySelector(".fill");
      if (fill) tl.fromTo(fill, { scaleX: 0 }, { scaleX: 1, duration: .7, ease: "power2.out" }, at + .2);
    }
  }

  function build() {
    const V = window.__hyperframes.getVariables();
    const LINES = typeof V.lines === "string" ? JSON.parse(V.lines || "[]") : (V.lines || []);
    const DUR = Number(V.duration) || 30;
    const STYLE = window.HF_STYLE || {};
    const root = document.getElementById("root");
    const rand = rng(hashSeed(V.kicker + "|" + (LINES[0] && LINES[0].words && LINES[0].words[0] ? LINES[0].words[0].w : "")));

    root.style.setProperty("--accent", V.accent);
    root.style.setProperty("--accent-30", hexA(V.accent, 0.30));
    root.style.setProperty("--accent-12", hexA(V.accent, 0.12));
    const setText = (id, t) => { const n = document.getElementById(id); if (n) n.textContent = t || ""; };
    setText("kicker", V.kicker); setText("badge", V.badge); setText("footer", V.footer);

    // --- scene: 1 câu narration = 1 cảnh, cảnh đầu hiện sẵn, còn lại opacity 0 ---
    const stage = document.getElementById("stage");
    // Video dài (longform.js): bố cục ảnh khác ô mặc định, sơ đồ, thẻ chương.
    // Style không nạp longform.js thì LONG = null và mọi thứ như cũ.
    const LONG = window.HF_LONG || null;
    if (LONG && LONG.begin) LONG.begin(LINES, V);  // hạt giống cho bộ chọn biến thể
    const layoutOf = (ln) => {
      const m = ln.media || (ln.media_cont && LINES[ln.media_cont - 1].media) || null;
      return (LONG && m && m.layout && LONG.layouts[m.layout]) ? LONG.layouts[m.layout] : null;
    };
    const visualOf = (ln) => (LONG && ln.visual && LONG.visuals[ln.visual.type]) || null;
    // Hết khoảng của một sơ đồ = cuối câu cuối cùng nó còn chiếm màn hình.
    const untilOf = (i) => { let k = i; while (k + 1 < LINES.length && LINES[k + 1].visual_cont === LINES[i].sentence_id) k++; return LINES[k].end; };
    const scenes = LINES.map((ln, i) => {
      const s = el("div", "scene");
      s.id = "scene" + i;
      s.style.opacity = i === 0 ? "1" : "0";
      const inner = el("div", "scene-inner");
      s.appendChild(inner);
      stage.appendChild(s);
      if (ln.media) {
        // MÀN VIDEO: một loại màn khác hẳn, không phải thẻ thường có dán
        // thêm clip. Style tự quyết cắt khung, che tối, nhãn, chữ.
        s.classList.add("has-media");
        const lay = layoutOf(ln);
        if (lay) lay.build(inner, ln, i, { rand, V });
        else (STYLE.buildMediaScene || defaultMediaScene)(inner, ln, i, LINES.length, { rand, V });
      } else if (visualOf(ln)) {
        s.classList.add("has-visual");
        visualOf(ln).build(inner, ln, i, { rand, V, LINES });
      } else if (ln.visual_cont) {
        // cảnh rỗng: sơ đồ của câu gốc vẫn đứng trên màn hình
      } else if (LONG && ln.chapter_no) {
        LONG.chapter.build(inner, ln, i, { rand, V });
      } else if (ln.media_cont && layoutOf(ln)) {
        s.classList.add("has-media");
        layoutOf(ln).build(inner, ln, i, { rand, V });
      } else if (ln.media_cont) {
        // Câu nối tiếp của một ảnh đang giữ (video dài): dựng lại ĐÚNG khung
        // đó ở trạng thái đứng yên, không có hoạt cảnh vào. Ảnh vẫn là clip
        // của câu gốc, chạy xuyên suốt bên dưới.
        s.classList.add("has-media");
        (STYLE.buildMediaScene || defaultMediaScene)(inner, ln, i, LINES.length, { rand, V });
      } else if (STYLE.buildScene) {
        STYLE.buildScene(inner, ln, i, LINES.length, { rand, V });
      }
      if (ln.figure && ln.figure.type !== "none") {
        s.classList.add("has-fig");
        inner.appendChild(buildFigure(ln.figure, ln.figure_labels));
      }
      return s;
    });

    // --- phụ đề: lớp riêng NẰM TRÊN transition, chữ luôn đọc được ---
    const capzone = document.getElementById("capzone");
    const caps = LINES.map((ln) => {
      const cap = el("div", "cap");
      (ln.words || []).forEach(w => {
        const span = el("span", "w" + (w.hot ? " hot" : ""), w.w);
        const on = el("span", "on", w.w);
        span.appendChild(on);
        cap.appendChild(span);
      });
      cap.style.opacity = "0";
      capzone.appendChild(cap);
      return cap;
    });

    // Lớp điện ảnh phủ CẢ video, không riêng màn ảnh -- vá từng chỗ thì mỗi
    // màn một chất, mất cảm giác cùng một cuộn phim. Chỉ BUD: nhịp chiêm
    // nghiệm chịu được hạt phim, nhịp nhanh và căng của CL thì không.
    let grain = null;
    if (V.series === "bud") {
      const cine = el("div"); cine.id = "cine";
      grain = el("div", "cine-grain");
      cine.appendChild(grain);
      cine.appendChild(el("div", "cine-bloom"));
      root.appendChild(cine);
    }

    const tl = gsap.timeline({ paused: true });

    if (STYLE.ambient) STYLE.ambient(tl, DUR, { rand, V, root });
    if (LONG && LONG.ambient) LONG.ambient(tl, DUR, { rand, V, root, LINES });  // hạt bay, vệt sáng

    if (grain) {
      // Hạt phim đứng yên là bụi trên ống kính, không phải hạt phim. Nhảy
      // từng nấc bằng steps() -- vẫn tất định, không dùng Math.random.
      tl.fromTo(grain, { backgroundPosition: "0px 0px" },
        { backgroundPosition: "190px 190px", duration: DUR, ease: "steps(" + Math.max(8, Math.round(DUR * 1.4)) + ")" }, 0);
    }

    // Chuyển cảnh qua kho hiệu ứng (longform.js) nếu style có nạp; kho từ chối
    // (hoặc style không nạp) thì dùng chuyển cảnh riêng của style như cũ.
    const clipOfGroup = (k) => {
      const L = LINES[k], gid = L.media_cont || (L.media && L.sentence_id);
      return gid ? document.getElementById("mediaclip" + gid) : null;
    };
    const transit = (oldIdx, newIdx, T) => {
      const ctx = { rand, V, toChapter: !!(LONG && LINES[newIdx].chapter_no), oldClip: clipOfGroup(oldIdx) };
      if (LONG && LONG.transition && LONG.transition(tl, scenes[oldIdx], scenes[newIdx], T, ctx)) return;
      (STYLE.transition || defaultTransition)(tl, scenes[oldIdx], scenes[newIdx], T, { rand, V });
    };

    LINES.forEach((ln, i) => {
      const inner = scenes[i].firstChild;
      if (ln.media) {
        const clip = document.getElementById("mediaclip" + (i + 1));
        if (clip) {
          // Khung tự bật/tắt thẻ media theo data-start -- tức là CẮT CỨNG,
          // trong khi mọi thứ còn lại đều chuyển mềm. Đó là cú khựng. Fade
          // opacity bằng GSAP để hai đầu màn nối liền. (opacity hợp lệ trên
          // .clip; chỉ display/visibility là cấm.)
          tl.fromTo(clip, { opacity: 0 },
            { opacity: 1, duration: .55, ease: "sine.out" }, ln.start);
          // Tắt XONG ngay tại điểm kết câu, không muộn hơn. Clip nằm DƯỚI
          // #stage nên khung giấy của cảnh là thứ giữ nó trong khuôn; cảnh
          // tan mà ảnh còn thì ảnh tràn ra kín khung, mất hẳn bố cục.
          // Đi cùng nhịp với cảnh mới là đủ mượt.
          const mEnd = ln.media_end || ln.end;
          tl.to(clip, { opacity: 0, duration: .45, ease: "sine.in" },
            Math.max(ln.start + .6, mEnd - .45));

          // Mask nở theo CẢ khung 1080x1920, trong khi cửa sổ nhìn thấy nhỏ
          // hơn nhiều -- để 210% thì nó phủ kín trước khi mắt kịp thấy.
          const how = ln.media.reveal || "";
          if (how === "ink") {
            // Vệt mực loang: ảnh thấm ra từ một điểm thay vì bật lên.
            tl.fromTo(clip, { "--ink": "4%" },
              { "--ink": "115%", duration: 2.6, ease: "power1.inOut" }, ln.start);
          } else if (how === "wipe") {
            tl.fromTo(clip, { "--wipe": "16%" },
              { "--wipe": "132%", duration: 1.9, ease: "power2.out" }, ln.start);
          } else if (how === "iris") {
            tl.fromTo(clip, { "--iris": "14%" },
              { "--iris": "128%", duration: 2.0, ease: "power2.out" }, ln.start);
          } else if (how === "rise") {
            tl.fromTo(clip, { "--rise": "16%" },
              { "--rise": "132%", duration: 1.9, ease: "power2.out" }, ln.start);
          }
        }
        const lay = layoutOf(ln);
        if (clip && lay && lay.motion && lay.motion(tl, clip, ln, ln.media_end || ln.end)) {
          // bố cục tự lo chuyển động của clip (thẻ 3D, màn chia đôi)
        } else if (clip) {
          // Ken Burns: clip đứng yên trong 6 giây là ảnh tĩnh biết nhúc nhích.
          // BUD đi chậm hơn: 1.12 trong sáu giây là cú đẩy thấy rõ, hợp nhịp
          // căng của CL; ở đây nó làm khuôn hình bồn chồn.
          const kb = V.series === "bud" ? 1.075 : 1.12;
          const kbx = (ln.kb_dir || -1.5) * (V.series === "bud" ? 0.6 : 1);
          tl.fromTo(clip, { scale: 1.0, xPercent: 0 },
            { scale: kb, xPercent: kbx,
              duration: Math.max(1, (ln.media_end || ln.end) - ln.start), ease: "none" }, ln.start);
        }
        if (lay) { if (lay.enter) lay.enter(tl, inner, ln, i, { rand, V, clip }); }
        else (STYLE.enterMedia || defaultEnterMedia)(tl, inner, ln, i, { rand, V, clip });
      } else if (visualOf(ln)) {
        visualOf(ln).enter(tl, inner, ln, { rand, V, LINES, i, until: untilOf(i) });
      } else if (ln.visual_cont) {
        // sơ đồ gốc tự chạy các bước của nó
      } else if (LONG && ln.chapter_no) {
        LONG.chapter.enter(tl, inner, ln, { rand, V });
      } else if (ln.media_cont) {
        const lay2 = layoutOf(ln);
        if (lay2 && lay2.enterCont) lay2.enterCont(tl, inner, ln);
      } else if (STYLE.enter) {
        STYLE.enter(tl, inner, ln, i, { rand, V });
      }
      if (ln.figure && ln.figure.type !== "none") {
        animateFigure(tl, inner.querySelector(".fig"), ln.figure, ln.start + .34);
      }

      // Transition sang cảnh kế: cảnh ra và cảnh vào chạy CÙNG mốc T --
      // bản thân chuyển động LÀ cú bàn giao, không fade-out rồi mới vào.
      if (i < LINES.length - 1) {
        const T = Math.max(ln.start + 0.2, ln.end - 0.34);
        const nx = LINES[i + 1];
        const vg = ln.visual_cont || (ln.visual && ln.sentence_id);
        if (nx.visual_cont && nx.visual_cont === vg) {
          // cùng một sơ đồ: không chuyển cảnh
        } else if (ln.visual_cont) {
          transit(ln.visual_cont - 1, i + 1, T);
        } else if (nx.media_cont && nx.media_cont === (ln.media_cont || (ln.media && ln.sentence_id))) {
          // Cùng một ảnh, cùng một khung: tráo cảnh tức thì. Crossfade hai
          // khung giống hệt nhau làm độ phủ tụt giữa chừng, và ảnh full-frame
          // bên dưới loé qua lớp giấy.
          tl.set(scenes[i], { opacity: 0 }, T);
          tl.set(scenes[i + 1], { opacity: 1 }, T);
        } else {
          transit(i, i + 1, T);
        }
      }

      // Phụ đề + karaoke theo timing thật của TTS
      const cap = caps[i];
      tl.fromTo(cap, { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.24, ease: "power2.out" }, ln.start);
      if (i < LINES.length - 1) tl.to(cap, { opacity: 0, duration: 0.14, ease: "power1.in" }, ln.end - 0.1);
      (ln.words || []).forEach((w, k) => {
        const on = cap.children[k] && cap.children[k].querySelector(".on");
        if (!on) return;
        tl.set(on, { opacity: 1 }, w.t);
        tl.set(on, { opacity: 0 }, w.t + w.d);
      });
    });

    // Cảnh cuối là cảnh DUY NHẤT được phép có animation thoát
    const lastLn = LINES[LINES.length - 1];
    const last = lastLn && lastLn.visual_cont ? scenes[lastLn.visual_cont - 1] : scenes[scenes.length - 1];
    if (last) tl.to(last, { opacity: 0, duration: 0.5, ease: "power2.in" }, Math.max(0, DUR - 0.5));
    const lastCap = caps[caps.length - 1];
    if (lastCap) tl.to(lastCap, { opacity: 0, duration: 0.4, ease: "power2.in" }, Math.max(0, DUR - 0.45));

    addAudio(root, "narration", V.narration, 1, null, DUR);
    addAudio(root, "bgm", V.bgm, V.bgm_gain != null ? V.bgm_gain : 0.16, 1.2, DUR);

    window.__timelines["main"] = tl;
    tl.seek(0);
  }

  function defaultMediaScene(inner, ln, i, n) {
    const veil = el("div", "media-veil");
    inner.appendChild(veil);
    const slug = el("div", "media-slug", "TƯ LIỆU MINH HOẠ");
    inner.appendChild(slug);
  }

  function defaultEnterMedia(tl, inner, ln) {
    tl.fromTo(inner.querySelector(".media-veil"), { opacity: 0 }, { opacity: 1, duration: .5 }, ln.start);
    const slug = inner.querySelector(".media-slug");
    if (slug) tl.fromTo(slug, { opacity: 0, x: -14 }, { opacity: 1, x: 0, duration: .45 }, ln.start + .15);
  }

  function defaultTransition(tl, oldS, newS, T) {
    tl.to(oldS, { opacity: 0, duration: 0.34, ease: "power2.inOut" }, T);
    tl.to(newS, { opacity: 1, duration: 0.34, ease: "power2.inOut" }, T);
  }

  function addAudio(root, id, src, vol, fadeOut, dur) {
    if (!src) return;
    const a = document.createElement("audio");
    a.id = id; a.className = "clip"; a.src = src;
    a.dataset.start = "0"; a.dataset.duration = String(dur);
    if (vol != null) a.dataset.volume = String(vol);
    if (fadeOut) a.dataset.fadeOut = String(fadeOut);
    root.appendChild(a);
  }

  function hashSeed(s) {
    let h = 2166136261;
    for (let i = 0; i < (s || "").length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }

  return { build, el, hexA, rng, hashSeed };
})();
