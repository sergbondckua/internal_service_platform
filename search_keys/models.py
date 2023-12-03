from django.db import models

from common.models import BaseModel
from search_keys.enums import PrefixStreetChoices


class Box(BaseModel):
    title = models.CharField(verbose_name="Title", max_length=50)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ("title",)
        verbose_name = "Box for keys"
        verbose_name_plural = "Boxes for keys"


class Cell(BaseModel):
    title = models.CharField(max_length=15)
    box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name="cells")

    def __str__(self):
        return f"{self.title}({self.box})"

    class Meta:
        ordering = ("title",)
        verbose_name = "Cell"
        verbose_name_plural = "Cells"


class Street(BaseModel):
    name = models.CharField(verbose_name="Name", max_length=100)
    prefix = models.CharField(
        verbose_name="Prefix",
        max_length=6,
        default=PrefixStreetChoices.ST,
        choices=PrefixStreetChoices.choices,
    )
    old_name = models.CharField(
        verbose_name="Old name",
        max_length=100,
        blank=True,
    )
    old_prefix = models.CharField(
        verbose_name="Old prefix",
        max_length=6,
        choices=PrefixStreetChoices.choices,
        blank=True,
    )

    def __str__(self):
        current_name = f"{self.prefix} {self.name}"
        if self.old_name:
            old_name = f"{self.old_prefix} {self.old_name}"
            return f"{current_name} / {old_name}"
        return current_name

    class Meta:
        ordering = ("name",)
        verbose_name = "Street"
        verbose_name_plural = "Streets"


class Building(BaseModel):
    number = models.CharField(
        verbose_name="Building number",
        max_length=15,
    )
    street = models.ForeignKey(
        Street,
        verbose_name="Street",
        on_delete=models.CASCADE,
        related_name="buildings",
    )
    cell = models.ForeignKey(
        Cell,
        verbose_name="Cell",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.street} {self.number}"

    class Meta:
        ordering = ("number",)
        verbose_name = "Building address"
        verbose_name_plural = "Building addresses"
