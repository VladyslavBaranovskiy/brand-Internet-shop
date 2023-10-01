from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Brand.urls')),
    path('accounts/', include('allauth.urls')),
    path('Login/', include('Brand.urls'))
]
