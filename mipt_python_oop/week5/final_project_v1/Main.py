import pygame
import os
import Objects
import ScreenEngine
import Logic
import Service


#SCREEN_DIM = (1400, 1050)
SCREEN_DIM = (1024, 800)

pygame.init()

video_info = pygame.display.Info()
SCREEN_DIM = (video_info.current_w, video_info.current_h)

gameDisplay = pygame.display.set_mode(SCREEN_DIM)
pygame.display.set_caption("MyRPG")
KEYBOARD_CONTROL = True

if not KEYBOARD_CONTROL:
    import numpy as np
    answer = np.zeros(4, dtype=float)

base_stats = {
    "strength": 20,
    "endurance": 20,
    "intelligence": 5,
    "luck": 5
}


def create_game(sprite_size, is_new):
    global hero, engine, drawer, iteration
    if is_new:
        hero = Objects.Hero(base_stats,
                            Service.create_sprite(
                                    os.path.join("texture", "Hero.png"),
                                    sprite_size))
        engine = Logic.GameEngine()
        Service.service_init(sprite_size)
        Service.reload_game(engine, hero)

        engine.screen_dim = SCREEN_DIM
        engine.info_width = int(SCREEN_DIM[0] * 0.15)
        engine.info_height = SCREEN_DIM[1]
        engine.progress_height = int(SCREEN_DIM[1] * 0.1)
        engine.progress_width = SCREEN_DIM[0] - engine.info_width
        engine.map_height = SCREEN_DIM[1] - engine.progress_height
        engine.map_width = SCREEN_DIM[0] - engine.info_width
        engine.help_height = 500
        engine.help_width = 700

        drawer = ScreenEngine.GameSurface(
                    (engine.map_width, engine.map_height),
                    pygame.SRCALPHA, (0, 0),
                    ScreenEngine.ProgressBar(
                        (engine.progress_width, engine.progress_height),
                        (engine.progress_width, 0),
                        ScreenEngine.InfoWindow(
                            (engine.info_width, engine.info_height),
                            ((engine.map_width - engine.help_width) // 2,
                             (engine.map_height - engine.help_height) // 2),
                            ScreenEngine.HelpWindow(
                                (engine.help_width, engine.help_height),
                                pygame.SRCALPHA,
                                ((engine.map_width - engine.help_width) // 2,
                                 (engine.map_height -
                                 engine.help_height) // 2),
                                ScreenEngine.GameOver(
                                    (engine.help_width, engine.help_height),
                                    pygame.SRCALPHA, (0, 0),
                                    ScreenEngine.ScreenHandle((0, 0))
                                )
                            )
                        )
                    )
        )

    else:
        sh = drawer
        while not isinstance(sh, ScreenEngine.ScreenHandle):
            sh = sh.successor
        sh.fill(ScreenEngine.colors['black'])

        engine.sprite_size = sprite_size
        hero.sprite = Service.create_sprite(
                os.path.join("texture", "Hero.png"),
                sprite_size
        )
        Service.service_init(sprite_size, False)

    Logic.GameEngine.sprite_size = sprite_size

    drawer.connect_engine(engine)

    iteration = 0


size = 60
create_game(size, True)

while engine.working:

    if KEYBOARD_CONTROL:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    engine.show_help = not engine.show_help
                if event.key == pygame.K_KP_PLUS:
                    size = size + 1
                    create_game(size, False)
                if event.key == pygame.K_KP_MINUS:
                    size = size - 1
                    create_game(size, False)
                if event.key == pygame.K_r:
                    create_game(size, True)
                if event.key == pygame.K_ESCAPE:
                    engine.working = False
                if engine.game_over:
                    continue
                if engine.game_process:
                    if event.key == pygame.K_UP:
                        engine.move_up()
                        iteration += 1
                    elif event.key == pygame.K_DOWN:
                        engine.move_down()
                        iteration += 1
                    elif event.key == pygame.K_LEFT:
                        engine.move_left()
                        iteration += 1
                    elif event.key == pygame.K_RIGHT:
                        engine.move_right()
                        iteration += 1
                else:
                    if event.key == pygame.K_RETURN:
                        create_game()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.working = False
        if engine.game_process:
            actions = [
                engine.move_right,
                engine.move_left,
                engine.move_up,
                engine.move_down,
            ]
            answer = np.random.randint(0, 100, 4)
            prev_score = engine.score
            move = actions[np.argmax(answer)]()
            state = pygame.surfarray.array3d(gameDisplay)
            reward = engine.score - prev_score
            print(reward)
        else:
            create_game()

    gameDisplay.blit(drawer, (0, 0))
    drawer.draw(gameDisplay)

    pygame.display.update()

pygame.display.quit()
pygame.quit()
exit(0)
