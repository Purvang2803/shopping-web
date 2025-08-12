# store/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to user
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_read = models.BooleanField(default=False)  # NEW

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'title', 'message')  # Avoid duplicates per user

    def __str__(self):
        return f"{self.user.username if self.user else 'All Users'} - {self.title}"

class Offer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('title', 'description')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from django.contrib.auth.models import User
        users = User.objects.all()
        for user in users:
            Notification.objects.get_or_create(
                user=user,
                title=self.title,
                message=self.description
            )

    def __str__(self):
        return self.title

