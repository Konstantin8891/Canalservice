from django.db.models import Sum
from django.http import JsonResponse
from django.views.generic import ListView

from .models import Order
from .tables import OrderTable


class OrderListView(ListView):
    model = Order
    table_class = OrderTable
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = Order.objects.aggregate(Sum('price'))[
            'price__sum'
        ]
        return context


def chart(request):
    labels = []
    data = []
    queryset = Order.objects.values('date').annotate(
        price=Sum('price')
    ).order_by('date')
    for entry in queryset:
        labels.append(entry['date'])
        data.append(entry['price'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
