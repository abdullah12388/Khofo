# Python
import bleach
# Django
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView
# Models
from .models import Iloc


# Create your views here.


class UserExportDetailView(DetailView):
    model = Iloc
    template_name = 'export/userExport.html'

    def get_queryset(self):
        return Iloc.objects.filter(pk=1)


class DelegateExportDetailView(DetailView):
    model = Iloc
    template_name = 'export/delegateExport.html'

    def get_queryset(self):
        return Iloc.objects.filter(pk=1)


def send_message(request):
    data = {'done': False}
    if request.method == 'GET':
        message_value = request.GET.get('message_value', None)
        if message_value:
            message_value = bleach.clean(message_value.strip())

    return JsonResponse(data)
