from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def InvalidUsernameValidator(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('Enter a valid username.')


def UniqueEmailValidator(value):
	if User.objects.filter(email__iexact = value).exists():
		raise ValidationError('User with this Email already exists.')


def UniqueUsernameIgnoreCaseValidator(value):
	denied = ['administrator', 'trending', 'book', 'link', 'login', 
	'logout', 'signup', 'oauth', 'navbar', 'project', 'inbox', 'link', 'import', 
	'comment', 'tags', 'recommendor', 'follow', 'follower', 'following']
	if User.objects.filter(username__iexact = value).exists():
		raise ValidationError('User with this Username already exists.')

	if value in denied:
		raise ValidationError('This username is not allowed. Please choose some other username.')



class SignUpForm(forms.ModelForm):
	first_name = forms.CharField(
		widget = forms.TextInput(attrs = {'id': 'FirstName'}),
		max_length = 30,
		required = True,
		)
	last_name = forms.CharField(
		widget = forms.TextInput(attrs = {'id': 'LastName'}),
		max_length = 30,
		required = True,
		)
	username = forms.CharField(
		widget = forms.TextInput(attrs = {'id': 'Username'}),
		max_length = 30,
		required = True,
		help_text = 'Usernames may contain <strong>alphanumeric</strong>, <strong>_</strong> and <strong>.</strong> characters') 
	
	password = forms.CharField(
		widget = forms.PasswordInput(attrs = {'id' : 'Password'}))
	
	confirm_password = forms.CharField(
		widget = forms.PasswordInput(attrs = {'id' : 'ConfirmYourPassword'}),
		label = "ConfirmYourPassword",
		required = True)
	
	email = forms.CharField(
		widget = forms.EmailInput(attrs = {'id': 'Email', 'class' : 'validate', 'autocomplete' : 'autocomplete'}),
		required = True,
		max_length = 75)

	class Meta:
		model = User
		exclude = ['last_login', 'date_joined']
		fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password',]

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(InvalidUsernameValidator)
		self.fields['username'].validators.append(UniqueUsernameIgnoreCaseValidator)
		self.fields['email'].validators.append(UniqueEmailValidator)

	def clean(self):
		super(SignUpForm, self).clean()
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if password and password != confirm_password:
			self._errors['password'] = self.error_class(['Passwords don\'t match'])
		return self.cleaned_data
