from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=True, blank=True)
    content = models.CharField(max_length=3000)
    favorite = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    summary = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or ""


class NoteVersion(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=True, blank=True)
    content = models.CharField(max_length=3000)
    version_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Embedding(models.Model):
    note = models.OneToOneField(
        Note,
        on_delete=models.CASCADE,
        related_name='embedding'
    )

    vector = models.JSONField(null=True, blank=True)
    provider = models.CharField(max_length=20, default="local")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Embedding for Note {self.note_id}"

class Tag(models.Model):
    name = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "user")   # prevent duplicates per user

    def __str__(self):
        return self.name


class NoteTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("tag", "note")  # one tag per note

    def __str__(self):
        return f"{self.tag.name} → Note {self.note.id}"
