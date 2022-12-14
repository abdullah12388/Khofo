function addCookie() {
    let quantity = document.getElementById('quantity_input');
    let productid = document.getElementById('productid');
    let specs_parent = document.getElementById('specs-parent');
    let max_quantity = document.getElementById('avail_quan');
    let product_specs = '';
    for (let i = 0; i < specs_parent.children.length; i++) {
        product_specs += specs_parent.children[i].children[0].id + ':' + specs_parent.children[i].children[1].value + ', '
    }
    $.ajax({
        type: 'GET',
        url: "/order/ajax/addCookie/",
        data: {
            quantity: quantity.value,
            productid: productid.value,
            product_specs: product_specs,
            max_quantity: max_quantity.value,
        },
        dataType: 'json',
        traditional: true,
        contentType: 'application/json; charset=utf-8',
        success: function(data) {
            if (data.done) {
                notifyMe('Max Quantity = ' + max_quantity.value);
            }
            if (data.remain) {
                notifyMe('You have reached the maximum available quantity.');
            }
        }
    })
}

let quan = document.getElementById('quantity_input');
let max_quan = document.getElementById('avail_quan');
quan.onkeyup = function() {
    if (parseInt(quan.value) > parseInt(max_quan.value)) {
        notifyMe('Max Quantity = ' + max_quan.value);
        quan.value = 1
    }
};