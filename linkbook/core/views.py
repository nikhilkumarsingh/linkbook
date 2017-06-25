from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from linkbook.links.models import Link, Book

from linkbook.core.forms import UpdateProfileForm


def index(request):
    return render(request, 'core/index.html')


def username_slugs(request, username):
    action = request.GET.get('show', None)
    user = get_object_or_404(User, username = username)

    if action == 'books':
        user_books = Book.objects.filter(user = user)
        return render(request, 'links/view_books.html', 
            {'user': user, 'view_books':user_books})

    elif action == 'links':
        user_links = Link.objects.filter(user = user)
        return render(request, 'links/view_links.html', 
            {'user': user, 'view_links':user_links})

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
            'following_count': following_count})


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username = username)
    if user != request.user:
        return redirect('/{}/'.format(user.username))

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, user = user)
        if form.is_valid():
            user.username = form.clean_username()
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            return redirect('/{}/'.format(user.username))
        else:
            return render(request, "core/edit_profile.html", {'form':form})

    form = UpdateProfileForm(user = user, 
        initial = {'username': user.username,
        'first_name':user.first_name, 'last_name': user.last_name,
        'email':user.email, 'image_url':user.profile.pic})
    return render(request, "core/edit_profile.html", {'form':form})



