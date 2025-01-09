from concurrent.futures import ThreadPoolExecutor
import time
import requests
from bs4 import BeautifulSoup
from etl.models import RawVikingsShow, RawNorsemenShow, RawVikingsNFL, ScrapingLog
from scraping.parsers import VikingsShowParser, NorsemenShowParser, NFLParser

VIKINGS_SHOW_BASE_URL = "https://www.history.com"
VIKINGS_SHOW_CAST_URL = "https://www.history.com/shows/vikings/cast"
NORSEMEN_SHOW_BASE_URL = "https://en.wikipedia.org/wiki/Norsemen_(TV_series)"
NFL_ROSTER_URL = "https://www.vikings.com/team/players-roster/"


class ScrapeService:

    def log_scraping_task(self, task_name, status, execution_time, retries=0, error_message=None, source=None):
        print("Storing Logs")  # Debugging
        """Log scraping task details in the database."""
        ScrapingLog.objects.create(
            task_name=task_name,
            status=status,
            execution_time=execution_time,
            retries=retries,
            error_message=error_message,
            source=source
        )

    def fetch(self, url: str) -> bytes:
        start_time = time.time()
        retries = 0
        try:
            response = requests.get(url)
            response.raise_for_status()
            execution_time = time.time() - start_time
            self.log_scraping_task(
                task_name=f"Fetch URL: {url}",
                status="success",
                execution_time=execution_time,
                retries=retries,
                source=url
            )
            return response.content
        except requests.exceptions.RequestException as e:
            execution_time = time.time() - start_time
            self.log_scraping_task(
                task_name=f"Fetch URL: {url}",
                status="failure",
                execution_time=execution_time,
                retries=retries,
                error_message=str(e),
                source=url
            )
            raise Exception(f"Error fetching {url}: {e}")

    def soupify(self, html_content) -> BeautifulSoup:
        return BeautifulSoup(html_content, "html.parser")


class VikingsShowRawDataService:

    def __init__(self):
        self.scrape_service = ScrapeService()

    def handle(self):
        start_time = time.time()
        try:
            content = self.scrape_service.fetch(VIKINGS_SHOW_CAST_URL)
            soup = self.scrape_service.soupify(content)
            parsed_data = self.parse_data(soup)
            RawVikingsShow.objects.create(data=parsed_data)
            execution_time = time.time() - start_time
            self.scrape_service.log_scraping_task(
                task_name="Scrape Vikings Show Data",
                status="success",
                execution_time=execution_time,
                source=VIKINGS_SHOW_CAST_URL
            )
        except Exception as e:
            execution_time = time.time() - start_time
            self.scrape_service.log_scraping_task(
                task_name="Scrape Vikings Show Data",
                status="failure",
                execution_time=execution_time,
                error_message=str(e),
                source=VIKINGS_SHOW_CAST_URL
            )
            raise

    def parse_data(self, soup):
        cast_data = VikingsShowParser(soup).parse_cast_page()
        for cast in cast_data:
            href = cast.get("href")
            if not href:
                continue
            try:
                character_page_html = self.scrape_service.fetch(f"{VIKINGS_SHOW_BASE_URL}{href}")
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
            except Exception as e:
                self.scrape_service.log_scraping_task(
                    task_name=f"Parse Character Page: {href}",
                    status="failure",
                    execution_time=0,
                    error_message=str(e),
                    source=f"{VIKINGS_SHOW_BASE_URL}{href}"
                )
        return cast_data


class NorsemenShowRawDataService:

    def __init__(self):
        self.scrape_service = ScrapeService()

    def handle(self):
        start_time = time.time()
        try:
            content = self.scrape_service.fetch(NORSEMEN_SHOW_BASE_URL)
            soup = self.scrape_service.soupify(content)
            character_list = NorsemenShowParser(soup).parse_character_list()
            RawNorsemenShow.objects.create(data=character_list)
            execution_time = time.time() - start_time
            self.scrape_service.log_scraping_task(
                task_name="Scrape Norsemen Show Data",
                status="success",
                execution_time=execution_time,
                source=NORSEMEN_SHOW_BASE_URL
            )
        except Exception as e:
            execution_time = time.time() - start_time
            self.scrape_service.log_scraping_task(
                task_name="Scrape Norsemen Show Data",
                status="failure",
                execution_time=execution_time,
                error_message=str(e),
                source=NORSEMEN_SHOW_BASE_URL
            )
            raise


class NFLRawDataService:

    def __init__(self):
        self.scrape_service = ScrapeService()

    def handle(self):
        start_time = time.time()
        try:
            content = self.scrape_service.fetch(NFL_ROSTER_URL)
            soup = self.scrape_service.soupify(content)
            players = NFLParser(soup).parse_players_table()

            with ThreadPoolExecutor(max_workers=8) as executor:
                players = list(executor.map(self.fetch_player_details, players))

            RawVikingsNFL.objects.create(data=players)
            execution_time = time.time() - start_time
            self.scrape_service.log_scraping_task(
                task_name="Scrape Vikings NFL Data",
                status="success",
                execution_time=execution_time,
                source=NFL_ROSTER_URL
            )
        except Exception as e:
            execution_time = time.time() - start_time
            self.scrape_service.log_scraping_task(
                task_name="Scrape Vikings NFL Data",
                status="failure",
                execution_time=execution_time,
                error_message=str(e),
                source=NFL_ROSTER_URL
            )
            raise

    def fetch_player_details(self, player):
        try:
            player_content = self.scrape_service.fetch(player["profile_link"])
            soup = self.scrape_service.soupify(player_content)
            player_details = NFLParser(soup).parse_player_details()
            player["details"] = player_details
            return player
        except Exception as e:
            self.scrape_service.log_scraping_task(
                task_name=f"Fetch Player Details: {player['profile_link']}",
                status="failure",
                execution_time=0,
                error_message=str(e),
                source=player["profile_link"]
            )
            return player