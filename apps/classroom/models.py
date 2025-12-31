from django.db import models
from django.conf import settings

class UserActivity(models.Model):
    # Link to the user who performed the action
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Information about the file/task
    file_name = models.CharField(max_length=255)
    tool_used = models.CharField(max_length=50) # e.g., 'Reading Assistant'

    # The URL to redirect back to so the user can "continue"
    target_url = models.CharField(max_length=500)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp'] # Show newest first


from django.db import models
from django.conf import settings

class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    tool_used = models.CharField(max_length=50) # e.g., 'Reading Assistant'
    target_url = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp'] # This ensures the "Recently Worked On" logic works

