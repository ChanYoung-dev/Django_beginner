from django.shortcuts import render
from third.models import Restaurant

def list(request):
    context = {
        'restaurants': Restaurant.objects.all()
    }
    return render(request, 'third/list.html', context)
