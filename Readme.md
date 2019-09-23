# Django - CRUD

> Django ORM(Object Relational Mapping)을 활용하여 게시판 기능 구현하기

## 1. 환경설정

- 가상환경(venv)

  - python 3.7.4에서 가상환경 생성

    ```bash
    $ python -v
    python 3.7.4
    $ python -m venv venv
    ```
    
  - 가상환경 실행

    ```bash
    $ source venv/Scripts/activate
    (venv)
    $
    ```

  - 가상환경 종료

    ```bash
    (venv)
    $ deactivate
    ```

  

- pip - `requirements.txt` 확인

  - 현재 패키지 리스트 작성

    ```bash
    $ pip freeze > requirements.txt
    ```

  - 만약, 다른 환경에서 동일하게 설치한다면

    ```bash
    $ pip install -r requirements.txt
    ```

  

- djaongo app - `articles`



## 2. Model 설정

### 1. `Article` 모델 정의

```python
# articels/models.py

class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextFiedl()
    created_at = models.DateTimeField(auto_now_add=True)
    updateted_at = models.DateTimeField(auto_now=True)
```

- 클래스 정의할 때는 `models.Model`을 상속 받아 만든다.

- 정의하는 변수는 실제 데이터베이스에서 각각의 필드(column)을 가지게 된다.

- 주요 필드

  - `CharField(max_length)`	
    - 필수 인자로 `max_length`를 지정하여야 한다.
    - 일반적으로 데이터베이스에서 `VARCHAR`로 지정된다.
    - `<input type="text">`
  - `TextField()`
    - 일반적으로 데이터베이스에서 `TEXT`으로 지정된다.
    - `CharField`보다 더 많은 글자를 저장할 때 사용된다.
    - `<textarea>`
  - `DateTimeField()`
    - 파이썬의 datetime 객체로 활용된다.
    - 옵션
      - `auto_now_add=True` : 생성시에 자동으로 저장(게시글 생성일)
      - `auto_now=True` : 변경시에 자동으로 저장(게시글 수정일)
  - `BooleanField(), FileField()` 등 다양한 필드를 지정할 수 있다.

- `id`값은 자동으로 `INTEGER`타입으로 필드가 생성되고, 이는 `PK(Primary Key)`이다.

- 모든 필드는 `NOT NULL`조건이 선언되며, 해당 옵션을 수정하려면 아래와 같이 정의할 수 있다.

  ```python
  username = models.CharField(max_length=10, null=True)
  ```

  

### 2. 마이그레이션(migration) 파일 생성

마이그레이션(migration)은 모델에 정의한 내용(데이터베이스의 스키마)의 변경사항을 관리한다. 

따라서, 모델의 필드 수정 혹은 삭제 등이 변경될 때마다 마이그레이션 파일을 생성하고 이를 반영하는 형식으로 

작업한다.

```bash
$ python manage.py makemigrations
Migrations for 'articles':
  articles\migrations\0001_initial.py
    - Create model Article
```

* 만약, 현재 데이터베이스에 반영되어 있는 마이그레이션을 확인하고 싶다면 아래의 명령어를 활용한다.

  ```bash
  $ python manage.py showmigrations
  articles
   [ ] 0001_initial
  ...
  ```

  

### 3. DB 반영(migrate)

만들어진 마이그레이션 파일을 실제 데이터베이스에 반영한다.

```bash
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, articles, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
```

- 만일 특정 app의 마이그레이션 혹은 특정 버전만 반영하고 싶다면 아래의 명령어를 활용한다.

  ```bash
  $ python manage.py migrate articles
  $ python manage.py migrate articels 0001
  ```

- 특정 마이그레이션 파일이 데이터베이스에 반영될 때 실행되는 쿼리문은 다음과 같이 확인할 수 있다. 

  ```bash
  $ python manage.py sqlmigrate articles 0001
  BEGIN;
  --
  -- Create model Article
  --
  CREATE TABLE "articles_article" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(10) NOT NULL, "content" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
  COMMIT;
  ```

- 데이터베이스에 테이블을 만들 때, 기본적으로 `app이름_model이름`으로 생성된다.



## 3. Django Query Method

