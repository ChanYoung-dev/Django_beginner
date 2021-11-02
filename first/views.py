from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import datetime

def index(request):
    # django.shortcuts의 render 기능때문에
    # template = loader.get_template('index.html')
    # 위 구문을 지워도 된다.
    now = datetime.now()
    context = {
        'current_date': now
    }
    # django.shortcuts의 render 기능때문에
    # return HttpResponse(template.render(context, request))
    return render(request, 'index.html', context)


def select(request):
    context = {
        'number': 4
    }
    return render(request, 'select.html', context)


def result(request):
    context = {
        'numbers': [1, 2, 3, 4]
    }
    return render(request, 'result.html', context)




