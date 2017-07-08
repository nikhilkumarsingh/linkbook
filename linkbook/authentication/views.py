from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from linkbook.authentication.forms import SignUpForm
from linkbook.authentication.models import Profile


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'authentication/signup.html',
                          {'form': form})

        else:
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username = username, password = password,
                                     email = email, first_name = first_name,
                                     last_name = last_name)
            user = authenticate(username = username, password = password)
            Profile.objects.get_or_create(user = user)
            login(request, user)
            return redirect('/')

    else:
        return render(request, 'authentication/signup.html',
                      {'form': SignUpForm()})

