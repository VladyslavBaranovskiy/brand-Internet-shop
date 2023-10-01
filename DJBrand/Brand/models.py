from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    title = models.CharField('Tasks', max_length=50)
    task = models.TextField('Опис')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачі'

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class ProductCatalog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=35, verbose_name='Назва товару')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ціна')
    discount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ціна зі знижкою', blank=True, null=True,
                                   help_text='Якщо знижка є - введіть ціну, якщо немає то залиште 0', default=0)
    size = models.CharField(max_length=255, verbose_name='Розміри в наявності')
    description_prefix = models.CharField(
        max_length=3,
        default='©',
        editable=False,
    )
    shop_name = models.CharField(
        max_length=27,
        verbose_name='Магазин',
    )
    description_detail = models.TextField(verbose_name='Детальний опис')

    def formatted_price(self):
        return "{:,.2f}".format(self.price).replace(",", " ")

    def description(self):
        return f'{self.description_prefix} {self.shop_name}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Каталог'

    def __str__(self):
        return self.title


class Image(models.Model):
    product = models.ForeignKey(ProductCatalog, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', verbose_name='Фото')
    alt_text = models.CharField(max_length=100)

    def __str__(self):
        return self.alt_text



class CartManager(models.Manager):
    def get_or_create_cart(self, user):
        try:
            cart = self.get(user=user)
        except Cart.DoesNotExist:
            cart = self.create(user=user)
        return cart

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductCatalog, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.title} ({self.quantity})"

class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=ProductCatalog, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукти: {self.product.title}'

    def sum(self):
        return self.product.price * self.quantity

class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=254)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    call_me = models.CharField(max_length=100)

    # Використовуйте поле AutoField для унікального номера замовлення
    order_number = models.AutoField(primary_key=True)

    # Додайте поле для дати та часу замовлення
    order_datetime = models.DateTimeField(auto_now_add=True)  # Автоматично додає поточну дату та час при створенні запису

    # Решта полів та методів моделі, які ви вже маєте

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_title = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price

