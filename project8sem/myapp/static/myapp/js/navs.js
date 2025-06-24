function openNav() {
    document.getElementById("sideMenu").style.width = "250px";
    document.getElementById("mainContent").classList.add("blur");
    document.getElementById("overlay").classList.add("show");
}

function closeNav() {
    document.getElementById("sideMenu").style.width = "0";
    document.getElementById("mainContent").classList.remove("blur");
    document.getElementById("overlay").classList.remove("show");
}

function openLoginPopup() {
    document.getElementById("loginPopup").style.display = "block";
}

function closeLoginPopup() {
    document.getElementById("loginPopup").style.display = "none";
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.onscroll = function() {
    var backToTopButton = document.getElementById("back-to-top");
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none";
    }
};
