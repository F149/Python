import pygame
import random
import math

SCREEN_DIM = (800, 600)

class Vec2d:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def __sub__(self, v):
        return self.x - v.x, self.y - v.y

    def __add__(self, v):
        return v.x + self.x, v.y + self.y

    def __len__(self):
        return int(math.sqrt(self.x * self.x + self.y * self.y))

    def __mul__(self, k):
        return self.x * k, self.y * k

    def __repr__(self):
        return f'x: {self.x}, y: {self.y}'



class Polyline():
    def __init__(self):
        self.points = []
        self.speeds = []
        self.steps = 35

    def draw_points(self, style="points", width=3, color=(255, 255, 255), points=None):
        if points is None:
            points = self.points
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(points[p_n].x), int(points[p_n].y)),
                                 (int(points[p_n + 1].x),
                                  int(points[p_n + 1].y)), width)
        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.x), int(p.y)), width)

class Knot(Polyline):
    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append(Vec2d(Vec2d(self.points[i] + self.points[i + 1]) * 0.5))
            ptn.append(self.points[i + 1])
            ptn.append(Vec2d(Vec2d(self.points[i + 1] + self.points[i + 2]) * 0.5))

            res.extend(self.get_points(ptn))

        self.draw_points("line", 3, color, res)

    def get_points(self, base_points):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return Vec2d(Vec2d(points[deg] * alpha) +
                     Vec2d(self.get_point(points, alpha, deg - 1) * (1 - alpha)))

    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)
        self.get_knot()

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = points[p] + speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = (- self.speeds[p].x, self.speeds[p].y)

            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = (self.speeds[p].x, -self.speeds[p].y)
        self.get_knot()




# Отрисовка справки
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



# Основная программа
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    points_ = Knot()

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
                points_.add_point(Vec2d(event.pos), Vec2d((random.random() * 2,
                                                           random.random() * 2)))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        points_.draw_points()
        points_.get_knot()
        if not pause:
            points_.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
