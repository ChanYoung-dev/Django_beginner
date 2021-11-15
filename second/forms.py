'''
from django import forms


class PostForm(forms.Form):  # django의 폼을 상속
    title = forms.CharField(label='제목', max_length=200)
    content = forms.CharField(label="내용", widget=forms.Textarea)
'''
# title과 content말고 새로운 변수를 추가하려하면 model.py와 forms.py 두개 다 추가해야한다.
# 이러한 번거로움을 없애기 위해 Model Form을 사용한다.
from django.forms import ModelForm
from second.models import Post
from django.utils.translation import gettext_lazy as _

class PostForm(ModelForm):
    class Meta:
        model = Post  # 어떤 모델 클래스를 사용할 것인지, 여기선 models.py의 Post를 사용
        fields = ['title', 'content']  # 입력받을 필드들
        labels = {
            'title': _('제목'), # from django.utils.translation import gettext_lazy as _
            'content': _('내용'),
        }
        help_texts = {
            'title': _('제목을 입력해주세요.'),
            'content': _('내용을 입력해주세요.'),
        }
        error_messages = {
            'name': {
                'max_length': _("제목이 너무 깁니다. 30자 이하로 해주세요."),
            },
        }
