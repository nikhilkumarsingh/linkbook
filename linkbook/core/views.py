from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from linkbook.links.models import Link, Book


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
        link_count = Link.objects.filter(user = user).count()
        book_count = Book.objects.filter(user = user).count()
        return render(request, 'core/profile.html', 
            {'user': user, 'link_count': link_count,
            'book_count': book_count})

