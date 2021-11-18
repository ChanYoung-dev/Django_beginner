from django.shortcuts import render
from third.models import Restaurant
from django.core.paginator import Paginator


def list(request):
    restaurants = Restaurant.objects.all()
    paginator = Paginator(restaurants, 5)  # 한 페이지에 5개씩 표시

    page = request.GET.get('page')  # query params에서 page 데이터를 가져옴
    items = paginator.get_page(page)  # 해당 페이지의 아이템으로 필터링

    context = {
        'restaurants': items
    }
    return render(request, 'third/list.html', context)

