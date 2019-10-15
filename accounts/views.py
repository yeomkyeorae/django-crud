from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login


# Create your views here.
def signup(request):
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
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }

    return render(request, 'accounts/login.html', context)