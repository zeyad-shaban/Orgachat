document.addEventListener('DOMContentLoaded', function () {
    document.querySelector("#close-sidebar").onclick = function () {
        document.querySelector(".page-wrapper").classList.remove("toggled");
    };
    document.querySelector("#show-sidebar").onclick = function () {
        document.querySelector(".page-wrapper").classList.add("toggled");
    };
});