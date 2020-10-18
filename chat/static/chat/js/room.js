document.addEventListener('DOMContentLoaded', function () {
    document.querySelector("#close-sidebar").onclick = function () {
        document.querySelector(".page-wrapper").classList.remove("toggled");
        document.querySelector('.chat-header').classList.add('scrolled-up');
        document.querySelector('.chat-header').classList.remove('scrolled-down');
    };
    document.querySelector("#show-sidebar").onclick = function () {
        document.querySelector(".page-wrapper").classList.add("toggled");
        document.querySelector('.chat-header').classList.remove('scrolled-up');
        document.querySelector('.chat-header').classList.add('scrolled-down');
    };
});