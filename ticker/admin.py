from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Transaction, Benchmark

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "ticker", "units", "cost_basis", "quote_currency", "timestamp")

class BenchmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "ticker", "units", "timestamp")

admin.site.register(User, UserAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Benchmark, BenchmarkAdmin)
