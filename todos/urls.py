from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='todos-home'),
    path('about/', views.about, name='todos-about'),
    path('personalTodos', views.personalTodos, name='todos-personal'),
    path('updateTodos', views.updateTodos, name='update-personal'),
]
