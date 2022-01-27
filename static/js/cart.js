"use strict";
window.onload = function() {
    $('.basket_list').on('change', "input[type='number']", function(event) {
        let t_href = event.target;
        $.ajax({
            url: "/cart/api/edit/" + t_href.name + "/" + t_href.value + "/",
            success: function(data){
            $('.basket_list').html(data.result);
            },
        });
    });
}
//window.onload = function () {
//    document.querySelector('.basket_record input[type="number"]').addEventListener('click', function(event){
//    const href = event.target;
//
//    fetch(`/cart/api/edit/${href.name}/${href.value}/`)
//        .then((data) => data.json())
//        .then((json) => {
//            document.querySelectorAll('.basket_list').innerHTML = json.result;
//        })
//
//    event.preventDefault();
//    })
//}