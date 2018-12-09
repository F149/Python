# V1
import pygame
import random
import math

SCREEN_DIM = (800, 600)


# ÐœÐµÑ‚Ð¾Ð´Ñ‹ Ð´Ð»Ñ Ñ€Ð°Ð±Ð¾Ñ‚Ñ‹ Ñ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð°Ð¼Ð¸

class Vec2d:
    def __init__(self, x: list):
        self.x = x

    def __add__(self, other):
        return Vec2d([self.x[0] + other.x[0], self.x[1] + other.x[1]])

    def __sub__(self, other):
        return Vec2d([self.x[0] - other.x[0], self.x[1] - other.x[1]])

    def __len__(self):
        return math.sqrt(self.x[0] * self.x[0] + self.x[1] * self.x[1])

    def __mul__(self, other):
        if type(other) == Vec2d:
            return self.x[0] * other.x[0] + self.x[1] * other.x[1]
        return Vec2d([self.x[0] * other, self.x[1] * other])

    def __getitem__(self, item):
        return self.x[item]

    def int_pair(self) -> tuple:
        return self.x[0], self.x[1]


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []
        self.for_draw = []

    def addPoint(self, point, speed):
        self.points.append(Vec2d(point))
        self.for_draw.append(Vec2d(point))
        self.speeds.append(Vec2d(speed))

    # "ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ°" Ñ‚Ð¾Ñ‡ÐµÐº
    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            points = self.for_draw
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, (int(points[p_n][0]), int(points[p_n][1])),
                                 (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p[0]), int(p[1])), width)

    # ÐŸÐµÑ€ÑÑ‡Ð¸Ñ‚Ñ‹Ð²Ð°Ð½Ð¸Ðµ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ Ð¾Ð¿Ð¾Ñ€Ð½Ñ‹Ñ… Ñ‚Ð¾Ñ‡ÐµÐº
    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = (- self.speeds[p][0], self.speeds[p][1])
            if \
                    self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = (self.speeds[p][0], -self.speeds[p][1])


class Knot(Polyline):
    def addPoint(self, point, speed, count):
        super(Knot, self).addPoint(point, speed)
        self._count = count
        self._get_knot()

    def _get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + (self._get_point(points, alpha, deg - 1) * (1 - alpha))

    def _get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self._get_point(base_points, i * alpha))
        return res

    def _get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append(((self.points[i] + self.points[i + 1]) * 0.5))
            ptn.append(self.points[i + 1])
            ptn.append(((self.points[i + 1] + self.points[i + 2]) * 0.5))

            res.extend(self._get_points(ptn, self._count))
        self.for_draw = res


# ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ° ÑÐ¿Ñ€Ð°Ð²ÐºÐ¸
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# ÐžÑÐ½Ð¾Ð²Ð½Ð°Ñ Ð¿Ñ€Ð¾Ð³Ñ€Ð°Ð¼Ð¼Ð°
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True

    knot = Knot()
    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.addPoint(event.pos, (random.random() * 2, random.random() * 2), steps)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        knot.draw_points()
        knot.draw_points("line", 3, color)
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)

##########################################
# V2
import pygame
import random
import math

SCREEN_DIM = (800, 600)



class Vec2d:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, vector):
        return Vec2d(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector):
        return self.x - vector.x, self.y - vector.y

    def __mul__(self, k):
        if isinstance(k, Vec2d):
            return self.x * k.x + self.y * k.y
        else:
            return Vec2d(self.x * k, self.y * k)

    def len(self, x):
        return (x.x ** 2 + x.y ** 2) ** 0.5

    def vec(self, start, end):  # ÑÐ¾Ð·Ð´Ð°Ð½Ð¸Ðµ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð° Ð¿Ð¾ Ð½Ð°Ñ‡Ð°Ð»Ñƒ (x) Ð¸ ÐºÐ¾Ð½Ñ†Ñƒ (y) Ð½Ð°Ð¿Ñ€Ð°Ð²Ð»ÐµÐ½Ð½Ð¾Ð³Ð¾ Ð¾Ñ‚Ñ€ÐµÐ·ÐºÐ°
        return Vec2d(start[0] - end[0], start[1] - end[1])

    def int_pair(self):
        return (int(self.x), int(self.y))

    def __str__(self):
        return str((self.x, self.y))


