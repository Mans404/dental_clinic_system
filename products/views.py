from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductPriceTier
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import ProtectedError
from django.core.paginator import Paginator
from django.http import JsonResponse
import csv
from io import TextIOWrapper


@login_required
def product_list(request):
    products = Product.objects.all().order_by('id')
    search_query = request.GET.get('search', '')
    
    # Filter products by search query
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Pagination: 10 products per page
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    products_with_tiers = []
    for p in page_obj:
        tiers = {t.key: t.price for t in p.price_tiers.all()}
        wholesale_unit = tiers.get('wholesale')
        wholesale_total = None
        try:
            if wholesale_unit is not None:
                wholesale_total = wholesale_unit * p.quantity
        except Exception:
            wholesale_total = None

        quantity_total = None
        try:
            quantity_total = p.price * p.quantity
        except Exception:
            quantity_total = None

        products_with_tiers.append({
            'product': p,
            'wholesale_unit': wholesale_unit,
            'wholesale_total': wholesale_total,
            'quantity_total': quantity_total,
        })
    return render(request, 'products/product_list.html', {
        'products': products_with_tiers, 
        'page_obj': page_obj,
        'search_query': search_query
    })


@login_required
def product_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        wholesale_price = request.POST.get('wholesale_price')

        if name and quantity.isdigit() and price.replace('.', '', 1).isdigit():
            product = Product.objects.create(
                name=name,
                quantity=int(quantity),
                price=Decimal(price)
            )

            # save only wholesale per-unit tier; other totals are computed from unit prices
            if wholesale_price and wholesale_price.replace('.', '', 1).isdigit():
                try:
                    pval = Decimal(wholesale_price)
                    ProductPriceTier.objects.update_or_create(product=product, key='wholesale', defaults={'price': pval, 'min_quantity': 1})
                except InvalidOperation:
                    pass
            return redirect('products:product_list')

        error = "الرجاء إدخال بيانات صحيحة."
        return render(request, 'products/product_form.html', {'error': error, 'tier_prices': {}})

    return render(request, 'products/product_form.html', {'tier_prices': {}})
@login_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        wholesale_price = request.POST.get('wholesale_price')

        if name and quantity.isdigit() and price.replace('.', '', 1).isdigit():
            product.name = name
            product.quantity = int(quantity)
            product.price = Decimal(price)
            product.save()

            # update or create only the wholesale per-unit tier; remove others if present
            if wholesale_price and wholesale_price.replace('.', '', 1).isdigit():
                try:
                    pval = Decimal(wholesale_price)
                    ProductPriceTier.objects.update_or_create(product=product, key='wholesale', defaults={'price': pval, 'min_quantity': 1})
                except InvalidOperation:
                    pass
            else:
                ProductPriceTier.objects.filter(product=product, key='wholesale').delete()

            # ensure computed tiers are not stored as editable values
            ProductPriceTier.objects.filter(product=product, key__in=['wholesale_for_quantity', 'quantity_price']).delete()
            return redirect('products:product_list')

        error = "الرجاء إدخال بيانات صحيحة."
        # include existing tier values when re-displaying the form
        existing = {t.key: t.price for t in product.price_tiers.all()}
        return render(request, 'products/product_form.html', {'product': product, 'error': error, 'tier_prices': existing})

    existing = {t.key: t.price for t in product.price_tiers.all()}
    return render(request, 'products/product_form.html', {'product': product, 'tier_prices': existing})
@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        try:
            product.delete()
            return redirect('products:product_list')
        except ProtectedError as e:
            # collect referencing objects to show to the user
            referencing = list(product.invoiceitem_set.all())
            error = "لا يمكن حذف هذا المنتج لأنه مستخدم في فواتير موجودة."
            return render(request, 'products/product_confirm_delete.html', {'product': product, 'error': error, 'referencing': referencing})
    return render(request, 'products/product_confirm_delete.html', {'product': product})


@login_required
def product_bulk_import(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            error = "يرجى اختيار ملف CSV."
            return render(request, 'products/product_bulk_import.html', {'error': error})
        
        csv_file = request.FILES['csv_file']
        try:
            # Read CSV file with UTF-8 encoding
            file_content = TextIOWrapper(csv_file, encoding='utf-8-sig').read()
            
            # Detect delimiter (comma or pipe)
            delimiter = ',' if ',' in file_content.split('\n')[0] else '|'
            
            # Parse CSV with detected delimiter
            csv_reader = csv.DictReader(file_content.split('\n'), delimiter=delimiter)
            
            imported_count = 0
            errors = []
            
            for row_num, row in enumerate(csv_reader, start=2):
                try:
                    if not row or not any(row.values()):
                        continue
                    
                    # Clean up column names (strip whitespace)
                    cleaned_row = {k.strip(): v.strip() if v else '' for k, v in row.items()}
                    
                    name = cleaned_row.get('name', '').strip()
                    quantity = cleaned_row.get('quantity', '').strip()
                    price = cleaned_row.get('price', '').strip()
                    wholesale_price = cleaned_row.get('wholesale_price', '').strip()
                    
                    # Validate required fields
                    if not name:
                        errors.append(f"الصف {row_num}: اسم المنتج مفقود")
                        continue
                    if not quantity or not quantity.isdigit():
                        errors.append(f"الصف {row_num}: الكمية غير صحيحة ({quantity})")
                        continue
                    if not price or not price.replace('.', '', 1).isdigit():
                        errors.append(f"الصف {row_num}: السعر غير صحيح ({price})")
                        continue
                    
                    # Create product
                    product = Product.objects.create(
                        name=name,
                        quantity=int(quantity),
                        price=Decimal(price)
                    )
                    
                    # Add wholesale price if provided
                    if wholesale_price and wholesale_price.replace('.', '', 1).isdigit():
                        try:
                            pval = Decimal(wholesale_price)
                            ProductPriceTier.objects.create(
                                product=product,
                                key='wholesale',
                                price=pval,
                                min_quantity=1
                            )
                        except Exception:
                            pass
                    
                    imported_count += 1
                except Exception as e:
                    errors.append(f"الصف {row_num}: {str(e)}")
            
            success_message = f"تم استيراد {imported_count} منتج بنجاح."
            return render(request, 'products/product_bulk_import.html', {
                'success': success_message,
                'errors': errors,
                'imported_count': imported_count
            })
        except Exception as e:
            error = f"خطأ في قراءة الملف: {str(e)}"
            return render(request, 'products/product_bulk_import.html', {'error': error})
    
    return render(request, 'products/product_bulk_import.html')


@login_required
def product_autocomplete(request):
    """API endpoint for product autocomplete in invoice creation."""
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        name__icontains=query
    ).values('id', 'name', 'price', 'quantity')[:10]
    
    # Add wholesale price info
    results = []
    for product in products:
        wholesale_tier = Product.objects.get(id=product['id']).price_tiers.filter(key='wholesale').first()
        wholesale_price = float(wholesale_tier.price) if wholesale_tier else float(product['price'])
        results.append({
            'id': product['id'],
            'name': product['name'],
            'price': float(product['price']),
            'wholesale_price': wholesale_price,
            'quantity': product['quantity']
        })
    
    return JsonResponse(results, safe=False)
