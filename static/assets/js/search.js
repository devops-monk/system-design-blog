document.addEventListener('DOMContentLoaded', function () {
  var fuse = null;

  fetch('/index.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      fuse = new Fuse(data, {
        keys: ['title', 'summary', 'tags'],
        threshold: 0.35,
        minMatchCharLength: 2
      });
    });

  var input = document.getElementById('search-query');
  if (!input) return;

  input.addEventListener('input', runSearch);

  document.getElementById('search-btn').addEventListener('click', function (e) {
    e.preventDefault();
    runSearch();
  });

  function runSearch() {
    var q = input.value.trim();
    var box = document.getElementById('search-results');
    if (!box) return;
    if (!fuse || q.length < 2) { box.innerHTML = ''; return; }

    var results = fuse.search(q).slice(0, 8);
    if (results.length === 0) {
      box.innerHTML = '<em class="no-results">No posts found.</em>';
      return;
    }

    var html = '';
    for (var i = 0; i < results.length; i++) {
      var item = results[i].item;
      html += '<a href="' + item.url + '">' + item.title + '<\/a>';
    }
    box.innerHTML = html;
  }
});
