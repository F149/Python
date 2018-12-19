import pygame
import random
import yaml
import os
import Objects

OBJECT_TEXTURE = os.path.join("texture", "objects")
ENEMY_TEXTURE = os.path.join("texture", "enemies")
ALLY_TEXTURE = os.path.join("texture", "ally")


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


def reload_game(engine, hero):
    global level_list
    level_list_max = len(level_list) - 1
    engine.level += 1
    hero.position = [1, 1]
    engine.objects = []
    generator = level_list[min(engine.level, level_list_max)]
    _map = generator['map'].get_map()
    engine.load_map(_map)
    engine.add_objects(generator['obj'].get_objects(_map))
    engine.add_hero(hero)


def restore_hp(engine, hero):
    engine.score += 0.1
    hero.hp = hero.max_hp
    engine.notify("HP restored")


def apply_blessing(engine, hero):
    if hero.gold >= int(20 * 1.5**engine.level) - \
            2 * hero.stats["intelligence"]:
        engine.score += 0.2
        hero.gold -= int(20 * 1.5**engine.level) - \
            2 * hero.stats["intelligence"]
        if random.randint(0, 1) == 0:
            engine.hero = Objects.Blessing(hero)
            engine.notify("Blessing applied")
        else:
            engine.hero = Objects.Berserk(hero)
            engine.notify("Berserk applied")
    else:
        engine.score -= 0.1


def remove_effect(engine, hero):
    if hero.gold >= int(10 * 1.5**engine.level) - \
            2 * hero.stats["intelligence"] and "base" in dir(hero):
        hero.gold -= int(10 * 1.5**engine.level) - \
                2 * hero.stats["intelligence"]
        engine.hero = hero.base
        engine.hero.calc_max_HP()
        engine.notify("Effect removed")
    elif 'base' not in dir(hero):
        engine.notify('No effect to be removed')
    else:
        engine.notify('Not enough gold to remove effect')


def add_gold(engine, hero):
    if random.randint(1, 10) == 1:
        engine.score -= 0.05
        engine.hero = Objects.Weakness(hero)
        engine.notify("You were cursed")
    else:
        engine.score += 0.1
        gold = int(random.randint(10, 1000) * (1.1**(engine.hero.level - 1)))
        hero.gold += gold
        engine.notify(f"{gold} gold added")


def fight(engine, hero):
    enemy = engine.cur_enemy
    hero = engine.hero

    engine.notify(f'Hero fights with {enemy.name}')

    coin = random.randint(0, 1)
    attacker = (hero, enemy)[coin]
    defender = (hero, enemy)[1 - coin]
    while (enemy.hp > 0 and hero.hp > 0):
        info = ''

        is_crit, damage = attacker.hit()
        if is_crit:
            info += f'Critical damage by {attacker.name}! '
        else:
            info += f'{attacker.name} hit: '

        is_miss, taken = defender.defend(damage)
        if is_miss:
            info += f'{attacker.name} missed!'
        else:
            info += f'{defender.name} lost {taken}HP'

        engine.notify(info)
        attacker, defender = defender, attacker

    if hero.hp > 0:
        engine.notify(f'{enemy.name} died')
        engine.notify(f'Hero earned {enemy.stats["experience"]}XP')
        hero.exp += enemy.stats['experience']
        engine.score += enemy.stats['experience'] // 100
        hero.level_up(engine)
    else:
        engine.notify('Hero died...')
        engine.game_over = True

    del engine.cur_enemy


