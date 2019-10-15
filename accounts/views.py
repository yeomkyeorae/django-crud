from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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