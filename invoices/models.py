from django.db import models
from products.models import Product
from django.db.models import Sum, F, FloatField
# Create your models here.


class Invoice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"فاتورة رقم {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def update_total(self):
        total = self.items.aggregate(
            total=Sum(F('price') * F('quantity'), output_field=FloatField())
        )['total'] or 0
        self.total = round(total, 2)
        self.save()

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # سعر البيع

    @property
    def total(self):
        return self.price * self.quantity
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        if self.pk:
            # تعديل عنصر فاتورة موجود
            old_item = InvoiceItem.objects.get(pk=self.pk)
            diff_quantity = self.quantity - old_item.quantity
        else:
            # عنصر جديد
            diff_quantity = self.quantity

        if self.product.quantity < diff_quantity:
            raise ValueError(f"الكمية غير كافية في المخزون للمنتج: {self.product.name}")

        self.product.quantity -= diff_quantity
        self.product.save()

        super().save(*args, **kwargs)

        # بعد حفظ العنصر، تحديث إجمالي الفاتورة
        self.invoice.update_total()
    def delete(self, *args, **kwargs):
        # استرجاع الكمية للمنتج عند حذف العنصر
        self.product.quantity += self.quantity
        self.product.save()
        invoice = self.invoice
        super().delete(*args, **kwargs)
        invoice.update_total()

