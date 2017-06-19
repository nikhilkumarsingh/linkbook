from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from linkbook.links.forms import LinkForm, BookForm, CommentForm
from linkbook.links.models import Link, Book, Comment

from taggit.models import Tag
UP = 0
DOWN = 1
vote_color = "btn-flat lighten-5"


def link(request, id):
    link = get_object_or_404(Link, id = id)
    comment_form = CommentForm()
    upvotes = link.votes.count(action = UP)
    downvotes = link.votes.count(action = DOWN)
    upvoted = link.votes.exists(request.user.id, action = UP)
    downvoted = link.votes.exists(request.user.id, action = DOWN)

    if not upvoted:
        upvote_button = ""
    else:
        upvote_button = vote_color

    if not downvoted:
        downvote_button = ""
    else:
        downvote_button = vote_color

    return render(request, 'links/link.html', 
        {'link': link, 'comment_form': comment_form, 
        'upvotes': upvotes, 'downvotes': downvotes,
        'upvote_button': upvote_button, 'downvote_button': downvote_button})


def book(request, id):
    book = get_object_or_404(Book, id = id)
    links = book.link_set.all()
    return render(request, 'links/book.html', {'book': links})


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
        form = LinkForm(request.user)
        return render(request, 'links/new_link.html', {'form': form})


def edit_link(request, id):
    if request.method == 'POST':
        form = LinkForm(request.user, request.POST)
        if form.is_valid():
            link = Link.objects.get(id = id)
            link.user = request.user
            link.url = form.cleaned_data.get('url')
            link.title = form.cleaned_data.get('title')
            link.description = form.cleaned_data.get('description')
            link.save()
            link.tags.clear()
            tag_list = form.cleaned_data.get('tags')
            for tag in tag_list:
                link.tags.add(tag)
            link.books = form.cleaned_data.get('books')
            link.save()
            return redirect("/link/{}/".format(id))
    else:
        old_link = get_object_or_404(Link, id = id)
        initial_dict = {'url': old_link.url, 'title': old_link.title,
                   'description': old_link.description,
                   'tags': ", ".join(tag.name for tag in old_link.tags.all()),
                   'books': old_link.books.all()}
        print(old_link.description)
        form = LinkForm(request.user, initial = initial_dict)
        return render(request, 'links/edit_link.html', 
            {'form': form, 'link':old_link})


@login_required
def vote_link(request, id):
    if request.method == 'GET':
        vote_type = request.GET['type']
        link = Link.objects.get(id = id)
        upvoted = link.votes.exists(request.user.id, action = UP)
        downvoted = link.votes.exists(request.user.id, action = DOWN)

        if vote_type == "U":
            if not upvoted:
                link.votes.up(request.user.id)
                link.save()
                upvote_button = vote_color
                if downvoted:
                    downvote_button = vote_color
                else:
                    downvote_button = ""
            else:
                link.votes.delete(request.user.id)
                print("hello")
                upvote_button = vote_color
                downvote_button = ""
            return JsonResponse({'upvotes': link.votes.count(action = UP), 
                'downvotes': link.votes.count(action = DOWN),
                'upvote_button': upvote_button,
                'downvote_button': downvote_button})


        elif vote_type == "D":
            if not downvoted:
                link.votes.down(request.user.id)
                link.save()
                downvote_button = vote_color
                if upvoted:
                    upvote_button = vote_color
                else:
                    upvote_button = ""
            else:
                link.votes.delete(request.user.id)
                downvote_button = vote_color
                upvote_button = ""
            return JsonResponse({'upvotes': link.votes.count(action = UP),
                'downvotes': link.votes.count(action = DOWN),
                'upvote_button': upvote_button,
                'downvote_button': downvote_button})

        
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

@login_required
def view_books(request):
    user_records = Book.objects.filter(user = request.user)
    return render(request, 'links/view_books.html', {'view_books':user_records})


@login_required
def create_comment(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.user = request.user
            comment.link = Link.objects.get(id = id)
            comment.text = form.cleaned_data.get('text')
            comment.save()
            return redirect('/link/{}'.format(id))

@login_required
def edit_book(request, id):
    if request.method == 'POST':
        form = BoookForm(request.POST)
        if form.is_valid():
            book = Book()
            book.user = request.user
            book.title = form.cleaned_data.get('title')
            book.description = form.cleaned_data.get('description')
            book.save()
            return redirect("/book/{}/".format(id))
    else:
        old_book = get_object_or_404(Book, id = id)
        initial_dict = {'title': old_book.title,
                   'description': old_book.description,
                   }
        print(old_book.description)
        form = BookForm(initial = initial_dict)
        return render(request, 'links/edit_book.html', 
            {'form': form, 'book':old_book, 'color' : 'red'})

@login_required
def view_tag(request, id):
    tag_obj = get_object_or_404(Tag, id = id)
    tagged = Link.objects.filter(tags__name = tag_obj)
    return render(request, "links/tags.html/", {'tag': tagged, 'tagname' : tag_obj})