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



# 6. Add static files

`CSS`, `Javascript`, `Bootstrap`, `favicon(title에 있는 작은 icon)` 등의 파일들은 `static` 폴더에 보관하는 것이 편리하다.

`project`이름(`crud`) 아래 `assets`라는 이름으로 폴더를 만들어 관리한다.

`Settings`에 있는 기본 `STATIC_URL`외에도 `STATICFILES_DIRS` 변수를 추가해 관리해 주어야 한다. 예를 들어,

```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'crud', 'assets')
]
```

`html`에서 `static` 파일을 불러들일 때는 반드시 `html` 위에`load static`을 명시해 주어야 한다. `base.html`을 `extends`할 경우에는 반드시 그 아래 작성해야 한다. 예를 들어,

```html
{% extends 'articles/base.html' %}
{% load static %}
<!-- -->
<link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.min.css' %}">
<!-- -->
```

 `load`할 때는 `{% static '~' %}` 식으로 작성해야 함을 잊지 말자. (static 경로에도 주의)





# 7. Add image file upload

- `models.py`

  - `models.ImageField`를 사용한다.
  - `thumnail`을 사용할 경우 [imagekit](https://github.com/matthewwithanm/django-imagekit)을 install해 사용한다.

  ```python
  from django.db import models
  from imagekit.models import ProcessedImageField, ImageSpecField
  from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail
  
  class Article(models.Model):
      title = models.CharField(max_length=30)
      content = models.TextField()
      image = models.ImageField(blank=True)  # blank=True를 사용하면 기존 DB에 영향을 주지 											않으면서 column을 추가할 수 있다.
      image_thumbnail = ProcessedImageField(
          processors=[ResizeToFill(300, 300)],
          format='JPEG',
          options={'quality': 80},
      )
  ```

  - `thumbnail`에 사용할 수 있는 대표적인 함수(?)에는 `ImageSpecField`와 `ProcessedImageField`가 있는데 전자는 `image`으로 삼아 썸네일화 하지만, 후자는 따로 입력을 받아 썸네일화한다. 



- `views.py`

  - `views.py`에서 이미지를 저장하려면 `request.POST` 이외에 `request.FILES`를 필요로 한다.
  - 예시 코드는 아래와 같다.

  ```python
  def create(request):
      if request.method == 'GET':
          article_form = ArticleForm()
      else:
          # ArticleForm(request.POST, request.FILES)를 활용할 수도 있다.
          article_form = ArticleForm(request.POST)
          if article_form.is_valid():
              article = article_form.save(commit=False) 
              # commit=False를 하면 바로 저장되지 않고 추가적으로 데이터를 저장할 수 있게 한다.
              article.image = request.FILES.get('image')
              article.image_thumbnail = article.image	# ProcessedImageField를 사용해서
              article.save()
              
              return redirect('articles:detail', article.pk)
        # ...
  ```



- `media` 폴더

  `media` 폴더를 사용해서 `이미지`, `썸네일`, `동영상` 등을 관리하자. `media`를 사용하기 위해서는 `settgins.py`에 `MEDIA_ROOT`와 `MEDIA`_URL`을 등록해야 한다.

  ```python
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
  MEDIA_URL = '/media/'
  ```

  

- `favicon`

  - `favicon`은 page의 `title` 옆에 있는 작은 `icon`을 말한다.
  - `favicon`이미지는 [여기](https://www.favicon-generator.org/)에서 기존 이미지를 변환하여 사용할 수 있다.
  - 아래와 같이 `load`해 사용하자

  ```html
  <link rel="icon" type="image/png" sizes="32x32" href="{% static 'favicon/favicon-32x32.png' %}">
    <link rel="shortcut icon" href="{% static 'favicon/favicon.ico'%}" type="image/x-icon">
  ```

  




## 8. Accounts(Signup, login, logout, authentication)

1. First of all, Create App `Accounts`, enroll App, make urls, ...

2. `views.py`에서`signup(회원가입)`, `login(로그인)`, `logout(로그아웃)`의 logic은 기존 게시글의 `create`와 유사하다.

   > `Signup`(회원가입)

   ```python
   from django.contrib.auth.forms import UserCreationForm, Authentication
   from django.contrib.auth import login as auth_login
   from django.contrib.auth import logout as auth_logout
   
   def signup(request):
       if request.user.is_authenticated:
           return redirect('articles:index')
       if request.method == 'POST':
           user_creation_form = UserCreationForm(request.POST)
           if user_creation_form.is_valid():
               user_creation_form.save()
               return redirect('articles:index')
       else:
           user_creation_form = UserCreationForm()
      	context = {
           'user_creation_form': user_creation_form,
       }
       
       return render(request, 'accounts/signup.html', context)
   ```

   - `회원가입`과 `로그인` 기능을 구현하기 위해 필요한 모듈은 `django.contrib.auth`에 포함돼 있으며, 추가적으로 `form`기능도 `django.contrib.auth.forms`에 회원가입과 로그인에 해당하는 `UseCreationForm` 과 `Authentication`에 있다.
   - `사용자`가 로그인이 되어있는지 판별하기 위해 `request.user.is_authenticated`변수를 활용하는데, 로그인이 되어있을 경우 `request`가 별도 작업없이도 `user`정보를 이미 가지고 있다. 
   - 그 외에는 `create`와 유사하다.

   > `Login`

   ```python
   def login(request):
       if request.method == 'POST':
           auth_form = AuthenticationForm(request, request.POST)
           if auth_form.is_valid():
               user = auth_form.get_user()
               auth_login(request, user)
               return redirect(request.GET.get('next') or 'articles:index')
       else:
           auth_form = AuthenticationForm()
       context = {
           'form': form,
       }
       
       return render(request, 'accounts/login.html', context)
   ```

   - `login`은 `Session`(?)을 생성해야 하므로 `Create`와 구성이 약간 다르다.
   - 다른 `form`과는 다르게 `AuthenticationForm`의 인자에 `request`와 `request.POST`가 순서대로 들어간다.
   - `auth_login`을 통해 로그인 로직 실행, 인자로 `request`와 `user`.
   - `request.GET.get('next') or 'articles:index'` 부분은 로그인이 되어 있는 상태이면 원래 실행될 상태(`next`)로 바꾸고, 아니라면 `index`페이지로 전환한다.

   > `Logout`

   ```python
   def logout(request):
       auth_logout(request)
       return redirect('articles:index')
   ```

   - `auth_logout`을 통해 로그아웃 로직을 실행

3. `html` logic

   > 로그인이 가능해짐에 따라서 `html`에서 로그인 상태일 때, 로그아웃 상태일 때 별로 서로 다른 logic을 만들 수 있다.

   ```html
   {% if user.is_authenticated %}
   <!-- 로그인 상태 -->
   <li class="nav-item">
     <a class="nav-link" href="{% url 'accounts:logout'%}">로그아웃</a>
   </li>
   {% else %}
   <!-- 로그아웃 상태 -->
   <li class="nav-item">
     <a class="nav-link" href="{% url 'accounts:signup'%}">회원가입</a>
   </li>
   <li class="nav-item">
     <a class="nav-link" href="{% url 'accounts:login'%}">로그인</a>
   </li>
   {% endif %}
   ```

   - `context`에 `user`정보를 넘겨주지 않아도 `request`에 기본적으로 `user`정보를 갖고 있으므로 `user.is_authenticated`를 사용해 로그인이 되어 있는지 아닌지 확인할 수 있다.
   - 로그인이 되어있다면 로그아웃 `a`태그를 활성화하고, 로그아웃 상태이면 회원가입과 로그인 `a`태그를 활성화한다.



## 9. Authentication

```
* 장고는 User 관련 기능이 내부적으로 있다.
	-> 가져다가 쓰면 됨.
? django.contrib.auth.models.User 변경할 상황에서?
 -> 상속 받아서 내가 만들면 됨.
 -> DB와 연결되어 있음. 다 바꿔야 함. 나중에
 -> 프로젝트 만들면서 미리 해라. django의 추천!
 -> 바꿨는데 그러면 장고 내부에서 어떻게 알지 ? -> settings 설정의 AUTH_USER_MODEL
 -> User 클래스를 어떻게 가져다 쓰는데? -> get_user_model(): settings 설정을 봄.
 
? models.py에서도 get_user_model() 쓸 수 있음?
 -> 아닐 수 있다. 장고가 명령어를 수행할 때, INSTALLED_APPS -> models / apps
 -> User 클래스가 아직 없을 수 있다. (이름)
 -> 그 땐 그냥 settings.AUTH_USER_MODEL로 문자열을 찍어 놓으면, 알아서 바꿔준다.
 
? 근데 왜 갑자기 UserCreationForm 못씀?
실제로 내부 코드 보면 바보 같이 user를 그대로 import해서 씀
(from django.contrib.auth.models import User)
-> 혼나야함. get_user_model()로 써야하는데. 그럼 어떻게 바꾼다?
-> 상속 받아서 덮어쓰자!
 
! 프로젝트 시작하면 User 모델 빼자
User 클래스가 필요하면, get_user_model()호출해서 쓰자.
models.py에서만 settings.AUTH_USER_MODEL 스자
```

### 1. `User` Class

- [기본 문서](https://docs.djangoproject.com/en/2.2/topics/auth/default/#user-objects)

> django에서는 프로젝트를 시작할 때, 항상 `User` Class를 직접 만드는 것을 추천함! [링크](https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model)
>
> django의 기본 Authentication과 관련된 설정 값들을 활용하기 위해 `accounts` 앱으로 시작하는 것을 추천함! (예 - LOGIN_URL = '/accounts/login/')

1. models.py

   ```python
   # accounts/models.py
   from django.contrib.auth.models import AbstractUser
   
   class User(AbstractUser):
       pass
   ```

   - django 내부에서 `User`를 기본적으로 사용한다. 예) `python manage.py createsuperuser`
   - 확장 가능성(변경)을 위해 내가 원하는 앱에 class를 정의!
   - `User` 상속관계( [Github 링크](https://github.com/django/django/blob/master/django/contrib/auth/models.py#L384) | [공식문서 링크](https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#fields) )
     - `AbstractUser` : `username`, `last_name`, `first_name`, `email`, ...
     - `AbstractBaseUser`: `password`, `last_login`
     - `models.Model`

2. Settings.py

   ```python
   # project/settings.py
   AUTH_USER_MODEL = 'accounts.User'
   ```

   - `User` 클래스를 활용하는 경우에는 `get_user_model()`함수를 호출하여 사용한다.

     ```python
     # accounts/forms.py
     from django.contrib.auth import get_user_model
     
     class CustomeUserCreation(UserCreatinForm):
         class Meta:
             model = get_user_model()
     ```

     

   - 단, `models.py`에서 사용하는 경우에는 `settings.AUTH_USER_MODEL`을 활용한다. [공식문서 - settings](https://docs.djangoproject.com/en/2.2/ref/settings/#auth-user-model)

     ```PYTHON
     # articles/models.py
     from django.conf import settings
     
     class Article(models.Model):
         user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     ```

   - [공식문서 - Referencing the `User` model](https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#referencing-the-user-model)

3. `admin.py`

   - admin 페이지를 활용하기 위해서는 직접 작성을 해야 한다.

   - `UserAdmin` 설정을 그대로 활용할 수 있다

     ```python
     # accounts/admin.py
     from django.contrib.auth.admin import UserAdmin
     from .models import User
     
     admin.site.register(User, UserAdmin)
     ```

     

### 2. Authentication Forms

- [공식문서 - Custom users and the built-in auth forms](https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms)

#### 1. `UserCreationForm` : `ModelForm`

- custom user를 사용하는 경우 반드시 직접 사용할 수 없음.
  - 실제 코드상에 `User`가 직접 import 되어 있기 때문에. [Github 링크 - UserCreationForm](https://github.com/django/django/blob/master/django/contrib/auth/forms.py#L94)

```python
# accounts/forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username',)
```

- `ModelForm`이므로 활용 방법은 동일하다.

#### 2. `UserChangeForm` : `ModelForm`

- custom user를 사용하는 경우 직접 사용할 수 없음.
- 그대로 활용하는 경우 `user`와 관련된 모든 내용을 수정하게 됨. 
  - 실제 코드 상에 필드가 `'__all__'`로 설정되어 있음. [Github 링크 - UserChangeForm](https://github.com/django/django/blob/master/django/contrib/auth/forms.py#L144)

```python
# accounts/forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', ...)
```

#### 3. `AuthenticationForm`

- `ModelForm`이 아님! <b>인자 순서를 반드시 기억하자!</b>
- `AuthenticationForm(request, data, ...)`: [Github 링크 - AuthenticationForm](https://github.com/django/django/blob/master/django/contrib/auth/forms.py#L183)

```python
form = AuthenticationForm(request=request, data=request.POST)
if form.is_valid():
    user= form.get_user()
```

- 로그인에 성공한 `user`의 인스턴스는 `get_user` 메소드를 호출하여 사용한다.

- 실제 로그인은 아래의 함수를 호출하여야 한다. [공식문서 링크]https://docs.djangoproject.com/en/2.2/topics/auth/default/#how-to-log-a-user-in()

  ```python
  from django.contrib.auth import login as auth_login
  auth_login(request, user)
  ```

- 로그인 여부에 따른 접근 제어는 직접 하거나 데코레이터를 활용한다. [공식문서 링크](https://docs.djangoproject.com/en/2.2/topics/auth/default/#limiting-access-to-logged-in-users)

#### 4. `PasswordChangeForm`

- `ModelForm`이 아님! <b> 인자 순서를 반드시 기억하자!</b>

- `passwordChangeForm(user, data)`

  ```python
  if request.method == 'POST':
      form = PasswordChangeForm(request.user, request.data)
  else:
      form = PasswordChangeForm(request.user)
  ```

- 비밀번호가 변경이 완료된 이후에는 기존 세션 인증 내역이 바뀌어서 자동으로 로그아웃이 된다. 아래의 함수를 호출하면, 변경된 비밀번호로 세션 내역을 업데이트한다. [공식문서 링크](https://docs.djangoproject.com/en/2.2/topics/auth/default/#session-invalidation-on-password-change)

  ```python
  from django.contrib.auth import update_session_auth_hash
  update_session_auth_hash(request, form.user)
  ```

  

### 3. Appendix. Import

```python
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import AutenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.decorators import login_required
```

```python
from django.conf import settings
```

```python
from django.db import models  # models.Model, models.CharField() ...
from django import forms  # forms.ModelForm, forms.Form 
```

```python
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
```

