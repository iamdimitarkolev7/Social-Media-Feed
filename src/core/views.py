from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse

from .models import Post, Comment, Profile, FollowersCount
from .forms import PostForm, CommentForm, ProfileEditForm

# Signup View
def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('feed')
    return render(request, 'signup.html', {'form': UserCreationForm()})

# Login View
def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('feed')
    return render(request, 'login.html', {'form': AuthenticationForm()})

# Logout View
@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')

# Feed View
def feed(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        following_users = FollowersCount.objects.filter(follower=request.user).values_list('user__username', flat=True)
        followed_posts = Post.objects.filter(user__in=following_users).order_by('-created_at')
        user_posts = Post.objects.filter(user=request.user.username).order_by('-created_at')
        posts = (followed_posts | user_posts).order_by('-created_at')

    return render(request, 'guest_feed.html' if not request.user.is_authenticated else 'feed.html', {'posts': posts})

# Create Post
@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('feed')
    return render(request, 'post_create.html', {'form': form})

# Edit Post
@login_required
def post_edit(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, id=pk)

    if post.user != request.user.username:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('feed')

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "Your post has been updated successfully!")
        return redirect('feed')

    return render(request, 'edit_post.html', {'form': form, 'post': post})

# Delete Post
@login_required
def post_delete(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, id=pk, user=request.user.username)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Your post has been deleted successfully.")
        return redirect('feed')

    return render(request, 'delete_post.html', {'post': post})

# Create Comment
@login_required
def comment_create(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, id=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        return redirect('feed')

    return render(request, 'comment_create.html', {'form': form, 'post': post})

# Delete Comment
@login_required
def comment_delete(request: HttpRequest, pk: int) -> HttpResponse:
    get_object_or_404(Comment, pk=pk, user=request.user).delete()
    return redirect('feed')

# Like a Post
@login_required
def like(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, id=pk)
    liked_posts = post.liked_posts
    if request.user in liked_posts.all():
        liked_posts.remove(request.user)
    else:
        liked_posts.add(request.user)
    return redirect('feed')

# Profile View
def user_profile(request: HttpRequest, username: str) -> HttpResponse:
    profile_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=profile_user)

    posts = Post.objects.filter(user=profile_user).order_by('-created_at')
    liked_posts = Post.objects.filter(likeposts__user=profile_user).distinct()

    is_following = (
        request.user.is_authenticated and
        FollowersCount.objects.filter(follower=request.user, user=profile_user).exists()
    )

    followers = FollowersCount.objects.filter(user=profile_user).count()
    following = FollowersCount.objects.filter(follower=profile_user).count()

    return render(request, 'user_profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'liked_posts': liked_posts,
        'is_following': is_following,
        'followers': followers,
        'following': following,
    })

# Guest Profile View
def guest_profile(request: HttpRequest, username: str) -> HttpResponse:
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=username)
    return render(request, 'guest_profile.html', {'profile_user': profile_user, 'posts': posts})

# Edit Profile View
@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    profile, _ = Profile.objects.get_or_create(user=request.user)

    form = ProfileEditForm(request.POST or None, instance=profile, user=request.user)
    if form.is_valid():
        form.save()
        request.user.username = form.cleaned_data['username']
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('user_profile', username=request.user.username)

    return render(request, 'edit_profile.html', {'form': form})

# Follow User
@login_required
def follow_user(request: HttpRequest, username: str) -> HttpResponse:
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow == request.user:
        messages.error(request, "You cannot follow yourself.")
    else:
        follow, created = FollowersCount.objects.get_or_create(follower=request.user, user=user_to_follow)
        message = f"You are now following {username}." if created else f"You are already following {username}."
        messages.success(request, message)
    
    return redirect('user_profile', username=username)

# Unfollow User
@login_required
def unfollow_user(request: HttpRequest, username: str) -> HttpResponse:
    user_to_unfollow = get_object_or_404(User, username=username)
    follow = FollowersCount.objects.filter(follower=request.user, user=user_to_unfollow)
    
    if follow.exists():
        follow.delete()
        messages.success(request, f"You have unfollowed {username}.")
    else:
        messages.info(request, f"You are not following {username}.")

    return redirect('user_profile', username=username)

# Search Users
def search_users(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q', '')
    users = User.objects.filter(Q(username__icontains=query))
    return render(request, 'search_users.html', {'users': users, 'query': query})
