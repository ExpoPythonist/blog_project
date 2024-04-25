from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display =["author", "title", "published_date"]
    list_filter = ["published_date"]
    

class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "post", "created_date", "approved_comment"]
    list_filter = ["created_date", "approved_comment"]
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved_comment=True)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

