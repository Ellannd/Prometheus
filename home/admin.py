from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(userInfo)
admin.site.register(Artwork)
admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(FollowingFollower)
admin.site.register(Rep)
