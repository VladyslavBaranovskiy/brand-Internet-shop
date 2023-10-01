from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import delete_task

urlpatterns = [
    path('',views.golovna, name='Head'),
    path('admin/', admin.site.urls),
    path('Koshuk', views.koshuk, name='Koshuk'),
    path('MakeAnOrder', views.order, name='MakeAnOrder'),
    path('SuccessOrder', views.successorder, name='SuccessOrder'),
    path('Create',views.create, name='Create'),
    path('About',views.about, name='About'),
    path('Catalog', views.catalog, name='Catalog'),
    path('Chanel', views.chanel, name='Chanel'),
    path('Louis', views.louis, name='Louis'),
    path('Dolce', views.dolce, name='Dolce'),
    path('Vovk', views.vovk, name='Vovk'),
    path('Versace', views.versace, name='Versace'),
    path('Ellesse', views.ellesse, name='Ellesse'),
    path('H&M', views.hm, name='H&M'),
    path('Colins', views.colins, name='Colins'),
    path('LCW', views.lcw, name='LCW'),
    path('Sinsay', views.sinsay, name='Sinsay'),
    path('task/<int:pk>/delete/', delete_task, name='delete_task'),
    path('Login', views.Login.as_view(), name='Login'),
    path('Register', views.Register.as_view(), name='Register'),
    path('Logout', views.MyProjectLogout.as_view(), name='Logout'),
    path('Success', views.success, name='Success'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('Tasks', views.tasks, name='Tasks'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)