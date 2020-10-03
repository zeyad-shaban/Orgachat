document.addEventListener('DOMContentLoaded', function () {
    tabs = document.querySelectorAll('.tabs h3 a');
    for (tab of tabs) {
        tab.onclick = function (event) {
            event.preventDefault();
            if (this.innerHTML.includes('Sign')) {
                // Buttons
                document.querySelector('.tabs .signup-tab a').classList.add('active')
                document.querySelector('.tabs .login-tab a').classList.remove('active')
                // Forms
                document.querySelector('#signup-tab-content').classList.add('active')
                document.querySelector('#login-tab-content').classList.remove('active')
            } else {
                // Buttons
                document.querySelector('.tabs .signup-tab a').classList.remove('active')
                document.querySelector('.tabs .login-tab a').classList.add('active')
                // Forms
                document.querySelector('#signup-tab-content').classList.remove('active')
                document.querySelector('#login-tab-content').classList.add('active')
            }
        };
    }
});