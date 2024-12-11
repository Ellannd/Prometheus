from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from . import views


urlpatterns = [
    path('',views.home, name="home"),
    path('profile/',views.profile, name="profile"),
    path('profile/<str:username>/',views.otherUser, name="otherProfile"),
    path('upload/', views.uploadArtwork, name="upload"),
    path('artworks/<int:pk>/',views.artwork, name="artworks"),
    path("artworks/<int:pk>/like/", views.like_artwork, name="like"),
    path('register/',views.register, name="register"),
    path('login/',views.login_user, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("settings/", views.settings, name="settings"),
    path("editProfile/", views.editProfile, name="editProfile"),
]
