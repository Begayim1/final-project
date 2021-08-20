from django.contrib import admin


from main.models import *


class CodeImageInline(admin.TabularInline):
    model = CodeImage
    max_num = 10

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CodeImageInline, ]

admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Like)

