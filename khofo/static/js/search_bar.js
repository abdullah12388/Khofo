let searchInput = document.getElementById("searchInput");
let searchResultList = document.getElementById("searchResultList");
let ul = searchResultList.firstElementChild;
searchInput.onfocus = function () {
    console.log("wikaaaaa");
    "use strict";
    searchResultList.classList.remove("display-hide");
    searchInput.onkeyup = function () {
        if (searchInput.value === "") {
            ul.innerHTML = "";
            searchResultList.classList.add("display-hide");
        } else {
            searchResultList.classList.remove("display-hide");
            $.ajax({
                type: 'GET',
                url: '/productHome/ajax/search/',
                data: {searchInput: searchInput.value.toString().trim()},
                dataType: "json",
                content_type: 'application/json; charset=utf-8',
                success: function (data) {
                    if (data.done) {
                        ul.innerHTML = "";
                        let productList = data.productList;
                        let s = '<a href="#">' + '<li>' + '<strong>lenovo</strong>' + '<span>in</span>' + '<b>Laptops</b>' + '</li>' + '</a>';
                        for (let i = 0; i < productList.length; i++) {
                            let productID = productList[i].product_id;
                            let productName = productList[i].product_name;
                            let productCategory = productList[i].product_category;
                            let productSubCategory = productList[i].product_sub_category;
                            let in_ = productList[i].in;
                            let link = document.createElement('a');

                            let li = document.createElement('li');
                            let strong = document.createElement('strong');
                            strong.innerText = productName;
                            let spanIn = document.createElement('span');
                            spanIn.innerHTML = in_;
                            let boldSubCategory = document.createElement('b');
                            boldSubCategory.innerHTML = productSubCategory;
                            if (productList[i].lang === 'ar') {
                                searchResultList.style.direction = "rtl";
                                link.setAttribute('href', '/ar/productHome/product/' + productID + '/');
                            } else {
                                link.setAttribute('href', '/en/productHome/product/' + productID + '/');
                            }
                            li.appendChild(strong);
                            li.appendChild(spanIn);
                            li.appendChild(boldSubCategory);
                            link.appendChild(li);
                            ul.appendChild(link);
                        }
                    } else {
                        ul.innerHTML = "";
                        searchResultList.classList.add("display-hide")
                    }
                }
            })
        }
    }
};