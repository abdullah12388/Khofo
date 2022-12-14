let finalCart1 = document.getElementById('cart3Div');
let confirmShipping = document.getElementById('confirmShipping');
let shipping_company_id = 0;
let address = {};
let order_description = '';
let site_info = {};
let user_email = '';
let lang_code = document.getElementById('lang_code').value;
if (finalCart1) {
    let expressElement = document.getElementById('express');
    let expressDate = document.getElementById('expressDate');
    let expressPrice = document.getElementById('expressPrice');
    let airFreightElement = document.getElementById('air');
    let airDate = document.getElementById('airDate');
    let airPrice = document.getElementById('airPrice');
    let seaFreightElement = document.getElementById('sea');
    let seaDate = document.getElementById('seaDate');
    let seaPrice = document.getElementById('seaPrice');
    let totalOrdersElement = document.getElementById('tpa3');
    let tpa4 = document.getElementById('tpa4');
    let tpa5 = document.getElementById('tpa5');
    let price;
    let total;
    let quantityInput;
    let productsCount = finalCart1.children.length;
    let totalOrders = 0;
    let totalShipping = 0;
    let totalPrice = 0;
    let productId = document.getElementsByClassName('productId');
    let productName = document.getElementsByClassName('productName');
    let quantityElement = document.getElementsByClassName('quantityElement');
    let weightElement = document.getElementsByClassName('weightElement');
    let sizeElement = document.getElementsByClassName('sizeElement');
    let id = [];
    let name = [];
    let quantity = [];
    let weight = [];
    let size = [];
    for (let o = 0; o < productsCount; o++) {
        quantityInput = finalCart1.children[o].children[2].children[0];
        price = finalCart1.children[o].children[5].children[0];
        total = finalCart1.children[o].children[6].children[0];
        totalForProduct = parseInt(quantityInput.innerHTML) * parseInt(price.innerHTML);
        total.innerHTML = totalForProduct;
        totalOrders = totalOrders + totalForProduct;
        weightElement[o].children[0].innerHTML = weightElement[o].children[0].innerHTML.replace(',', '.');
        sizeElement[o].children[0].innerHTML = sizeElement[o].children[0].innerHTML.replace(',', '.');
        id.push(productId[o].innerHTML);
        quantity.push(quantityElement[o].children[0].innerHTML);
        name.push(productName[o].children[0].innerHTML);
        weight.push(parseFloat(weightElement[o].children[0].innerHTML));
        size.push(sizeElement[o].children[0].innerHTML);
        order_description += quantity[o] + 'x ' + name[o] + ', ';
        changeShipping(o);
    }

    totalOrdersElement.innerHTML = totalOrders;

    function changeShipping(n) {
        shippingSelect = finalCart1.children[n].children[7].children[0].children[0].children[0];
        shippingSelect.onchange = function () {
            'use strict';
            let shippingType = [];
            for (let x = 0; x < productsCount; x++) {
                var shipping = document.getElementById("shipping" + x);
                shippingType.push(shipping.options[shipping.selectedIndex].value);
            }
            console.log(shippingType);
            var found = shippingType.find(function (element) {
                return element === "Choose" || element === "اختر";
            });
            var args = 'products_count=' + productsCount + '&';
            for (let i = 0; i < id.length; i++) {
                args += 'id[' + i + ']=' + id[i] + '&' + 'name[' + i + ']=' + name[i] + '&' +
                    'quantity[' + i + ']=' + quantity[i] + '&' + 'weight[' + i + ']=' + weight[i] + '&' +
                    'size[' + i + ']=' + size[i] + '&' + 'shipping_type[' + i + ']=' + shippingType[i] + '&';
            }
            $.ajax({
                type: 'GET',
                url: '/shipping/ajax/shipping-details/',
                data: args,
                dataType: 'json',
                contentType: 'application/json; charset=utf-8',
                success: function (data) {
                    // console.log("data = ", data.done);
                    if (data.done) {
                        confirmShipping.classList.add('display-hide');
                        expressElement.classList.add('display-hide');
                        expressPrice.innerHTML = 0;
                        airFreightElement.classList.add('display-hide');
                        airPrice.innerHTML = 0;
                        seaFreightElement.classList.add('display-hide');
                        seaPrice.innerHTML = 0;
                        tpa4.innerHTML = 0;
                        tpa5.innerHTML = 0;
                        totalShipping = 0;
                        totalPrice = 0;
                        if (data.express && data.air && data.sea) {
                            let express = data.express;
                            let air = data.air;
                            let sea = data.sea;
                            displayShippingAll(express, air, sea, found);
                        } else if (data.express && data.air) {
                            let express = data.express;
                            let air = data.air;
                            displayShippingTwo(express, air, found);
                        } else if (data.express && data.sea) {
                            let express = data.express;
                            let sea = data.sea;
                            displayShippingTwo(express, sea, found);
                        } else if (data.sea && data.air) {
                            let sea = data.sea;
                            let air = data.air;
                            displayShippingTwo(sea, air, found);
                        } else if (data.express) {
                            let express = data.express;
                            displayShippingOne(express, found);
                        } else if (data.sea) {
                            let sea = data.sea;
                            displayShippingOne(sea, found);
                        } else if (data.air) {
                            let air = data.air;
                            displayShippingOne(air, found);
                        } else {
                            expressElement.classList.add('display-hide');
                            expressPrice.innerHTML = 0;
                            airFreightElement.classList.add('display-hide');
                            airPrice.innerHTML = 0;
                            seaFreightElement.classList.add('display-hide');
                            confirmShipping.classList.add('display-hide');
                            seaPrice.innerHTML = 0;
                            tpa4.innerHTML = 0;
                            tpa5.innerHTML = 0;
                            totalShipping = 0;
                            totalPrice = 0;
                        }
                        /////////////////////////////////////////////////////////////
                        if (data.user_address) {
                            // console.log('user_address= ', data.user_address);
                            address = data.user_address;
                            // console.log('address = ', address);
                        } else {
                            console.log('No user address founded');
                        }
                        if (data.site_info) {
                            // console.log('site_info1 = ', data.site_info);
                            site_info = data.site_info;
                            // console.log('site_info2 = ', site_info);
                        } else {
                            console.log('no site info founded');
                        }
                        if (data.user_email) {
                            // console.log('user_email = ', data.user_email);
                            user_email = data.user_email;
                            // console.log('user_email = ', user_email);
                        } else {
                            console.log('no user email founded');
                        }
                        /////////////////////////////////////////////////////////////
                    } else {
                        expressElement.classList.add('display-hide');
                        expressPrice.innerHTML = 0;
                        airFreightElement.classList.add('display-hide');
                        airPrice.innerHTML = 0;
                        seaFreightElement.classList.add('display-hide');
                        confirmShipping.classList.add('display-hide');
                        seaPrice.innerHTML = 0;
                        tpa4.innerHTML = 0;
                        tpa5.innerHTML = 0;
                        totalShipping = 0;
                        totalPrice = 0;
                    }
                }
            });
        };
    }

    confirmShipping.onclick = function () {
        "use strict";
        get_session_id();
    };

    function displayShippingAll(one, two, three, found) {
        let onePrice = document.getElementById('' + one.type.toString() + 'Price');
        let twoPrice = document.getElementById('' + two.type.toString() + 'Price');
        let threePrice = document.getElementById('' + three.type.toString() + 'Price');
        let oneDate = document.getElementById('' + one.type.toString() + 'Date');
        let twoDate = document.getElementById('' + two.type.toString() + 'Date');
        let threeDate = document.getElementById('' + three.type.toString() + 'Date');
        let oneElement = document.getElementById('' + one.type.toString());
        let twoElement = document.getElementById('' + two.type.toString());
        let threeElement = document.getElementById('' + three.type.toString());
        shipping_company_id = one.shipping_company_id;
        onePrice.innerHTML = one.price;
        twoPrice.innerHTML = two.price;
        threePrice.innerHTML = three.price;
        totalShipping = parseFloat(one.price) + parseFloat(two.price) + parseFloat(three.price);
        totalPrice = parseFloat(totalOrders) + parseFloat(totalShipping);
        tpa4.innerHTML = totalShipping;
        tpa5.innerHTML = totalPrice;
        // get_session_id(); // Function That Create Session
        oneDate.innerHTML = one.afterDate;
        twoDate.innerHTML = two.afterDate;
        threeDate.innerHTML = three.afterDate;
        oneElement.classList.remove('display-hide');
        twoElement.classList.remove('display-hide');
        threeElement.classList.remove('display-hide');
        if (!found) {
            confirmShipping.classList.remove('display-hide');
        }
        return totalPrice;
    }

    function displayShippingTwo(one, two, found) {
        let onePrice = document.getElementById('' + one.type.toString() + 'Price');
        let twoPrice = document.getElementById('' + two.type.toString() + 'Price');
        let oneDate = document.getElementById('' + one.type.toString() + 'Date');
        let twoDate = document.getElementById('' + two.type.toString() + 'Date');
        let oneElement = document.getElementById('' + one.type.toString());
        let twoElement = document.getElementById('' + two.type.toString());
        shipping_company_id = one.shipping_company_id;
        onePrice.innerHTML = one.price;
        twoPrice.innerHTML = two.price;
        totalShipping = parseFloat(one.price) + parseFloat(two.price);
        totalPrice = parseFloat(totalOrders) + parseFloat(totalShipping);
        tpa4.innerHTML = totalShipping;
        tpa5.innerHTML = parseFloat(totalOrders) + parseFloat(totalShipping);
        // get_session_id(); // Function That Create Session
        oneDate.innerHTML = one.afterDate;
        twoDate.innerHTML = two.afterDate;
        oneElement.classList.remove('display-hide');
        twoElement.classList.remove('display-hide');
        if (!found) {
            confirmShipping.classList.remove('display-hide');
        }
        return totalPrice;
    }

    function displayShippingOne(one, found) {
        let onePrice = document.getElementById('' + one.type.toString() + 'Price');
        let oneDate = document.getElementById('' + one.type.toString() + 'Date');
        let oneElement = document.getElementById('' + one.type.toString());
        shipping_company_id = one.shipping_company_id;
        onePrice.innerHTML = one.price;
        totalShipping = parseFloat(one.price);
        totalPrice = parseFloat(totalOrders) + parseFloat(totalShipping);
        tpa4.innerHTML = totalShipping;
        tpa5.innerHTML = totalPrice;
        // get_session_id(); // Function That Create Session
        oneDate.innerHTML = one.afterDate;
        oneElement.classList.remove('display-hide');
        if (!found) {
            confirmShipping.classList.remove('display-hide');
        }
        return totalPrice;
    }


    function get_session_id() {
        $.ajax({
            type: "GET",
            url: '/' + lang_code + '/shipping/sendapi/',
            data: {'gsi': 'get_session_id'},
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                // console.log(data.done);
                if (data.done) {
                    // console.log('url = ', url)
                    // console.log('username = ', username)
                    // console.log('password = ', password)
                    // console.log('api_data = ', args)
                    // console.log('respone from checkout_create_seesion = ', data.res)
                    // console.log(data.merchant, data.currency, data.locale, data.order_id)
                    resp = data.res;
                    // console.log('session_id = ', resp.session.id);
                    document.getElementById('payBtn').classList.remove('display-hide');
                    config_checkout(resp.session.id, [data.merchant, data.currency, data.locale, data.order_id])
                }
            },
        });
    }

    function showProcess() {
        document.getElementById('processPay').classList.remove('display-hide');
    }

    function config_checkout(session_id, merchant_data) {
        // console.log('Entered Checkout Configure Creation Function');
        Checkout.configure({
            merchant: merchant_data[0],
            order: {
                amount: parseFloat(totalPrice),
                currency: merchant_data[1],
                description: order_description.substring(0, 124) + '...',
                id: merchant_data[3]
            },
            session: {
                id: session_id,
            },
            billing: {
                address: {
                    street: address.address,
                    city: address.city,
                    postcodeZip: address.zip_code,
                    stateProvince: address.region,
                    country: address.country
                }
            },
            shipping: {
                address: {
                    street: address.address,
                    city: address.city,
                    postcodeZip: address.zip_code,
                    stateProvince: address.region,
                    country: address.country
                }
            },
            customer: {
                email: user_email,
            },
            interaction: {
                operation: "PURCHASE",
                merchant: {
                    name: site_info.name,
                    address: site_info.address,
                    email: site_info.email,
                    phone: site_info.phone,
                    // logo: 'https://drive.google.com/file/d/1Fh8v82U9S7BhfwGNd2_vnJdNhPr_HRn9/view?usp=sharing'
                },
                locale: merchant_data[2],
                theme: 'default',
                displayControl: {
                    orderSummary: 'SHOW',
                    paymentConfirmation: 'SHOW',
                    billingAddress: 'OPTIONAL',
                    customerEmail: 'OPTIONAL',
                    shipping: 'READ_ONLY'
                }
            }
        });
        // console.log('checkout_configure = ', {
        //     merchant: 'TESTKHOFU_EGP',
        //     order: {
        //         amount: 5000,
        //         currency: 'EGP',
        //         description: 'fdbvdfzvnkjdfzbvjkfzsbzdf',
        //         id: ord_id
        //     },
        //     session: {
        //         id: session_id
        //     },
        //     billing: {
        //         address: {
        //             street: '123 Customer Street',
        //             city: 'Metropolis',
        //             postcodeZip: '99999',
        //             stateProvince: 'NY',
        //             country: 'USA'
        //         }
        //     },
        //     interaction: {
        //         operation: "PURCHASE",
        //         merchant: {
        //             name: 'KHOFU',
        //             address: {
        //                 line1: '200 Sample St',
        //                 line2: '1234 Example Town'
        //             },
        //             email: 'knics2020@gmail.com',
        //             phone: '+1 123 456 789 012',
        //             logo: 'https://drive.google.com/file/d/1Fh8v82U9S7BhfwGNd2_vnJdNhPr_HRn9/view?usp=sharing'
        //         },
        //         locale: 'en_US',
        //         theme: 'default',
        //         displayControl: {
        //             billingAddress: 'OPTIONAL',
        //             customerEmail: 'OPTIONAL',
        //             orderSummary: 'SHOW',
        //             shipping: 'HIDE'
        //         }
        //     }
        // });
    }

    function errorCallback(error) {
        console.log(JSON.stringify(error));
    }

    function cancelCallback() {
        window.location.href = '?s=canceled';
    }

    function completeCallback(resultIndicator, sessionVersion) {
        console.log('Payment completed');
        console.log('resultIndicator', resultIndicator);
        console.log('sessionVersion', sessionVersion);
        $.ajax({
            type: 'GET',
            url: '/en/shipping/request-order/',
            data: {
                del: 'deleted',
                scid: shipping_company_id,
                invoice: parseInt(Math.random() * (999999999)),
            },
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                if (data.done) {
                    console.log('ordered Successfully');
                    window.location.href = '?s=done';
                }
            },
        });
    }
}


// var url = 'https://banquemisr.gateway.mastercard.com/api/rest/version/54/merchant/TESTKHOFU_EGP/session';
// var username = 'Merchant.TESTKHOFU_EGP';
// var password = '50484e0dd923993588a9098834f32bd4';
// var ord_id = parseInt(Math.random() * (999999 - 0) + 0);
// var args = {
//     apiOperation: "CREATE_CHECKOUT_SESSION",
//     interaction: {
//         operation: "PURCHASE",
//         // returnUrl: "http://khofu.com/en/shipping/choose_shipping/"
//     },
//     order: {
//         id: ord_id,
//         currency: "EGP"
//     }
// };