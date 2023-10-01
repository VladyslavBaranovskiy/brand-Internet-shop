from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm, DeleteTaskForm, AuthUserForm, RegisterUserForm, OrderForm
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import Profile
from django import forms
from django.http import HttpResponse, JsonResponse
from .models import ProductCatalog
from .models import Order, OrderItem
from django.utils import timezone
from datetime import timedelta




def koshuk(request):



    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            number = request.POST.get('number')
            product_id = request.POST.get('product_id')
            product_title = request.POST.get('product_title')
            product_price = request.POST.get('product_price')

            # Отримання списку товарів з сесії або створення нового списку
            products = request.session.get('products', [])

            # Перевірка, чи товар з даним product_id вже існує у кошику
            product_exists = False
            for product in products:
                if product['product_id'] == product_id:
                    # Оновлення даних товару
                    product['number'] = number
                    product['product_title'] = product_title
                    product['product_price'] = product_price
                    product_exists = True
                    break

            # Якщо товар не існує у кошику, додавання нового товару до списку
            if not product_exists:
                products.append({
                    'number': number,
                    'product_id': product_id,
                    'product_title': product_title,
                    'product_price': product_price,
                })

            # Оновлення даних у сесії
            request.session['products'] = products

            response_data = {
                'result': 'success',
                'message': 'Товар додано до кошика'
            }
            return JsonResponse(response_data)
        elif action == 'remove':
            product_index = int(request.POST.get('product_index'))

            # Отримання списку товарів з сесії
            products = request.session.get('products', [])

            # Видалення товару зі списку за індексом
            if 0 <= product_index < len(products):
                del products[product_index]

                # Оновлення даних у сесії
                request.session['products'] = products

            return redirect('Koshuk')
        elif action == 'update':
            product_index = int(request.POST.get('product_index'))
            quantity = int(request.POST.get('quantity'))
            print(f'quantity: {quantity}')

            # Отримання списку товарів з сесії
            products = request.session.get('products', [])

            # Оновлення кількості товару у списку
            if 0 <= product_index < len(products):
                old_quantity = products[product_index]['number']
                products[product_index]['number'] = quantity

                # Оновлення даних у сесії
                request.session['products'] = products

                response_data = {
                    'result': 'success',
                    'message': 'Кількість товару оновлено',
                    'old_quantity': old_quantity,
                }
            else:
                response_data = {
                    'result': 'error',
                    'message': 'Помилка оновлення кількості товару'
                }
            return JsonResponse(response_data)

        else:
            response_data = {
                'result': 'error',
                'message': 'Невідома дія'
            }
            return JsonResponse(response_data)
    else:
        # Отримання списку товарів з сесії
        products = request.session.get('products', [])

        # Отримання ціни за певну кількість товару
        for product in products:
            product_price = float(product['product_price'].replace(',', '.').replace(' ', ''))

            product_total_price = int(product['number']) * product_price
            product['product_total_price'] = product_total_price

        # Обчислення загальної суми кошика
        total_price = 0
        for product in products:
            total_price += product['product_total_price']

        # Отримання списку фотографій для кожного товару
        for product in products:
            product_obj = ProductCatalog.objects.get(id=product['product_id'])
            product['images'] = product_obj.images.all()[:2]

        # Передача даних у контекст шаблону
        context = {
            'products': products,
            'total_price': total_price,
        }

        # Перевірка значення параметра action
        if request.method == 'POST' and request.POST.get('action') == 'add':
            context['product_total_price'] = product_total_price

        return render(request, 'Brand/Koshuk.html', context)




def golovna(request):
    tasks = Task.objects.order_by('-id') #[:1]
    return render(request, 'Brand/index.html', {'title':'BVO', 'tasks':tasks})


def catalog(request):
    products = ProductCatalog.objects.all()
    if request.method == 'POST':
        number = request.POST.get('number')
        product_id = request.POST.get('product_id')
        product_title = request.POST.get('product_title')
        product_price = request.POST.get('product_price')

        # збереження даних з форми у сесії
        request.session['number'] = number
        request.session['product_id'] = product_id
        request.session['product_title'] = product_title
        request.session['product_price'] = product_price

    return render(request, 'Brand/Catalog.html', {'products': products})

