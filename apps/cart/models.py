from django.db import models
from apps.product.models import Product
from django.db.models import Sum, F, FloatField
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart for session {self.session_key}"

    def get_total_price_for_all_items(self):
        total = self.items.aggregate(
            total_price=Sum(F('product__price') * F('quantity'), output_field=FloatField())
        )['total_price']
        return total or 0


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        existing = CartItem.objects.filter(cart=self.cart, product=self.product).first()
        if existing and existing.pk != self.pk:
            existing.quantity += self.quantity
            existing.save()
            return existing
        super().save(*args, **kwargs)

    def get_total_price(self):
        return self.product.price * self.quantity


