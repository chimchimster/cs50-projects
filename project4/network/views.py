import json

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError, connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Profile
from .forms import PostFrom

def index(request):
    """ View represents creating new User's post """

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
    flag = 'all_posts'
    return render(request, 'network/index.html', {
        'flag': flag,
    })

def posts(request):
    """ API which does lazy-load for all posts  """

    start = int(request.GET.get('start') or 0)
    end = int(request.GET.get('end') or (start+9))

    qwry = "SELECT network_user.id, username, publishing_date, edit_date, text," \
           " likes FROM network_user INNER JOIN network_post" \
           " ON network_user.id = network_post.user_id ORDER BY network_post.id DESC;"

    # Normalize query to JSON
    posts = json.dumps(create_posts(qwry), default=str)

    # Create list and fill it by JSON objects
    data = []
    try:
        for i in range(start, end + 1):
            data.append(json.loads(posts)[i])
    except IndexError:
        pass

    return JsonResponse({
       'posts': data,
    })


def profile(request, profile):
    # Counting followers_amount and follows_amount
    # to display it at the user's profile
    followers_amount = Profile.objects.get(user__username=profile).followers.count()
    follows_amount = Profile.objects.get(user__username=profile).follows.count()

    # Creating QuerySet which contains all posts of user
    profile_posts = Post.objects.filter(user__username=profile).select_related('user').order_by('-pk')

    # Creating object of Paginator with posts of user (display 5)
    paginator = Paginator(profile_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/index.html', {
        'profile': profile,
        'followers_amount': followers_amount,
        'follows_amount': follows_amount,
        'page_obj': page_obj,
    })

def follows(request, profile):
    """ Generates all posts of profiles which particular profile follows  """
    profile_id = User.objects.get(username=profile).id

    qwry = "SELECT username, publishing_date, edit_date, text, likes" \
           " FROM network_post" \
           " INNER JOIN network_profile_follows ON network_post.user_id = network_profile_follows.user_id" \
           " INNER JOIN network_user ON network_user.id = network_post.user_id" \
           " WHERE network_user.id IN (SELECT profile_id  FROM  network_profile_follows)" \
           f" AND profile_id='{profile_id}'" \
           f" ORDER BY network_post.id DESC;"

    paginator = Paginator(create_posts(qwry), 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/follows.html', {
        'page_obj': page_obj,
    })


@csrf_exempt
def subscribe(request, profile):
    """ API which adds particular User into DB """

    if request.method == 'POST':
        # Load JSON data from request
        data = json.loads(request.body)

        # Take user which is going to be follower
        user = data.get('follower')

        # Take profile on which particular user will be follower
        profile_to_subscribe = Profile.objects.get(user__username=user)

        # Add user to table followers
        profile_to_subscribe.followers.add(request.user)
        profile_to_subscribe.save()

        # Take profile of user to update table follows
        # profiles on which user is subscribed
        follows_profile = Profile.objects.get(user__username=request.user)
        follows_profile.follows.add(profile_to_subscribe.id)
        follows_profile.save()

    return JsonResponse([profile], safe=False)

@csrf_exempt
def unsubscribe(request, profile):
    """ API which removes particular User out of DB """

    if request.method == 'POST':
        # Load data from request
        data = json.loads(request.body)

        # Define user which is going to unsubscribe
        user = data.get('unfollower')

        # Find out profile from which user is going to unsubscribe
        profile_to_unsubscribe = Profile.objects.get(user__username=user)
        profile_to_unsubscribe.followers.remove(request.user)
        profile_to_unsubscribe.save()

        # Update table follows in user's profile
        follows_profile = Profile.objects.get(user__username=request.user)
        follows_profile.follows.remove(request.user)
        follows_profile.save()

    return JsonResponse([profile], safe=False)


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


def create_posts(qwry):
    """ SQL query which connects 2 tables. """

    with connection.cursor() as cursor:
        cursor.execute(qwry)
        columns = [col[0] for col in cursor.description]
        connected_tables = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return connected_tables