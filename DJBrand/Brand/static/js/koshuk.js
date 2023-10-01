$(document).ready(function() {
    // Функція для оновлення кількості товару у кошику
    function updateQuantity(productIndex, quantity) {
        console.log('updateQuantity called');
        console.log('productIndex:', productIndex);
        console.log('quantity:', quantity);

            // Перевірка, чи не перевищує нова кількість максимальне значення
    if (quantity > 50) {
        quantity = 50;
    }

        var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: 'Koshuk',
            data: {
                csrfmiddlewaretoken: csrfToken,
                action: 'update',
                product_index: productIndex,
                quantity: quantity,
            },
            dataType: 'json',
            success: function(response) {
            console.log('response.old_quantity:', response.old_quantity);

                if (response.result === 'success') {
                    // Оновлення кількості товару у вигляді
                    var taskElement = $('.task').eq(productIndex);
                    taskElement.find('.quantity-value').text(quantity);

                // Оновлення ціни товару
                var productPriceElement = taskElement.find('.price p');
                var productPrice = parseFloat(productPriceElement.data('price').replace(/ /g, ''));
                var newProductPrice = productPrice * quantity;
                productPriceElement.text(newProductPrice.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}).replace(/,/g, '.') + ' UAH');


                // Оновлення загальної суми кошика
                var totalPriceElement = $('#total-price');
                var currentTotalPrice = parseFloat(totalPriceElement.text().replace('Загальна сума:', '').replace(/ /g, '').trim());
                var newTotalPrice = currentTotalPrice + (quantity - response.old_quantity) * productPrice;
                totalPriceElement.text('Загальна сума: ' + newTotalPrice.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}).replace(/,/g, ' '));

                // Отримання текстового значення загальної суми кошика
                var totalPriceText = totalPriceElement.text().replace('Загальна сума:', '').replace(/ /g, '').trim();

                // Перетворення текстового значення на число
                var totalPrice = parseFloat(totalPriceText);



                } else {
                    alert('Помилка оновлення кількості товару');
                }
            },
            error: function() {
                alert('Помилка оновлення кількості товару');
            }
        });
    }

    // Обробка кліку на кнопці "-"
    $('.decrease-quantity').click(function() {
        console.log('Decrease button clicked');
        var taskElement = $(this).closest('.task');
        var productIndex = $('.task').index(taskElement);
        var quantityElement = taskElement.find('.quantity-value');
        console.log('quantityElement.length:', quantityElement.length);

        console.log('quantityElement.text():', quantityElement.text());

        var quantity = parseInt(quantityElement.text()) - 1;
        console.log('quantity:', quantity);
        console.log('isNaN(quantity):', isNaN(quantity));

        if (!isNaN(quantity) && quantity >= 0) {
            console.log('Calling updateQuantity');
            updateQuantity(productIndex, quantity);
        }
    });

    // Обробка кліку на кнопці "+"
    $('.increase-quantity').click(function() {
        console.log('Increase button clicked');
        var taskElement = $(this).closest('.task');
        var productIndex = $('.task').index(taskElement);
        var quantityElement = taskElement.find('.quantity-value');
        console.log('quantityElement.length:', quantityElement.length);

        console.log('quantityElement.text():', quantityElement.text());
        var quantity = parseInt(quantityElement.text()) + 1;
        console.log('quantity:', quantity);
        console.log('isNaN(quantity):', isNaN(quantity));
        if (!isNaN(quantity)) {
            console.log('Calling updateQuantity');
            updateQuantity(productIndex, quantity);
        }
    });
});

