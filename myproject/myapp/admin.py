from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Person, Product, OrderHeader, OrderPart, OrderItem, Party

admin.site.register(Person)
admin.site.register(Product)
admin.site.register(OrderHeader)
admin.site.register(OrderPart)
admin.site.register(OrderItem)
admin.site.register(Party)