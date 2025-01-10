from django.contrib import admin

from etl.models import (
    RawVikingsShow,
    ScrapingLog,
    VikingsShow,
    RawNorsemenShow,
    NorsemenShow,
    RawVikingsNFL,
    VikingsNFL,
)


@admin.register(RawVikingsShow)
class RawVikingsShowAdmin(admin.ModelAdmin):
    list_display = ("id", "data")
    search_fields = ("id", "data")

@admin.register(VikingsShow)
class VikingsShowAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "actor_url",
        "img_src",
        "name",
        "character_name",
        "character_description",
    )
    search_fields = (
        "id",
        "actor_url",
        "img_src",
        "name",
        "character_name",
        "character_description",
    )


@admin.register(RawNorsemenShow)
class RawNorsemenShowAdmin(admin.ModelAdmin):
    list_display = ("id", "data")
    search_fields = ("id", "data")


@admin.register(NorsemenShow)
class NorsemenShowAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "character_name")
    search_fields = ("id", "name", "description", "character_name")


@admin.register(RawVikingsNFL)
class RawVikingsNFLAdmin(admin.ModelAdmin):
    list_display = ("id", "data")
    search_fields = ("id", "data")


@admin.register(VikingsNFL)
class VikingsNFLAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "profile_link",
        "college",
        "experience",
        "image_src",
    )
    search_fields = (
        "id",
        "name",
        "profile_link",
        "college",
        "experience",
        "image_src",
    )


@admin.register(ScrapingLog)
class ScrapingLogAdmin(admin.ModelAdmin):
    list_display = ("task_name", "status", "execution_time", "retries", "timestamp")
    list_filter = ("status", "source")
    search_fields = ("task_name", "error_message")