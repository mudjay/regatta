import pygame
import numpy as np
from common import *
from network import Network
import csv

boardSize = (0, 0)
blockSize = 20
borderSize = 2


def draw_asset(asset, centre, scale=1.0, rotation=0.0, colour=colours['black'], lineWidth=0, boundingBox=None):
    def scale2fit(asset, boundingBox):
        assetSize = (max([vertex[0] for vertex in asset]) - min([vertex[0] for vertex in asset]),
                     max([vertex[1] for vertex in asset]) - min([vertex[1] for vertex in asset]))
        scales = (boundingBox[0] / assetSize[0], boundingBox[1] / assetSize[1])
        return min(scales)

    imgOut = []
    rotImg = []
    rotMatrix = np.array([[np.cos(rotation), -np.sin(rotation)],  # rotation matrix
                          [np.sin(rotation), np.cos(rotation)]])
    if boundingBox is not None:
        scale = scale2fit(asset, boundingBox)
    for vertex in asset:
        imgOut.append(np.add(rotMatrix.dot(vertex) * scale, centre))
    pygame.draw.polygon(window, colour, imgOut, width=lineWidth)


def create_map(file):
    global boardSize #! do something about this
    terrainKey = {'0': 'sea',
                  '1': 'land',
                  '2': 'buoy'
                  }
    with open(file, newline='') as f:
        reader = csv.reader(f)
        terrain = list(reader)
    boardSize = [len(terrain[0]), len(terrain)]
    board = []
    for x in range(boardSize[0]):   #! using list comprehension would be nicer
        board.append([])
        for y in range(boardSize[1]):
            board[x].append([terrainKey[terrain[y][x]]])
    return board


def draw_board():
    global window

    def coord2pixel(pos, corner='topLeft'):
        switch = {'topLeft': (pos[0] * (blockSize + borderSize) + borderSize, pos[1] * (blockSize + borderSize) + borderSize),
                  'centre':  ((pos[0] + 0.5)*blockSize + (pos[0] + 1)*borderSize, (pos[1] + 0.5)*blockSize + (pos[1] + 1)*borderSize)
                  }
        return switch[corner]

    def draw_terrain(start=(0, 0), end=boardSize):
        for x in range(start[0], end[0]):
            for y in range(start[1], end[1]):
                rect = pygame.Rect(coord2pixel((x, y)), (blockSize, blockSize))
                pygame.draw.rect(window, colours[terrain[x][y][0]], rect)

    def draw_boats(flotilla):
        #! should handle boats as objects
        # draw all blankets first to prevent overdrawing
        for boat in flotilla:
            blankets = [tuple(map(lambda x, y: x - y, boat, point2vec[wind]))]
            # if boat.spinnaker:
            #     blankets.append(tuple(map(lambda x, y: x - y, blankets[0], point2vec[wind])))
            for pos in blankets:
                rect = pygame.Rect(coord2pixel(pos), (blockSize, blockSize))
                pygame.draw.rect(window, colours['blanketed'], rect)
        for boat in flotilla:
            draw_asset(assets['boat'], coord2pixel(boat, 'centre'), boundingBox=[blockSize-3]*2)
        # for boat in flotilla:
        #     draw_asset(assets['boat'], coord2pixel(boat.pos, 'centre'), rotation=boat.heading, colour= boat.colour )

    def draw_buoys(buoys):  #! doesn't really need to be a function
        for buoy in buoys:
            draw_asset(assets['buoy'], coord2pixel(buoy, 'centre'), boundingBox=[blockSize - 5]*2, colour=colours['buoy'])

    draw_terrain()
    wind = 7
    draw_boats([(0, 10), (1, 11), (2, 12)])
    draw_buoys([(0, 0), (1, 1), (2, 2)])


def threaded_listen():
    pass
    # listen for updates


def main():
    run = True
    if n.connected:
        draw_board()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    draw_board()
            pygame.display.update()
    else:
        print("could not connect")
    threaded_listen()


########################################################################################################################
pygame.init()
n = Network()
clientID = n.connect()
if n.connected:
    print('connected')
    n.send('join', 0)
    print('DEBUG: joined')
    # get initial values
    print('DEBUG: get mapPath')
    mapPath = n.send('get', 'mapPath')
    print(mapPath)
    print('DEBUG: get boats')
    boats = n.send('get', 'boats')
    print('DEBUG: get buoys')
    buoys = n.send('get', 'buoys')
    print('DEBUG: get wind')
    wind = n.send('get', 'wind')
    # ^collate this into one get request
    print('DEBUG: make terrain')
    terrain = create_map(mapPath)
    window = pygame.display.set_mode(tuple(i * (blockSize + borderSize) + borderSize for i in boardSize))
    pygame.display.set_caption("boardViewer")
    window.fill(colours['viewerBackground'])
    main()


# pygame.init()
# terrain = create_map('boards/testMap.csv')
# boats = {}
# buoys = {}
# window = pygame.display.set_mode(tuple(i * (blockSize + borderSize) + borderSize for i in boardSize))
# pygame.display.set_caption("boardViewer")
# window.fill(colours['viewerBackground'])
# main()


# listen for updates
# if update:
#     draw board
#     draw players
