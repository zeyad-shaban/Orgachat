document.addEventListener('DOMContentLoaded', function () {
    // ------------------
    // HEADER
    // ------------------
    // ---------Navbar----------
    document.querySelector('body').style.paddingTop = document.querySelector('.navbar').clientHeight + 'px'
    // detect scroll top or down
    try { // check if element exists
        var last_scroll_top = 0;
        window.onscroll = function () {
            scroll_top = this.scrollY;
            if (scroll_top < last_scroll_top) {
                document.querySelector('.navbar-main').classList.remove('scrolled-down');
                document.querySelector('.navbar-main').classList.add('scrolled-up');
            } else {
                document.querySelector('.navbar-main').classList.remove('scrolled-up');
                document.querySelector('.navbar-main').classList.add('scrolled-down');
            }
            last_scroll_top = scroll_top;
        };
    } catch (error) {}

    // -------------------------
    // REUSABLE
    // -------------------------
    // var modalBtns = document.querySelectorAll('.modal-link');
    // for (modalBtn of modalBtns) {
    //     modalBtn.onclick = function (e) {

    //     }
    // }
})
var backdrop = document.getElementById('backdrop')

function openModal(dataTarget) {
    let modal = document.querySelector(dataTarget)
    backdrop.style.display = 'block'
    modal.style.display = 'block'
    modal.classList.add('show')
}

function closeModal(dataTarget) {
    let modal = document.querySelector(dataTarget);
    backdrop.style.display = 'none';
    modal.style.display = 'none';
    modal.classList.remove('show');
}

function toggleDropdown(dataTarget) {
    let dropdown = document.querySelector(dataTarget)
    if (dropdown.style.display == 'block') {
        dropdown.style.display = 'none'
    } else {
        dropdown.style.display = 'block'
    }
};