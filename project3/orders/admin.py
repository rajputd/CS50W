from django.contrib import admin

from .models import *

class ToppingsOrderInline(admin.TabularInline):
    model = ToppingsOrder
    show_change_link = True

class PizzaOrderAdmin(admin.ModelAdmin):
    inlines = [
        ToppingsOrderInline,
    ]

class AddonOrderInline(admin.TabularInline):
    model = AddonOrder
    show_change_link = True

class SubOrderAdmin(admin.ModelAdmin):
    inlines = [
        AddonOrderInline,
    ]

class PizzaOrderInline(admin.TabularInline):
    model = PizzaOrder
    show_change_link = True

class SubOrderInline(admin.TabularInline):
    model = SubOrder
    show_change_link = True

class EntreeOrderInline(admin.TabularInline):
    model = EntreeOrder
    show_change_link = True

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        PizzaOrderInline,
        SubOrderInline,
        EntreeOrderInline,
    ]

admin.site.register(Topping)
admin.site.register(Size)
admin.site.register(PizzaType)
admin.site.register(Pizza)
admin.site.register(EntreeType)
admin.site.register(Entree)
admin.site.register(Sub)
admin.site.register(Addon)

admin.site.register(PizzaOrder, PizzaOrderAdmin)
admin.site.register(ToppingsOrder)
admin.site.register(SubOrder, SubOrderAdmin)
admin.site.register(AddonOrder)
admin.site.register(EntreeOrder)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatus)
