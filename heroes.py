from typing import List
import csv
from classes import Hero

HEROES: List[Hero] = [
    Hero(
        id=1,
        nick_name="Gale",
        full_name="Gale Dekarious",
        occupation=["Wizard", "Adventurer", "Deity"],
        powers=["Magical prowess", "High intelligence", "Charisma"],
        hobby=["Studying magic", "Drinking", "Cooking"],
        type="Wizard",
        rank=54
    ),

    Hero(
        id=2,
        nick_name="Ragnar",
        full_name="Ragnar Steelheart",
        occupation=["Warrior", "Mercenary", "Blacksmith"],
        powers=["Super strength", "Sword mastery", "Endurance"],
        hobby=["Forging weapons", "Training", "Hunting"],
        type="Warrior",
        rank=48
    ),

    Hero(
        id=3,
        nick_name="Lyra",
        full_name="Lyra Moonshadow",
        occupation=["Assassin", "Spy", "Thief"],
        powers=["Stealth", "Agility", "Poison mastery"],
        hobby=["Lockpicking", "Night walks", "Collecting jewels"],
        type="Assassin",
        rank=51
    ),

    Hero(
        id=4,
        nick_name="Thorn",
        full_name="Thorn Wildroot",
        occupation=["Druid", "Healer", "Herbalist"],
        powers=["Nature control", "Healing magic", "Animal communication"],
        hobby=["Gardening", "Meditation", "Brewing potions"],
        type="Druid",
        rank=46
    ),

    Hero(
        id=5,
        nick_name="Kael",
        full_name="Kael Stormbreaker",
        occupation=["Knight", "Commander", "Guardian"],
        powers=["Lightning control", "Leadership", "Shield mastery"],
        hobby=["Horse riding", "Strategy games", "Fishing"],
        type="Knight",
        rank=57
    ),

    Hero(
        id=6,
        nick_name="Nyx",
        full_name="Nyx Ravencrest",
        occupation=["Necromancer", "Scholar", "Cult Leader"],
        powers=["Dark magic", "Summoning undead", "Mind control"],
        hobby=["Reading ancient books", "Collecting skulls", "Chess"],
        type="Necromancer",
        rank=62
    ),

    Hero(
        id=7,
        nick_name="Astra",
        full_name="Astra Solwind",
        occupation=["Archer", "Explorer", "Scout"],
        powers=["Perfect aim", "Enhanced vision", "Speed"],
        hobby=["Traveling", "Climbing", "Bird watching"],
        type="Archer",
        rank=44
    ),

    Hero(
        id=8,
        nick_name="Drako",
        full_name="Drako Infernis",
        occupation=["Dragon Rider", "Bounty Hunter", "Gladiator"],
        powers=["Fire breathing", "Combat mastery", "Fear aura"],
        hobby=["Arena fights", "Treasure hunting", "Cooking meat"],
        type="Dragon Rider",
        rank=66
    ),

    Hero(
        id=9,
        nick_name="Selene",
        full_name="Selene Frostveil",
        occupation=["Ice Sorceress", "Queen", "Diplomat"],
        powers=["Ice manipulation", "Telepathy", "Charm"],
        hobby=["Painting", "Ice skating", "Playing harp"],
        type="Sorceress",
        rank=59
    ),

    Hero(
        id=10,
        nick_name="Orion",
        full_name="Orion Nightflare",
        occupation=["Paladin", "Monster Hunter", "Priest"],
        powers=["Holy magic", "Monster tracking", "Healing"],
        hobby=["Praying", "Training", "Storytelling"],
        type="Paladin",
        rank=53
    )
]


def format_array(py_list):
    return '{' + ', '.join(f'"{item}"' for item in py_list) + '}'

with open("heroes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # HEADERS
    writer.writerow([
        "nick_name",
        "full_name",
        "occupation",
        "powers",
        "hobby",
        "type",
        "rank"
    ])

    # DATA
    for hero in HEROES:
        writer.writerow([
            hero.nick_name,
            hero.full_name,
            format_array(hero.occupation),
            format_array(hero.powers),
            format_array(hero.hobby),
            hero.type,
            hero.rank
        ])

# PSQL COMMAND TO IMPORT THE CSV FILE (DONT USE PGADMIN, ITS CRAP) AND INSTRUCTIONS :

# PRODUCE THE FILE WITH F5
# PUT THE LOCAL FILE IN HOME DIRECTORY AND APPLY FULL ACCESS RIGHTS (ALSO TO TOP FOLDER IF NECESSARY)
# ENTER PSQL WITH : sudo -u postgres psql.
# LOG TO THE RIGHT DB
# \copy public.heroes (nick_name, full_name, occupation, powers, hobby, type, rank) FROM '/your/directory/heroes.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF8' QUOTE '"' ESCAPE '''';