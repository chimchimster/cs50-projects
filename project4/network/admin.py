from django.contrib import admin
from .models import Post, User, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')
    search_fields = ('user', )
    list_filter = ('user', )


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'publishing_date', 'edit_date', 'text', 'likes')
    list_display_links = ('id', 'user')
    search_fields = ('user__username', )
    list_editable = ('text', 'likes')
    list_filter = ('user', 'publishing_date', 'edit_date', 'likes')

admin.site.register(Post, PostAdmin)
admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)