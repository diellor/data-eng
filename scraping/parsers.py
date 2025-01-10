from bs4 import BeautifulSoup


class VikingsShowParser:

    def __init__(self, soup: BeautifulSoup):
        """Initialize with the BeautifulSoup object."""
        self.soup = soup

    def parse_cast_page(self) -> list | None:
        """Parse the main cast page to extract character links, image src, and hrefs."""

        container_div = self.soup.find("div", class_="tile-list tile-boxed")
        if not container_div:
            print("No div with class 'tile-list tile-boxed' found.")
            return None

        li_elements = container_div.find_all("li")
        if not li_elements:
            print("No <li> elements found in container_div.")
            return []

        cast_data = [
            {
                "href": item.find("a").get("href") if item.find("a") else None,
                "img_src": (
                    item.find("div", class_="img-container").find("img").get("src")
                    if item.find("div", class_="img-container")
                    else None
                ),
            }
            for item in li_elements
        ]

        return cast_data

    def parse_character_page(self) -> tuple[str | None, str | None, str | None]:
        """Parse a character's page to extract the character name, actor name, and first <p> description."""

        header = self.soup.find("header", class_="section-title")
        if not header:
            print("No header with class 'section-title' found.")
            return None, None, None

        h1_tag = header.find("h1")
        if not h1_tag:
            print("No <h1> tag found in the header.")
            return None, None, None

        character_name = h1_tag.find("strong").get_text(strip=True) if h1_tag.find("strong") else None
        actor_name = (
            h1_tag.find("small").get_text(strip=True).replace("Played by", "").strip()
            if h1_tag.find("small")
            else None
        )

        article = self.soup.find("article", class_="main-article")
        if not article:
            print("No article with class 'main-article' found.")
            return character_name, actor_name, None

        character_description = article.find("p").get_text(strip=True) if article.find("p") else None

        return character_name, actor_name, character_description


class NorsemenShowParser:

    def __init__(self, soup: BeautifulSoup):
        """Initialize with the BeautifulSoup object."""
        self.soup = soup

    def parse_character_list(self) -> list | None:
        """Parse the Wikipedia page to extract character names and descriptions."""

        target_div = self.soup.find("div", class_="mw-content-ltr mw-parser-output")
        if not target_div:
            print("Target div not found.")
            return None

        character_data = []
        for item in target_div.find_all("li"):
            if item.find_parent("table"):
                continue

            link_tag = item.find("a")
            character_name = (
                link_tag["title"] if link_tag and "title" in link_tag.attrs else None
            )

            description = item.get_text(strip=False)
            actor_name, description = self.parse_actor_and_description(description)

            if character_name:
                character_data.append(
                    {
                        "character_name": character_name,
                        "description": description,
                        "actor_name": actor_name,
                    }
                )

        return character_data

    def parse_actor_and_description(self, description) -> tuple[str | None, str | None]:
        """
        Parses the input string to extract the actor name (from 'as <name>') and the description.
        Returns None for actor_name or description if they are missing.
        """

        if " as " not in description:
            print("The string does not contain 'as'.")
            return None, None

        actor_and_description = description.split(" as ", 1)[1].strip()
        if "," in actor_and_description:
            actor_name, description = map(
                str.strip, actor_and_description.split(",", 1)
            )
        else:
            actor_name, description = actor_and_description, None

        return actor_name or None, description or None


class NFLParser:

    def __init__(self, soup: BeautifulSoup):
        """Initialize with the BeautifulSoup object."""
        self.soup = soup

    def parse_players_table(self) -> list | None:
        """Parse the players table to extract names, profile links, and picture URLs."""

        table = self.soup.find("table")
        if not table:
            return None

        players = []
        for row in table.find_all("tr"):
            name_span = row.find("span", class_="nfl-o-roster__player-name")

            if not name_span:
                continue

            name_link = name_span.find("a")
            if not name_link:
                continue

            player_name = name_link.text.strip()
            player_profile_link = f"https://www.vikings.com{name_link['href']}"
            img_tag = row.find("img", class_="img-responsive")
            player_image_src = img_tag["src"].strip() if img_tag else None

            players.append(
                {
                    "player_name": player_name,
                    "profile_link": player_profile_link,
                    "image_src": player_image_src,
                }
            )

        return players

    def parse_player_details(self) -> dict:
        """
        Fetch and parse the player's profile page to extract details dynamically for each paragraph,
        career stats, and biography section as raw HTML.
        """
        stats_div = self.soup.find("div", class_="nfl-t-person-tile__stat-details")
        player_details = {}
        if stats_div:
            for p in stats_div.find_all("p"):
                strong_tag = p.find("strong")
                if strong_tag:
                    label, _, value = p.get_text(strip=True).partition(":")
                    player_details[label.strip()] = value.strip()

        player_details["career_stats"] = self.parse_career_stats()

        biography_div = self.soup.find("div", class_="d3-l-grid--inner nfl-c-biography")
        player_details["biography_html"] = str(biography_div) if biography_div else None

        return player_details

    def parse_career_stats(self):
        """
        Parse the player's career stats table to extract the first season (e.g., 2023)
        and stats for 2021 (if present).
        """

        stats_table = self.soup.find("table", attrs={"summary": "Career Stats"})
        if not stats_table:
            return None

        headers = [
            header.get_text(strip=True)
            for header in stats_table.find("thead").find_all("th")
        ]

        rows = stats_table.find("tbody").find_all("tr")
        stats_data = {}
        for row in rows:
            season_text = row.find("td").text.strip()
            row_data = [td.get_text(strip=True) for td in row.find_all("td")]
            stats_data[season_text] = dict(zip(headers, row_data))

        stats_data["2021"] = stats_data.get("2021", None)
        latest_season = next(iter(stats_data), None)

        return {
            "latest_season": stats_data.get(latest_season),
            "2021": stats_data["2021"],
        }
