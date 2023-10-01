from django import forms
from django.contrib import admin
from .models import ProductCatalog, Image, Basket, Order, OrderItem
from .forms import OrderForm
from django.utils import timezone


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class ProductAdminCatalogForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = ProductCatalog
        fields = '__all__'


class ProductAdminCatalog(admin.ModelAdmin):
    form = ProductAdminCatalogForm
    inlines = [ImageInline]
    list_display = ['id', 'title', 'price', 'discount',
                    'size', 'description', 'description_detail']
    search_fields = ['title', 'description']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        images = request.FILES.getlist('images')
        for image in images:
            Image.objects.create(product=obj, image=image)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['images'].widget.attrs['multiple'] = True
        form.base_fields['images'].widget.attrs['name'] = 'images'
        return form

class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_timestamp')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__title')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'first_name', 'last_name', 'email', 'phone_number', 'country', 'city', 'payment_method', 'call_me', 'order_datetime')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'quantity', 'price', 'total_price', 'order', 'order_number', 'order_datetime')
    search_fields = ('product_title', 'order__first_name', 'order__last_name', 'order__email', 'order__order_number')

    def order_number(self, obj):
        return obj.order.order_number  # Отримайте номер замовлення через зовнішній ключ

    def order_datetime(self, obj):
        return obj.order.order_datetime

    order_number.short_description = 'Order Number'  # Задайте короткий опис для колонки
    order_datetime.short_description = 'Order Datetime'


admin.site.register(Basket, BasketAdmin)
admin.site.register(ProductCatalog, ProductAdminCatalog)
admin.site.register(Image)