> Django ORM을 활용하게 되면, 파이썬 객체 조작으로 데이터베이스 조작이 가능하다.
>
> ORM(Object Relational Mapping)에서는 주로 활용되는 쿼리문들이 모두 method로 구성돼 있다.

```bash
$ python manage.py shell
$ python manage.py shell_plus
```

- `shell`에서는 내가 활용할 모델을 직접 import 해야 한다.

  ```python
  from articles.models import Article
  ```

- `shell_plus`는 `django_extensions`를 설치후 `INSTALLED_APPS`에 등록하고 활용해야 한다.

  ```bash
  $ pip install django-extensions
  ```

  ```python
  # crud/settings.py
  INSTALLED_APPS = [
      'django_extensions',
      ...
  ]
  ```

  

  

### 1. Create

```python
# 1. 인스턴스 생성 및 저장
article = Article()
article.title = '1번 글'
article.content = '1번 내용'
# article = Article(title='글', content='내용')
article.save()

# 2. create 메서드 활용
article = Article.objects.create(title='글', content='내용')
```

- 데이터베이스에 저장되면, `id`값이 자동으로 부여된다. `.save()` 호출하기 전에는 `None`이다.



### 2. Read

- 모든 데이터 조회

  ```python
  Article.objects.all()
  ```

  -  리턴되는 값은 `QuerySet` 오브젝트
  - 각 게시글 인스턴스들을 원소로 가지고 있다.

- 특정(단일) 데이터 조회

  ```python
  Article.objests.get(pk=1)
  ```

  - 리턴되는 값은 `Article` 인스턴스
  - `.get()`은 그 결과가 여러 개이거나 없는 경우 오류를 발생시킴.
  - 따라서, 단일 데이터 조회시(primary key를 통해)에만 사용한다.

- 특정 데이터 조회

  ```python
  Articles.objects.filter(title='제목1')
  Articles.objects.filter(title__contains='제목')   # '제목'이 들어간 title
  Articles.objects.filter(title__startswith='제목') # '제목'으로 시작하는 title
  Articles.objects.filter(title__endswith='제목')   # '제목'으로 끝나는 title
  ```

  - 리턴되는 값은 `QuerySet`오브젝트
  - `.filter()`는 없는 경우/하나인 경우/여러 개인 경우 모두 `QuerySet`리턴



### 3. Update

```python
article = Article.objects.get(pk=1)
article.content = '내용 수정'
article.save()
```

- 수정은 특정 게시글을 데이터베이스에서 가져와서 인스턴스 자체를 수정한 후 `save()` 호출.



### 4. Delete

```python
article = Article.objects.get(pk=1)
article.delete()
```



### 5. 기타

	#### 1. Limiting

```python
Article.objects.all()[0] # LIMIT 1 : 1개만
Article.objects.all()[2] # LIMIT 1 OFFSET 2
Article.objects.all()[:3]
```

### 6. Ordering

```python
Article.objects.order_by('-id')   # id 순으로 내림차순 정렬
Article.objects.order_by('title') # title을 기준으로 오름차순 정렬
```





## 4. urls.py에 app_name을 등록함에 따른 변화들

 일일이 `html`과 django `파이썬 코드`에 url이 변경될 때마다 불편함을 느낀 `짱구`는 구글링을 한 결과 용이한 방법을 찾아내었다. 그것은 바로 `urls.py`에 `app_name`을 등록해 사용하는 것이다.

 먼저, `urls.py`를 살펴보자.

```python
from django.urls import path
from . import views


app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/', views.detail, name='detail'),
   	# ...
]
```

 두 가지 변화가 있다.

- `app_name` 변수를 선언한 점.
- 각각의 `path`에 `name` 변수가 생긴 점.



 두 번째로 `views.py`의 `create` 함수를 보자.

```python
def create(request):
    if request.method == 'GET':
        return render(request, 'articles/new.html')
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article(title=title, content=content)
        article.save()
        
        return redirect('articles:detail', article.pk)
```

 위 함수의 `redirect` 부분을 보면 `articles:detail`로 명시한 부분이 있다. `articles`라는 `app_name`의 `name`이 `detail`인 `path`를 가리킨다. `article.pk`는 해당 path에서 `variable routing`부분의 인자 값을 가리킨다.



 세 번째로 새 글을 작성하는`new.html`의 `form` tag를 보자

