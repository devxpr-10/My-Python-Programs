import pygame
from UI import Button
from ctypes import windll
from sys import exit

pygame.init()
pygame.font.init()
font = pygame.font.Font("C:\\WINDOWS\\FONTS\\AGENCYB.TTF", 35)

def addDPIAwr():
    try:
        windll.user32.SetProcessDPIAware()
    except:
        pass

idx = 1
mazeSolvable = True
FPS = 60
WIDTH, HEIGHT = 1600, 1080
colors = {
    'disp' : "#000000",
    'block' : "#282727",
    'grid' : '#FFFFFF',
    'dest' : "#E10000",
    'fail' : "#8A0000",
    'path' : "#E1BF0065",
    'init' : "#00B812",
}

distX, distY = 100, 100
gridSize = (WIDTH - distX, HEIGHT - distY)
gridLoc = (distX // 2, distY // 2)

def calculateSizes(mazeDat):
    rows = max(len(md) for md in mazeDat)
    cols = len(mazeDat)

    cellSize = (gridSize[0] // rows, gridSize[1] // cols)
    return rows, cols, cellSize

unsolvableTxt = font.render(f"Unsolvable Maze", True, colors['fail'])
unsolvableTxtX = WIDTH // 2 - unsolvableTxt.get_width() // 2
unsolvableTxtY = HEIGHT - unsolvableTxt.get_height()
modeBTN = Button((distX, 5), (50, 40), ("#000000","#1C1C1C",
                    "#302F2F","#FFFFFF", '#FFFFFF'),font)

def render(disp: pygame.Surface, toggleMode, mazeDat):
    global active_mode, modeBTN
    disp.fill(colors['disp'])
    
    rows, cols, cellSize = calculateSizes(mazeDat)
    cursorX, cursorY = gridLoc[0], gridLoc[1]
    for c in range(cols):
        cursorX = gridLoc[0]
        for r in range(rows):
            match mazeDat[c][r]:
                case '#' : color = colors['block']
                case '*' : color = colors['path']
                case 'A' : color = colors['init']
                case 'B' : color = colors['dest']
                case _ : color = colors['disp']

            pygame.draw.rect(disp, color, [cursorX, cursorY, cellSize[0], cellSize[1]])
            cursorX += cellSize[0]
        cursorY += cellSize[1]

    pygame.draw.rect(disp, colors['grid'], [gridLoc[0], gridLoc[1], 
                                            gridSize[0], gridSize[1]], 1)
    
    # UI
    mazeTxt = font.render(f"Maze {idx}", True, colors['grid'])
    mazeTxtX = WIDTH // 2 - mazeTxt.get_width() // 2

    disp.blit(mazeTxt, (mazeTxtX, 0))
    
    if not mazeSolvable: disp.blit(unsolvableTxt, (unsolvableTxtX, unsolvableTxtY))
    modeBTN.onClick(toggleMode)
    modeBTN.render(disp, active_mode)

def update(mazedata, mode: str):
    global mazeDat, active_mode
    active_mode = mode
    mazeDat = mazedata
    pygame.display.update()

active_mode: str

def initGUI(mazedata: list[str], mode: str, toggleMode, mainEventHandle):
    global mazeDat, active_mode
    active_mode = mode
    mazeDat = mazedata
    addDPIAwr()
    disp = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MAZE")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            mainEventHandle(event)
        render(disp, toggleMode, mazeDat)
        update(mazeDat, active_mode)