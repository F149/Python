from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []

        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,

            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):

    def __init__(self, base):
        super().__init__()
        self.base = base

    def get_stats(self):  # Возвращает итоговые хараетеристики
        # после применения эффекта
        self.base.get_stats()

    def get_positive_effects(self):
        self.base.get_positive_effects()

    def get_negative_effects(self):
        self.base.get_negative_effects()


class AbstractPositive(AbstractEffect):

    def __init__(self, base: Hero):
        super().__init__(base)

    def get_stats(self):
        super().get_stats()

    def get_positive_effects(self):
        super().get_positive_effects()


class AbstractNegative(AbstractEffect):

    def __init__(self, base: Hero):
        super().__init__(base)

    def get_stats(self):
        super().get_stats()

    def get_negative_effects(self):
        super().get_negative_effects()


class Blessing(AbstractPositive):

    def __init__(self, base):
        super().__init__(base)
        for stat in self.base.stats.keys():
            self.base.positive_effects.append((stat, 2))
            self.base.stats[stat] += 2

    def get_stats(self):
        return self.base.stats.copy()

    def get_positive_effects(self):
        return self.base.positive_effects.copy()


if __name__ == '__main__':
    hero = Hero()
    print(hero.get_positive_effects())
    print(hero.get_negative_effects())
    print(hero.get_stats())

    bless = Blessing(hero)
    print(bless.get_positive_effects())
    print(bless.get_stats())

    more_blessing = Blessing(bless)
    print(more_blessing.get_stats())

## Объявим абстрактный декоратор
#class AbstractEffect(Hero, ABC):
#
#    def __init__(self, base):
#        self.base = base
#
#    @abstractmethod
#    def get_positive_effects(self):
#        return self.positive_effects
#
#    @abstractmethod
#    def get_negative_effects(self):
#        return self.negative_effects
#
#    @abstractmethod
#    def get_stats(self):
#        pass
#
#
## В AbstractPositive будем возвращать список наложенных отрицательных эффектов без изменений, чтобы не определять данный метод во всех положительных эффектах
#class AbstractPositive(AbstractEffect):
#
#    def get_negative_effects(self):
#        return self.base.get_negative_effects()
#
#
## Объявим несколько положительных эффектов
#class Berserk(AbstractPositive):
#
#    def get_stats(self):
#        # Получим характеристики базового объекта, модифицируем их и вернем
#        stats = self.base.get_stats()
#        stats["HP"] += 50
#        stats["Strength"] += 7
#        stats["Endurance"] += 7
#        stats["Agility"] += 7
#        stats["Luck"] += 7
#        stats["Perception"] -= 3
#        stats["Charisma"] -= 3
#        stats["Intelligence"] -= 3
#        return stats
#
#    def get_positive_effects(self):
#        # Модифицируем список эффектов, добавив в него новый эффект
#        return self.base.get_positive_effects() + ["Berserk"]
#
#
#class Blessing(AbstractPositive):
#
#    def get_stats(self):
#        stats = self.base.get_stats()
#        stats["Strength"] += 2
#        stats["Endurance"] += 2
#        stats["Agility"] += 2
#        stats["Luck"] += 2
#        stats["Perception"] += 2
#        stats["Charisma"] += 2
#        stats["Intelligence"] += 2
#        return stats
#
#    def get_positive_effects(self):
#        return self.base.get_positive_effects() + ["Blessing"]
#
#
## Для отрицательных эффектов неизменным останется список положительных эффектов
#class AbstractNegative(AbstractEffect):
#
#    def get_positive_effects(self):
#        return self.base.get_positive_effects()
#
#
## Аналогично положительным эффектам, объявим отрицательные
#class Weakness(AbstractNegative):
#
#    def get_stats(self):
#        stats = self.base.get_stats()
#        stats["Strength"] -= 4
#        stats["Endurance"] -= 4
#        stats["Agility"] -= 4
#        return stats
#
#    def get_negative_effects(self):
#        return self.base.get_negative_effects() + ["Weakness"]
#
#
#class Curse(AbstractNegative):
#
#    def get_stats(self):
#        stats = self.base.get_stats()
#        stats["Strength"] -= 2
#        stats["Endurance"] -= 2
#        stats["Agility"] -= 2
#        stats["Luck"] -= 2
#        stats["Perception"] -= 2
#        stats["Charisma"] -= 2
#        stats["Intelligence"] -= 2
#        return stats
#
#    def get_negative_effects(self):
#        return self.base.get_negative_effects() + ["Curse"]
#
#
#class EvilEye(AbstractNegative):
#
#    def get_stats(self):
#        stats = self.base.get_stats()
#        stats["Luck"] -= 10
#        return stats
#
#    def get_negative_effects(self):
#        return self.base.get_negative_effects() + ["EvilEye"]
