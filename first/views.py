from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello world.")


def select(request):
    message = '수 하나를 입력해주세요.'
    return HttpResponse(message)


def result(request):
    message = '추첨 결과입니다.'
    return HttpResponse(message)




