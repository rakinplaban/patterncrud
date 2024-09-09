from django.contrib import admin
from .models import Item

# Register your models here.

class Item_display(admin.ModelAdmin):
    list_display = ('id','name', 'description')

admin.site.register(Item, Item_display)