from django.db import models


class PrefixStreetChoices(models.TextChoices):
    ST = "вул.", "вулиця"
    BUL = "б.", "бульвар"
    PROSPECT = "пр.", "проспект"
    PROV = "пров.", "провулок"
    UZV = "узв.", "узвіз"
