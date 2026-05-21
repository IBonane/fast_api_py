from heroes import HEROES


def find_proper_hero_id(hero):
    hero.id = 1 if len(HEROES) == 0 else HEROES[-1].id + 1
    return hero
