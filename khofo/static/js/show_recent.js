$.ajax({
    type: 'GET',
    url: "/productHome/ajax/recentviewed/",
    data: {'a': 1,},
    dataType: 'json',
    contentType: 'application/json; charset=utf-8',
    success: function (data) {
        "use strict";
        if (data.done) {
            var recent_parent = document.getElementById('recentParent');
            if (recent_parent) {
                recent_parent.innerHTML = '';
                for (var i = data.products.length - 1; i >= 0; i--) {
                    var cardDiv = document.createElement('div');
                    var imgDiv = document.createElement('div');
                    var image = document.createElement('img');
                    var cardBodyDiv = document.createElement('div');
                    var cardBodylink = document.createElement('a');
                    var cardBodyName = document.createElement('h6');
                    var imglink = document.createElement('a');
                    if (window.location.href.toString().indexOf('/ar/') !== -1 || window.location.href.toString().indexOf('/ar-eg/') !== -1) {
                        cardDiv.setAttribute('class', 'card');
                        imgDiv.setAttribute('class', 'text-center imageDiv');
                        imglink.setAttribute('href', '/ar/productHome/product/' + data.products[i].id);
                        image.setAttribute('src', '/media/' + data.products[i].main_img);
                        cardBodyDiv.setAttribute('class', 'card-body text-center');
                        cardBodylink.setAttribute('href', '/ar/productHome/product/' + data.products[i].id);
                        cardBodyName.setAttribute('class', 'card-title');
                        console.log(data.products[i].name_ar);
                        cardBodyName.innerHTML = data.products[i].name_ar
                    } else {
                        cardDiv.setAttribute('class', 'card');
                        imgDiv.setAttribute('class', 'text-center imageDiv');
                        imglink.setAttribute('href', '/en/productHome/product/' + data.products[i].id);
                        image.setAttribute('src', '/media/' + data.products[i].main_img);
                        cardBodyDiv.setAttribute('class', 'card-body text-center');
                        cardBodylink.setAttribute('href', '/en/productHome/product/' + data.products[i].id);
                        cardBodyName.setAttribute('class', 'card-title');
                        console.log(data.products[i].name);
                        cardBodyName.innerHTML = data.products[i].name
                    }
                    var cardBodyPrice = document.createElement('p');
                    cardBodyPrice.setAttribute('class', 'card-text');
                    cardBodyPrice.setAttribute('style', 'font-size:12px;');
                    cardBodyPrice.innerHTML = data.products[i].price;
                    cardBodylink.appendChild(cardBodyName);
                    cardBodylink.appendChild(cardBodyPrice);
                    cardBodyDiv.appendChild(cardBodylink);
                    imglink.appendChild(image);
                    imgDiv.appendChild(imglink);
                    cardDiv.appendChild(imgDiv);
                    cardDiv.appendChild(cardBodyDiv);
                    recent_parent.appendChild(cardDiv)
                }
            }
        } else {
            console.log("Error", data)
        }
    }
});
