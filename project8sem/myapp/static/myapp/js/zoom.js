// zoom.js
document.addEventListener('DOMContentLoaded', function() {
    const zoomContainers = document.querySelectorAll('.zoom-container');

    zoomContainers.forEach(container => {
        const overlay = container.querySelector('.zoom-overlay');

        container.addEventListener('click', function(event) {
            if (container.classList.contains('zoomed')) {
                container.classList.remove('zoomed');
            } else {
                zoomContainers.forEach(cont => cont.classList.remove('zoomed'));
                container.classList.add('zoomed');
            }
        });

        overlay.addEventListener('click', function(event) {
            event.stopPropagation();
            container.classList.remove('zoomed');
        });
    });
});
