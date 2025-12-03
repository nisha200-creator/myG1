from django.db import models
from django.utils import timezone

class UserTable(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.email


class PasswordResetToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


# article model


from django.db import models
from django.utils import timezone

class Article(models.Model):

    CATEGORY_CHOICES = [
        ('NEWS', 'News'),
        ('DRIVER', 'Driver'),
        ('HIGHLIGHTS', 'Highlights'),
        ('VIDEO', 'Video'),
        ('DEBRIEF', 'Friday Debrief'),
    ]

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField()

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    thumbnail = models.ImageField(upload_to='articles/')

    is_featured = models.BooleanField(default=False)  # for hero section

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    # “time ago” format
    def time_ago(self):
        now = timezone.now()
        diff = now - self.created_at

        if diff.days >= 1:
            return f"{diff.days} days ago"
        elif diff.seconds >= 3600:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds >= 60:
            return f"{diff.seconds // 60} minutes ago"
        return "Just now"
