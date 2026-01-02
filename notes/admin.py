from django.contrib import admin
from .models import Folder,Note,NoteVersion,Embedding
# Register your models here.
admin.site.register(Folder)
admin.site.register(Note)
admin.site.register(NoteVersion)
admin.site.register(Embedding)