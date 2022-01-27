"use strict";

window.onload = function() {

    var TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    var _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    var quantities = [];
    var prices = [];

    for (var i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantities[i] = _quantity;
       if (_price) {
           prices[i] = _price;
       } else {
           prices[i] = 0;
       }
        }

    var order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    var order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    $('.order_form').on('click', 'input[type="number"]', function() {
        console.log('kjsdfklj');
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitem-', '').replace('-quantity', ''));

        if(prices[orderitem_num]){
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantities[orderitem_num];
            quantities[orderitem_num] = orderitem_quantity;
            order_summary_update(prices[orderitem_num], delta_quantity)
        }
    });

    $('.order_form').on('click', 'input[type=checkbox]', function(){
        console.log('aaaaaa');
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitem-', '').replace('-quantity', ''));
        if(target.checked){
            delta_quantity = -quantities[orderitem_num];
        } else {
            delta_quantity = quantities[orderitem_num];
        }
        order_summary_update(prices[orderitem_num], delta_quantity);
    });

    function order_summary_update(orderitem_price, delta_quantity){
        delta_cost = orderitem_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(fractionDigits:2));
        order_total_quantity = order_total_quantity + delta_quantity;

            $('.order_total_quantity').html(order_total_quantity.toString());
            $('.order_total_cost').html(order_total_cost.toString());

    };

}