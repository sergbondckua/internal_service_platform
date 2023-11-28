from django.db import models

class BaseModel(models.Model):
    """Basic model-workpiece"""

    created_at = models.DateTimeField("Created", auto_now_add=True)
    updated_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        abstract = True
