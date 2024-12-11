from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, artworkForm, edit_Profile, CommentForm
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse


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



@login_required(login_url="/login/")
def profile(request):
    user = get_object_or_404(User, username=request.user.username)
    arts = Artwork.objects.filter(author=user).count()

    try:
        recents = Artwork.objects.filter(author=user)[8]
    except:
        recents = Artwork.objects.filter(author=user)

    following = FollowingFollower.objects.filter(user_follow=user).count()
    followers = FollowingFollower.objects.filter(user_followed=user).count()

    context = {
        "profile": user,
        "arts": arts,
        "followers": followers,
        "following": following,
        "recent_artworks": recents
    }
    return render(request, "profile.html", context)

def editProfile(request):
    if request.method == "POST":
        form = edit_Profile(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            for field in form.cleaned_data:
                if form.cleaned_data[field]:
                    setattr(user, field, form.cleaned_data[field])
            user.save()
            messages.success(request, "Your profile info has been saved sucessfully.")
            return redirect("home")
        else:
            messages.error(request, "There was an error when submitting your info." + str(form.cleaned_data) + "with the following errors:" + str(form.errors) + "Request.FILES:" + str(request.FILES))

    form = edit_Profile()

    return render(request, "editProfile.html", context={"edit_profile":form})


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

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.artwork = artwork
            comment.pub_date = datetime.datetime.now()
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.is_reply = True
                comment.parent = parent_comment
                comment.save()
                messages.success(request, 'Your comment has been posted!')
                return redirect('artworks', pk=artwork.pk)
            else:
                comment.save()
                messages.success(request, 'Your comment has been posted!')
                return redirect('artworks', pk=artwork.pk)
        return render(request, 'artwork.html', {'artwork': artwork, 'comments': comments, 'form': form})

    likes=artwork.likes.all().count()
    comments_count = Comment.objects.filter(artwork=artwork).count()
    #if comments_count<1:
    context={"artwork":artwork, "comments_count":comments_count, "likes_count":likes, "morefrom": morefrom, "comments":comments, "replies":replies}

    return render(request, "artwork.html", context)

@login_required
def artwork_comment(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    comments = Comment.objects.filter(artwork=artwork).order_by('-pub_date')
    replies = Comment.objects.filter(artwork=artwork, is_reply=True).order_by('-pub_date')
    if request.method == 'POST':
        form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.artwork = artwork
        comment.save()
        messages.success(request, 'Your comment has been posted!')
        return redirect('artwork', pk=artwork_id)
    else:
        form = CommentForm()
    return render(request, 'artwork.html', {
        'artwork': artwork, 'comments': comments, 'replies': replies, 'form': form
    })


@login_required(login_url="/login/")
def myArtwork(request):
    return render(request, "myArtwork.html", context=None)



@login_required(login_url="/login/")
def uploadArtwork(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        form = artworkForm(request.POST, request.FILES, initial={"author": user})
        if form.is_valid():
           # artwork = form.save(user=request.user, date=datetime.datetime.now(), artwork=image)
            artwork = form.save(date=datetime.datetime.now(),author=user)
            messages.success(request, "Your artwork has been submitted sucessfully")
            return redirect("home")
        else:
            messages.error(request, "There was an error when submitting your artwork." + str(form.cleaned_data) + "with the following errors:" + str(form.errors) + "Request.FILES:" + str(request.FILES))

    form = artworkForm()

    return render(request, "uploadArtwork.html", context={"upload_artwork":form})

@user_passes_test(lambda u: u.is_anonymous)
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='home.backend.UserBackend')
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
				login(request, user, backend='home.backend.UserBackend')
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"User is none. Form: "+ str(form.cleaned_data))
		else:
			messages.error(request,"Invalid username or password: "+ str(form.cleaned_data))
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("home")

@login_required(login_url="/login/")
def like_artwork(request, pk):
    artwork = get_object_or_404(Artwork, id=pk)
    try:
        if artwork.likes.contains(request.user):
            artwork.likes.remove(request.user);
            artwork.save
        else:
            artwork.likes.add(request.user)
            artwork.save()
        return JsonResponse({'likes': artwork.likes.count()})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def settings(request):
    pass