class Polyline:

    def __init__(self):
        self.points = []
        self.speeds = []

    # "Ð”Ð¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¸Ðµ" Ñ‚Ð¾Ñ‡ÐµÐº
    def add_points(self, pos):
        self.points.append(Vec2d(pos[0], pos[1]))
        self.speeds.append(Vec2d(random.random() * 2, random.random() * 2))

    # Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ Ñ‚Ð¾Ñ‡ÐµÐº
    def del_point(self, pos):
        len = max(SCREEN_DIM[0], SCREEN_DIM[1])
        if self.points != []:
            for point in self.points:
                if point.len(point.vec(pos, point.int_pair())) < len:
                    len = point.len(point.vec(pos, point.int_pair()))
                    point_to_del = point
            ind = self.points.index(point_to_del)
            del self.points[ind]
            del self.speeds[ind]

    # "ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ°" Ñ‚Ð¾Ñ‡ÐµÐº
    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color, self.points[p_n].int_pair(),
                                 self.points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)

    # ÐŸÐµÑ€ÑÑ‡Ð¸Ñ‚Ñ‹Ð²Ð°Ð½Ð¸Ðµ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ Ð¾Ð¿Ð¾Ñ€Ð½Ñ‹Ñ… Ñ‚Ð¾Ñ‡ÐµÐº
    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(-self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)



