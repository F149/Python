import pygame
import collections

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
}


class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["black"])

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    # FIXED connect_engine
    def connect_engine(self, engine):
        # Save engine
        self.engine = engine
        # Send it so the successor, if any
        if self.successor is not None:
            self.successor.connect_engine(engine)


class GameSurface(ScreenHandle):

    # FIXED save engine and send it to next in chain (inherited)

    def draw_hero(self):
        self.engine.hero.draw(self)

    def draw_map(self):
        size = self.engine.sprite_size
        # FIXED calculate (min_x,min_y) - left top corner

         sprites_x = self.engine.map_width // size
         sprites_y = self.engine.map_height // size
         if ((self.engine.hero.position[0] +
                 sprites_x // 2) >= len(self.engine.map[0]) or
                 (self.engine.hero.position[1] +
                  sprites_y // 2) >= len(self.engine.map)):
             sh = self
             while not isinstance(sh, ScreenHandle):
                 sh = sh.successor
             sh.fill(colors['black'])

        min_x = self.engine.map_min_x
        min_y = self.engine.map_min_y

        if self.engine.map:
            for i in range(len(self.engine.map[0]) - min_x):
                for j in range(len(self.engine.map) - min_y):
                    self.blit(self.engine.map[min_y + j][min_x + i][0],
                              (i * size,
                              self.engine.progress_height + j * size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        size = self.engine.sprite_size
        # FIXED calculate (min_x,min_y) - left top corner

        min_x = self.engine.map_min_x
        min_y = self.engine.map_min_y

        if not (coord[0] >= min_x and coord[1] >= min_y):
            return

        self.blit(sprite, ((coord[0] - min_x) * size,
                           self.engine.progress_height +
                           (coord[1] - min_y) * size))

    def draw(self, canvas):
        self.draw_map()
        for obj in self.engine.objects:
            self.draw_object(obj.sprite[0], obj.position)
        self.draw_hero()

        # FIXED draw next surface in chain
        super().draw(canvas)


class ProgressBar(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    # FIXED save engine and send it to next in chain (inherited)

    def draw(self, canvas):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(
                self,
                colors["red"],
                (
                    50, 30, 200 * self.engine.hero.hp /
                    self.engine.hero.max_hp,
                    30
                )
        )
        pygame.draw.rect(
                self,
                colors["green"],
                (50, 70, 200 * self.engine.hero.exp /
                 (100 * (2**(self.engine.hero.level - 1))),
                 30)
        )

        font = pygame.font.SysFont("comicsansms", 26)
        self.blit(font.render(f'Hero at {self.engine.hero.position}',
                  True, colors["black"]), (250, 0))
        self.blit(font.render(f'{self.engine.level} floor',
                  True, colors["black"]), (10, 0))
        self.blit(font.render(f'HP', True, colors["black"]), (10, 30))
        self.blit(font.render(f'Exp', True, colors["black"]), (10, 70))

        self.blit(font.render(
                        f'{self.engine.hero.hp}/{self.engine.hero.max_hp}',
                        True, colors["black"]
                  ),
                  (60, 30))
        self.blit(font.render(
                        f'{self.engine.hero.exp}/'
                        f'{(100*(2**(self.engine.hero.level-1)))}',
                        True, colors["black"]
                  ),
                  (60, 70))
        self.blit(font.render(f'Level', True, colors["black"]), (300, 30))
        self.blit(font.render(f'Gold', True, colors["black"]), (300, 70))
        self.blit(font.render(f'{self.engine.hero.level}',
                  True, colors["black"]), (360, 30))
        self.blit(font.render(f'{self.engine.hero.gold}',
                  True, colors["black"]), (360, 70))
        self.blit(font.render(f'Str', True, colors["black"]), (420, 30))
        self.blit(font.render(f'Luck', True, colors["black"]), (420, 70))

        self.blit(font.render(f'{self.engine.hero.stats["strength"]}',
                  True, colors["black"]), (480, 30))
        self.blit(font.render(f'{self.engine.hero.stats["luck"]}',
                  True, colors["black"]), (480, 70))
        self.blit(font.render(f'SCORE', True, colors["black"]), (550, 30))
        self.blit(font.render(f'{self.engine.score:.4f}',
                  True, colors["black"]), (550, 70))

        # FIXED draw next surface in chain
        super().draw(canvas)


class InfoWindow(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill(colors["green"])
        # size = self.get_size()

        rec_num = (self.engine.info_height - 20) // 18
        thrhold = max(0, len(self.data) - rec_num)
        font = pygame.font.SysFont("comicsansms", 20)
        for i, text in enumerate(self.data):
            if i >= thrhold:
                self.blit(font.render(text, True, colors["black"]),
                                     (5, 20 + 18 * i))

        # FIXED draw next surface in chain
        super().draw(canvas)

    # FIXED set this class as Observer to engine and send it to next in chain
    def connect_engine(self, engine):
        super().connect_engine(engine)
        engine.subscribe(self)


class HelpWindow(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])
    # FIXME You can add some help information

    # FIXED save engine and send it to next in chain (inherited)

    def draw(self, canvas):
        alpha = 0
        if self.engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        # size = self.get_size()
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.engine.show_help:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                              (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, ((128, 128, 255))),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1], True, ((128, 128, 255))),
                          (150, 50 + 30 * i))

        # FIXED draw next surface in chain
        super().draw(canvas)


class GameOver(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = [
            'Game Over',
            "press 'R' to restart the game"
        ]

    def draw(self, canvas):
        alpha = 0
        if self.engine.game_over:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        # size = self.get_size()
        font1 = pygame.font.SysFont("courier", 80)
        font2 = pygame.font.SysFont("serif", 18)

        if self.engine.game_over:
            pygame.draw.lines(self, (255, 0, 0, 255), True,
                              [(0, 0), (700, 0), (700, 500), (0, 500)], 5)
            self.blit(font1.render(self.data[0], True,
                                   ((255, 0, 0))), (130, 120))
            self.blit(font2.render(self.data[1], True,
                                   ((255, 255, 255))), (250, 300))

        super().draw(canvas)
