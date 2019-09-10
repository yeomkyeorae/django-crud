from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


def new(request):
    return render(request, 'articles/new.html')


def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    article = Article(title=title, content=content)
    article.save()
    # context = {
    #     'number': len(Article.objects.all()),
    # }

    # return render(request, 'articles/create.html', context)
    return redirect('articles:detail', article.pk)


def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article': article,
    }

    return render(request, 'articles/detail.html', context)


def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    article.delete()

    return redirect('articles:index')


def update(request, article_pk):
    article = Article.objects.get(pk=article_pk) 
    context = {
        'article': article,
        'article_pk': article_pk,
    }
    return render(request, 'articles/update.html', context)


def updated(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    article.title = request.POST.get('title')
    article.content = request.POST.get('content')
    article.save()
    return render(request, 'articles/updated.html')