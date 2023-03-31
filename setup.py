"""This will setup the knowledge the program needs on the various characters"""

from bs4 import BeautifulSoup
from requests import get

PLAYER_LIST_URL = "https://mobile-legends.fandom.com/wiki/List_of_heroes"
PLAYER_BASE_URL = "https://mobile-legends.fandom.com/wiki/"


list_of_heroes_page = get(PLAYER_LIST_URL)
list_of_heroes_page.raise_for_status()

selector = "#mw-content-text > div.mw-parser-output > div:nth-child(4)"
soup = BeautifulSoup(list_of_heroes_page.text, "html.parser")

data = soup.select(selector)[0]
rows = data.find_all("tr")[1:]

def get_section(text:str, is_ability_page=False):

    sections = text.split("Abilities")
    skill_section = ""

    if is_ability_page:
        sections = text.split("Level Scaling")
        return sections[1] + sections[2]

    for section in sections:
        if "Gallery" in section:
            skill_section = section.split("Gallery")[0]
        else:
            if "Trivia" in section:
                skill_section = section.split("Trivia")[0]
            
    
    if "Passive" not in skill_section and not is_ability_page:
        return ""

    return skill_section

hero_dict = {}

for row in rows:
    td = row.find_all("td")[1]
    hero_name = td.text.strip()

    # Gets the page for that hero
    hero_page = get(PLAYER_BASE_URL + hero_name)

    # Gotta parse the page
    skill_section = get_section(hero_page.text)

    # A list to store the damage types
    damage_type = []
    if not skill_section:
        hero_page = get(PLAYER_BASE_URL + hero_name + "/" + "Abilities")
        print("Had to get an ability page")
        skill_section = get_section(hero_page.text, True)

    if not skill_section:
        print("Could not get skills for character", hero_name)
        continue

    if "Physical Damage" in skill_section:
        damage_type.append("PHYSICAL")
    if "Magic Damage" in skill_section:
        damage_type.append("MAGICAL")

    hero_dict[hero_name] = damage_type