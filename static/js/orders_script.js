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
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));

        if(prices[orderitem_num]){
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantities[orderitem_num];
            quantities[orderitem_num] = orderitem_quantity;
            var sum_price = (quantities[orderitem_num] * prices[orderitem_num]).toFixed(2);
            console.log(sum_price)
            $('.orderitems-' + orderitem_num + '-sum_price').html(sum_price.toString())
            order_summary_update(prices[orderitem_num], delta_quantity);
        }
    });


    function order_summary_update(orderitem_price, delta_quantity){

        delta_cost = orderitem_price * delta_quantity;
        order_total_cost = (Number(order_total_cost)+delta_cost).toFixed(2)
        order_total_quantity = order_total_quantity + delta_quantity;

            $('.order_total_quantity').html(order_total_quantity.toString());
            $('.order_total_cost').html(order_total_cost.toString());

    };

    $('.formset_row').formset({
       addText: 'добавить продукт',
       deleteText: 'удалить',
       prefix: 'orderitems',
       removed: delete_order_item,
    });


    function delete_order_item(row){
        var target_name = row[0].querySelector('input').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantities[orderitem_num];
        order_summary_update(prices[orderitem_num], delta_quantity);
    };


    $('.formset_row').on('change', 'select', function(event) {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''))
        var product_id = target.value;
        if(product_id){
            $.ajax({
                url: "/order/product/price/"+ product_id + "/",
                success: function(data){
                    if(data.price){
                        prices[orderitem_num]=data.price;
                        if(isNaN(quantities[orderitem_num])){
                            quantities[orderitem_num]=0;
                        }
                        var sum_price = (quantities[orderitem_num] * data.price).toFixed(2)
                        var price_string = '<span>' + data.price.toString()+ '</span> руб';
                        var sum_price_string = '<span>' + sum_price.toString()+ '</span> руб';
                        var current_tr = $('.order_form table').find('tr:eq('+ (orderitem_num + 1) +')');
                        current_tr.find('td:eq(2)').html(price_string);
                        current_tr.find('td:eq(3)').html(sum_price_string);
                        $('.order_total_quantity').html(order_total_quantity.toString());
                        $('.order_total_cost').html(order_total_cost.toString());
                    }

                }
            })
        }


    });

}