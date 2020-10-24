document.addEventListener('DOMContentLoaded', function () {
    var node = document.querySelectorAll(".friend")[0];
    var longpress = false;
    var presstimer = null;
    var longtarget = null;
    var cancel = function (e) {
        if (presstimer !== null) {
            clearTimeout(presstimer);
            presstimer = null;
        }

        this.classList.remove("longpress");
    };

    var click = function (e) {
        if (presstimer !== null) {
            clearTimeout(presstimer);
            presstimer = null;
        }

        this.classList.remove("longpress");

        if (longpress) {
            return false;
        }
    };

    var start = function (e) {

        if (e.type === "click" && e.button !== 0) {
            return;
        }

        longpress = false;

        this.classList.add("longpress");

        if (presstimer === null) {
            e.preventDefault()
            roomId = this.getAttribute("data-id")
            presstimer = setTimeout(function () {
                openModal("#editRoom")
                longpress = true;
            }, 1000);
        }

        return false;
    };
    var roomId = 1;
    var rooms = document.querySelectorAll('.friend')

    function addHoldListener(node) {
        node.addEventListener("mousedown", start);
        node.addEventListener("touchstart", start);
        node.addEventListener("click", click);
        node.addEventListener("mouseout", cancel);
        node.addEventListener("touchend", cancel);
        node.addEventListener("touchleave", cancel);
        node.addEventListener("touchcancel", cancel);
    }
    for (room of rooms) {
        addHoldListener(room)
    }

    // Move Room
    var moveBtns = document.querySelectorAll(".moveRoomBtn")
    for (btn of moveBtns) {
        btn.onclick = function (e) {
            e.preventDefault()
            var xhr = new XMLHttpRequest()
            xhr.onreadystatechange = function (e) {
                if (this.readyState == 4 && this.status == 200) {
                    alert("Please refresh or restart the app to see changes")
                }
            }
            xhr.open("POST", this.getAttribute("href"), true)
            let data = {
                "room_id": roomId,
            };
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
            xhr.setRequestHeader("X-CSRFToken", "{{csrf_token}}")
            xhr.send(JSON.stringify(data))
        }
    }
});