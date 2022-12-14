var finalCart = document.getElementById('cart2Div');
if (finalCart) {
    var tpa2 = document.getElementById('tpa2');
    var price;
    var total;
    var quantityInput;
    var c = finalCart.children.length;
    for (let o = 0; o < c; o++) {
        quantityInput = finalCart.children[o].children[2].children[0];
        price = finalCart.children[o].children[3].children[0];
        total = finalCart.children[o].children[4].children[0];
        total.innerHTML = parseInt(quantityInput.innerHTML) * parseInt(price.innerHTML);
        tpa2.innerHTML = parseInt(tpa2.innerHTML) + parseInt(total.innerHTML)
    }
}