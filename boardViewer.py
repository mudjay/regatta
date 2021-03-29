import pygame
import numpy as np
from game import colours
import csv

boardSize = [0, 0]
blockSize = 20
borderSize = 2

################
# for testing only
def create_map(file):
    global boardSize #! do something about this
    terrainKey = {'0': 'sea',
                  '1': 'land',
                  '2': 'bouy'
                  }
    with open(file, newline='') as f:
        reader = csv.reader(f)
        terrain = list(reader)
    boardSize = [len(terrain[0]), len(terrain)]
    board = []
    for x in range(boardSize[0]):   #! using list comprehension would be nicer
        board.append([])
        for y in range(boardSize[1]):
            if terrainKey[terrain[y][x]] == 'bouy':
                board[x].append(['sea', terrainKey[terrain[y][x]], None])
            else:
                board[x].append([terrainKey[terrain[y][x]], None, None])
    return board
################

def draw_asset(asset, centre, scale, rotation, colour, lineWidth):
    imgOut = []
    rotImg = []
    rotMatrix = np.array([[np.cos(rotation), -np.sin(rotation)],  # rotation matrix
                          [np.sin(rotation), np.cos(rotation)]])
    for vertex in asset:
        imgOut.append(np.add(rotMatrix.dot(vertex) * scale, centre))
    pygame.draw.polygon(window, colour, imgOut, width=lineWidth)


def draw_board(board):
    global window
    for x in range(boardSize[0]):
        for y in range(boardSize[1]):
            gridCentre = ((x + 0.5)*blockSize, (y + 0.5)*blockSize)
            topCorner = [x * (blockSize + borderSize) + borderSize, y * (blockSize + borderSize) + borderSize]
            # draw terrain
            rect = pygame.Rect(topCorner[0], topCorner[1], blockSize, blockSize)
            pygame.draw.rect(window, colours[board[x][y][0]], rect)

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        draw_board(board)
        pygame.display.update()
        #listen for updates


board = create_map('boards/testMap.csv')
pygame.init()
window = pygame.display.set_mode(tuple(i * (blockSize + borderSize) + borderSize for i in boardSize))
pygame.display.set_caption("boardViewer")
window.fill(colours['grey'])
main()


# listen for updates
# if update:
#     draw board
#     draw players
