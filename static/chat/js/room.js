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
});