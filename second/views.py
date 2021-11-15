from django.shortcuts import render
from second.models import Post
from .forms import PostForm
from django.http import HttpResponseRedirect

# Create your views here.
def list(request):
    context = {
        'items': Post.objects.all()
    }
    return render(request, 'second/list.html', context)

def create(request):
    form = PostForm()
    return render(request, 'second/create.html', {'form': form})

'''
def create(request):
    context = {
        'form': PostForm()
    }
    return render(request, 'second/create.html', context)
'''

def confirm(request):
    form = PostForm(request.POST)  # request의 POST 데이터들을 바로 PostForm에 담을 수 있습니다.
    if form.is_valid(): # 데이터가 form 클래스에서 정의한 조건 (max_length 등)을 만족하는지 체크합니다.
        return render(request, 'second/confirm.html', {'form': form})
    return HttpResponseRedirect('second/create/')  # 데이터가 유효하지 않으면 되돌아갑니다.

def create(request):
    if request.method == 'POST': # POST 입력
        form = PostForm(request.POST)  # request의 POST 데이터들을 바로 PostForm에 담을 수 있습니다.
        if form.is_valid():  # 데이터가 form 클래스에서 정의한 조건 (max_length 등)을 만족하는지 체크합니다.
            # 여기에 데이터를 저장 (= 레코드 추가)하는 코드가 필요합니다.
            # print(form)
            new_item = form.save()  # save 메소드로 입력받은 데이터를 레코드로 추가합니다.
        return HttpResponseRedirect('/second/list/')  # 게시글 리스트 화면으로 이동합니다.
    form = PostForm() # GET 입력
    return render(request, 'second/create.html', {'form': form}) # GET일경우는 create
