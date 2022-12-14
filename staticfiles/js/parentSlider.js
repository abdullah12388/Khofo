$(document).ready(function () {
    var parent = document.getElementById('fatherDiv');
    if (parent !== null) {
        if (parent.children.length !== 1) {
            var gallery;
            var gallery_scroller;
            var gallery_item_size;
            var d = parent.children.length;
            for (let x = 0; x < d; x++) {
                test_(x)
            }

            function test_(w) {
                "use strict";
                gallery = parent.children[w].children[1].children[0];
                gallery_scroller = gallery.children[0];
                gallery_item_size = gallery_scroller.children[w].clientWidth;
                gallery.querySelector('.btn.next').onclick = function () {
                    gallery = parent.children[w].children[1].children[0];
                    gallery_scroller = gallery.children[0];
                    gallery_item_size = gallery_scroller.children[w].clientWidth;
                    gallery_scroller.scrollBy(gallery_item_size, 0)
                };
                gallery.querySelector('.btn.prev').onclick = function () {
                    gallery = parent.children[w].children[1].children[0];
                    gallery_scroller = gallery.children[0];
                    gallery_item_size = gallery_scroller.children[w].clientWidth;
                    gallery_scroller.scrollBy(-gallery_item_size, 0)
                }
            }
        }
    }
});
