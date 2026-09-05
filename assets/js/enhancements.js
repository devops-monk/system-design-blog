document.addEventListener('DOMContentLoaded', function () {

  /* ── Reading progress bar ── */
  var bar = document.createElement('div');
  bar.id = 'reading-progress';
  document.body.prepend(bar);

  window.addEventListener('scroll', function () {
    var doc = document.documentElement;
    var scrolled = doc.scrollTop || document.body.scrollTop;
    var total = doc.scrollHeight - doc.clientHeight;
    bar.style.width = total > 0 ? (scrolled / total * 100) + '%' : '0';
  }, { passive: true });

  /* ── Copy code buttons ── */
  document.querySelectorAll('pre').forEach(function (pre) {
    if (pre.classList.contains('mermaid')) return;
    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.innerHTML = '<i class="fa-regular fa-copy"></i>';
    btn.title = 'Copy code';
    pre.style.position = 'relative';
    pre.appendChild(btn);

    btn.addEventListener('click', function () {
      var code = pre.querySelector('code');
      var text = code ? code.innerText : pre.innerText;
      navigator.clipboard.writeText(text).then(function () {
        btn.innerHTML = '<i class="fa-solid fa-check"></i>';
        btn.classList.add('copied');
        setTimeout(function () {
          btn.innerHTML = '<i class="fa-regular fa-copy"></i>';
          btn.classList.remove('copied');
        }, 2000);
      });
    });
  });

  /* ── Diagram zoom ──
     213 mermaid diagrams, most of them unreadable on a phone. Clicking one
     opens it full-screen with wheel/pinch zoom and drag to pan.

     Clicks are delegated from the document rather than bound to each <pre>,
     because mermaid renders asynchronously from a module script in <head> and
     replaces each block's innerHTML — anything bound earlier would be lost. */
  (function () {
    var overlay, stage, inner, level;
    var scale = 1, tx = 0, ty = 0;
    var ptrs = new Map(), pinch = 0, dragX = 0, dragY = 0, dragging = false;

    var MIN = 0.4, MAX = 8;

    function apply() {
      inner.style.transform =
        'translate(-50%, -50%) translate(' + tx + 'px, ' + ty + 'px) scale(' + scale + ')';
      level.textContent = Math.round(scale * 100) + '%';
    }

    function zoomAt(factor, clientX, clientY) {
      var next = Math.min(MAX, Math.max(MIN, scale * factor));
      var k = next / scale;
      if (k === 1) return;
      var r = stage.getBoundingClientRect();
      // Keep the point under the cursor fixed: the inner is centred, so work
      // in offsets from the stage centre.
      var cx = clientX - r.left - r.width / 2 - tx;
      var cy = clientY - r.top - r.height / 2 - ty;
      tx -= cx * (k - 1);
      ty -= cy * (k - 1);
      scale = next;
      apply();
    }

    function reset() { scale = 1; tx = 0; ty = 0; apply(); }

    // Buttons and keys zoom about the middle of the stage, which sits below
    // the toolbar — not the middle of the window.
    function zoomCentre(factor) {
      var r = stage.getBoundingClientRect();
      zoomAt(factor, r.left + r.width / 2, r.top + r.height / 2);
    }

    function close() {
      overlay.hidden = true;
      inner.innerHTML = '';
      document.body.classList.remove('dz-open');
    }

    function build() {
      overlay = document.createElement('div');
      overlay.className = 'dz-overlay';
      overlay.hidden = true;
      overlay.innerHTML =
        '<div class="dz-bar">' +
          '<button class="dz-btn" data-dz="out" aria-label="Zoom out">&minus;</button>' +
          '<span class="dz-level">100%</span>' +
          '<button class="dz-btn" data-dz="in" aria-label="Zoom in">+</button>' +
          '<button class="dz-btn" data-dz="reset">Reset</button>' +
          '<button class="dz-btn dz-close" data-dz="close" aria-label="Close diagram">&times;</button>' +
        '</div>' +
        '<div class="dz-stage"><div class="dz-inner"></div></div>' +
        '<div class="dz-hint">Scroll or pinch to zoom &middot; drag to pan &middot; Esc to close</div>';
      document.body.appendChild(overlay);
      stage = overlay.querySelector('.dz-stage');
      inner = overlay.querySelector('.dz-inner');
      level = overlay.querySelector('.dz-level');

      overlay.addEventListener('click', function (e) {
        var act = e.target.closest('[data-dz]');
        if (act) {
          var a = act.getAttribute('data-dz');
          if (a === 'close') close();
          else if (a === 'reset') reset();
          else zoomCentre(a === 'in' ? 1.25 : 0.8);
          return;
        }
        if (e.target === stage || e.target === overlay) close();
      });

      stage.addEventListener('wheel', function (e) {
        e.preventDefault();
        zoomAt(e.deltaY < 0 ? 1.12 : 1 / 1.12, e.clientX, e.clientY);
      }, { passive: false });

      stage.addEventListener('dblclick', reset);

      stage.addEventListener('pointerdown', function (e) {
        ptrs.set(e.pointerId, e);
        stage.setPointerCapture(e.pointerId);
        if (ptrs.size === 1) { dragging = true; dragX = e.clientX; dragY = e.clientY; }
        else if (ptrs.size === 2) { dragging = false; pinch = spread(); }
      });

      stage.addEventListener('pointermove', function (e) {
        if (!ptrs.has(e.pointerId)) return;
        ptrs.set(e.pointerId, e);
        if (ptrs.size === 2) {
          var d = spread();
          if (pinch > 0) {
            var mid = midpoint();
            zoomAt(d / pinch, mid.x, mid.y);
          }
          pinch = d;
        } else if (dragging) {
          tx += e.clientX - dragX;
          ty += e.clientY - dragY;
          dragX = e.clientX; dragY = e.clientY;
          apply();
        }
      });

      ['pointerup', 'pointercancel', 'pointerleave'].forEach(function (type) {
        stage.addEventListener(type, function (e) {
          ptrs.delete(e.pointerId);
          if (ptrs.size < 2) pinch = 0;
          if (ptrs.size === 0) dragging = false;
        });
      });

      document.addEventListener('keydown', function (e) {
        if (overlay.hidden) return;
        if (e.key === 'Escape') close();
        else if (e.key === '+' || e.key === '=') zoomCentre(1.25);
        else if (e.key === '-') zoomCentre(0.8);
        else if (e.key === '0') reset();
      });
    }

    function spread() {
      var p = [...ptrs.values()];
      return Math.hypot(p[0].clientX - p[1].clientX, p[0].clientY - p[1].clientY);
    }

    function midpoint() {
      var p = [...ptrs.values()];
      return { x: (p[0].clientX + p[1].clientX) / 2, y: (p[0].clientY + p[1].clientY) / 2 };
    }

    function open(pre) {
      var svg = pre.querySelector('svg');
      if (!svg) return;
      if (!overlay) build();
      var copy = svg.cloneNode(true);
      // mermaid sets max-width in a style attribute so the diagram fits the
      // article column. Dropping it is not enough: an <svg> with a viewBox and
      // no explicit size collapses to the CSS default 300x150, so the clone is
      // measured from the viewBox and sized to fill the stage.
      copy.style.maxWidth = 'none';
      copy.removeAttribute('width');
      copy.removeAttribute('height');
      inner.innerHTML = '';
      inner.appendChild(copy);

      overlay.hidden = false;
      document.body.classList.add('dz-open');

      var box = svg.viewBox && svg.viewBox.baseVal;
      var rect = svg.getBoundingClientRect();
      var w = (box && box.width) || rect.width || 800;
      var h = (box && box.height) || rect.height || 600;
      var sr = stage.getBoundingClientRect();      // needs the overlay visible
      var fit = Math.min((sr.width - 48) / w, (sr.height - 48) / h);
      copy.style.width = (w * fit) + 'px';
      copy.style.height = (h * fit) + 'px';

      reset();
    }

    document.addEventListener('click', function (e) {
      if (overlay && !overlay.hidden) return;
      var pre = e.target.closest ? e.target.closest('pre.mermaid') : null;
      if (pre && pre.querySelector('svg')) open(pre);
    });
  })();

  /* ── Dark mode ── */
  var toggle = document.getElementById('dark-mode-toggle');
  var icon   = document.getElementById('dm-icon');

  function applyTheme(dark) {
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
    if (icon) {
      icon.className = dark ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
    }
  }

  var saved = localStorage.getItem('dm-theme');
  applyTheme(saved === 'dark');

  if (toggle) {
    toggle.addEventListener('click', function () {
      var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      applyTheme(!isDark);
      localStorage.setItem('dm-theme', !isDark ? 'dark' : 'light');
    });
  }

});
