from django.shortcuts import render


def list(request):
    context = {
    }
    return render(request, 'third/list.html', context)
