from django.contrib import admin
from .models import User, Category, Item

class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ['available', 'shoppers']

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
