from django.contrib import admin
from .models import *

# Register your models here.

class AdminRead(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Author,AdminRead)
admin.site.register(Post,AdminRead)
admin.site.register(Request,AdminRead)
admin.site.register(Like,AdminRead)
admin.site.register(Comment,AdminRead)