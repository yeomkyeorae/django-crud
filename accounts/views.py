from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


# Create your views here.
def signup(request):
    # 로그인됐는데 회원가입 하려고 하는 경우 방지
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

    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('articles:index')