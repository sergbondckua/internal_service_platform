import shutil
from django.contrib.sessions.models import Session
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from pathlib import Path


@receiver(post_delete, sender=Session)
def delete_session_folder(sender, instance, **kwargs):
    session_folder = Path(settings.MEDIA_ROOT) / "filled_docx" / instance.session_key
    if session_folder.exists() and session_folder.is_dir():
        shutil.rmtree(session_folder)  # Видаляє папку та всі файли в ній
