from third.models import Restaurant, Review
from django.core.paginator import Paginator
from third.forms import RestaurantForm, ReviewForm, UpdateRestaurantForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Avg



def list(request):
    # restaurants = Restaurant.objects.all()
    restaurants = Restaurant.objects.all().annotate(reviews_count=Count('review'))\
        .annotate(average_point=Avg('review__point'))
    # 여기서 review는 models.py의 review 모델 클래스이다 대소문자 상관이 없으며 외래키로 이어져있기 때문에 restaurats도 외래키와 연동되어 있다.
    # 그다음 review__point는 rivew 모델클래스의 point 변수를 말한다.
    # annotate는 자동으로 Restraunt 모델필드에 reviews_count 변수를 추가할수 있다.
    paginator = Paginator(restaurants, 5)  # 한 페이지에 5개씩 표시

    page = request.GET.get('page')  # query params에서 page 데이터를 가져옴 ex) http:~/third/list?page=1
    items = paginator.get_page(page)  # 해당 페이지의 아이템으로 필터링

    context = {
        'restaurants': items
    }
    return render(request, 'third/list.html', context)

def create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)  # request의 POST 데이터(html에서의 form에서 작성된 데이터)들을 바로 PostForm에 담을 수 있습니다.
        if form.is_valid():  # 데이터가 form 클래스에서 정의한 조건 (max_length 등)을 만족하는지 체크합니다.
            new_item = form.save()  # save 메소드로 입력받은 데이터를 레코드로 추가합니다.
        return HttpResponseRedirect('/third/list/')  # 리스트 화면으로 이동합니다.
    form = RestaurantForm()
    return render(request, 'third/create.html', {'form': form})

def update(request):
    if request.method == 'POST' and 'id' in request.POST: #request의 POST 데이터 = html에서의 form에서 작성된 데이터에서 id가 있을시
        # item = Restaurant.objects.get(pk=request.POST.get('id'))
        item = get_object_or_404(Restaurant, pk=request.POST.get('id')) # 이렇게 하면 id가 없을시 404페이지가 띄어진다
        password = request.POST.get("password", "")
        # form = RestaurantForm(request.POST, instance=item)  # NOTE: instance 인자(수정대상) 지정
        form = UpdateRestaurantForm(request.POST, instance=item)  # NOTE: instance 인자(수정대상) 지정
        # if form.is_valid():
        if form.is_valid() and password == item.password:  # 비밀번호 검증 추가
            item = form.save()
    elif 'id' in request.GET:
        # item = Restaurant.objects.get(pk=request.GET.get('id')) #http~third/update/?id=2 이렇게 값이 입력됐다고 가정.
        item = get_object_or_404(Restaurant, pk=request.GET.get('id'))  # 이렇게 하면 id가 없을시 404페이지가 띄어진다
        form = RestaurantForm(instance=item) #From에 id를 통해 get한 item 의 내용이 들어간다.
        return render(request, 'third/update.html', {'form': form})

    return HttpResponseRedirect('/third/list/')  # 리스트 화면으로 이동합니다.

#하나의 객체만 보여주기
def detail(request, id):
    # if 'id' in request.GET: #http~third/update/?id=2 이렇게 값이 입력됐다면
    if id is not None:
        item = get_object_or_404(Restaurant, pk=id) # http://~/third/detail/5/, path parameter 사용
        # path parameter사용시
        # html에서 <a href="{% url 'restaurant-detail' id=item.id %}" class="card-link">자세히 보기</a>
        # item = get_object_or_404(Restaurant, pk=request.GET.get('id')) http://~/third/detail?id=5
        # httml에서 <a href="{% url 'restaurant-detail' %}?id={{ item.id }}" class="card-link">자세히 보기</a>
        reviews = Review.objects.filter(restaurant=item).all()
        return render(request, 'third/detail.html', {'item': item, 'reviews': reviews})

    return HttpResponseRedirect('/third/list/')  # 리스트 화면으로 이동합니다.


def delete(request, id):
    '''
    if 'id' in request.GET: #http~third/update/?id=2 이렇게 값이 입력됐다면
        item = get_object_or_404(Restaurant, pk=request.GET.get('id'))
        item.delete()

    return HttpResponseRedirect('/third/list/')
    '''
    item = get_object_or_404(Restaurant, pk=id)
    if request.method == 'POST' and 'password' in request.POST:
    #request의 POST 데이터 = html에서의 form에서 작성된 데이터(=이 form은 forms.py에서의 modelform의 필드)에서 password가 있을시
        if item.password == request.POST.get('password') or item.password is None:
            item.delete()
            return redirect('list')  # 리스트 화면으로 이동합니다.
        return redirect('restaurant-detail', id=id) # 비밀번호가 입력되지 않으면 상세페이지로 되돌아감
    return render(request, 'third/delete.html', {'item': item})


def review_create(request, restaurant_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)  #
        if form.is_valid():  # 데이터가 form 클래스에서 정의한 조건 (max_length 등)을 만족하는지 체크합니다.
            new_item = form.save()  # save 메소드로 입력받은 데이터를 레코드로 추가합니다.
        return redirect('restaurant-detail', id=restaurant_id)  # 전화면으로 이동합니다.
        # return HttpResponseRedirect('/third/list/') 와의 차이점은 url기반이아니라 view name 기반이다
    item = get_object_or_404(Restaurant, pk=restaurant_id)
    form = ReviewForm(initial={'restaurant': item})
    return render(request, 'third/review_create.html', {'form': form, 'item':item})


def review_delete(request, restaurant_id, review_id):
    item = get_object_or_404(Review, pk=review_id)
    item.delete()

    return redirect('restaurant-detail', id=restaurant_id)  # 전 화면으로 이동합니다.


def review_list(request):
    reviews = Review.objects.select_related().all().order_by('-created_at')
    paginator = Paginator(reviews, 10)  # 한 페이지에 10개씩 표시

    page = request.GET.get('page')  # query params에서 page 데이터를 가져옴
    items = paginator.get_page(page)  # 해당 페이지의 아이템으로 필터링

    context = {
        'reviews': items
    }
    return render(request, 'third/review_list.html', context)
