from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Topping(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class PizzaType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Size(models.Model):
    size = models.CharField(max_length=15)

    def __str__(self):
        return self.size

class Pizza(models.Model):
    name = models.CharField(max_length=30)
    pizza_type = models.ForeignKey(PizzaType, on_delete=models.CASCADE)
    max_toppings = models.PositiveIntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return f"{self.size} - {self.name} - {self.pizza_type} Pizza - ${self.price}"

    def toppings_to_str(self):
        output = []
        for topping in self.toppings.all():
            output.append(str(topping))
        return ", ".join(output)

class EntreeType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Entree(models.Model):
    name = models.CharField(max_length=30)
    entree_type = models.ForeignKey(EntreeType, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, default=None, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        if self.size == None:
            return f"{self.name} - ${self.price}"

        return f"{self.name} - {self.size} - ${self.price}"

class Sub(models.Model):
    name = models.CharField(max_length=50)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return f"{self.size} - {self.name} - ${self.price}"

class Addon(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=4)
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - ${self.price} - ({self.sub})"

class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.status}"

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)

    def price(self):
        price = 0

        for pizza_order in self.pizzas.all():
            price += pizza_order.price()

        for sub_order in self.subs.all():
            price += sub_order.price()

        for entree_order in self.entrees.all():
            price += entree_order.price()

        return price

    def __str__(self):
        return f"{self.customer} - {self.date} - {self.status} - ${self.price()}"

class PizzaOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pizzas")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def add_topping(self, topping):
        if len(self.toppings.all()) + 1 > self.pizza.max_toppings:
            return

        topping_order = ToppingsOrder(pizzaOrder=self, topping=topping)
        topping_order.save()

    def price(self):
        return self.pizza.price * self.quantity

    def __str__(self):
        toppings_str = ""

        for topping_order in self.toppings.all():
            toppings_str += " - " + str(topping_order)

        if toppings_str == "":
            toppings_str == "no toppings"

        return f"{self.pizza} - ${toppings_str}"

class ToppingsOrder(models.Model):
    pizzaOrder = models.ForeignKey(PizzaOrder, on_delete=models.CASCADE, related_name="toppings")
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.topping}"


class SubOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="subs")
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def add_addons(self, addon):
        addon_order = AddonOrder(subOrder=self, addon=addon)
        addon_order.save()

    def price(self):
        price = self.sub.price

        for addon_order in self.addons.all():
            price += addon_order.addon.price

        return price * self.quantity

    def __str__(self):
        addons_str = ""

        for addon_order in self.addons.all():
            addons_str += " - " + str(addon_order)

        if addons_str == "":
            addons_str == "no addons"

        return f"{self.sub} - ${addons_str}"


class AddonOrder(models.Model):
    subOrder = models.ForeignKey(SubOrder, on_delete=models.CASCADE,  related_name="addons")
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.addon}"


class EntreeOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="entrees")
    entree = models.ForeignKey(Entree, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def price(self):
        return self.entree.price * self.quantity

    def __str__(self):
        return f"{self.entree} - {self.quantity}"



class CartItem(models.Model):
    quantity = models.PositiveIntegerField()

    product = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product_obj=GenericForeignKey('product', 'object_id')


