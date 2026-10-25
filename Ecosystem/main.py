from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

''''''''''''''''''''''''''''''
import pygame
from objects import *
from methods import *
from ctypes import windll
''''''''''''''''''''''''''''''

try:
    windll.user32.SetProcessDPIAware()
except:
    pass

pygame.init()

### CONSTS AND VARS

WIDTH, HEIGHT = 1600, 1080
title = "ECOSYSTEM"
clock = pygame.time.Clock()
FPS = 60
colors = {
    'window':'#000000',
}

load_data()

def update(delta: float, WIDTH, HEIGHT) -> None:
    update_objects(delta, WIDTH, HEIGHT)

def render(window: pygame.Surface) -> None:
    window.fill(colors['window'])
    render_objects(window)

    pygame.display.flip()

last_spawn = 0
delay = 0

def main():
    global last_spawn, delay
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(title)
    running = True

    while running:
        delta = clock.tick(FPS) / 1000

        m_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data()
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_u:
                        add_unit(m_pos[0], m_pos[1])
                    case pygame.K_r:
                        add_resource(m_pos[0], m_pos[1], False)
                    case pygame.K_f:
                        add_resource(m_pos[0], m_pos[1], True)
                    case pygame.K_SPACE:
                        add_resources(WIDTH, HEIGHT)

        update(delta, WIDTH, HEIGHT)
        render(window)

    pygame.quit()

if __name__ == '__main__':
    main()