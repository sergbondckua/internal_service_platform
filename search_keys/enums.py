from django.db import models


class PrefixStreetChoices(models.TextChoices):
    ST = "вул.", "вулиця"
    BUL = "б-р", "бульвар"
    PROSPECT = "просп.", "проспект"
    PROV = "пров.", "провулок"
    UZV = "узвіз", "узвіз"
