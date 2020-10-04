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
            console.log(this.scrollY)
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

})