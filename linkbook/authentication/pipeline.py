from .models import Profile
import requests

def save_profile(backend, user, response, *args, **kwargs):

	if Profile.objects.filter(user = user).exists():
		return
	else:
		if backend.name == "github":
			pic = "https://avatars.githubusercontent.com/u/{}".format(response.get('id'))
		elif backend.name == "twitter":
			pic = "https://twitter.com/{}/profile_image?size=normal".format(response.get('screen_name'))
		elif backend.name == "facebook":
			pic = "https://graph.facebook.com/{}/picture?type=large&height=720&width=720".format(response.get('id'))
		elif backend.name == "google-oauth2":
			try:
				r = requests.get("http://picasaweb.google.com/data/entry/api/user/{}?alt=json".format(response.get('id')))
				pic = r.json()['entry']['gphoto$thumbnail']['$t']
			except:
				pic = "http://i.imgur.com/xz4vNF9.png"
		Profile.objects.create(user=user, backend=backend.name, pic=pic)

