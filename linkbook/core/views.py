from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import User

from PIL import Image
import pyimgur
import os
from notifications.models import Notification

from linkbook.links.models import Link, Book
from linkbook.core.forms import UpdateProfileForm


IMGUR_CLIENT_ID = "fd0c3e407af9974"
TEMP_IMAGE_PATH = 'linkbook/media/temp.png'


def index(request):
    return render(request, 'core/index.html')


def navbar(request):
    if request.is_ajax():
        books = [book.title for book in Book.objects.filter(user = request.user)]
        notifs = [{'id':notif.target.id, 'text': notif. __str__(), 'pic': notif.actor.profile.pic} 
        for notif in request.user.notifications.unread()]
        return JsonResponse({'books':books, 'notifs':notifs})


def username_slugs(request, username):
    action = request.GET.get('show', None)
    user = get_object_or_404(User, username = username)

    if request.user.is_authenticated:
        follows = request.user.profile in user.profile.followers.all()
        if follows:
            follow_button = "1"
        else:
            follow_button = "2"
    else:
        follow_button = "1"

    if action == 'books':
        user_books = Book.objects.filter(user = user)
        return render(request, 'links/view_books.html', 
            {'user': user, 'view_books':user_books})

    elif action == 'links':
        user_links = Link.objects.filter(user = user)
        user_books = Book.objects.filter(user = user)
        return render(request, 'links/view_links.html', 
            {'user': user, 'view_links':user_links, 'view_books':user_books})

    else:
        links = Link.objects.filter(user = user)[:5]
        books = Book.objects.filter(user = user)[:5]
        link_count = Link.objects.filter(user = user).count()
        book_count = Book.objects.filter(user = user).count()
        follower_count = user.profile.followers.count()
        following_count = user.profile.following.count()
        return render(request, 'core/profile.html', 
            {'user': user, 'links': links, 'books': books, 
            'link_count': link_count, 'book_count': book_count, 
            'follower_count': follower_count,
            'following_count': following_count,
            'follow_button': follow_button})


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username = username)
    if user != request.user:
        return redirect('/{}/'.format(user.username))

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES or None, user = user)
        if form.is_valid():
            user.username = form.clean_username()
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')

            if 'pic' in request.FILES:
                Image.open(request.FILES['pic']).save(TEMP_IMAGE_PATH)
                uploaded_image = pyimgur.Imgur(IMGUR_CLIENT_ID).upload_image(TEMP_IMAGE_PATH)
                os.remove(TEMP_IMAGE_PATH) 
                user.profile.pic = uploaded_image.link
            
            user.profile.save()
            user.save()
            return redirect('/{}/'.format(user.username))
        else:
            return render(request, "core/edit_profile.html", {'form':form})

    form = UpdateProfileForm(user = user, 
        initial = {'username': user.username,
        'first_name':user.first_name, 'last_name': user.last_name,
        'email':user.email})
    return render(request, "core/edit_profile.html", {'form':form})


@login_required
def follow_profile(request):

    if request.method == 'GET':
        user = User.objects.get(username = request.GET['to_follow'])
        if request.user == user:
            return None
        follows = request.user.profile in user.profile.followers.all()

        if follows:
            user.profile.followers.remove(request.user.profile)
            follow_button = "1"
        else:
            user.profile.followers.add(request.user.profile)
            follow_button = "2"
        follower_count = user.profile.followers.count()

        return JsonResponse({'follower_count':follower_count,
            'follow_button': follow_button})



def get_follower_list(request):

    if request.method == 'GET':
        user = User.objects.get(username = request.GET['user'])
        followers = user.profile.followers.all()
        data = []
        for follower in followers:
            row = {}
            row['username'] = follower.user.username
            row['pic'] = follower.pic
            data.append(row)
        return JsonResponse({'data':data})


def get_following_list(request):
    if request.method == 'GET':
        user = User.objects.get(username = request.GET['user'])
        followings = user.profile.following.all()
        data = []
        for following in followings:
            row = {}
            row['username'] = following.user.username
            row['pic'] = following.pic
            data.append(row)
        return JsonResponse({'data':data})
