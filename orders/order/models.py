from django.db import models


class Order(models.Model):
    order_id = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    rub_price = models.FloatField()
    date = models.DateField()
