from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, CustomUserCreationForm


# Create your views here.
def signup(request):
    # 로그인됐는데 회원가입 하려고 하는 경우 방지
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            return redirect('articles:index')
    else:
        user_creation_form = CustomUserCreationForm()
    context = {
        'form': user_creation_form,
    }

    return render(request, 'accounts/form.html', context)


# login은 Session을 생성해야하므로 게시글 create와 형식이 조금 다르다.
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)   # 인자 순서가 이전과 다르다.
        if form.is_valid():
            # 로그인
            user = form.get_user()  # User의 instance return
            auth_login(request, user)
            # request 안에 user 정보가 들어있다.
            return redirect(request.GET.get('next') or 'articles:index')
            # @login_required 달고 왔을 때 다음으로 redirect 아니면 index 페이지로 redirect
            # http://127.0.0.1:8000/accounts/login/?next=/articles/create/
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }

    return render(request, 'accounts/form.html', context)


def logout(request):
    auth_logout(request)
    return redirect('articles:index')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)    # 비밀번호 변경 후 로그인 상태가 유지되도록
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)


@login_required
def profile(request, account_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=account_pk)

    context = {
        'user_profile': user,
    }
    return render(request, 'accounts/profile.html', context)


def follow(request, account_pk):
    User = get_user_model()
    follower = get_object_or_404(User, pk=account_pk)
    if follower != request.user:
        # following
        if request.user in follower.followers.all():
            follower.followers.remove(request.user)
        # not following
        else:
            follower.followers.add(request.user)

    return redirect('accounts:profile', account_pk)