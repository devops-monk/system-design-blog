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
