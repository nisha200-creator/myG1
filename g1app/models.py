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

    video = models.FileField(upload_to='articles/videos/', blank=True, null=True)  # ✅ ADDED

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

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



#  <!-- FEATURED VIDEO -->

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='videos/thumbnails/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title



# shedule model

class Race(models.Model):
    round_number = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    date_range = models.CharField(max_length=255)  
    image = models.ImageField(upload_to='races/')

    def __str__(self):
        return f"Round {self.round_number} - {self.name}"






# race results model

class RaceResult(models.Model):
    grand_prix = models.CharField(max_length=100)
    country_flag = models.ImageField(upload_to='flags/')
    date = models.DateField()
    winner = models.CharField(max_length=100)
    winner_img = models.ImageField(upload_to='drivers/')
    team = models.CharField(max_length=100)
    team_logo = models.ImageField(upload_to='teams/')
    laps = models.IntegerField()
    time = models.CharField(max_length=20)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.grand_prix
