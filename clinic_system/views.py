from django.shortcuts import render
from products.models import Product
from invoices.models import Invoice
from django.db import models
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    total_products = Product.objects.count()
    total_invoices = Invoice.objects.count()
    total_sales = sum(inv.total for inv in Invoice.objects.all())
    
    # Calculate total inventory value: sum of (quantity * wholesale price) for all products
    inventory_value = 0
    for product in Product.objects.all():
        # Get the wholesale price for the product
        wholesale_tier = product.price_tiers.filter(key='wholesale').first()
        if wholesale_tier:
            wholesale_price = wholesale_tier.price
        else:
            wholesale_price = product.price
        inventory_value += product.quantity * wholesale_price
    
    # Calculate net profit: (selling price - wholesale price) * quantity
    net_profit = 0
    from invoices.models import InvoiceItem
    for item in InvoiceItem.objects.all():
        selling_price = item.price
        wholesale_price = item.product.unit_price_for_quantity(item.quantity)
        profit_per_item = (selling_price - wholesale_price) * item.quantity
        net_profit += profit_per_item

    context = {
        'total_products': total_products,
        'total_invoices': total_invoices,
        'total_sales': total_sales,
        'inventory_value': round(inventory_value, 2),
        'net_profit': round(net_profit, 2),
    }

    return render(request, 'dashboard.html', context)