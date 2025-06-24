// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Sticky navigation bar
window.addEventListener('scroll', function() {
    var nav = document.querySelector('nav');
    nav.classList.toggle('sticky', window.scrollY > 0);
});

// Back to top button
var backToTopButton = document.getElementById('back-to-top');

window.onscroll = function() {
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none";
    }
};

backToTopButton.addEventListener('click', function() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Side menu toggle
function openNav() {
    document.getElementById("side-menu").style.width = "250px";
    document.getElementById("overlay").style.visibility = "visible";
    document.getElementById("overlay").style.opacity = "1";
    document.body.classList.add("blur");
}

function closeNav() {
    document.getElementById("side-menu").style.width = "0";
    document.getElementById("overlay").style.visibility = "hidden";
    document.getElementById("overlay").style.opacity = "0";
    document.body.classList.remove("blur");
}

document.getElementById("menu-icon").addEventListener("click", openNav);
document.getElementById("closebtn").addEventListener("click", closeNav);
document.getElementById("overlay").addEventListener("click", closeNav);

// Popup close button
document.querySelectorAll('.close-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        this.closest('.popup-container').style.display = 'none';
    });
});
