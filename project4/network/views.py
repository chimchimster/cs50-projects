import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Profile
from .forms import PostFrom

def index(request):
    if request.method == "POST":
        post_form = PostFrom(request.POST)
        if post_form.is_valid():
            text = post_form.cleaned_data.get('text_area')
            post = Post(text=text, user=request.user)
            post.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        post_form = PostFrom()
        return render(request, "network/index.html", {
            'post_form': post_form,
        })

def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'network/index.html', {
        'posts': posts[::-1],
    })

@csrf_exempt
def profile(request, profile):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data.get('follower')
        new_follower = request.user
        check_for_profile = Profile.objects.filter(user__username=user)
        return render(request, 'network/index.html')
    else:
        return render(request, 'network/index.html', {
            'profile': profile,
            'followers_amount': 1,
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
