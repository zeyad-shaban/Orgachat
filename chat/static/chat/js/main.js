document.addEventListener('DOMContentLoaded', function () {
    // --------------------------
    // Service worker 
    // --------------------------
    // -------Add to homepage--------
    // --------Add to homepage----------

    let deferredPrompt;
    const addBtn = document.querySelector('#addToHomescreen');
    addBtn.style.display = 'none';
    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent Chrome 67 and earlier from automatically showing the prompt
        e.preventDefault();
        // Stash the event so it can be triggered later.
        deferredPrompt = e;
        // Update UI to notify the user they can add to home screen
        addBtn.style.display = 'block';

        addBtn.addEventListener('click', (e) => {
            // hide our user interface that shows our A2HS button
            addBtn.style.display = 'none';
            // Show the prompt
            deferredPrompt.prompt();
            // Wait for the user to respond to the prompt
            deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('User accepted the A2HS prompt');
                    // var xhr = new XMLHttpRequest()
                    // xhr.open("GET", "/metrics/user_installed/", true)
                    // xhr.send()
                } else {
                    console.log('User dismissed the A2HS prompt');
                }
                deferredPrompt = null;
            });
        });
    });

    // Displaying err
    if (document.querySelector("#addToHomescreen").style.display == "none") {
        // Showo err message
        document.querySelector("#errInstallApp").style.display = "block"
    } else {
        // Hide err message
        document.querySelector("#errInstallApp").style.display = "none"
    }


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
    } catch (error) { }

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