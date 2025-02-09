# core/urls.py

from django.urls import path, re_path
from . import views

from django.shortcuts import redirect

def redirect_to_feed(request):
    return redirect('feed')

urlpatterns = [
    # Redirecting to Home Page to Feed Page
    path('', redirect_to_feed),
    
    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Feed
    path('feed/', views.feed, name='feed'),

    # Posts
    path('post/create/', views.post_create, name='post_create'),
    path('post/<uuid:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<uuid:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<uuid:pk>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('post/<uuid:pk>/like/', views.like, name='like'),

    # Profile
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('guest/profile/<str:username>/', views.guest_profile, name='guest_profile'),

    # Follow/Unfollow
    path('follow/<str:username>/', views.follow_user, name='follow_user'),  # Follow user
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),  # Unfollow user

    # Search
    path('search/', views.search_users, name='search_users'),
]