document.addEventListener('DOMContentLoaded', function () {
    // Sidebar
    document.querySelector("#close-sidebar").onclick = function () {
        document.querySelector(".page-wrapper").classList.remove("toggled");
    };
    document.querySelector("#show-sidebar").onclick = function () {
        document.querySelector(".page-wrapper").classList.add("toggled");
    };
    // Uploading
    for (input of document.querySelectorAll(".upload")) {
        input.onchange = function (e) {
            document.querySelector("#saveAttachedFile").click()
        }
    }
    // Pop up area
    document.querySelector("#messageText").onfocus = function (e) {
        document.querySelector(".areaSelector").classList.remove("hide")
    }
    document.querySelector("#messageText").addEventListener("focusout", function (e) {
        document.querySelector(".areaSelector").classList.add("hide");
    })

    document.querySelector("#scrollBottom").onclick = function (e) {
        scroll({
            top: window.scrollMaxY,
            behavior: "smooth"
        })
    }
    function toggleScrollDown() {
        let messages = document.querySelectorAll('.message')
        let lastMessageHeight = messages[messages.length - 1].offsetHeight
        console.log(lastMessageHeight)
        if (window.scrollY < window.scrollMaxY - lastMessageHeight) {
            document.querySelector("#scrollBottom").style.display = "block"
        }
        else {
            document.querySelector("#scrollBottom").style.display = "none"
        }
    }
    toggleScrollDown()
    window.addEventListener("scroll", function (e) {
        toggleScrollDown()
    })
    // -------------Push notifications-------------
    function notifyMe() {
        // Let's check if the browser supports notifications
        if (!("Notification" in window)) {
            alert("This browser does not support desktop notification");
        }
        else if (Notification.permission === "granted") {
            // If user already granted permission
        }
        else if (Notification.permission !== "denied") {
            Notification.requestPermission().then(function (permission) {
                // If the user accepts, let's create a notification
                if (permission === "granted") {
                    alert("Don't forget to click on 'subsribe to push messaging' in the homepage")
                    var notification = new Notification("Don't forget to click on 'Subsribe to Push Messaging' in the homepage");
                }
            });
        }
    }
    setTimeout(() => {
        notifyMe()
    }, 6000);
});