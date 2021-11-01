from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('select/', views.select, name='select'),
    path('result/', views.result, name='result'),

    # path parameter / form parameter / query parameter
    # 변수화: 기본 path converter
    #  path('articles/2003/', views.special_case_2003)
    #  path('articles/<int:year>/<int:month>/', views.month_archive),
    #  path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail)


    # 변수화2: 정규식 사용
    # re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    # re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail),
]
