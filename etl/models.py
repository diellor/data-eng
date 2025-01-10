from django.db import models
from mixins import BaseModel
from django.utils.timezone import now


class RawVikingsShow(BaseModel):
    """"""

    data = models.JSONField()

    class Meta:
        """"""

        verbose_name = "Raw Vikings Show"
        verbose_name_plural = "Raw Vikings Show"


class VikingsShow(models.Model):
    actor_url = models.URLField(max_length=500)
    img_src = models.URLField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=255)
    character_name = models.CharField(max_length=255, unique=True)
    character_description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Vikings Show"
        verbose_name_plural = "Vikings Show"


class RawNorsemenShow(BaseModel):
    """"""

    data = models.JSONField()

    class Meta:
        """"""

        verbose_name = "Raw Norsemen Show"
        verbose_name_plural = "Raw Norsemen Show"


class NorsemenShow(BaseModel):
    """"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    character_name = models.CharField(max_length=255, unique=True)

    class Meta:
        """"""

        verbose_name = "Norsemen Show"
        verbose_name_plural = "Norsemen Show"


class RawVikingsNFL(BaseModel):
    """"""

    data = models.JSONField()

    class Meta:
        """"""

        verbose_name = "Raw Vikings NFL"
        verbose_name_plural = "Raw Vikings NFL"


class VikingsNFL(BaseModel):
    """"""

    name = models.CharField(max_length=255)
    age = models.IntegerField()
    height = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    college = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    profile_link = models.URLField(max_length=500)
    biography_html = models.TextField(blank=True, null=True)
    image_src = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        """"""

        verbose_name = "Vikings NFL"
        verbose_name_plural = "Vikings NFL"


class CareerStat(BaseModel):
    player = models.ForeignKey(
        VikingsNFL, related_name="career_stats", on_delete=models.CASCADE
    )
    games_played = models.IntegerField(null=True, blank=True)
    games_started = models.IntegerField(null=True, blank=True)
    touchdowns = models.IntegerField(null=True, blank=True)
    attempts = models.IntegerField(null=True, blank=True)
    average = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fumbles = models.IntegerField(null=True, blank=True)
    longest = models.IntegerField(null=True, blank=True)
    receptions = models.IntegerField(null=True, blank=True)
    yards = models.IntegerField(null=True, blank=True)
    lost = models.IntegerField(null=True, blank=True)
    team = models.CharField(max_length=255, null=True, blank=True)
    season = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Career Stat"
        verbose_name_plural = "Career Stats"

class ScrapingLog(models.Model):
    task_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('success', 'Success'), ('failure', 'Failure')])
    execution_time = models.FloatField() 
    retries = models.IntegerField(default=0)
    error_message = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.task_name} - {self.status} at {self.timestamp}"