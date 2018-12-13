import random
import yaml
from abc import ABC
from pprint import pprint


class AbstractLevel(yaml.YAMLObject):
    @classmethod
    def from_yaml(Class, loader, node):
        def get_level(loader, node):
            data = loader.construct_mapping(node)
            level = {'map': Class.get_map(), 'obj': Class.get_objects()}
            level['obj'].config = data
            return level
        return get_level(loader, node)

    @classmethod
    def get_map(cls):
        return cls.Map()

    @classmethod
    def get_objects(cls):
        return cls.Objects()

    class Map(ABC):
        pass

    class Objects(ABC):
        pass


class EasyLevel(AbstractLevel):
    yaml_tag = "!easy_level"

    def __init__(self):
        self.map = self.Map()
        self.obj = self.Objects()

    class Map:
        def __init__(self):
            self.Map = [[0 for _ in range(5)] for _ in range(5)]
            for i in range(5):
                for j in range(5):
                    if i == 0 or j == 0 or i == 4 or j == 4:
                        self.Map[j][i] = -1
                    else:
                        self.Map[j][i] = random.randint(0, 2)

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = [('next_lvl', (2, 2))]
            self.config = {}

        def get_objects(self, _map):
            for obj_name in ['rat']:
                coord = (random.randint(1, 3), random.randint(1, 3))
                intersect = True
                while intersect:
                    intersect = False
                    for obj in self.objects:
                        if coord == obj[1]:
                            intersect = True
                            coord = (random.randint(1, 3), random.randint(1, 3))

                self.objects.append((obj_name, coord))

            return self.objects


class MediumLevel(AbstractLevel):
    yaml_tag = "!medium_level"

    def __init__(self):
        self.map = self.Map()
        self.obj = self.Objects()

    class Map:
        def __init__(self):
            self.Map = [[0 for _ in range(8)] for _ in range(8)]
            for i in range(8):
                for j in range(8):
                    if i == 0 or j == 0 or i == 7 or j == 7:
                        self.Map[j][i] = -1
                    else:
                        self.Map[j][i] = random.randint(0, 2)

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = [('next_lvl', (4, 4))]
            self.config = {'enemy': ['rat']}

        def get_objects(self, _map):
            for obj_name in self.config['enemy']:
                coord = (random.randint(1, 6), random.randint(1, 6))
                intersect = True
                while intersect:
                    intersect = False
                    for obj in self.objects:
                        if coord == obj[1]:
                            intersect = True
                            coord = (random.randint(1, 6), random.randint(1, 6))

                self.objects.append((obj_name, coord))

            return self.objects


class HardLevel(AbstractLevel):
    yaml_tag = "!hard_level"

    def __init__(self):
        self.map = self.Map()
        self.enemy = self.Objects

    class Map:
        def __init__(self):
            self.Map = [[0 for _ in range(10)] for _ in range(10)]
            for i in range(10):
                for j in range(10):
                    if i == 0 or j == 0 or i == 9 or j == 9:
                        self.Map[j][i] = -1
                    else:
                        self.Map[j][i] = random.randint(-1, 8)

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = [('next_lvl', (5, 5))]
            self.config = {'enemy_count': 10, 'enemy': ['rat', 'snake', "dragon"]}

        def get_objects(self, _map):
            for obj_name in self.config['enemy']:
                for tmp_int in range(self.config['enemy_count']):
                    coord = (random.randint(1, 8), random.randint(1, 8))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[0]][coord[1]] == -1:
                            intersect = True
                            coord = (random.randint(1, 8), random.randint(1, 8))
                            continue
                        for obj in self.objects:
                            if coord == obj[1]:
                                intersect = True
                                coord = (random.randint(1, 8), random.randint(1, 8))

                    self.objects.append((obj_name, coord))

            return self.objects


Levels_Standard = {'levels':[]}
_map = EasyLevel.Map()
_obj = EasyLevel.Objects()
Levels_Standard['levels'].append({'map': _map, 'obj': _obj})

_map = MediumLevel.Map()
_obj = MediumLevel.Objects()
_obj.config = {'enemy':['rat']}
Levels_Standard['levels'].append({'map': _map, 'obj': _obj})

_map = HardLevel.Map()
_obj = HardLevel.Objects()
_obj.config = {'enemy': ['rat', 'snake', 'dragon'], 'enemy_count': 10}
Levels_Standard['levels'].append({'map': _map, 'obj': _obj})

print()
print('Standard')
print()
pprint(Levels_Standard)

Levels_yaml = yaml.load('''levels:
  - !easy_level {}
  - !medium_level
    enemy: ['rat']
  - !hard_level
    enemy:
    - rat
    - snake
    - dragon
    enemy_count: 10''');

print()
print('YAML')
print()
pprint(Levels_yaml)
