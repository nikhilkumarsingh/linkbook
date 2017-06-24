from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from linkbook.links.models import Link, Book


def index(request):
    return render(request, 'core/index.html')


def username_slugs(request, username):
    action = request.GET.get('show', None)
    # view all books by a user
    if action == 'books':
        user_books = Book.objects.filter(user = get_object_or_404(User, username = username))
        return render(request, 'links/view_books.html', {'view_books':user_books})
    # view all links by a user
    elif action == 'links':
        user_links = Link.objects.filter(user = get_object_or_404(User, username = username))
        return render(request, 'links/view_links.html', {'view_links':user_links})
    else:
        pass