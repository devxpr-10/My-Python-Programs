import gui
from approach import *

def readFile(number: int = 1) -> list[str]:
    with open(f'maze{number}.txt', 'r') as file:
        return file.read().split('\n')

def updateMazeDat(pathway: list[tuple]) -> None:
    global mazeDat
    tempDat = [list(row) for row in mazeDat]
    for x, y in pathway:
        tempDat[x][y] = '*'
    mazeDat = [''.join(row) for row in tempDat]

modes: str = ['DFS', 'BFS']
curr_mode: int = 0

def toggleMode():
    global modes, curr_mode
    curr_mode += 1
    curr_mode = 0 if curr_mode > len(modes) - 1 else curr_mode
    loadSolvedMaze(modes[curr_mode])
    gui.update(mazeDat, modes[curr_mode])

def mainEventHandle(event) -> None:
    if event.type == gui.pygame.KEYDOWN:
        if event.key == gui.pygame.K_RIGHT:
            updateIndex(1)
            loadSolvedMaze()
            gui.update(mazeDat, modes[curr_mode])
        if event.key == gui.pygame.K_LEFT:
            updateIndex(-1)
            loadSolvedMaze()
            gui.update(mazeDat, modes[curr_mode])
        if event.key == gui.pygame.K_s:
            toggleMode()

index = 1

def updateIndex(dir) -> None:
    """Updates index by clamping it"""
    global index
    index += 1 * dir
    index = max(1, min(index, 5))
    gui.idx = index

def loadSolvedMaze(mode = 'BFS'):
    """Loads the maze into 'mazeDat' and then updates it for solved pathways"""
    global mazeDat
    gui.mazeSolvable = True
    mazeDat = readFile(index)
    # print("Unsolved Maze:\n" +'\n'.join(mazeDat))
    if (pathway := solve(mazeDat, mode)) == None:
        gui.mazeSolvable = False
        print("Maze Unsolvable")
        return
    updateMazeDat(pathway)
    # print("Solved Maze:\n" +'\n'.join(mazeDat))

def main():
    global modes, curr_mode
    loadSolvedMaze()
    gui.initGUI(mazeDat, modes[curr_mode], toggleMode, mainEventHandle)

if __name__ == "__main__":
    main()