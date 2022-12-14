function myFunction(x) {
    // If media query matches
    let checkOut = document.getElementById('cartDiv');
    let imgTitle = document.getElementById('imgTitle');
    let nameTitle = document.getElementById('nameTitle');
    let specificationsTitle = document.getElementById('specificationsTitle');
    let quantityTitle = document.getElementById('quantityTitle');
    let priceTitle = document.getElementById('priceTitle');
    let totalTitle = document.getElementById('totalTitle');
    let removeTitle = document.getElementById('removeTitle');
    let cartBody = document.getElementById('cartBody');
    let hr = document.getElementById('hr');
    let c = checkOut.children.length;
    for (let o = 0; o < c; o++) {
        let row = checkOut.children[o];
        let img = row.children[0];
        let name = row.children[1];
        let specifications = row.children[2];
        let quantity = row.children[3];
        let price = row.children[4];
        let total = row.children[5];
        let remove = row.children[6];
        if (x.matches) {
            // cartBody
            cartBody.classList.replace("cart-body", "cart-body2");
            // hr
            hr.classList.add("title-cart-hr");
            // IMG
            imgTitle.classList.replace("col-3", "col-1");
            img.classList.replace("col-3", "col-1");
            img.classList.replace("cart-product-img", "cart-product-img2");
            console.log("img1 = ", img);
            // Name
            nameTitle.classList.replace("col-2", "col-1");
            name.classList.replace("col-2", "col-1");
            name.classList.replace("cart-product-1", "cart-product-2");
            // name.classList.replace("cart-product-img", "cart-product-img2");
            console.log("name = ", name);
            // specifications
            specificationsTitle.classList.replace("col-3", "col-1");
            specifications.classList.replace("col-3", "col-1");
            specifications.classList.replace("cart-product-1", "cart-product-2");
            // specifications.classList.replace("cart-product-img", "cart-product-img2");
            console.log("specifications = ", specifications);
            // quantity
            quantity.classList.replace("col-3", "col-1");
            quantity.classList.replace("cart-product-1", "cart-product-2");
            // quantity.classList.replace("cart-product-img", "cart-product-img2");
            console.log("quantity = ", quantity);
            // price
            price.classList.replace("cart-product-1", "cart-product-2");
            // price.classList.replace("cart-product-img", "cart-product-img2");
            console.log("price = ", price);
            // total
            total.classList.replace("cart-product-1", "cart-product-2");
            // total.classList.replace("cart-product-img", "cart-product-img2");
            console.log("total = ", total);
            // remove
            remove.classList.replace("cart-product-1", "cart-product-2");
            // remove.classList.replace("cart-product-img", "cart-product-img2");
            console.log("remove = ", remove);

        } else {
            // cartBody
            cartBody.classList.replace("cart-body2", "cart-body");
            // hr
            hr.classList.remove("title-cart-hr");
            // IMG
            imgTitle.classList.replace("col-1", "col-3");
            img.classList.replace("col-1", "col-3");
            img.classList.replace("cart-product-img2", "cart-product-img");
            console.log("img2 = ", img);

            nameTitle.classList.replace("col-1", "col-2");
            name.classList.replace("col-1", "col-2");
            name.classList.replace("cart-product-2", "cart-product-1");
            console.log("name2 = ", name);
            // specifications
            specificationsTitle.classList.replace("col-1", "col-3");
            specifications.classList.replace("col-1", "col-3");
            specifications.classList.replace("cart-product-2", "cart-product-1");
            // quantity
            quantity.classList.replace("cart-product-2", "cart-product-1");
            console.log("quantity = ", quantity);
            // price
            price.classList.replace("cart-product-2", "cart-product-1");
            console.log("price = ", price);
            // total
            total.classList.replace("cart-product-2", "cart-product-1");
            console.log("total = ", total);
            // remove
            remove.classList.replace("cart-product-2", "cart-product-1");
            console.log("remove = ", remove);

        }
    }

}

let cartResponse = window.matchMedia("(max-width: 768px)");
myFunction(cartResponse); // Call listener function at run time
cartResponse.addListener(myFunction);