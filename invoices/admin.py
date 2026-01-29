from django.contrib import admin
from .models import Invoice, InvoiceItem

# Register your models here.


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]
    readonly_fields = ('total', 'created_at')
