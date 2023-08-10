from django.contrib import admin
from .models import Customer, Diary, Snippet, Dictionary, ToDo, Quote, Cashier
import csv


# # Register your models here.
# @admin.register(Job)
# class JobAdmin(admin.ModelAdmin):
#     list_display = ['id', 'order_number', 'customer', 'status']
#     list_filter = ['created', 'updated']
#     list_editable = ['status']

@admin.register(Cashier)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'name', 'last_name', 'password', 'is_deleted', 'is_administrator', 'is_active', 'login_at']
    list_filter = ['user_name', 'name', 'last_name']
    list_editable = ['is_deleted', 'is_administrator', 'is_active', 'password']
    
