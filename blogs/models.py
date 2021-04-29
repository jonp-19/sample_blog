from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    """A blog post."""
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'posts'

    def __str__(self):
        """Return the blogs title and text. This might be incorrect"""
        return (f"{self.title} {self.text}")
