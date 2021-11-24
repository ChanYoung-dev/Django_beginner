from django.db import models


class Restaurant(models.Model): # Restaurant 라는 상점을 나타내는 모델을 정의
    name = models.CharField(max_length=30)  # 이름
    address = models.CharField(max_length=200)  # 주소

    password = models.CharField(max_length=20, default=None, null=True)
    image = models.CharField(max_length=500, default=None, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # 글 작성 시 (이 모델의 데이터(레코드) 저장 시) 생성 시각
    updated_at = models.DateTimeField(auto_now=True)  # 저장된 레코드 수정 시 수정 시각


class Review(models.Model):
    point = models.IntegerField()
    comment = models.CharField(max_length=500)

    # 식당 모델과의 릴레이션 정의,
    # on_delete CASCADE로 지정하면 식당이 삭제되면 같이 삭제된다.
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)  # 글 작성 시 (이 모델의 데이터(레코드) 저장 시) 생성 시각
    updated_at = models.DateTimeField(auto_now=True)


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

'''
Column(Field) Lookup

Filter 조건을 더 잘 사용하면 좀 더 복잡한 조건도 조회할 수 있습니다. 이런식으로 제공되는 것을 django orm의 field lookup이라고 하는데, 사용해봅시다.

기본적으로 Field lookup은 다음과 같이 사용합니다.
Restaurant.objects.filter(name__exact=’Korean Food’)


위와 같이 filter, exclude나, get 메소드 내에 검색을 원하는 필드명과 field lookup을 붙여서 값을 전달합니다.
(형태: {field명}__{조건 키워드(lookup type)})

쟝고 쉘을 시작하여 다음의 코드들을 실행해봅시다.
(python manage.py shell)
Contains: 특정 키워드가 포함된 레코드를 조회
>> from third.models import Restaurant
>> Restaurant.objects.filter(name__contains=’Korea’).values()


Exact: 특정 키워드랑 정확하게 일치하는 레코드 조회
>> Restaurant.objects.filter(name__contains=’Korean Food’).values()


Gt, Gte, Lte, Lt: 더 크거나, 더 크거나 같거나, 더 작거나 같거나, 더 작거나한 레코드를 조회
>> Restaurant.objects.filter(created_at__lt='2018-01-01 00:00:00').values()
>> Restaurant.objects.filter(created_at__gt='2018-01-01 00:00:00').values()


Startswith, Endswith: 특정 문자열로 시작하거나 종료되는 레코드를 조회
>> Restaurant.objects.filter(name__startswith='Korea').values()
>> Restaurant.objects.filter(name__endswith='Food').values()


In: 여러 값을 한 번에 검색에 조건으로 걸 때 사용
>> Restaurant.objects.filter(id__in=[1,3]).values()


Range: 특정 값 사이의 레코드를 조회
>> import datetime
>> start_date = datetime.datetime(2018,12,3,0,0,0)
>> end_date = datetime.datetime(2018,12,8,0,0,0)
>> Restaurant.objects.filter(created_at__range=(start_date, end_date)).values()


'''

'''
데이터 수정/삭제

UPDATE: 수정하기
우리가 이미 배운 데이터를 조회하는 방식을 써서 원하는 데이터를 가져온 후에 속성 값을 변경하고 데이터를 추가했을 때 처럼 save를 호출하면 수정이 완료됩니다.

>> item = Restaurant.objects.get(pk=1)
>> item.name 
‘Deli Shop’
>> item.name = ‘My Shop’
>> item.save() # save를 호출해야 실제로 저장됩니다.


save를 호출할 때 데이터를 추가하는 INSERT인지, 데이터를 수정하는 UPDATE인지 어떻게 구분할까요?
모델의 인스턴스에 id (primary key) 값이 지정되어 있으면 save를 호출 시 UPDATE로 인식하고 수행합니다.
만약 UPDATE에 실패했으면, 해당 id에 해당하는 레코드가 존재하지 않는 것이므로 새로운 값을 INSERT합니다.

>>> new_item = Restaurant() # 새로운 모델의 인스턴스를 생성
>>> new_item
<Restaurant: Restaurant object (None)>
>>> new_item.name = 'My Shop 2'
>>> new_item.address = 'Yeoksam'
>>> new_item.id = 1 # id를 지정 (primary key) 예전에 My Shop으로 이름을 지정한 레코드가 선택된다.
>>> new_item.created_at = datetime.datetime.now()
>>> new_item.updated_at = datetime.datetime.now()
>>> new_item.save() # update가 이루어 진다.



DELETE: 삭제하기

삭제는 조회한 레코드(모델의 인스턴스)에서 delete를 메소드를 호출하면 됩니다.

>>> item.delete()
(1, {'third.Restaurant': 1})
>>> Restaurant.objects.all().values()


'''