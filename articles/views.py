from django.shortcuts import render, redirect
# POST 요청만 허용할 수 있도록 'require_POST'를 import, 아래 delete에서 사용
from django.views.decorators.http import require_POST
# embed를 사용하면 embed() 함수에서 실행이 멈추고 IPython이 열려 현재까지의 변수 내용을 출력해 볼 수 있음.
from IPython import embed

from .models import Article


# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    # embed()
    return render(request, 'articles/index.html', context)


def create(request):
    # request의 방식이 'GET'이면
    if request.method == 'GET':
        return render(request, 'articles/new.html')
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article(title=title, content=content)
        article.save()
        # app_name: articles의 name이 detail인 path
        return redirect('articles:detail', article.pk)



def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article': article,
    }

    return render(request, 'articles/detail.html', context)

# POST 요청만 받아들이기 위한 decorator
@require_POST
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    article.delete()
    # app_name: articles의 name이 index인 path
    return redirect('articles:index')
    # else:
    #     return redirect('articles:detail', article.pk)


def update(request, article_pk):
    article = Article.objects.get(pk=article_pk) 
    # 요청 방식이 'GET'이면
    if request.method == 'GET':
        context = {
            'article': article,
            'article_pk': article_pk,
        }

        return render(request, 'articles/update.html', context)
    else:
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.save()

        return render(request, 'articles/updated.html')
