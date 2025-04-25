from django.urls import path
from . import views


urlpatterns = [
    path('users/',views.usersGetListOrPost),
    path('users/<int:user_id>/',views.usersPatchOrDelete),
    path('posts/',views.postsGetListOrPost),
    path('posts/<int:post_id>/', views.postsPatchOrDelete)
]