class MapFactory(yaml.YAMLObject):

    @staticmethod
    def get_obj_category(obj):
        # Here we consider that yaml files are always correct
        for category in object_list_prob:
            if obj in object_list_prob[category]:
                return category

    @staticmethod
    def gen_coord(map, objects, max_coords):
        coord = (
            random.randint(1, max_coords[0]),
            random.randint(1, max_coords[1])
        )
        intersect = True
        while intersect:
            intersect = False
            if map[coord[1]][coord[0]] == wall:
                intersect = True
                coord = (
                    random.randint(1, max_coords[0]),
                    random.randint(1, max_coords[1])
                )
                continue
            for obj in objects:
                if coord == obj.position or coord == (1, 1):
                    intersect = True
                    coord = (
                        random.randint(1, max_coords[0]),
                        random.randint(1, max_coords[1])
                    )
        return coord

    # FIXED Add generating from yaml
    @classmethod
    def from_yaml(cls, loader, node):
        _map = cls.Map()
        _obj = cls.Objects()
        level_objects = loader.construct_mapping(node)

        map = _map.get_map()
        objects = _obj.get_objects(map)

        for obj, count in level_objects.items():
            category = cls.get_obj_category(obj)
            prop = object_list_prob[category][obj]

            if category in ('objects', 'ally'):
                for _ in range(count):
                    coord = cls.gen_coord(map, objects, (39, 39))
                    objects.append(
                            Objects.Ally(
                                obj,
                                prop['sprite'],
                                prop['action'],
                                coord
                            )
                    )
            else:   # category == 'enemies'
                for _ in range(count):
                    coord = cls.gen_coord(map, objects, (39, 39))
                    objects.append(
                            Objects.Enemy(
                                obj,
                                prop['sprite'],
                                prop,
                                prop['experience'],
                                coord
                            )
                    )

        _obj.objects = objects
        return {'map': _map, 'obj': _obj}


class EndMap(MapFactory):
    yaml_tag = "!end_map"

    class Map:
        def __init__(self):
            self.Map = ['000000000000000000000000000000000000000',
                        '0                                     0',
                        '0                                     0',
                        '0  0   0   000   0   0  00000  0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  000    0   0  00000  0000   0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  0   0   000   0   0  00000  00000  0',
                        '0                                   0 0',
                        '0                                     0',
                        '000000000000000000000000000000000000000'
                        ]
            self.Map = list(map(list, self.Map))
            for i in self.Map:
                for j in range(len(i)):
                    i[j] = wall if i[j] == '0' else floor1

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            return self.objects


class RandomMap(MapFactory):
    yaml_tag = "!random_map"

    class Map:
        def __init__(self):
            self.Map = [[0 for _ in range(41)] for _ in range(41)]
            for i in range(41):
                for j in range(41):
                    if i == 0 or j == 0 or i == 40 or j == 40:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = [
                                            wall, floor1, floor2, floor3,
                                            floor1, floor2, floor3, floor1,
                                            floor2
                                        ][random.randint(0, 8)]

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            for obj_name in object_list_prob['objects']:
                prop = object_list_prob['objects'][obj_name]
                for i in range(random.randint(prop['min-count'],
                               prop['max-count'])):
                    coord = MapFactory.gen_coord(_map, self.objects, (39, 39))
                    # coord = (random.randint(1, 39), random.randint(1, 39))
                    # intersect = True
                    # while intersect:
                    #    intersect = False
                    #    if _map[coord[1]][coord[0]] == wall:
                    #        intersect = True
                    #        coord = (random.randint(1, 39),
                    #                 random.randint(1, 39))
                    #        continue
                    #    for obj in self.objects:
                    #        if coord == obj.position or coord == (1, 1):
                    #            intersect = True
                    #            coord = (random.randint(1, 39),
                    #                     random.randint(1, 39))

                    self.objects.append(
                            Objects.Ally(obj_name, prop['sprite'],
                                         prop['action'], coord)
                            )

            for obj_name in object_list_prob['ally']:
                prop = object_list_prob['ally'][obj_name]
                for i in range(random.randint(prop['min-count'],
                               prop['max-count'])):
                    coord = MapFactory.gen_coord(_map, self.objects, (39, 39))
                    # coord = (random.randint(1, 39), random.randint(1, 39))
                    # intersect = True
                    # while intersect:
                    #    intersect = False
                    #    if _map[coord[1]][coord[0]] == wall:
                    #        intersect = True
                    #        coord = (random.randint(1, 39),
                    #                 random.randint(1, 39))
                    #        continue
                    #    for obj in self.objects:
                    #        if coord == obj.position or coord == (1, 1):
                    #            intersect = True
                    #            coord = (random.randint(1, 39),
                    #                     random.randint(1, 39))

                    self.objects.append(
                            Objects.Ally(obj_name, prop['sprite'],
                                         prop['action'], coord)
                            )

            for obj_name in object_list_prob['enemies']:
                prop = object_list_prob['enemies'][obj_name]
                for i in range(random.randint(0, 5)):
                    coord = MapFactory.gen_coord(_map, self.objects, (30, 22))
                    # coord = (random.randint(1, 30), random.randint(1, 22))
                    # intersect = True
                    # while intersect:
                    #    intersect = False
                    #    if _map[coord[1]][coord[0]] == wall:
                    #        intersect = True
                    #        coord = (random.randint(1, 39),
                    #                 random.randint(1, 39))
                    #        continue
                    #    for obj in self.objects:
                    #        if coord == obj.position or coord == (1, 1):
                    #            intersect = True
                    #            coord = (random.randint(1, 39),
                    #                     random.randint(1, 39))

                    self.objects.append(
                            Objects.Enemy(obj_name, prop['sprite'],
                                          prop, prop['experience'], coord)
                            )

            return self.objects


