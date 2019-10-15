from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),   # accounts C
    path('login/', views.login, name="login"),
]