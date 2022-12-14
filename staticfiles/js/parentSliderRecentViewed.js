var parent2 = document.getElementById('recentViewed');
if (parent2) {
    var gallery2;
    var gallery_scroller2;
    var gallery_item_size2;
    var d = parent2.children.length;
    for (var x = 0; x < d; x++) {
        test_(x)
    }

    function test_(w) {
        "use strict";
        gallery2 = parent2.children[w].children[1].children[0];
        gallery_scroller2 = gallery2.children[0];
        gallery_item_size2 = gallery_scroller2.children[w].clientWidth;
        gallery2.querySelector('.btn.next').onclick = function () {
            gallery2 = parent2.children[w].children[1].children[0];
            gallery_scroller2 = gallery2.children[0];
            gallery_item_size2 = gallery_scroller2.children[w].clientWidth;
            gallery_scroller2.scrollBy(gallery_item_size2, 0)
        };
        gallery2.querySelector('.btn.prev').onclick = function () {
            gallery2 = parent2.children[w].children[1].children[0];
            gallery_scroller2 = gallery2.children[0];
            gallery_item_size2 = gallery_scroller2.children[w].clientWidth;
            gallery_scroller2.scrollBy(-gallery_item_size2, 0)
        }
    }
}