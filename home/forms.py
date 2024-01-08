from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Artwork

YEARS=[]
if YEARS.count(1951)<1:
	for i in range(1, 74):
		YEARS.append(i+1950)

OCCUPATIONS={"Enthusiast","Artist","Student"}

User=get_user_model()

class NewUserForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput, required=True)
	birth = forms.DateTimeField(widget=forms.SelectDateWidget(years=YEARS), required=True)
	# add default in all models

	occupation = forms.CharField(required=False)


	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", "birth", "occupation")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.username= self.cleaned_data["username"]
		user.password= self.cleaned_data["password1"]
		user.email = self.cleaned_data['email']
		user.birth = self.cleaned_data["birth"]
		user.occupation = self.cleaned_data["occupation"]

		if commit:
			user.save()
		return user

class LoginForm(forms.Form):
	username= forms.CharField(label="Username")
	pwd= forms.PasswordInput()
	class Meta:
		model = User

class edit_Profile(forms.Form):
	pass


class artworkForm(forms.ModelForm):
	#artwork= forms.ImageField()
	#name= forms.CharField(widget=forms.TextInput, max_length=160)
	#description= forms.CharField(widget=forms.TextInput)
	tags= forms.CharField(max_length=500)

	class Meta:
		model = Artwork
		fields = ("artwork", "name", "description", "tags")
		enctype = "multipart/form-data"

	def save(self, date=None, author=None, commit=True):
		artwork = super(artworkForm, self).save(commit=False)
		artwork.author=author
		artwork.pub_date=date
		if commit:
			artwork.save()
	"""def save(self,user=None, date=None, artwork=None, commit=True):
		artwork = super(artworkForm, self).save(commit=False)
		artwork.author= user
		artwork.name= self.cleaned_data["name"]
		artwork.description= self.cleaned_data["description"]
		artwork.tags = self.cleaned_data['tags']
		artwork.artwork = artwork
		artwork.pub_date = date

		if commit:
			artwork.save()"""