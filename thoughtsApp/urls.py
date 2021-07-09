from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('post_message', views.post_message),
    path('post_comment/<int:user_id>', views.post_comment),
    path('profile/<int:user_id>', views.profile),
    path('like/<int:user_id>', views.like),
    path('delete_comment/<int:user_id>', views.delete_comment),
    path('edit/<int:user_id>', views.edit),
]