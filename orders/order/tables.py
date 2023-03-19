import django_tables2 as tables
from .models import Order


class OrderTable(tables.Table):
    rub_price = tables.Column(attrs={
        "td": {
            "data-length": lambda value: "{:.2f}".format(value)
        }
    })

    class Meta:
        model = Order
        # template_name = 'django_tables2/table.html'
        fields = ('id', 'order_id', 'price', 'rub_price', 'date')
