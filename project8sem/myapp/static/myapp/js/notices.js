
document.querySelectorAll('.read-more').forEach(function (element) {
    element.addEventListener('click', function () {
        var parent = this.parentNode.parentNode;
        parent.classList.toggle('expanded');
        if (parent.classList.contains('expanded')) {
            this.textContent = 'Read less';
        } else {
            this.textContent = 'Read more';
        }
    });
});
