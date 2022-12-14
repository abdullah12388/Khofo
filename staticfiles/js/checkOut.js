let checkOut = document.getElementById('cartDiv');
let totalOrderDiv = document.getElementById('totalOrderDiv');
let quantity_before_update = 0;
let total_before_update = 0;
let tpa_before_update = 0;
if (checkOut) {
    if (checkOut.children.length > 0) {
        totalOrderDiv.classList.remove("display-hide");
        let tpa = document.getElementById('tpa');
        let totalPriceAmount = 0;
        let cartQuantities = [];
        let price;
        let total;
        let quantityInput;
        let quan;
        let incBtn;
        let decBtn;
        let deleteBtn;
        let proid;
        let cartid;
        let max_quan;
        let c = checkOut.children.length;
        for (let o = 0; o < c; o++) {
            quantityInput = checkOut.children[o].children[3].children[0].children[0];
            max_quan = checkOut.children[o].children[3].children[0].children[3];
            incBtn = checkOut.children[o].children[3].children[0].children[2].children[0];
            decBtn = checkOut.children[o].children[3].children[0].children[2].children[1];
            price = checkOut.children[o].children[4].children[0];
            total = checkOut.children[o].children[5].children[0];
            proid = checkOut.children[o].children[6].children[0];
            cartid = checkOut.children[o].children[6].children[1];
            deleteBtn = checkOut.children[o].children[6].children[0].children[0];
            total.innerHTML = parseInt(quantityInput.value) * parseInt(price.innerHTML);
            tpa.innerHTML = parseInt(tpa.innerHTML) + parseInt(total.innerHTML);
            quan = checkOut.children[o].children[3].children[0].children[0].value;
            cartQuantities.push(quan);
            test_(o)
        }

        function test_(y) {
            quantityInput = checkOut.children[y].children[3].children[0].children[0];
            max_quan = checkOut.children[y].children[3].children[0].children[3];
            incBtn = checkOut.children[y].children[3].children[0].children[2].children[0];
            decBtn = checkOut.children[y].children[3].children[0].children[2].children[1];
            proid = checkOut.children[y].children[6].children[0];
            cartid = checkOut.children[y].children[6].children[1];
            deleteBtn = checkOut.children[y].children[6].children[0].children[0];
            price = checkOut.children[y].children[4].children[0];
            total = checkOut.children[y].children[5].children[0];
            incBtn.onclick = function () {
                quantityInput = checkOut.children[y].children[3].children[0].children[0];
                max_quan = checkOut.children[y].children[3].children[0].children[3];
                price = checkOut.children[y].children[4].children[0];
                total = checkOut.children[y].children[5].children[0];
                quantity_before_update = parseInt(quantityInput.value);
                total_before_update = parseInt(total.innerHTML);
                tpa_before_update = parseInt(tpa.innerHTML);
                if (parseInt(quantityInput.value) < parseInt(max_quan.value)) {
                    quantityInput.value = parseInt(quantityInput.value) + 1;
                    total.innerHTML = parseInt(quantityInput.value) * parseInt(price.innerHTML);
                    tpa.innerHTML = parseInt(tpa.innerHTML) + parseInt(price.innerHTML);
                    prepare_context(y);
                    send_context('plus', y)
                }
            };
            decBtn.onclick = function () {
                quantityInput = checkOut.children[y].children[3].children[0].children[0];
                price = checkOut.children[y].children[4].children[0];
                total = checkOut.children[y].children[5].children[0];
                if (parseInt(quantityInput.value) > 1) {
                    quantityInput.value = parseInt(quantityInput.value) - 1;
                    total.innerHTML = parseInt(quantityInput.value) * parseInt(price.innerHTML);
                    tpa.innerHTML = parseInt(tpa.innerHTML) - parseInt(price.innerHTML);
                    prepare_context(y);
                    send_context('negative', y)
                }
            };
            deleteBtn.onclick = function () {
                proid = checkOut.children[y].children[6].children[0];
                cartid = checkOut.children[y].children[6].children[1];
                quantityInput = checkOut.children[y].children[3].children[0].children[0];
                // console.log(this.name);
                delete_product(proid.id, cartid.id, quantityInput.value, this.name)
            };
            quantityInput.onkeyup = function () {
                quantityInput = checkOut.children[y].children[3].children[0].children[0];
                max_quan = checkOut.children[y].children[3].children[0].children[3];
                price = checkOut.children[y].children[4].children[0];
                total = checkOut.children[y].children[5].children[0];
                // console.log(quantityInput.value);
                if (parseInt(quantityInput.value) > 0 && parseInt(quantityInput.value) <= parseInt(max_quan.value)) {
                    tpa.innerHTML = parseInt(tpa.innerHTML) - parseInt(total.innerHTML);
                    total.innerHTML = parseInt(quantityInput.value) * parseInt(price.innerHTML);
                    tpa.innerHTML = parseInt(tpa.innerHTML) + parseInt(total.innerHTML);
                    prepare_context(y);
                    send_context('type', y)
                } else if (quantityInput.value === '') {
                    quantityInput.setAttribute('placeholder', '1',);
                    quantityInput.setAttribute('value', 1);
                    tpa.innerHTML = parseInt(tpa.innerHTML) - parseInt(total.innerHTML);
                    total.innerHTML = 0;
                    tpa.innerHTML = parseInt(tpa.innerHTML) + parseInt(total.innerHTML)
                } else {
                    notifyMe("Max Quantity =  " + max_quan.value + ".")
                }
            }
        }

        function prepare_context(y) {
            quan = checkOut.children[y].children[3].children[0].children[0].value;
            cartQuantities[y] = quan
        }

        function send_context(operator, index) {
            console.log('index = ', index)
            let args = 'operator=' + operator + '&index=' + index + '&';
            for (let i = 0; i < cartQuantities.length; i++) {
                args += 'cart[' + i + ']=' + cartQuantities[i] + '&'
            }
            $.ajax({
                type: 'GET',
                url: "/order/ajax/updateCookie/",
                data: args,
                dataType: 'json',
                traditional: true,
                contentType: 'application/json; charset=utf-8',
                success: function (data) {
                    if (data.done) {
                        notifyMe('You have reached the maximum available quantity.');
                        checkOut.children[index].children[3].children[0].children[0].value = quantity_before_update;
                        checkOut.children[index].children[5].children[0].innerHTML = total_before_update;
                        document.getElementById('tpa').innerHTML = tpa_before_update;
                    }
                }
            })
        }

        function delete_product(proid, cartid, quantityInput, langType) {
            // console.log("/" + langType + "/order/ajax/deleteProduct/");
            // console.log('cartid = ', cartid);
            $.ajax({
                type: 'GET',
                url: "/" + langType + "/order/ajax/deleteProduct/",
                data: {'proid': proid, 'cartid': cartid, 'quantity': quantityInput, 'deleted': 'true'},
                dataType: 'json',
                traditional: true,
                contentType: 'application/json; charset=utf-8',
                success: function (data) {
                    location.reload();
                }
            })
        }
    } else {
        totalOrderDiv.classList.add("display-hide");
    }

} else {
    totalOrderDiv.classList.add("display-hide");
}
