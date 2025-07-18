from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from posts.forms import SignUpForm, PostForm
from posts.models import Post, Profile
import logging

logger = logging.getLogger(__name__)


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# @login_required
def home(request):
    logger.info("Home view accessed")
    posts = Post.objects.all().order_by("-created_at")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        logger.info(f"PostForm data: {form.data}, files: {form.files}")
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "home.html", {"form": form, "posts": posts})


# @login_required
def profile_view(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    posts = Post.objects.filter(author=user).order_by("-created_at")
    return render(request, "profile.html", {"profile": profile, "posts": posts})


@login_required
def create_post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "create_post.html", {"form": form})


# @login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "post_detail.html", {"post": post})
