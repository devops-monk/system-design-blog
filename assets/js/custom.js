function searchSite(e) {
    e.preventDefault();
    var t = document.getElementById("query");
    window.location = "https://www.google.com/search?q=" + encodeURIComponent(t.value) + "+site%3Adevops-monk.com";
    return false;
}

let scrollTopBtn = document.getElementById("scrollTopBtn");

window.onscroll = function() { scrollFunction() };

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        scrollTopBtn.style.display = "block";
    } else {
        scrollTopBtn.style.display = "none";
    }
}

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}