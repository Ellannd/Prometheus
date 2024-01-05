from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, artworkForm, LoginForm
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm


from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

import logging

#User = settings.AUTH_USER_MODEL
User = get_user_model()
logger = logging.getLogger(__name__)

def home(request):
    artworks= Artwork.objects.all()
    user=request.user

    context= {"Artworks":artworks,
              "user":user,}

    return render(request, "home.html", context)



@login_required()
def profile(request):

    user=request.user
    context={"User":user}
    return render(request, "profile.html", context)



def otherUser(request, username):

    user=get_object_or_404(User, username=username)
    arts=Artwork.objects.filter(author=user).count()

    try:
        recents = Artwork.objects.filter(author=user)[8]
    except:
        recents = Artwork.objects.filter(author=user)

    following= FollowingFollower.objects.filter(user_follow=user).count()
    followers= FollowingFollower.objects.filter(user_followed=user).count()

    context={
        "profile":user,
        "arts":arts,
        "followers":followers,
        "following":following,
        "recent_artworks":recents
    }
    return render(request, "publicProfile.html", context)



def artwork(request, pk):
    artwork=get_object_or_404(Artwork, pk=pk)
    comments=Comment.objects.filter(artwork=artwork)
    replies=Rep.objects.filter(artwork=artwork)
    try:
        morefrom=Artwork.objects.filter(author=artwork.author)[12]
    except:
        morefrom = Artwork.objects.filter(author=artwork.author)

    likes=artwork.likes.all().count()
    comments_count = Comment.objects.filter(artwork=artwork).count()
    #if comments_count<1:
    context={"artwork":artwork, "comments_count":comments_count, "likes_count":likes, "morefrom": morefrom, "comments":comments, "replies":replies}

    return render(request, "artwork.html", context)



@login_required()
def myArtwork(request):
    return render(request, "myArtwork.html", context=None)



@login_required(login_url="/login/")
def uploadArtwork(request):
    if request.method == "POST":
        form = artworkForm(request.POST, request.FILES, initial={"author": request.user})
        if form.is_valid():
            artwork = form.save(user=request.user, date=datetime.datetime.now())
            messages.success(request, "Your artwork has been submitted sucessfully")
            return redirect("home")
        else:
            messages.error(request, "There was an error when submitting your artwork." + str(form.cleaned_data) + "with the following errors:" + str(form.errors))

    form = artworkForm()

    return render(request, "uploadArtwork.html", context={"upload_artwork":form})

@user_passes_test(lambda u: u.is_anonymous)
def register(request):
    messages.success(request, "Yeah!! we rendered the register page")
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information." + str(form.cleaned_data))
    
    form = NewUserForm()

    return render(request, "register.html", context={"register_form":form})

def login_user(request):
	if request.method == "POST":
		form = AuthenticationForm(request, request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password."+ str(form.cleaned_data))
		else:
			messages.error(request,"Invalid username or password."+ str(form.cleaned_data))
	form = LoginForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("home")

def settings(request):
    pass