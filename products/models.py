from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def unit_price_for_quantity(self, qty):
        """Return the best per-unit price available for a given purchase quantity.

        Looks up price tiers with min_quantity <= qty and returns the lowest per-unit price.
        Falls back to `self.price`.
        """
        tiers = self.price_tiers.filter(min_quantity__lte=qty)
        if not tiers.exists():
            return self.price
        # choose the tier with the lowest per-unit price
        best = min((t.price for t in tiers))
        return best


class ProductPriceTier(models.Model):
    TIER_CHOICES = [
        ('wholesale', 'سعر الجملة'),
        ('wholesale_for_quantity', 'سعر الجملة للكمية'),
        ('quantity_price', 'سعر الكمية'),
    ]

    product = models.ForeignKey(Product, related_name='price_tiers', on_delete=models.CASCADE)
    key = models.CharField(max_length=32, choices=TIER_CHOICES)
    min_quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('product', 'key')

    def __str__(self):
        return f"{self.product.name} - {self.get_key_display()}"
