$(document).ready(function() {
    $('#MakeAnOrder_id').submit(function(event) {
        event.preventDefault();  // Заборонити стандартну подію форми

        $.ajax({
            type: 'POST',
            url: 'MakeAnOrder',  // Замініть "make_order" на свій URL
            data: $(this).serialize(),
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    // Показати повідомлення із номером замовлення
                    var orderNumber = data.order_number;
                    var orderDatetime = data.order_datetime;  // Отримайте дату та час замовлення
                    var successMessage = 'Ваше замовлення прийнято!'+'\nНомер замовлення: ' + orderNumber + '\nЗамовлення прийнято: ' + orderDatetime +
                    '\nДякуємо, за замовлення! Очікуйте повідомлення про доставку!';
                    alert(successMessage);
                } else {
                    alert('Помилка при оформленні замовлення.');
                }
            },
            error: function() {
                alert('Помилка при відправці запиту на сервер.');
            }
        });
    });
});