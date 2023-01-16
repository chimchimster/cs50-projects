import json
import time

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
    return render(request, 'network/index.html')

def posts(request):

    # Get start and end points
    start = int(request.GET.get('start') or 0)
    end = int(request.GET.get('end') or (start+9))

    # Load all posts of all users
    posts = Post.objects.all().values()
    posts = [post for post in posts]
    posts.reverse()

    # Generate list of posts
    data = []
    try:
        for i in range(start, end + 1):
            user = User.objects.get(pk=posts[i]['user_id'])
            print(user)
            data.append((
                user,
                posts[i]['publishing_date'],
                posts[i]['edit_date'],
                posts[i]['text'],
                posts[i]['likes']
            ))
    except IndexError:
        pass

    # Delay speed of response
    time.sleep(1)

    # Return list of posts
    return JsonResponse({
       'posts': data,
    })


def profile(request, profile):
    followers_amount = Profile.objects.get(user__username=profile).followers.count()
    follows_amount = Profile.objects.get(user__username=profile).follows.count()
    profile_posts = Post.objects.filter(user__username=profile).select_related('user')
    all_posts = [post for post in profile_posts]
    all_posts.reverse()
    return render(request, 'network/index.html', {
        'profile': profile,
        'followers_amount': followers_amount,
        'follows_amount': follows_amount,
        'profile_posts': all_posts,
    })

@csrf_exempt
def subscribe(request, profile):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data.get('follower')
        _profile = Profile.objects.get(user__username=user)
        _profile.followers.add(request.user)
        _profile.save()
        _follows_profile = Profile.objects.get(user__username=request.user)
        _follows_profile_id = _profile.id
        _follows_profile.follows.add(_follows_profile_id)
        _follows_profile.save()
    return JsonResponse([profile], safe=False)

@csrf_exempt
def unsubscribe(request, profile):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data.get('unfollower')
        _profile = Profile.objects.get(user__username=user)
        _profile.followers.remove(request.user)
        _profile.save()
    return JsonResponse([profile], safe=False)

def get_followers(request, profile):
    # for button follow/unfollow
    pass

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
