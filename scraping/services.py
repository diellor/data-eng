from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

from etl.models import RawVikingsShow, RawNorsemenShow, RawVikingsNFL
from scraping.parsers import VikingsShowParser, NorsemenShowParser, NFLParser

VIKINGS_SHOW_BASE_URL = "https://www.history.com"
VIKINGS_SHOW_CAST_URL = "https://www.history.com/shows/vikings/cast"
NORSEMEN_SHOW_BASE_URL = "https://en.wikipedia.org/wiki/Norsemen_(TV_series)"
NFL_BASE_URL = "https://www.vikings.com"
NFL_ROSTER_URL = "https://www.vikings.com/team/players-roster/"


class ScrapeService:

    def fetch(self, url: str) -> bytes:
        try:
            return requests.get(url).content
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching {url}: {e.response.status_code}")

    def soupify(self, html_content) -> BeautifulSoup:
        return BeautifulSoup(html_content, "html.parser")


class VikingsShowRawDataService:

    def __init__(self):
        self.scrape_service = ScrapeService()

    def handle(self):
        content = self.scrape_service.fetch(VIKINGS_SHOW_CAST_URL)
        soup = self.scrape_service.soupify(content)
        parsed_data = self.parse_data(soup)
        RawVikingsShow.objects.create(data=parsed_data)

    def parse_data(self, soup):

        cast_data = VikingsShowParser(soup).parse_cast_page()
        for cast in cast_data:
            href = cast.get("href")
            character_page_html = self.scrape_service.fetch(
                f"{VIKINGS_SHOW_BASE_URL}{href}"
            )

            if not href and not character_page_html:
                continue

            character_page_soup = self.scrape_service.soupify(character_page_html)
            character_name, actor_name, character_description = VikingsShowParser(
                character_page_soup
            ).parse_character_page()

            cast.update(
                {
                    "character_name": character_name,
                    "actor_name": actor_name,
                    "character_description": character_description,
                }
            )

        return cast_data


class NorsemenShowRawDataService:

    def __init__(self):
        self.scrape_service = ScrapeService()

    def handle(self):
        content = self.scrape_service.fetch(NORSEMEN_SHOW_BASE_URL)
        soup = self.scrape_service.soupify(content)
        character_list = NorsemenShowParser(soup).parse_character_list()
        RawNorsemenShow.objects.create(data=character_list)


class NFLRawDataService:

    def __init__(self):
        self.scrape_service = ScrapeService()

    def handle(self):
        content = self.scrape_service.fetch(NFL_ROSTER_URL)
        soup = self.scrape_service.soupify(content)
        players = NFLParser(soup).parse_players_table()

        with ThreadPoolExecutor(max_workers=8) as executor:
            players = list(executor.map(self.fetch_player_details, players))

        RawVikingsNFL.objects.create(data=players)

    def fetch_player_details(self, player):
        """Fetch player details concurrently."""
        player_content = self.scrape_service.fetch(player["profile_link"])
        soup = self.scrape_service.soupify(player_content)
        player_details = NFLParser(soup).parse_player_details()
        player["details"] = player_details
        return player
