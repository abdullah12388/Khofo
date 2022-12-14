var myVar;

function myFunction(time) {
    myVar = setTimeout(showPage, parseInt(time))
}

function showPage() {
    document.getElementById("loader").style.display = "none";
    document.getElementById("myBodyDiv").style.display = "block"
}