```html
<!-- ... -->
<form action="{% url 'articles:create' %}" method="POST">
    <!-- ... -->
</form>
<!-- ... -->
```

 위 `form` 태그의 `action` 부분을 보면 `form`태그 내 내용들을 어디로 보낼지 설정한다. `views.py`와 마찬가지로 `articles`라는 `app_name`의 `name`이 `create`로 보낸다는 것을 의미한다. `varible routing`이 필요할 경우에는 아래와 같이 쉼표 없이 순서에 맞게 변수를 적어준다.

```html
<form action="{% url 'articles:create' article.pk %}" method="POST">
```

 마지막으로 `url` 인자로 명시해주는 것을 인지한다. 

 짱구는 이로인해 쉽게 url을 바꿀 수 있게 되었다. 끝.





## 5. Django Form

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

​	`forms.py` 를 살펴보자

```python
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
    	max_length = 10,
        label = '제목',
        help_text = '10자 이내로 작성바랍니다.',
        widget = forms.TextInput(
        	attrs = {
                'placeholder': '제목을 입력바랍니다.',
            }
        )
    )
    
    class Meta:
        model = Article
        fields = '__all__'
        
        widgets = {
            'title': forms.TextInput(
            	attrs = {
                    'placeholder': '제목을 입력바랍니다.'
                }
            )
        }
```

- 일반 `Form`과 달라진 점은 상속하는 대상이 `forms.ModelForm`이라는 것.
- 결정적으로 내부 클래스로 `Meta`를 선언해서 이용하고자 하는 `Model`을 `model = Article`처럼 명시해주어야 한다는 사실이다.
- `fields`변수를 통해서 어떤 컬럼을 이용할지 정할 수 있다.



​	`views.py`의 `update`함수를 살펴보자.

```python
def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
 
    if request.method == 'GET':
        article_form = ArticleForm(instance=article)

    else:
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article = article_form.save()
            return render(request, 'articles/updated.html')

    context = {
        'article_form': article_form,
    }
    return render(request, 'articles/form.html', context)
```

- 확실히 일반 `Form`보다 훨씬 간결해졌다.
- `Form`과 다르게 어떤 `Model`의 instance인지 명시하기 위해 `ArticleForm`인스턴스를 만들 때, 추가 파라미터로 `instance=article`를 입력한다.



​	`form.html`를 살펴보자. `form.html`를 사용하면 동일한 기능을 하는 html 파일을 통합하여 관리할 수 있다. 예를 들면 `create.html`와 `update.html`은 같은 form을 이용하므로 `form.html`로 관리하면 편리하다.

```html
{% extends 'articles/base.html' %}
{% load bootstrap4 %}

{% block body %}
{% if request.resolver_match.url_name == 'create' %}
    <h1 class="text-center">글 작성하기</h1>
{% else %}
    <h1 class="text-center">글 수정하기</h1>
{% endif %}
<form role="form" action="" method="POST">
  {% csrf_token %}
  {% bootstrap_form article_form %}
  {% buttons %}
  <button type="submit" class="btn btn-primary">Submit</button>
  {% endbuttons %}
</form>
{% endblock %}
```

- `{% load bootstrap4 %}`를 이용해 django template에서 손쉽게 `bootstrap`을 이용할 수 있다. [django-bootstrap4](https://github.com/zostera/django-bootstrap4), `form`태그 내부에 `{% boostrap_form article_form %}` 명시해서 사용하였다. 
- `{% if request.resolver_match.url_name == 'create' %}` -> `urls.py`에서 `path`의 `name`이 `create`이면 이라는 뜻.



## ※ get_object_or_404

`Model`의 `instance`를 생성할 때 `get_object_or_404`로 만들 수 있다. 이것으로 `instance`를 만들면 존재하지 않는 `instance`를 `url`로 호출할 때 `500 Server Error`가 아닌 `404 error` message를 전달하도록 해준다.

 ```python
# ...
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment

def detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comments': comments,
        'count': comments.count(),
    }

    return render(request, 'articles/detail.html', context)
 ```

