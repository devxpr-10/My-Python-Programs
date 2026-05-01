import pygame
from os import path, sys
from random import randrange
from ctypes import windll
from time import time

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = path.dirname(path.abspath(__file__))

path_img = path.join(base_path, "assets", "imgs")
path_aud = path.join(base_path, "assets", "auds")

try:
    windll.user32.SetProcessDPIAware()
except:
    pass

pygame.init()
pygame.font.init()
pygame.mixer.init()

# CONSTS & vars

font = pygame.font.SysFont("Calibri",42)
font2 = pygame.font.SysFont("Calibri",70)

collected_flowers = 0
placed_flowers = 0
gameOver = False
gameWon = False
paused = False
started = True
won_played = False

hit_aud = pygame.mixer.Sound(path.join(path_aud, "hit.wav"))
pick_aud = pygame.mixer.Sound(path.join(path_aud, "pick.wav"))
win_aud = pygame.mixer.Sound(path.join(path_aud, "win.wav"))
over_aud = pygame.mixer.Sound(path.join(path_aud, "over.wav"))
place_aud = pygame.mixer.Sound(path.join(path_aud, "place.wav"))
pygame.mixer.music.load(path.join(path_aud, "bg.wav"))
pygame.mixer.music.play(-1)  

icon = pygame.image.load(path.join(path_img, "icon.png"))
pygame.display.set_icon(icon)
pygame.display.set_caption("Jeroo")

t_st,t_en = 14,18
def_timer = randrange(t_st,t_en)
timer = def_timer
start_time = time()
elapsed_time = 0
remaining_time = def_timer

keys = {
    'up' : [pygame.K_UP,pygame.K_w],
    'down' : [pygame.K_DOWN,pygame.K_s],
    'left' : [pygame.K_LEFT,pygame.K_a],
    'right' : [pygame.K_RIGHT,pygame.K_d],
}

colors = {
    "bg" : "#513500",
    "border" : "#1C7700",
    "font1" :"#D4D4D4",
}

go_text = font2.render("Game Over",True,colors["font1"])
paused_text = font.render("Paused",True,colors['font1'])
won_text = font2.render("You Won!",True,colors['font1'])
rst_text_t = "Press 'R' to Restart or 'Q' to Quit"

WIN_WIDTH,WIN_HEIGHT = 1600,1100
FPS = 60

FRAME_WIDTH, FRAME_HEIGHT = WIN_WIDTH - 100, WIN_HEIGHT - 200
FRAME_X, FRAME_Y = WIN_WIDTH // 2 - FRAME_WIDTH // 2, WIN_HEIGHT // 2 - FRAME_HEIGHT // 2
cell_size = FRAME_WIDTH // 20

jeroo = pygame.Surface((cell_size, cell_size))
jeroo_pos = (randrange(FRAME_X,FRAME_WIDTH,cell_size),randrange(FRAME_Y,FRAME_HEIGHT,cell_size))
jeroo_rect = jeroo.get_rect()

jeroo_img = pygame.image.load(path.join(path_img, "Jeroo.png"))
jeroo_img = pygame.transform.scale(jeroo_img, (cell_size, cell_size))

flwr_ticked = pygame.image.load(path.join(path_img, "FlowerTicked.png"))
flwr_ticked = pygame.transform.scale(flwr_ticked, (cell_size, cell_size))

total_flowers = randrange(4,8)
total_enemies = randrange(15,25)

flowers = []
placing_points = []
enemies = []

flower_img = pygame.image.load(path.join(path_img, "Flower.png"))
flower_img = pygame.transform.scale(flower_img, (cell_size, cell_size))

enemy_img = pygame.image.load(path.join(path_img, "Net.png"))
enemy_img = pygame.transform.scale(enemy_img, (cell_size, cell_size))

point_img = pygame.image.load(path.join(path_img, "Point.png"))
point_img = pygame.transform.scale(point_img, (cell_size, cell_size))

for _ in range(0,total_flowers):
    flowers.append([pygame.Surface((cell_size, cell_size)),(randrange(FRAME_X,FRAME_WIDTH,cell_size),randrange(FRAME_Y,FRAME_HEIGHT,cell_size))])
for _ in range(0,total_flowers):
    placing_points.append([pygame.Surface((cell_size, cell_size)),(randrange(FRAME_X,FRAME_WIDTH,cell_size),randrange(FRAME_Y,FRAME_HEIGHT,cell_size)),0])
