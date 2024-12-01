from django.db import transaction

from etl.models import (
    RawVikingsShow,
    VikingsShow,
    NorsemenShow,
    RawNorsemenShow,
    VikingsNFL,
    RawVikingsNFL,
    CareerStat,
)


class VikingsShowService:

    def handle(self):
        """Process raw data and save/update the VikingsShow model."""

        for raw_show in RawVikingsShow.objects.all():
            for record in raw_show.data:
                if (character_name := record.get("character_name")) and (
                    actor_url := record.get("href")
                ):
                    VikingsShow.objects.update_or_create(
                        character_name=character_name,
                        defaults={
                            "actor_url": actor_url,
                            "img_src": record.get("img_src"),
                            "actor_name": record.get("actor_name"),
                            "character_description": record.get(
                                "character_description"
                            ),
                        },
                    )


class NorsemenShowService:

    def handle(self):
        """Process raw data and save/update the Norsemen model."""

        for raw_entry in RawNorsemenShow.objects.all():
            for item in raw_entry.data:
                if character_name := item.get("character_name"):
                    with transaction.atomic():
                        NorsemenShow.objects.update_or_create(
                            character_name=character_name,
                            defaults={
                                "actor_name": item.get("actor_name"),
                                "description": item.get("description"),
                            },
                        )


class VikingsNFLService:

    def handle(self):
        """Process raw data and save/update the VikingsNFL model along with career stats."""

        for raw_show in RawVikingsNFL.objects.all():
            for record in raw_show.data:
                details = record.get("details", {})

                player, created = VikingsNFL.objects.update_or_create(
                    player_name=record.get("player_name", ""),
                    defaults={
                        "age": int(details.get("Age", 0)),
                        "height": details.get("Height", ""),
                        "weight": details.get("Weight", ""),
                        "college": details.get("College", ""),
                        "experience": details.get("Experience", ""),
                        "profile_link": record.get("profile_link", ""),
                        "biography_html": details.get("biography_html", ""),
                        "image_src": record.get("image_src", ""),
                    },
                )

                career_stats = details.get("career_stats", {})
                for season_key, season_data in career_stats.items():
                    self.handle_season_data(player, season_key, season_data)

    def handle_season_data(self, player, season_key, season_data):
        """Handles the season data, ensuring missing or empty fields are properly set to None or defaults."""

        if season_data is None:
            season_data = {
                "SEASON": season_key,
                "G": None,
                "GS": None,
                "TD": None,
                "ATT": None,
                "AVG": None,
                "FUM": None,
                "LNG": None,
                "REC": None,
                "YDS": None,
                "LOST": None,
                "TEAM": None,
            }

        CareerStat.objects.create(
            player=player,
            season=season_data.get("SEASON") or season_key,
            games_played=self.get_int(season_data.get("G")),
            games_started=self.get_int(season_data.get("GS")),
            touchdowns=self.get_int(season_data.get("TD")),
            attempts=self.get_int(season_data.get("ATT")),
            average=self.get_float(season_data.get("AVG")),
            fumbles=self.get_int(season_data.get("FUM")),
            longest=self.get_int(season_data.get("LNG")),
            receptions=self.get_int(season_data.get("REC")),
            yards=self.get_int(season_data.get("YDS")),
            lost=self.get_int(season_data.get("LOST")),
            team=season_data.get("TEAM", None),
        )

    def get_int(self, value):
        """Safely converts a value to an integer, returns None if invalid or missing."""
        if value in [None, "", ""]:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    def get_float(self, value):
        """Safely converts a value to a float, returns None if invalid or missing."""
        if value in [None, "", ""]:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
