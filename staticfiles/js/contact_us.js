var attachParent = document.getElementById("attach");
var addFile = document.getElementById("addFile");
var counter = 0;
addFile.onclick = function () {
    for (var i = 1; i < attachParent.children.length - 1; i++) {
        if (window.getComputedStyle(attachParent.children[i]).display === "none") {
            attachParent.children[i].classList.remove("display-hide");
            counter++;
            break
        }
    }
    if (counter === 4) {
        console.log("counter = " + counter);
        addFile.classList.remove("btn", "fa", "fa-plus")
    }
};