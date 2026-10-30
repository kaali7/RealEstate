const date = new Date();
const year = document.querySelector('.year');
if (year) {
    year.innerHTML = date.getFullYear();
}

const navToggle = document.querySelector('[data-nav-toggle]');
const navMenu = document.querySelector('[data-nav-menu]');
if (navToggle && navMenu) {
    navToggle.addEventListener('click', function() {
        const isOpen = navMenu.classList.toggle('is-open');
        navToggle.setAttribute('aria-expanded', isOpen);
    });
}

const message = document.querySelector('#message');
if (message && window.jQuery) {
    setTimeout(function() {
        $('#message').fadeOut('slow');
    }, 3000);
}