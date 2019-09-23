from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# POST 요청만 허용할 수 있도록 'require_POST'를 import, 아래 delete에서 사용
from django.views.decorators.http import require_POST, require_GET
# embed를 사용하면 embed() 함수에서 실행이 멈추고 IPython이 열려 현재까지의 변수 내용을 출력해 볼 수 있음.
from IPython import embed

from .models import Article, Comment
from .forms import ArticleForm, CommentForm


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
        article_form = ArticleForm()
    else:
    # POST 요청 -> 검증 및 저장
        # title = request.POST.get('title')
        # content = request.POST.get('content')
        article_form = ArticleForm(request.POST)
        # 검증
        # embed()
        if article_form.is_valid():
            # title = article_form.cleaned_data.get('title')
            # content = article_form.cleaned_data.get('content')
            # article = Article(title=title, content=content)
            # article.save()

            # article = article_form.save()
            article = article_form.save(commit=False)
            article.image = request.FILES.get('image')
            article.save()

            return redirect('articles:detail', article.pk)
    
    context = {
        'article_form': article_form,
    }
    return render(request, 'articles/form.html', context)




def detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    
    comment_form = CommentForm()

    comments = article.comment_set.all()
       
    context = {
        'article': article,
        'comments': comments,
        'count': comments.count(),
        'comment_form': comment_form,
        'image': article.image,
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
        # article_form = ArticleForm(initial={
        #     'title': article.title, 
        #     'content': article.content,
        #     })
        article_form = ArticleForm(instance=article)

    else:
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            # article.title = article_form.cleaned_data.get('title')
            # article.content = article_form.cleaned_data.get('content')
            # article.save()
            article = article_form.save()

            return render(request, 'articles/updated.html')

    context = {
        'article_form': article_form,
        # 'article': article,
        # 'article_pk': article_pk,
    }
    return render(request, 'articles/form.html', context)


@require_POST
def comment_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    # 1. modelForm에 사용자 입력 값 넣고
    comment_form = CommentForm(request.POST)
    # 2. 검증하고
    if comment_form.is_valid():
    # 3. 맞으면 저장
        # 3-1. 사용자 입력값으로 comment instance 생성 (저장은 x)
        comment = comment_form.save(commit=False)
        # 3-2. FK 넣고 저장
        comment.article = article
        comment.save()
        messages.add_message(request, messages.INFO, '댓글이 생성되었습니다.')

    # 4. redirect
        return redirect('articles:detail', article_pk)
    # comment = Comment()
    # comment.content = request.POST.get('comment')
    # comment.article = article
    # comment.save()
    
    # return redirect('articles:detail', article_pk)


@require_POST
def comment_delete(request, comment_pk, article_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()

    messages.warning(request, '댓글이 삭제되었습니다.')

    return redirect('articles:detail', article_pk)