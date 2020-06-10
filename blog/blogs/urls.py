from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles', views.articles, name='articles'),
    path('articles/<str:filter_blog>', views.articles, name='articles'),
    path('blog-detail/<str:blog_id>', views.blog_detail, name='blog-detail'),
    path('blog-post', views.blog_post, name='blog-post'),
    path('delete-blog/<str:blog_id>', views.delete_blog, name='delete-blog'),
]