class Knot(Polyline):
    def __init__(self, steps):
        super().__init__()
        self.steps = steps
        self.res = []

    def add_point(self, pos):
        super().add_points(pos)
        self.get_knot(self.steps)

    def del_point(self, pos):
        super().del_point(pos)
        self.get_knot(self.steps)

    def set_points(self):
        super().set_points()
        self.get_knot(self.steps)

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.res) - 1):
                pygame.draw.line(gameDisplay, color, self.res[p_n].int_pair(),
                                 self.res[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)

    def get_knot(self, count):
        if len(self.points) < 3:
            self.res = []
            return self.res
        self.res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            self.res.extend(self.get_points(ptn, count))
        return self.res

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res


# ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ° ÑÐ¿Ñ€Ð°Ð²ÐºÐ¸
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["LeftMouse", "Add point"])
    data.append(["RightMouse", "Del point"])
    data.append(["Key 1-9", "To sellect needed curve"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

# ÐžÑÐ½Ð¾Ð²Ð½Ð°Ñ Ð¿Ñ€Ð¾Ð³Ñ€Ð°Ð¼Ð¼Ð°
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True

    show_help = False
    pause = True
    index = 0
    lines = [Knot(steps) for i in range(9)]

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key in range(49, 58):
                    index = event.key - 49
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    lines = [Knot(steps) for i in range(9)]
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    lines[index].steps -= 1 if lines[index].steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    lines[index].add_point(event.pos)
                elif event.button == 3:
                    lines[index].del_point(event.pos)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        for line in lines:
            if line == lines[index]:
                line.draw_points("line", 3)
                line.draw_points(color=(255, 0, 32))
            else:
                line.draw_points("line", 3, color)
                line.draw_points()
            if not pause:
                line.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
########################################
# V3
import pygame
import random

SCREEN_DIM = (800, 600)


class Vec2d:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        return (self.x**2 + self.y**2)**0.5

    def __add__(self, other):
        return Vec2d(self.x + other.x,  self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x * other.x, self.y * other.y)
        return Vec2d(self.x * other, self.y * other)

    def int_pair(self):
        return int(self.x), int(self.y)

    @classmethod
    def vec(cls, x, y):
        return Vec2d(y[0] - x[0], y[1] - x[1])

    def __str__(self):
        return f"({self.x}; {self.y})"

    def __repr__(self):
        return self.__str__()


class Polyline:

    def __init__(self):
        self.points = list()
        self.speeds = list()

    def insert(self, vec, speed):
        self.points.append(Vec2d(*vec))
        self.speeds.append(Vec2d(*speed))

    def rem_last(self):
        if len(self.points) and len(self.speeds) and \
                len(self.points) == len(self.speeds):
            self.points.pop()
            self.speeds.pop()

    @staticmethod
    def filter_points(array, indexes):
        res = [array[i] for i in range(len(array))
               if i not in indexes]
        return res

    def delete_points(self, indexes):
        self.points = Polyline.filter_points(self.points, indexes)
        self.speeds = Polyline.filter_points(self.speeds, indexes)

    def set_points(self, screen_dim):
        for p in range(len(self.speeds)):
            self.points[p] += self.speeds[p]
            if self.points[p].x > screen_dim[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(-self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > screen_dim[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, points=None, width=3, color=(255, 255, 255)):
        points = points or self.points
        for p in points:
            pygame.draw.circle(gameDisplay, color,
                               p.int_pair(), width)


class Knot(Polyline):

    def __init__(self, steps):
        super().__init__()
        self.steps = steps

    def insert(self, point, speed):
        super().insert(point, speed)

    def set_points(self, screen_dim):
        super().set_points(screen_dim)

    def rem_last(self):
        super().rem_last()

    def delete_points(self, indexes):
        super().delete_points(indexes)

    def inc_steps(self):
        self.steps += 1

    def dec_steps(self):
        self.steps -= 1 if self.steps > 1 else 0

    def speed_change(self, inc=True):
        for i in range(len(self.speeds)):
            self.speeds[i] *= 1.1 if inc else 0.9

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = [
                (self.points[i] + self.points[i + 1]) * 0.5,
                self.points[i + 1],
                (self.points[i + 1] + self.points[i + 2]) * 0.5
            ]
            res.extend(self.get_points(ptn))
        return res

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.steps
        return [self.get_point(base_points, i * alpha) for i in range(self.steps)]

    def draw_points(self, points=None, width=3, color=(255, 255, 255)):
        super().draw_points()
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color,
                             (points[p_n].int_pair()),
                             (points[p_n + 1].int_pair()), width)


# ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ° ÑÐ¿Ñ€Ð°Ð²ÐºÐ¸
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = list()
    data.append(["0", "Make slower"])
    data.append(["1", "Make faster"])
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["3", "Start to add many points. Press E to finish"])
    data.append(["E", "Finish adding many points"])
    data.append(["D", "Delete amount of points."])
    data.append(["", "Insert indexes(0 1 2...) of deleted points into console in one row."])
    data.append(["", "Separate them with space"])
    data.append(["Delete", "Remove last point"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current steps"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# ÐžÑÐ½Ð¾Ð²Ð½Ð°Ñ Ð¿Ñ€Ð¾Ð³Ñ€Ð°Ð¼Ð¼Ð°
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    speed = 2
    working = True
    show_help = False
    pause = True
    knot = Knot(steps)
    hue = 0
    color = pygame.Color(0)

    while working:
        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knot = Knot(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    knot.inc_steps()
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    knot.dec_steps()
                if event.key == pygame.K_0:
                    knot.speed_change(False)
                if event.key == pygame.K_1:
                    knot.speed_change(True)
                if event.key == pygame.K_DELETE:
                    knot.rem_last()
                if event.key == pygame.K_d:
                    points_for_delete = map(int, input("Which points to delete: ").split())
                    knot.delete_points(points_for_delete)
                if event.key == pygame.K_3:
                    sub_working = True
                    while sub_working:
                        for sub_event in pygame.event.get():
                            if sub_event.type == pygame.KEYDOWN:
                                if sub_event.key == pygame.K_e:
                                    sub_working = False
                            if sub_event.type == pygame.MOUSEBUTTONDOWN:
                                tmp = (sub_event.pos, (random.random() * speed, random.random() * speed))
                                knot.insert(*tmp)
            if event.type == pygame.MOUSEBUTTONDOWN:
                tmp = (event.pos, (random.random() * speed, random.random() * speed))
                knot.insert(*tmp)
        knot.draw_points(knot.get_knot(), color=color)
        if not pause:
            knot.set_points(SCREEN_DIM)
        if show_help:
            draw_help()
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)

