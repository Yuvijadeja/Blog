from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('account', views.account, name='account'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('update-profile', views.update_profile, name='update-profile'),
    path('change-password', views.change_pass, name='change-password'),
    path('forgot-password', views.forgot_pass, name='forgot-password'),
]
