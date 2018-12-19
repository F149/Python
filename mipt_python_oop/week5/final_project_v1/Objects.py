from abc import ABC, abstractmethod
import pygame
import random

import Service


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class AbstractObject(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def draw(self, display):
        if display.engine.game_over:
            return

        size = display.engine.sprite_size

        min_x = display.engine.map_min_x
        min_y = display.engine.map_min_y

        if not (self.position[0] >= min_x and self.position[1] >= min_y):
            return

        display.blit(self.sprite, ((self.position[0] - min_x) * size,
                                   display.engine.progress_height +
                                   (self.position[1] - min_y) * size))


class Interactive(ABC):
    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):
    def __init__(self, name, icon, action, position):
        self.name = name.capitalize()
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):
    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2

    def hit(self):
        is_crit = random.randint(1, 100) <= self.stats['luck']
        if is_crit:
            damage = (random.randint(50, 100) / 100) * self.stats['strength']
        else:
            damage = (random.randint(35, 65) / 100) * self.stats['strength']
            damage *= 1 + \
                random.randint(1, self.stats['intelligence'] * 2) / 100
        return is_crit, int(damage)

    def defend(self, damage):
        is_miss = random.randint(1, 100) <= self.stats['luck']
        taken = damage * (1 - random.randint(1, self.stats['endurance']) / 100)
        taken = int(taken)
        if not is_miss:
            self.hp = max(0, self.hp - taken)
        return is_miss, taken


class Enemy(Creature, Interactive):
    def __init__(self, name, icon, stats, xp, position):
        super().__init__(icon, stats, position)
        self.name = name.capitalize()
        self.stats['experience'] = xp

    def interact(self, engine, hero):
        engine.cur_enemy = self
        Service.fight(engine, hero)


class Hero(Creature):
    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.name = 'Hero'
        super().__init__(icon, stats, pos)

    def level_up(self, engine):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.stats["intelligence"] += 1
            self.calc_max_HP()
            self.hp = self.max_hp
            engine.notify(f'Level up! ({self.level})')


class Effect(Hero):
    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @property
    def name(self):
        return self.base.name

    @abstractmethod
    def apply_effect(self):
        pass


# FIXED
# add classes

class Berserk(Effect):
    def apply_effect(self):
        for param in 'strength', 'endurance':
            self.stats[param] += 4
        for param in ('luck',):
            self.stats[param] += 2
        for param in ('intelligence',):
            self.stats[param] -= 2


class Blessing(Effect):
    def apply_effect(self):
        for param in 'strength', 'endurance', 'intelligence':
            self.stats[param] += 3
        self.stats['luck'] += 2


class Weakness(Effect):
    def apply_effect(self):
        for param in 'strength', 'endurance':
            self.stats[param] -= 4
