# Accounts 인증 함수 모음

1~7번 실습과 번외로 accounts 기능들은 아래 코드를 통해 구축할 수 있다.

urls.py
```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

# Create your views here.
def index(request):
    persons = User.objects.all()
    context = {
        'persons': persons
    }
    return render(request, 'accounts/index.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

def logout(request):
    auth_logout(request)
    return redirect('accounts:index')


from django.contrib.auth import update_session_auth_hash

def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/change_password.html', context)
```

템플릿

- index.html
로그인할 경우 계정정보 업데이트 및 로그아웃만 활성화됨
그렇지 않을 경우 회원가입과 로그인만 활성화 됨.
```html
{% extends 'base.html' %}

{% block content %}
{% if request.user.is_authenticated %}
  <a href="{% url 'accounts:update' %}">[Update]</a>
  <form action="{% url "accounts:logout" %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="LOGOUT">
  </form>

{% else %}
  <a href="{% url 'accounts:login' %}">[LOGIN]</a>
  <a href="{% url 'accounts:signup' %}">[Sign Up]</a>
{% endif %}

  <h1>전체 유저 목록</h1>
  <ul>
    {% for person in persons %}
      <li>{{ person.username }}</li>
      <hr>
    {% endfor %}
  </ul>
{% endblock content %}
```

login.html
```html
{% extends 'base.html' %}

{% block content %}
  <h1>LOGIN Page</h1>
  <form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="LOGIN">
  </form>
{% endblock content %}
```

signup.html
```html
{% extends 'base.html' %}

{% block content %}
  <h1>Sign Up Page</h1>
  <form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Sign up">
  </form>
{% endblock content %}
```

update.html
```
{% extends 'base.html' %}

{% block content %}
<a href="{% url "accounts:update" %}">[Update]</a>
<form action="{% url "accounts:logout" %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="LOGOUT">
</form>
  <h1>Update Page</h1>
    <form action="{% url "accounts:update" %}" method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Update">
    </form> 
{% endblock content %}
```

change_password.html
```html
{% extends "base.html" %}
{% block content %}
<a href="{% url "accounts:update" %}">[Update]</a>
<form action="{% url "accounts:logout" %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="LOGOUT">
</form>
<h1>Password Change Page</h1>
<form action="{% url "accounts:change_password" %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Password Change">
</form>
{% endblock content %}
```

urls.py
```python
from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
]
```

models.py
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass
```

forms.py
```python
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    
     class Meta(UserCreationForm.Meta):
        model = get_user_model()

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ['first_name', 'last_name']
```