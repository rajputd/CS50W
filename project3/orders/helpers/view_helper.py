from orders.models import *

#returns a dictionary of dictionaries organized by
# pizza_type -> name -> size -> price
def getPizzaMenu():
    output = {}
    pizzas = Pizza.objects.all()

    for pizza in pizzas:
        pizza_type = pizza.pizza_type.name
        name = pizza.name
        size = pizza.size.size
        price = pizza.price

        #if type does not exist then add it to output
        if pizza_type not in output.keys():
            output[pizza_type] = {}

        #if name does not exist for type then add it
        if name not in output[pizza_type].keys():
            output[pizza_type][name] = {}

        #add size and price
        if size not in output[pizza_type][name].keys():
            output[pizza_type][name][size] = price

    return output

#returns a dictionary of dictionaries containing sub info
# sub_name -> size -> price
def getSubMenu():
    output = {}
    subs = Sub.objects.all()

    for sub in subs:
        name = sub.name
        size = sub.size.size
        price = sub.price

        #if name does not exist for type then add it
        if name not in output.keys():
            output[name] = {}

        #if size for sub, price pair does not exist then add it
        if size not in output[name].keys():
            output[name][size] = price

    return output

#returns a dictionary of dictionaries containing sub info
# sub_name -> addon_name -> size -> price
def getSubAddons():
    output = {}
    addons = Addon.objects.all()

    for addon in addons:
        if addon.sub == None:
            sub_name = "Any Sub"
            sub_size = ""
        else:
            sub_name = addon.sub.name
            sub_size = addon.sub.size

        addon_name = addon.name
        price = addon.price

        if sub_name not in output.keys():
            output[sub_name] = {}

        if addon_name not in output[sub_name].keys():
            output[sub_name][addon_name] = {}

        output[sub_name][addon_name][sub_size] = price

    return output

def getEntrees():
    output = {}
    entrees = Entree.objects.all()

    for entree in entrees:
        entree_type = entree.entree_type
        name = entree.name
        size = entree.size
        price = entree.price

        if entree_type not in output.keys():
            output[entree_type] = {}

        #if name does not exist for type then add it
        if name not in output[entree_type].keys():
            output[entree_type][name] = {}

        # #if size for sub, price pair does not exist then add it
        if size not in output[entree_type][name].keys():
            output[entree_type][name][size] = price

    return output

def getUniquePizzaNames():
    pizzas = Pizza.objects.all()
    output = set()

    for pizza in pizzas:
        output.add(pizza.name)

    return output
