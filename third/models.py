from django.db import models


class Restaurant(models.Model): # Restaurant 라는 상점을 나타내는 모델을 정의
    name = models.CharField(max_length=30)  # 이름
    address = models.CharField(max_length=200)  # 주소

    created_at = models.DateTimeField(auto_now_add=True)  # 글 작성 시 (이 모델의 데이터(레코드) 저장 시) 생성 시각
    updated_at = models.DateTimeField(auto_now=True)  # 저장된 레코드 수정 시 수정 시각

'''
데이터필터링
>> Restaurant.objects.filter(name='Deli Shop').values()
<QuerySet [{'id': 1, 'name': 'Deli Shop', 'address': 'Gangbuk', 'created_at': datetime.datetime(2018, 12, 5, 22, 18, 34, 950381, tzinfo=<UTC>), 'updated_at': datetime.datetime(2018, 12, 5, 22, 48, 50, 482695, tzinfo=<UTC>)}]>

>>  Restaurant.objects.exclude(name='Sushi').values()
<QuerySet [{'id': 1, 'name': 'Deli Shop', 'address': 'Gangbuk’, 'created_at': datetime.datetime(2018, 12, 5, 22, 18, 34, 950381, tzinfo=<UTC>), 'updated_at': datetime.datetime(2018, 12, 5, 22, 48, 50, 482695, tzinfo=<UTC>)}, {'id': 2, 'name': 'Korean Food', 'address': 'Gangnam', 'created_at': datetime.datetime(2018, 12, 5, 22, 21, 52, 35871, tzinfo=<UTC>), 'updated_at': datetime.datetime(2018, 12, 5, 22, 21, 52, 35921, tzinfo=<UTC>)}]>

>>> query = Restaurant.objects.exclude(name='Sushi')
>>> query = query.exclude(address='Gangnam')
>>> query.values() # 이 시점에 쿼리 실행
<QuerySet [{'id': 2, 'name': 'Korean Food', 'address': 'Gangbuk', 'created_at': datetime.datetime(2018, 12, 5, 22, 21, 52, 35871, tzinfo=<UTC>), 'updated_at': datetime.datetime(2018, 12, 5, 22, 55, 56, 81772, tzinfo=<UTC>)}]>

'''


'''
페이징
Restaurant.objects.all()[0:1] 
Restaurant.objects.order_by('-created_at')[1:3].values()
<QuerySet [{'id': 2, 'name': 'Korean Food', 'address': 'Gangbuk', 'created_at': datetime.datetime(2018, 12, 5, 22, 21, 52, 35871, tzinfo=<UTC>), 'updated_at': datetime.datetime(2018, 12, 5, 22, 55, 56, 81772, tzinfo=<UTC>)}, {'id': 1, 'name': 'Deli Shop', 'address': 'Gangnam', 'created_at': datetime.datetime(2018, 12, 5, 22, 18, 34, 950381, tzinfo=<UTC>), 'updated_at': datetime.datetime(2018, 12, 5, 22, 55, 35, 384595, tzinfo=<UTC>)}]>

'''