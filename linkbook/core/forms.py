from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class UpdateProfileForm(forms.Form):

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(UpdateProfileForm, self).__init__(*args, **kwargs)

	username = forms.CharField(required=True, validators=[alphanumeric])
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)
	pic = forms.ImageField(required=False)

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if self.user.username != username and User.objects.filter(username = username).count():
			raise forms.ValidationError('This username is already taken.')    		
		return username

