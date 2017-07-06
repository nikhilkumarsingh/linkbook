from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from PIL import Image
import pyimgur
import os
from notifications.models import Notification
from notifications.signals import notify

from linkbook.links.models import Link, Book, Comment
from linkbook.links.forms import LinkForm, BookForm, CommentForm
from linkbook.core.forms import UpdateProfileForm

from taggit.models import Tag
from taggit.utils import _parse_tags
import humanize
from datetime import datetime, timezone

IMGUR_CLIENT_ID = "fd0c3e407af9974"
TEMP_IMAGE_PATH = 'linkbook/media/temp.png'

UP = 0
DOWN = 1
vote_color = "lighten-5"


def project(request):
    return render(request, 'core/project.html')



def index(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            user = User.objects.get(username = request.user)
            followings = user.profile.following.all()
            all_links = []
            for following in followings:
                links = Link.objects.filter(user = following.user).order_by('-last_updated')
                for link in links[:5]:
                    row = {}
                    link_time = humanize.naturaltime(datetime.now(timezone.utc) - link.date)
                    comment_form = CommentForm()
                    upvotes = link.votes.count(action = UP)
                    downvotes = link.votes.count(action = DOWN)
                    upvoted = link.votes.exists(request.user.id, action = UP)
                    downvoted = link.votes.exists(request.user.id, action = DOWN)

                # upvote button config
                    if not upvoted:
                        upvote_button = ""
                    else:
                        upvote_button = vote_color

                # downvote button config
                    if not downvoted:
                        downvote_button = ""
                    else:
                        downvote_button = vote_color

                    row['link'] = link
                    row['comment_form'] = comment_form
                    row['og'] = link.og_data
                    row['upvotes'] = upvotes
                    row['downvotes'] = downvotes
                    row['time'] = link_time
                    row['upvote_button'] = upvote_button
                    row['downvote_button'] = downvote_button

                    all_links.append(row)

        return render(request, 'core/index.html', {'all_links':all_links})
    else:
        return render(request, 'core/home.html')


def fetch_notifs(user):
    # fetch last 15 notifications
    notifs = []
    for notif in user.notifications.all()[:15]:
        try:
            mydict = {}
            if notif.verb == "followed":
                mydict['url'] = "/" + notif.actor.username
                mydict['text'] = notif. __str__().replace(notif.recipient.username, "you")
            else:
                mydict['url'] = "/link/" + str(notif.target.id)
                mydict['text'] = notif. __str__()

            mydict['unread'] = notif.unread
            mydict['pic'] = notif.actor.profile.pic
            notifs.append(mydict)       
        except:
            notif.delete()
    return notifs


@csrf_exempt
def navbar(request):
    if request.is_ajax():
        books = [book.title for book in Book.objects.filter(user = request.user)]
        print((request.user.notifications.count()))

        # check if any new notifications
        if len(request.user.notifications.unread()):
            new_notifs = True
            notifs = fetch_notifs(request.user)
        else:
            new_notifs = False
            if 1:#int(request.POST.get('notif')) == 1:
                notifs = fetch_notifs(request.user)
            else:
                notifs = None

        return JsonResponse({'books':books, 'notifs':notifs, 'new_notifs':new_notifs})



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
        user_books = Book.objects.filter(user = user).order_by('-last_updated')
        return render(request, 'links/view_links.html', 
            {'user': user, 'view_links':user_links, 'view_books':user_books})

    elif action == 'upvoted':
        upvoted_links = user.profile.upvoted_links.all()    
        return render(request, 'links/view_upvoted_links.html', {'links':upvoted_links})        

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
                x,y,w,h = float(request.POST.get('imageX')), float(request.POST.get('imageY')), \
                float(request.POST.get('imageW')),float(request.POST.get('imageH'))
                Image.open(request.FILES['pic']).crop((x,y,x+w,y+h)).save(TEMP_IMAGE_PATH)
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
            notify.send(request.user, recipient = user, 
                    target = user, verb = "followed")
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


def trending(request):
    if request.method == 'GET':
        return render(request, 'core/trending.html')