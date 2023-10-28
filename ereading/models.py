from django.db import models
from django.contrib.auth.models import User

class Ereading(models.Model):
    STATE_CHOICES = [
        (0, 'Checked by admin'),
        (1, 'Accepted'),
        (2, 'Rejected'),
    ]

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    state = models.IntegerField(choices=STATE_CHOICES, default=0)

    def save(self, *args, **kwargs):
        # Set the created_by field to the username of the user who created the object
        if self.user:
            self.created_by = self.user.username
        super().save(*args, **kwargs)