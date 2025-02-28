"""
URL configuration for e_commerce_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import *
from django.conf.urls.static import *
from django.contrib.auth import views as auth_views

from .import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('master/',views.Master,name = 'masters'),
    path('',views.Index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('account/',include('django.contrib.auth.urls')),
path(
        "account/password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html"  # Force Django to use your template
        ),
        name="password_reset"),
        path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
        path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
        path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
        path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
        path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
        path('cart/cart-detail/', views.cart_detail, name='cart_detail'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)