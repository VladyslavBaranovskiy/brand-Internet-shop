from .models import Task
from django import forms
from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy
from .models import Profile, Order
from django.core.validators import RegexValidator


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "task"]
        widgets = {"title": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть назву'
        }),
            "task": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть опис'
            })
        }

class EditTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "task"]
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву'
            }),
            "task": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть опис'
            })
        }

class DeleteTaskForm(forms.ModelForm):
    confirm_title = forms.CharField(label='Введіть назву завдання для підтвердження видалення', required=True)

    class Meta:
        model = Task
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        confirm_title = cleaned_data.get('confirm_title')
        if confirm_title != self.instance.title:
            raise forms.ValidationError('Введіть правильну назву завдання для підтвердження видалення')
        return cleaned_data

class AuthUserForm(AuthenticationForm, forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Логін', 'class': 'form-control', 'style': 'margin-bottom: 20px;'}),
        label=''
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control', 'style': 'margin-bottom: 30px;', 'id': 'id_password1'}),
        label=''
    )
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class RegisterUserForm(UserCreationForm):

    first_name = forms.CharField(
        label="",
        max_length=30,
        widget=forms.TextInput( attrs={'placeholder': 'Ім\'я', 'class': 'form-control', 'style': 'margin-bottom: 20px;'} )
    )

    last_name = forms.CharField(
        label="",
        max_length=29,
        widget=forms.TextInput(attrs={'placeholder': 'Прізвище', 'class': 'form-control', 'style': 'margin-bottom: 20px;'})
         )

    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={'placeholder': 'Логін', 'class': 'form-control', 'style': 'margin-bottom: 30px;'}),
        label=''
    )

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={'placeholder': 'Електронна пошта', 'class': 'form-control', 'style': 'margin-bottom: 30px;'}),
        label=''
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введіть пароль', 'class': 'form-control', 'style': 'margin-bottom: 20px;', 'id': 'id_password1'}),
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Підтвердьте пароль', 'class': 'form-control', 'style': 'margin-bottom: 20px;', 'id': 'id_password1'}),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Логін'
        self.fields['username'].widget.attrs['class'] = 'form-control'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Паролі не співпадають')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):

    first_name = forms.CharField(label="Ім'я")
    last_name = forms.CharField(label="Прізвище")
    username = forms.CharField(label='Логін')
    email = forms.EmailField(label='Електронна пошта')
    avatar = forms.ImageField(label="Фото")

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'avatar', 'email']


    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile.user

class OrderForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={'placeholder': "Ім'я *", 'class': 'form-control', 'style': 'margin-bottom: 30px;'}),
        label='',
        required=True
    )
    last_name = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={'placeholder': "Прізвище *", 'class': 'form-control', 'style': 'margin-bottom: 30px;'}),
        label='',
        required=True
    )
    middle_name = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={'placeholder': "По батькові *", 'class': 'form-control', 'style': 'margin-bottom: 30px;'}),
        label='',
        required=True
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={'placeholder': 'Електронна пошта *', 'class': 'form-control', 'style': 'margin-bottom: 30px;'}),
        label='',
        required=True
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефону повинен бути в форматі: '+999999999'. Максимум 15 цифр дозволено."
    )

    phone_number = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={'placeholder': 'Номер телефону *', 'class': 'form-control', 'style': 'margin-bottom: 30px;'}),
        label='',
        validators=[phone_regex],
        required=True
    )

    COUNTRY_CHOICES = [
        ('', 'Виберіть країну *'),
        ('Україна', 'Україна'),
        ('США', 'Сполучені Штати'),
        ('Канада', 'Канада'),
        # Додайте інші країни за потребою
    ]

    country = forms.ChoiceField(
        label="",
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='',
        required=True
    )

    city = forms.CharField(
        max_length=254,
        label="",
        widget=forms.TextInput(
            attrs={'placeholder': 'Місто і область *', 'class': 'form-control', 'style': 'margin-bottom: 30px;'}),
        required=True
    )


    PAYMENT_CHOICES = [
        ('Монобанк', 'Оплата на сайті Monopay'),
        ('Реквізити IBAN', 'Оплата за реквізитами IBAN'),
        ('Післяплата', 'Післяплата'),
    ]


    payment_method = forms.ChoiceField(
        label='',
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(),
        required=True
    )

    CALL_CHOICES = [
        ('', 'Виберіть один із варіантів'),
        ('Не телефонуйте', 'Не дзвоніть мені, я впевнена(ий) в замовленні'),
        ('Зателефонуйте', 'Прошу зателефонувати після замовлення'),
    ]

    call_me = forms.ChoiceField(
        label="Зателефонувати після замовлення? *",
        choices=CALL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'margin-bottom: 30px;'}),
        initial='',
        required=True
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'middle_name', 'phone_number',
                  'email', 'country', 'city', 'payment_method', 'call_me']

