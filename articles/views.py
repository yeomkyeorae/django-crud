from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
# POST 요청만 허용할 수 있도록 'require_POST'를 import, 아래 delete에서 사용
from django.views.decorators.http import require_POST, require_GET
# embed를 사용하면 embed() 함수에서 실행이 멈추고 IPython이 열려 현재까지의 변수 내용을 출력해 볼 수 있음.
from IPython import embed
from accounts.models import User
# from django.contrib.auth import get_user_model
from .models import Article, Comment, HashTag
from .forms import ArticleForm, CommentForm


# Create your views here.
def index(request):
    articles = Article.objects.all()
    # embed()
    context = {
        'articles': articles,
    }
    # embed()
    return render(request, 'articles/index.html', context)


@login_required
def create(request):
    # request의 방식이 'GET'이면

    # if not request.user.is_authenticated:
    #     return redirect('accounts:login')

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
            article.image_thumbnail = article.image
            article.user = request.user
            article.save()
            # 해시태그 저장 및 연결 작업
            
            for word in article.content.split():
                if len(word) > 1 and word[0] == '#':
                    hashtag, created = HashTag.objects.get_or_create(content=word)
                    article.hashtags.add(hashtag)

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
        # 'count': comments.count(),
        'comment_form': comment_form,
        'image': article.image,
    }

    return render(request, 'articles/detail.html', context)


# POST 요청만 받아들이기 위한 decorator
@require_POST
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if article.user == request.user:
        article.delete()
    # app_name: articles의 name이 index인 path
        return redirect('articles:index')
    else:
        return HttpResponseForbidden()
    # else:
    #     return redirect('articles:detail', article.pk)


def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    # article = get_object_or_404(Article, article_pk)
    # 요청 방식이 'GET'이면    
    if request.method == 'GET':
        if article.user != request.user:
            return HttpResponseForbidden()
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
            article = article_form.save()  # return 되는 것은 article instance
            article.hashtags.clear()
            for word in article.content.split():
                if len(word) > 1 and word[0] == '#':
                    hashtag, created = HashTag.objects.get_or_create(content=word)
                    article.hashtags.add(hashtag)

            return redirect('articles:detail', article_pk)

    context = {
        'article_form': article_form,
        # 'article': article,
        # 'article_pk': article_pk,
    }
    return render(request, 'articles/form.html', context)


@require_POST
def comment_create(request, article_pk):
    if request.user.is_authenticated:
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
            comment.user = request.user
            comment.save()
            messages.add_message(request, messages.INFO, '댓글이 생성되었습니다.')

        # 4. redirect
            return redirect('articles:detail', article_pk)
    else:
        return HttpResponse('Unauthorized', status=401)
    # comment = Comment()
    # comment.content = request.POST.get('comment')
    # comment.article = article
    # comment.save()
    
    # return redirect('articles:detail', article_pk)


@require_POST
def comment_delete(request, comment_pk, article_pk):
    comment = Comment.objects.get(pk=comment_pk)
    # comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        messages.warning(request, '댓글이 삭제되었습니다.')

        return redirect('articles:detail', article_pk)
    else:
        return HttpResponseForbidden()


@login_required
def like(request, article_pk):
    if request.is_ajax():
        article = get_object_or_404(Article, pk=article_pk)
        # 좋아요를 누른 적이 있다면
        # if article.like_users.filter(id=request.user.id):
        is_liked = True
        if request.user in article.like_users.all():
            request.user.like_articles.remove(article)
            is_liked = False
        else:
            request.user.like_articles.add(article)
            is_liked = True
        like_cnt = article.like_users.count()
        return JsonResponse({'is_liked': is_liked, 'like_cnt': like_cnt})
    else:
        return HttpResponseForbidden()


def hashtag(request, tag):
    hashtag = get_object_or_404(HashTag, pk=tag)
    context = {
        'hashtag': hashtag,
    }
    return render(request, 'articles/hashtag.html', context)


def explore(request):
    from itertools import chain
    followings = request.user.followings.all()
    followings = chain(followings, [request.user])
    articles = Article.objects.filter(user__in=followings).order_by('-id')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)