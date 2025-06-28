from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # New fields for group project partner seeking
    seeking_partner = models.BooleanField(default=False)
    project_title = models.CharField(max_length=100, blank=True)
    project_description = models.TextField(blank=True)
    skills_needed = models.CharField(max_length=200, blank=True)
    preferred_partner_details = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return f"{self.author.username}: {self.project_title[:30]}"
