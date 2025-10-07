from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'get_total_price')
    fields = ('product', 'quantity', 'get_total_price')

    def get_total_price(self, obj):
        return f"{obj.get_total_price():.2f} грн."
    get_total_price.short_description = "Сума"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_owner', 'get_total', 'item_count')
    list_filter = ('user',)
    search_fields = ('user__username', 'session_key')
    inlines = [CartItemInline]
    ordering = ('-id',)

    def get_owner(self, obj):
        if obj.user:
            return obj.user.username
        return f"Session: {obj.session_key}"
    get_owner.short_description = "Покупець"

    def get_total(self, obj):
        total = obj.get_total_price_for_all_items()
        return f"{total:.2f} ₴"
    get_total.short_description = "Загальна сума"

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "К-сть товарів"



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'get_total_price')
    list_filter = ('cart__user',)
    search_fields = ('product__name', 'cart__user__username')
    ordering = ('-id',)

    def get_total_price(self, obj):
        return f"{obj.get_total_price():.2f} грн."
    get_total_price.short_description = "Сума"