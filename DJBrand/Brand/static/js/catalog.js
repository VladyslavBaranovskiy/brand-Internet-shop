$(document).ready(function(){
    $('.form_buying_product').on('submit', function(e){
        e.preventDefault();

        var form = $(this); // Отримуємо посилання на поточну форму
        var nmb = form.find('input[name="number"]').val();
        var submit_btn = form.find('.btn-buy');
        var product_id = submit_btn.data("product_id");
        var product_title = submit_btn.data("product_title");
        var product_price = submit_btn.data("product_price");

        var csrf_token = form.find('input[name="csrfmiddlewaretoken"]').val();

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
                // Обробляємо успішну відповідь від сервера
            },
            error: function(error) {
                // Обробляємо відповідь про помилку від сервера
            }
        });

        return false; // Відміняємо дії за замовчуванням для submit
    });
});

