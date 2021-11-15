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