for _ in range(total_enemies):
    while True:
        pos = (randrange(FRAME_X, FRAME_WIDTH, cell_size), randrange(FRAME_Y, FRAME_HEIGHT, cell_size))
        occupied = any(pos == f[1] for f in flowers
        ) or any(pos == p[1] for p in placing_points
        ) or any(pos == e[1] for e in enemies) or pos == jeroo_pos
        if not occupied:
            enemies.append([pygame.Surface((cell_size, cell_size)), pos])
            break

global win
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Jeroo")

def draw():
    win.fill(colors["bg"])
    
    #----- Texts -----#
    win.blit(font.render(f"Flowers Collected: {collected_flowers}", True, colors['font1']), (55, 20))
    timer_txt = font.render(f"Remaining Time: {remaining_time}", True, colors['font1'])
    win.blit(timer_txt, (WIN_WIDTH//2-timer_txt.get_size()[0]//2, 20))
    if paused: win.blit(paused_text, (WIN_WIDTH-160, 20))

    #----- Grid -----#
    pygame.draw.rect(win, colors['border'], (FRAME_X, FRAME_Y, FRAME_WIDTH, FRAME_HEIGHT), 5)
    for i in range(FRAME_X + cell_size, FRAME_X + FRAME_WIDTH, cell_size):
        pygame.draw.line(win, colors["border"], (i, FRAME_Y), (i, FRAME_Y + FRAME_HEIGHT), 2)
    for j in range(FRAME_Y + cell_size, FRAME_Y + FRAME_HEIGHT, cell_size):
        pygame.draw.line(win, colors["border"], (FRAME_X, j), (FRAME_X + FRAME_WIDTH, j), 2)

    #----- Placing Points -----#
    for point in placing_points:
        if point[2] == 0:
            win.blit(point_img,point[1])
        else:
            win.blit(flwr_ticked,point[1])

    #----- Enemies -----#
    for enemy in enemies:
        win.blit(enemy_img,enemy[1])

    #----- Flowers -----#
    for flower in flowers:
        win.blit(flower_img,flower[1])

    #----- Jeroo -----#
    win.blit(jeroo_img, jeroo_pos)
    pygame.display.update()

def drawOver():
    win.fill(colors["bg"])
    rst_text = font.render(rst_text_t,True,colors['font1'])
    txt = font.render("Press 'R' to restart or 'Q' to quit",True,colors['font1'])
    win.blit(go_text,(WIN_WIDTH//2-go_text.get_size()[0]//2,WIN_HEIGHT//2-150))
    win.blit(rst_text,(WIN_WIDTH//2-rst_text.get_size()[0]//2,WIN_HEIGHT//2-70))
    win.blit(txt,(WIN_WIDTH//2-txt.get_size()[0]//2,WIN_HEIGHT//2-10))
    pygame.display.update()

def drawWin():
    win.fill(colors["bg"])
    txt = font.render("Press 'R' to restart or 'Q' to quit",True,colors['font1'])
    win.blit(won_text,(WIN_WIDTH//2-won_text.get_size()[0]//2,WIN_HEIGHT//2-150))
    win.blit(txt,(WIN_WIDTH//2-txt.get_size()[0]//2,WIN_HEIGHT//2-10))
    pygame.display.update()

def jeroo_move(dir_x=0, dir_y=0):
    """Use 1,-1,0"""
    global jeroo_pos, cell_size, paused
    if not paused:
        jeroo_pos = (jeroo_pos[0]+dir_x*cell_size,jeroo_pos[1]+dir_y*cell_size) 
    else: 
        jeroo_pos = jeroo_pos

def reset():
    global gameOver,paused,started,jeroo_pos,jeroo_rect,total_flowers,total_enemies,enemies,flowers,placing_points,collected_flowers,timer,gameWon,placed_flowers,def_timer,remaining_time,elapsed_time,current_time,start_time,won_played
    gameOver = False
    started = True
    paused = False
    gameWon = False
    won_played = False
    collected_flowers,timer = 0, def_timer
    placed_flowers = 0
    jeroo_pos = (randrange(FRAME_X,FRAME_WIDTH,cell_size),randrange(FRAME_Y,FRAME_HEIGHT,cell_size))
    jeroo_rect = jeroo.get_rect()

    pygame.mixer.music.play(-1)

    enemies = []
    flowers = []
    placing_points = []
    
    timer = randrange(t_st,t_en)
    def_timer = timer
    start_time = time()
    elapsed_time = 0
    remaining_time = def_timer
    
    total_flowers = randrange(4,8)
    total_enemies = randrange(15,25)

    for _ in range(0,total_flowers):
        flowers.append([pygame.Surface((cell_size, cell_size)),(randrange(FRAME_X,FRAME_WIDTH,cell_size),randrange(FRAME_Y,FRAME_HEIGHT,cell_size))])
    for _ in range(0,total_flowers):
        placing_points.append([pygame.Surface((cell_size, cell_size)),(randrange(FRAME_X,FRAME_WIDTH,cell_size),randrange(FRAME_Y,FRAME_HEIGHT,cell_size)),0])
    for _ in range(total_enemies):
        while True:
            pos = (randrange(FRAME_X, FRAME_WIDTH, cell_size), randrange(FRAME_Y, FRAME_HEIGHT, cell_size))
            occupied = any(pos == f[1] for f in flowers
            ) or any(pos == p[1] for p in placing_points
            ) or any(pos == e[1] for e in enemies) or pos == jeroo_pos
            if not occupied:
                enemies.append([pygame.Surface((cell_size, cell_size)), pos])
                break

def main():
    running = True
    global paused, gameOver, started, jeroo_img, elapsed_time, start_time, remaining_time, gameWon, rst_text_t, won_played
    flipped = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key in keys['up'] and jeroo_pos[1] > FRAME_Y:
                    jeroo_move(0,-1)
                if event.key in keys['down'] and jeroo_pos[1] < FRAME_HEIGHT:
                    jeroo_move(0,1)
                if event.key in keys['left'] and jeroo_pos[0] > FRAME_X:
                    jeroo_move(-1,0)
                    if not flipped and not paused: 
                        jeroo_img = pygame.transform.flip(jeroo_img, True, False)
                        flipped = True
                if event.key in keys['right'] and jeroo_pos[0] < FRAME_WIDTH  - cell_size:
                    jeroo_move(1,0)
                    if flipped and not paused: 
                        jeroo_img = pygame.transform.flip(jeroo_img, True, False)
                        flipped = False
                if event.key == pygame.K_ESCAPE and not gameOver:
                    paused = not paused
                    if paused:
                        pause_start = time()
                        pygame.mixer.music.pause()
                    else:
                        start_time += time() - pause_start
                        pygame.mixer.music.unpause()
                if event.key == pygame.K_q and paused:
                    running = False
                    break
                if event.key == pygame.K_r and paused:
                    reset()

        if started:
            draw()
            if not paused:
                current_time = time()
                elapsed_time = current_time - start_time
                remaining_time = max(0, timer - int(elapsed_time)) 

            jeroo_rect.topleft = jeroo_pos
            global collected_flowers, placed_flowers
            for flower in flowers:
                flwr_rect = flower[0].get_rect(topleft=flower[1])
                if jeroo_rect.colliderect(flwr_rect):
                    flowers.remove(flower)
                    collected_flowers += 1
                    pick_aud.play()
            for point in placing_points:
                point_rect = point[0].get_rect(topleft=point[1])
                if jeroo_rect.colliderect(point_rect) and (placing_points[placing_points.index(point)][2] == 0):
                    if collected_flowers > 0:
                        placing_points[placing_points.index(point)][2] = 1
                        collected_flowers -= 1
                        placed_flowers += 1
                        place_aud.play()
            for enemy in enemies:
                enemy_rect = enemy[0].get_rect(topleft=enemy[1])
                if jeroo_rect.colliderect(enemy_rect) or remaining_time <= 0:
                    over_aud.play()
                    pygame.mixer.music.pause()
                    rst_text_t = "You couldn't complete in time" if remaining_time <= 0 else "Jeroo hit a net"
                    gameOver = True
                    started = False
                    paused = True

        if placed_flowers == len(placing_points):
            gameWon = True
            started = False
            paused = True
        

        if gameWon:
            if not won_played:
                pygame.mixer.music.pause()
                win_aud.play()
            won_played = True
            drawWin()
            
        elif gameOver and not started:
            drawOver()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()