def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Зберігайте дані форми у новому замовленні
            order = form.save()
            order.order_datetime = timezone.now()  # Отримайте поточну дату та час
            # Додайте 3 години до години
            adjusted_datetime = order.order_datetime + timedelta(hours=3)
            formatted_datetime = adjusted_datetime.strftime('%d-%m-%Y, %H:%M:%S')
            order.save()

            # Отримання списку товарів з сесії
            products = request.session.get('products', [])

            # Зберігання товарів у базі даних, пов'язаних зі зробленим замовленням
            for product_data in products:
                # Видалення всіх пробілів із рядка ціни тут
                product_price_str = product_data['product_price'].replace(' ', '')
                product_price = float(product_price_str.replace(',', '.'))

                OrderItem.objects.create(
                    order=order,
                    product_title=product_data['product_title'],
                    quantity=product_data['number'],
                    price=product_price
                )

            # Очистити кошик після оформлення замовлення
            request.session['products'] = []

            # Отправити номер замовлення у відповіді на клієнтську сторінку
            response_data = {'success': True, 'order_number': order.order_number, 'order_datetime': formatted_datetime}
            return JsonResponse(response_data)

        response_data = {'success': False}
        return JsonResponse(response_data)
    else:
        form = OrderForm()

    # Отримання списку товарів з сесії
    products = request.session.get('products', [])

    # Отримання ціни за певну кількість товару
    for product in products:
        # Видалення всіх пробілів із рядка ціни тут
        product_price_str = product['product_price'].replace(' ', '')
        product_price = float(product_price_str.replace(',', '.'))

        product_total_price = int(product['number']) * product_price
        product['product_total_price'] = product_total_price

    # Обчислення загальної суми кошика
    total_price = 0
    for product in products:
        total_price += product['product_total_price']

    # Отримання списку фотографій для кожного товару
    for product in products:
        product_obj = ProductCatalog.objects.get(id=product['product_id'])
        product['images'] = product_obj.images.all()[:2]

    # Передача даних у контекст шаблону
    context = {
        'products': products,
        'total_price': total_price,
        'form': form,  # Додавання форми до контексту
    }
    return render(request, 'Brand/MakeAnOrder.html', context)

def successorder(request):
    return render(request, 'Brand/SuccessOrder.html')

def chanel(request):
    return render(request, 'Chanel/Chanel.html')

def louis(request):
    return render(request, 'Louis/Louis.html')

def dolce(request):
    return render(request, 'Dolce/Dolce.html')

def vovk(request):
    return render(request, 'Vovk/Vovk.html')

def versace(request):
    return render(request, 'Versace/Versace.html')

def ellesse(request):
    return render(request, 'Ellesse/Ellesse.html')

def hm(request):
    return render(request, 'H&M/H&M.html')

def colins(request):
    return render(request, 'Colins/Colins.html')

def lcw(request):
    return render(request, 'LCW/LCW.html')

def sinsay(request):
    return render(request, 'Sinsay/Sinsay.html')

def about(request):
    return render(request, 'Brand/About.html')

def success(request):
    return render(request, 'Brand/Success.html')

def product_detail(request, product_id):
    product = get_object_or_404(ProductCatalog, id=product_id)
    if request.method == 'POST':
        number = request.POST.get('number')
        product_id = request.POST.get('product_id')
        product_title = request.POST.get('product_title')
        product_price = request.POST.get('product_price')

        # збереження даних з форми у сесії
        request.session['number'] = number
        request.session['product_id'] = product_id
        request.session['product_title'] = product_title
        request.session['product_price'] = product_price

    return render(request, 'Product_detail/product_detail.html', {'product': product})

def tasks(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks
    }
    return render(request, 'Brand/tasks.html', context)

def create(request):
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Tasks')
        else:
            error = 'Заповніть коректно'
    form = TaskForm()
    context = {
        'form': form
    }
    return render(request, 'Brand/Create.html', context)

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect('Tasks')
    else:
        delete_form = DeleteTaskForm(instance=task)
        return render(request, 'delete_task.html', {'delete_form': delete_form, 'task': task})


class Login(LoginView):
    template_name = 'Brand/Login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('Head')

    def form_valid(self, form):
        user = form.get_user()
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=user)
        profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url

class Register(CreateView):

    model = User
    template_name = 'Brand/Register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('Success')
    def form_valid(self,form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        aut_user = authenticate(username=username,password=password)
        login(self.request, aut_user)
        profile = Profile.objects.create(user=aut_user, first_name=first_name, last_name=last_name)

        return form_valid

class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('Head')

class ProfileSettingsForm(forms.ModelForm):
    username = forms.CharField(label='Позивний', disabled=True, max_length=20)
    email = forms.EmailField(label='Електронна пошта', disabled=True)
    first_name = forms.CharField(label='Ім\'я', max_length=30)
    last_name = forms.CharField(label='Прізвище', max_length=29)
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), label="Фото", required=False,
        error_messages={'required': 'Фото не обрано'})

    delete_avatar = forms.BooleanField(label='Видалити фото', required=False)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        self.fields['email'].initial = self.instance.user.email
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['avatar'].widget.attrs['class'] = 'form-control custom-file-input  border-0'
        self.fields['avatar'].widget.attrs['placeholder'] = 'Обрати Фото'

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile.user

def profile_settings(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if 'delete' in request.POST.keys():  # Перевірка натискання кнопки "Видалити"
                profile.avatar.delete()  # Видалення фотографії
            else:
                form.save()
    else:
        form = ProfileSettingsForm(instance=profile)

    avatar_url = profile.avatar.url if profile.avatar else None

    context = {
        'form': form,
        'full_name': f'{profile.first_name} {profile.last_name}',
        'avatar_url': avatar_url,

    }

    return render(request, 'Brand/profile_settings.html', context)












