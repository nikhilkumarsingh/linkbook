from .models import Profile


def save_profile(backend, user, response, *args, **kwargs):
	
	print(user)
	'''
	p = Profile()
	p.user = user
	p.social_id = response['id']
	p.save()
	'''