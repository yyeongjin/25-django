from django.urls import path
from .views import index, num, create, delete

app_name = 'articles'

urlpatterns = [
    path('', index, name="index"),
    path('<int:num>/', num, name="num"),
    path('create/', create, name="create"),
    path('delete/<int:num>/', delete, name="delete"),
]