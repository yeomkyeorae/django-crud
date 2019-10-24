from django import forms
from .models import Article, Comment

# model form
class ArticleForm(forms.ModelForm):
    # 위젯 설정 1.
    title = forms.CharField(
        max_length = 140,
        label = '제목',
        help_text= '30자 이내로 작성바랍니다.',
        widget = forms.TextInput(
            attrs = {
                'placeholder': '제목을 입력바랍니다.',
            }
        )
    )
    class Meta: # 데이터에 대한 데이터, ArticleForm에 대한 정보를 담고 있다. 
        # 예: 사진 데이터의 정보로서 위치, 감도, 일시 등
        model = Article
        fields = '__all__'
        exclude = ('image_thumbnail', 'user', 'like_users', 'hashtags')
        # fields = ('title', )
        # exclue = ('title', )
        
        # 위젯 설정 2.
        widgets = {
            'title': forms.TextInput(
                attrs = {
                    'placeholder': '제목을 입력바랍니다.'
                }
            )
        }


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('content',)

# 그냥 form
# class ArticleForm(forms.Form):
#     title = forms.CharField(
#         max_length = 140,
#         label = '제목',
#         widget = forms.TextInput(
#             attrs = {
#                 'placeholder': '제목을 입력바랍니다.',
#             }
#         )
#     )
#     content = forms.CharField(
#         # label 내용 수정
#         label = '내용',
#         # Django form에서 HTML 속성 지정 -> widget
#         widget=forms.Textarea(
#             attrs = {
#                 'class': 'my-content',
#                 'placeholder': '내용을 입력바랍니다.',
#                 'rows': 5,
#                 'cols': 60,
#             }
#         )
#     )