# FIXED
# add classes for YAML !empty_map and !special_map{}

class EmptyMap(MapFactory):
    yaml_tag = '!empty_map'

    class Map:
        def __init__(self):
            self.Map = [[0 for _ in range(41)] for _ in range(41)]
            ground = [
                        floor1, floor2, floor3,
                        floor1, floor2, floor3,
                        floor1, floor2, floor3
                     ][random.randint(0, 8)]
            for i in range(41):
                for j in range(41):
                    if i == 0 or j == 0 or i == 40 or j == 40:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = ground

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            return self.objects


class SpecialMap(MapFactory):
    yaml_tag = '!special_map'

    class Map:
        def __init__(self):
            self.Map = [[0 for _ in range(41)] for _ in range(41)]
            ground = [
                        floor1, floor2, floor3,
                        floor1, floor2, floor3,
                        floor1, floor2, floor3
                     ][random.randint(0, 8)]
            for i in range(41):
                for j in range(41):
                    if i == 0 or j == 0 or i == 40 or j == 40:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = ground
            self.Map[2][2] = floor2

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            return self.objects


wall = [0]
floor1 = [0]
floor2 = [0]
floor3 = [0]


def service_init(sprite_size, full=True):
    global object_list_prob, level_list

    global wall
    global floor1
    global floor2
    global floor3

    wall[0] = create_sprite(os.path.join("texture", "wall.png"), sprite_size)
    floor1[0] = create_sprite(os.path.join("texture", "Ground_1.png"),
                              sprite_size)
    floor2[0] = create_sprite(os.path.join("texture", "Ground_2.png"),
                              sprite_size)
    floor3[0] = create_sprite(os.path.join("texture", "Ground_3.png"),
                              sprite_size)

    with open("objects.yml") as file:
        object_list_tmp = yaml.load(file.read())
        if full:
            object_list_prob = object_list_tmp

        object_list_actions = {'reload_game': reload_game,
                               'add_gold': add_gold,
                               'apply_blessing': apply_blessing,
                               'remove_effect': remove_effect,
                               'restore_hp': restore_hp}

        for obj in object_list_prob['objects']:
            prop = object_list_prob['objects'][obj]
            prop_tmp = object_list_tmp['objects'][obj]
            prop['sprite'][0] = create_sprite(
                                    os.path.join(
                                            OBJECT_TEXTURE,
                                            prop_tmp['sprite'][0]
                                    ),
                                    sprite_size
                                )
            prop['action'] = object_list_actions[prop_tmp['action']]

        for ally in object_list_prob['ally']:
            prop = object_list_prob['ally'][ally]
            prop_tmp = object_list_tmp['ally'][ally]
            prop['sprite'][0] = create_sprite(
                                    os.path.join(
                                        ALLY_TEXTURE,
                                        prop_tmp['sprite'][0]
                                    ),
                                    sprite_size
                                )
            prop['action'] = object_list_actions[prop_tmp['action']]

        for enemy in object_list_prob['enemies']:
            prop = object_list_prob['enemies'][enemy]
            prop_tmp = object_list_tmp['enemies'][enemy]
            prop['sprite'][0] = create_sprite(
                                    os.path.join(
                                        ENEMY_TEXTURE,
                                        prop_tmp['sprite'][0]
                                    ),
                                    sprite_size
                                )

    if full:
        with open("levels.yml") as file:
            level_list = yaml.load(file.read())['levels']
            level_list.append({'map': EndMap.Map(), 'obj': EndMap.Objects()})
