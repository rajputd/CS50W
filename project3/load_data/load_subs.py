import csv
from orders.models import Sub, Size

small_size = Size.objects.get(pk=2)
large_size = Size.objects.get(pk=1)

with open("load_data/subs.csv") as input:
    reader = csv.reader(input, delimiter=",", quotechar="\"")
    for row in reader:
        name = row[0]

        small_price = float(row[1])
        large_price = float(row[2])

        small_sub = Sub.objects.create(name=name, size=small_size, price=small_price)
        large_sub = Sub.objects.create(name=name, size=large_size, price=large_price)

        small_sub.save()
        large_sub.save()