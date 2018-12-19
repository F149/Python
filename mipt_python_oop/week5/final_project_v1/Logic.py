import Service


class GameEngine:
    objects = []
    map = None
    hero = None
    level = -1
    working = True
    subscribers = set()
    score = 0.
    game_process = True
    show_help = False
    game_over = False

    # Current top left map position among those being displayed
    map_min_x = 0
    map_min_y = 0

    def subscribe(self, obj):
        self.subscribers.add(obj)

    def unsubscribe(self, obj):
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def notify(self, message):
        for i in self.subscribers:
            i.update(message)

    # HERO
    def add_hero(self, hero):
        self.hero = hero

    def interact(self):
        for obj in self.objects:
            if list(obj.position) == self.hero.position:
                obj.interact(self, self.hero)
                if self.hero.hp > 0 and obj in self.objects:
                    self.delete_object(obj)

    def center_hero(self):
        sprites_x = self.map_width // self.sprite_size
        sprites_y = self.map_height // self.sprite_size
        center_x = sprites_x // 2 if sprites_x % 2 == 0 else sprites_x // 2 + 1
        center_y = sprites_y // 2 if sprites_y % 2 == 0 else sprites_y // 2 + 1
        center_x -= 1
        center_y -= 1

        self.map_min_x = max(0, self.hero.position[0] - center_x)
        self.map_min_y = max(0, self.hero.position[1] - center_y)

        self.map_min_x = min(self.map_min_x, len(self.map[0]) - sprites_x)
        self.map_min_y = min(self.map_min_y, len(self.map) + 1 - sprites_y)

        # After last opreration min values may happen < 0
        self.map_min_x = max(self.map_min_x, 0)
        self.map_min_y = max(self.map_min_y, 0)

    # MOVEMENT
    def move_up(self):
        if (self.map[self.hero.position[1] - 1][self.hero.position[0]] ==
                Service.wall):
            return
        self.hero.position[1] -= 1
        self.score -= 0.02
        self.center_hero()
        self.interact()

    def move_down(self):
        if (self.map[self.hero.position[1] + 1][self.hero.position[0]] ==
                Service.wall):
            return
        self.hero.position[1] += 1
        self.score -= 0.02
        self.center_hero()
        self.interact()

    def move_left(self):
        if (self.map[self.hero.position[1]][self.hero.position[0] - 1] ==
                Service.wall):
            return
        self.hero.position[0] -= 1
        self.score -= 0.02
        self.center_hero()
        self.interact()

    def move_right(self):
        if (self.map[self.hero.position[1]][self.hero.position[0] + 1] ==
                Service.wall):
            return
        self.hero.position[0] += 1
        self.score -= 0.02
        self.center_hero()
        self.interact()

    # MAP
    def load_map(self, game_map):
        self.map = game_map

    # OBJECTS
    def add_object(self, obj):
        self.objects.append(obj)

    def add_objects(self, objects):
        self.objects.extend(objects)

    def delete_object(self, obj):
        self.objects.remove(obj)
