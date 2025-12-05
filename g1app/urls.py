from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news, name='news'),
    path('teams/', views.teams, name='teams'),
    path('about/', views.about, name='about'),
    path('schedule/', views.schedule, name='schedule'),



    path('signin/', views.Register_signIn, name='Register_signIn'),
    path('register/', views.Register_page, name='Register_page'),
    path('logout/', views.logout_user, name='logout_user'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),


    # article model url
    path('article/<int:id>/', views.article_detail, name='article_detail'),

    # race result
    path("race-results/", views.race_results, name="race_results"),

    # video details
    path("video/<int:id>/", views.video_detail, name="video_detail"),




]
