from django.db import models
from userApp.models import User

class Todo(models.Model):
  """ Todo Model Definition """

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField()
  content = models.TextField()
  is_checked = models.BooleanField(default=False)
  emoji = models.CharField(
    max_length=1,
    default="",
    blank=True
  )
  is_bookmarked = models.BooleanField(default=False)
  dark_mode = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.content