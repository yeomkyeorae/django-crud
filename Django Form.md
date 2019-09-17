## Django Form

### Form

 먼저, `form`을 활용하기 위해서 `form`을 활용하고자 하는 `app`에 `forms.py`라는 입으로 파일을 생성한다.

활용할 수 있는 `form`은 두 가지가 있다.

#### 1. 일반 form

​	`forms.py`를 살펴보자.

```python
from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length = 140,
        label = '제목',
        widget = forms.TextInput(
            attrs = {
                'placeholder': '제목을 입력바랍니다.',
            }
        )
    )
    content = forms.CharField(
        # label 내용 수정
        label = '내용',
        # Django form에서 HTML 속성 지정 -> widget
        widget=forms.Textarea(
            attrs = {
                'class': 'my-content',
                'placeholder': '내용을 입력바랍니다.',
                'rows': 5,
                'cols': 60,
            }
        )
    )
```

- `Class ArticleFomr`에서 `forms.ModelForm`을 상속받는다.
- 위에서 `title`과 `content`항목을 설정하였다. 선언할 때를 살펴보면 `models.py`에서 컬럼을 설정할 때와 비슷한 것을 볼 수 있다. -> `modelForm`으로 변경하면 중복을 크게 줄일 수 있다.
- `label`로 값을 설정할 수 있다.
- `widget`으로 `css`와 같은 기본적인 특성을 설정할 수 있다.



​	`views.py`에서 `create`함수를 살펴보자.

```python
from .forms import ArticleForm


def create(request):
    # request의 방식이 'GET'이면
    if request.method == 'GET':
        article_form = ArticleForm()
    else:	# POST 요청 -> 검증 및 저장
        article_form = ArticleForm(request.POST)
        
        # 검증
        if article_form.is_valid():
            title = article_form.cleaned_data.get('title')
            content = article_form.cleaned_data.get('content')
            article = Article(title=title, content=content)
            article.save()
            return redirect('articles:detail', article.pk)
    
    context = {
        'article_form': article_form,
    }
    return render(request, 'articles/form.html', context)
```

- 먼저, `GET`요청에서 `ArticleForm()`인스턴스를 생성, `POST`요청에서 `ArticleForm(request.POST)` 인스턴트를 생성하고 `article_form.is_valid()`로 유효한지 검증.
- `article_form`으로 data를 가져올 때는 `cleaned_data.get()`을 사용한다. 



​	`new.html`을 살펴보자

```html
{% extends 'articles/base.html' %}
{% block body %}
<form action="" method="POST">
  {% csrf_token %}
  {{ article_form.as_p }}
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
{% endblock %}
```

- `form`태그를 사용할때 `forms.py`를 사용하므로 `action`이 None이어도 된다.
- `form`태그 내부에 `{{ article_form.as_p }}`를 사용하여 내용을 불러온다.



#### 2. ModelForm



### Model Form?

