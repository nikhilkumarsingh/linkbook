from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from linkbook.links.forms import LinkForm, BookForm
from linkbook.links.models import Link, Book

from taggit.models import Tag


def link(request, id):
    link = get_object_or_404(Link, id = id)
    return render(request, 'links/link.html', {'link': link})


def book(request, id):
    book = get_object_or_404(Book, id = id)
    return render(request, 'links/book.html', {'book': book})


@login_required
def create_link(request):
    if request.method == 'POST':
        form = LinkForm(request.user, request.POST)
        if form.is_valid():
            link = Link()
            link.user = request.user
            link.url = form.cleaned_data.get('url')
            link.title = form.cleaned_data.get('title')
            link.description = form.cleaned_data.get('description')
            link.save()
            tag_list = form.cleaned_data.get('tags')
            for tag in tag_list:
                link.tags.add(tag)
            link.books = form.cleaned_data.get('books')
            link.save()
            print("Done")
            return redirect('/')
    else:
        form = LinkForm(request.user)#initial = {'books': Book.objects.filter(user = request.user)})
        return render(request, 'links/new_link.html', {'form': form})


@login_required
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = Book()
            book.user = request.user
            book.title = form.cleaned_data.get('title')
            book.description = form.cleaned_data.get('description')
            book.save()
            return redirect('/')
    else:
        form = BookForm()
        return render(request, 'links/new_book.html', {'form': form})