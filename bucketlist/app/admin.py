from django.contrib import admin
from .models import BucketList, BucketListItem
from .forms import SignUpForm
from models import SignUp


class SignUpAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "username"]
    
    class Meta:
        model = SignUp



class BucketListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_per_page = 25


class BucketListItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'bucketlist', 'done')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_per_page = 25

admin.site.register(SignUp, SignUpAdmin)
admin.site.register(BucketList, BucketListAdmin)
admin.site.register(BucketListItem, BucketListItemAdmin)
