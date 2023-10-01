$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);
    form.on('submit', function(e){
        e.preventDefault();
        console.log('123');
        var nmb = $('#number').val();
        console.log(nmb)
        var submit_btn = $('#submit_btn');
        var product_id = submit_btn.data("product_id");
        var product_title = submit_btn.data("product_title");
        var product_price = submit_btn.data("product_price");
        console.log(product_id);
        console.log(product_title);

        var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: {
                "csrfmiddlewaretoken": csrf_token,
                "action": "add",
                "number": nmb,
                "product_id": product_id,
                "product_title": product_title,
                "product_price": product_price,
            },
            success: function(data) {
                // handle successful response from server
            },
            error: function(error) {
                // handle error response from server
            }
        });
    })
});
