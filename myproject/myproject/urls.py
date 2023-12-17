"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from rest_framework.routers import DefaultRouter

# myproject/urls.py
from myapp.views import add_order_items
from django.contrib import admin
from django.urls import path, include
from myapp.views import PersonViewSet, OrderViewSet, get_orders, get_order, update_order, home

router = DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('add_order_items/', add_order_items, name='add_order_items'),
    path('get-orders/', get_orders, name='get_orders'),
    path('get-order/<str:order_id>/', get_order, name='get_order'),
    path('update-order/<str:order_id>', update_order, name='update_order'),
    path('', home, name='home'), # ye homepage jahan api endpoints hain
]

