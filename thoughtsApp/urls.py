from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('thoughts', views.show_all),
    path('create_thoughts', views.create_thoughts),
    path('user', views.show_one),
    path('like/<int:user_id>', views.like),
    path('delete/<int:user_id>', views.delete),
]
