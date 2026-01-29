from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice, InvoiceItem
from products.models import Product
from django.forms import modelform_factory
from django.contrib.auth.decorators import login_required
import json


@login_required
def invoice_list(request):
    invoices = Invoice.objects.order_by('-created_at')
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})


@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})


@login_required
def invoice_create(request):
    if request.method == 'POST':
        # Handle JSON request for adding items
        try:
            data = json.loads(request.body)
            items = data.get('items', [])
        except json.JSONDecodeError:
            items = []

        if not items:
            return render(request, 'invoices/invoice_create.html', {
                'error': 'يجب إضافة منتج واحد على الأقل.'
            })

        # Create invoice
        invoice = Invoice.objects.create(total=0)

        # Add items to invoice
        for item in items:
            product = get_object_or_404(Product, pk=item['product_id'])
            qty = int(item['quantity'])
            unit_price = float(item['price'])

            # Validate quantity
            if qty <= 0:
                invoice.delete()
                return render(request, 'invoices/invoice_create.html', {
                    'error': 'الكمية يجب أن تكون أكبر من صفر.'
                })

            if qty > product.quantity:
                invoice.delete()
                return render(request, 'invoices/invoice_create.html', {
                    'error': f'الكمية المطلوبة من {product.name} أكبر من المخزون المتاح.'
                })

            InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=qty,
                price=unit_price
            )

        return redirect('invoices:invoice_detail', invoice_id=invoice.id)

    return render(request, 'invoices/invoice_create.html')
