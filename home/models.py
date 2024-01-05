import datetime
import django.contrib.auth.models

from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, AbstractUser

from django.utils import timezone

User = settings.AUTH_USER_MODEL
default_user_avatar="https://i.imgur.com/WxNkK7J.png"

class User(AbstractUser):
    userImgLink=True
    birth=models.DateTimeField(null=True, blank=True)
    profile_Picture_Link=models.CharField(max_length=120, blank=True, null=True)
    #add default in all models
    profile_Picture=models.ImageField(upload_to="profilepics",null=True, blank=True, default="default_user.png")

    occupation=models.CharField(max_length=200, blank=True, null=False)
    backgroundImgLink=True
    background_Picture_Link=models.CharField(max_length=120, blank=True, null=True)
    background_Picture=models.ImageField(upload_to="avatarbg",null=True, blank=True)

    followers=models.ManyToManyField(User, related_name="users_following", blank=True)

    @property
    def generate_profile_url(self):
        return "/profile/"+ self.username+"/"

    @property
    def provide_image(self):
        try:
            if self.profile_Picture and hasattr(self.profile_Picture, 'url'):
                return self.profile_Picture.url
        except:
            try:
                if not self.profile_Picture and not self.profile_Picture_Link.blank:
                    return self.profile_Picture_Link
            except:
                if not hasattr(self.profile_Picture, 'url') and self.profile_Picture_Link.blank :
                    return default_user_avatar
                else:
                    return None
    @property
    def count_followers(self):
            return self.followers.count()

    def __str__(self):
        return self.username

class userInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    userImgLink=True
    birth=models.DateTimeField(null=True, blank=True)
    profile_Picture_Link=models.CharField(max_length=120, blank=True, null=True)
    #add default in all models
    profile_Picture=models.ImageField(upload_to="profilepics",null=True, blank=True, default="default_user.png")

    occupation=models.CharField(max_length=200, blank=True, null=False)
    backgroundImgLink=True
    background_Picture_Link=models.CharField(max_length=120, blank=True, null=True)
    background_Picture=models.ImageField(upload_to="avatarbg",null=True, blank=True)


    @property
    def generate_profile_url(self):
        return "/profile/"+ self.username+"/"

    @property
    def provide_image(self):
        try:
            if self.profile_Picture and hasattr(self.profile_Picture, 'url'):
                return self.profile_Picture.url
        except:
            try:
                if not self.profile_Picture and not self.profile_Picture_Link.blank:
                    return self.profile_Picture_Link
            except:
                if not hasattr(self.profile_Picture, 'url') and self.profile_Picture_Link.blank :
                    return default_user_avatar
                else:
                    return None
    @property
    def count_followers(self):
            return self.followers.count()

    def __str__(self):
        return self.username

class FollowingFollower(models.Model):
    user_follow = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="following")
    user_followed = models.ForeignKey(User, null=True, blank= False, on_delete=models.CASCADE, related_name="follower")

    class Meta:
        unique_together=["user_follow", "user_followed"]

    def __str__(self):
        return str(self.user_follow) +" follows " + str(self.user_followed)

    class Meta:
        verbose_name = "Follow"
        verbose_name_plural = "Followings"

class Artwork(models.Model):
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    artwork=models.ImageField(upload_to="artworks",null=True, blank=False)
    name= models.CharField(max_length=30)
    pub_date= models.DateTimeField()
    description= models.TextField(max_length=200000, null=True, blank=True)
    comments=models.IntegerField(default=0)
    tags= models.TextField(max_length=600, null=True, blank=True)
    likes= models.ManyToManyField(User, related_name="users_liked",default=None)

    @property
    def generate_artwork_url(self):
        return "/artworks/"+ str(self.pk)+"/"

    @property
    def generate_artwork_url_from_view(self):
        return "/artworks/" + str(self.pk)+"/"

    @property
    def generate_artwork_urlb(self):
        return "/artworks/"+ str(self.name).replace(" ", "%20")+"/"

    @property
    def image_name(self):
        if self.artwork and hasattr(self.artwork, 'filename'):
            return self.artwork.filename

    @property
    def image_url(self):
        if self.artwork and hasattr(self.artwork, 'url'):
            return self.artwork.url

    @property
    def count_likes(self):
            return self.likes.count()

    def __str__(self):
        return self.name

class Group(models.Model):
    users=models.ManyToManyField(User)
    name=models.CharField(max_length=20, blank=True, null=False)
    bio= models.TextField(max_length=200, blank=True, null=True)
    usesImgLink = True
    profile_Picture_Link = models.CharField(max_length=120, blank=True, null=True)
    profile_Picture = models.ImageField(upload_to="group-pics",null=True, blank=True)

    backgroundImgLink=True
    background_Picture_Link=models.CharField(max_length=120, blank=True, null=True)
    background_Picture=models.ImageField(upload_to="groupbg", null=True, blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    #Fix for cases when user is deleted and the comments should stay but saying "deleted user"
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, null=True, blank=False)
    comment=models.TextField(max_length=1000)
    pub_date = models.DateTimeField()
    likes = models.ManyToManyField(User, related_name="users_liked_comment", blank=True)

    @property
    def has_reply(self):
        if Rep.objects.filter(replying=self).count()>0:
            return True
        else:
            return False

    @property
    def time_elapsed(self):
        time_elapsed= timezone.now() - self.pub_date
        return time_elapsed


    def __str__(self):
        return str(self.author) + " : " + str(self.comment)


class Reply(Comment):
    #Fix for cases when user is deleted and the comments should stay but saying "deleted user"

    replying = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, related_name="replied_comment")

    def __str__(self):
        return str(self.author) + " replied to " + str(self.replying.author)

    class Meta:
        verbose_name = "Reply"
        verbose_name_plural = "Replies"

class Rep(models.Model):
    #Fix for cases when user is deleted and the comments should stay but saying "deleted user"
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, null=True, blank=False)
    replying= models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=False)
    comment = models.TextField(max_length=1000)
    pub_date = models.DateTimeField()
    likes = models.ManyToManyField(User, related_name="users_liked_rep", blank=True)


    @property
    def time_elapsed(self):
        time_elapsed = timezone.now() - self.pub_date
        return time_elapsed

    def __str__(self):
        return str(self.author) + " : " + str(self.comment)
