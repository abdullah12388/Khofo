var gallery1 = document.querySelector('#singleSlider');
if (gallery1) {
    var gallery_scroller1 = gallery1.children[0];
    var gallery_item_size1 = gallery_scroller1.children[0].clientWidth;
    gallery1.querySelector('.btn.next').onclick = function () {
      gallery_scroller1 = gallery1.children[0];
      gallery_item_size1 = gallery_scroller1.children[0].clientWidth;
      gallery_scroller1.scrollBy(gallery_item_size1, 0);
    };
    gallery1.querySelector('.btn.prev').onclick = function () {
      gallery_scroller1 = gallery1.children[0];
      gallery_item_size1 = gallery_scroller1.children[0].clientWidth;
      gallery_scroller1.scrollBy(-gallery_item_size1, 0)
    }
}
