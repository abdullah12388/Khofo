var parentSelect = document.getElementById('adsParent');
var adsDisplay = document.getElementById('displayAds');
var i = 0;
f();

function f() {
    if (parentSelect !== null && parentSelect.length > 0) {
        if (i < parentSelect.length) {
            adsDisplay.children[0].style.display = 'none';
            adsDisplay.children[1].style.display = 'none';
            if (parentSelect.children[i].getAttribute('name') === 'image') {
                adsDisplay.children[0].style.display = 'block';
                adsDisplay.children[1].style.display = 'none';
                adsDisplay.children[0].src = parentSelect.children[i].innerHTML;
                setTimeout(f, parseInt(parentSelect.children[i].value) * 1000);
                i++
            } else {
                adsDisplay.children[0].style.display = 'none';
                adsDisplay.children[1].style.display = 'block';
                adsDisplay.children[1].src = parentSelect.children[i].innerHTML;
                setTimeout(f, parseInt(parentSelect.children[i].value) * 1000);
                i++
            }
        }
        if (i === parentSelect.length) {
            i = 0
        }
    }
}

function send_current_ad_num(e) {
    let n = parentSelect.children[e];
    console.log("show_num = ", n.id);
    $.ajax({
        type: "GET",
        url: "/ads/adNumToCookie/",
        data: {show_num: n.id},
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (e) {
            console.log("send succeeded")
        }
    })
}

f();