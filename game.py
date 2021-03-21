import pygame
import numpy as np
import csv
import random

#########################
# TO FIX
# - constantly drawing console, so constantly making paths etc, make more efficient
# - check when board is drawn, should be only after moves
# - tails
# - make board a class?
# - better way of talking to the buttons
#########################

# compass point: vector
point2vec = {0: (0, -1),
             1: (1, -1),
             2: (1, 0),
             3: (1, 1),
             4: (0, 1),
             5: (-1, 1),
             6: (-1, 0),
             7: (-1, -1)
             }
#   relative point: spaces moved
point2sailing = {0: 0,
                 1: 1,
                 2: 2,
                 3: 3,
                 4: 2,
                 5: 3,
                 6: 2,
                 7: 1
                 }


boardSize = (30, 24) #! should be set by create map
def create_map(file):
    global boardSize #! do something about this
    terrainKey = {'0': 'sea',
                  '1': 'land',
                  '2': 'bouy'
                  }
    with open(file, newline='') as f:
        reader = csv.reader(f)
        terrain = list(reader)
    boardSize = (len(terrain[0]), len(terrain))
    board = []
    for x in range(boardSize[0]):   #! using list comprehension would be nicer
        board.append([])
        for y in range(boardSize[1]):
            if terrainKey[terrain[y][x]] == 'bouy':
                board[x].append(['sea', terrainKey[terrain[y][x]], None])
            else:
                board[x].append([terrainKey[terrain[y][x]], None, None])
    return board


# graphics variables
blockSize = 20
boardOffset = 5
consoleWidth = 400
consoleOrigin = (boardSize[0] * blockSize + 2 * boardOffset, boardOffset)
winSize = (boardSize[0] * blockSize + 2 * boardOffset + consoleWidth, boardSize[1] * blockSize + 2 * boardOffset)

colours = {'sea': (80, 180, 255),
           'land': (20, 100, 40),
           'bouy': (255, 0, 0),
           'cboat': (255, 255, 255),
           'sfline': (135, 135, 135),
           'boat1': (0, 255, 0),
           'grey': (10, 120, 120),
           'btnEnabled': (0, 0, 0),
           'btnDisabled': (70, 70, 70),
           'black': (0, 0, 0),
           'tail': (0, 200, 0),
           'blanketed': (64, 144, 204)
           }
assets = {'windArrow': [(0, -64), (15, -40), (15, 40), (-15, 40), (-15, -40)]
          }


class player:
    def __init__(self, pos, tack):
        # self.x = x
        # self.y = y
        self.pos = pos
        self.colour = (0, 255, 0)
        self.spinnaker = False
        self.tack = tack
        self.heading = 0
        self.legCounter = 0
        board[self.pos[0]][self.pos[1]][1] = 'boat1'

    def move(self, point):
        self.heading = point
        print(point)
        start = self.pos
        end = move(p.pos, wind, point, p)
        # print(make_path(self.pos, end, 'move'))
        board[self.pos[0]][self.pos[1]][1] = None
        self.pos = end
        board[self.pos[0]][self.pos[1]][1] = 'boat1'
        draw_board()
        # #tails
        # for pos in make_path(start, end, 'tail'):
        #     rect = pygame.Rect(pos[0] * blockSize + boardOffset + 1, pos[1] * blockSize + boardOffset + 1, 22,
        #                       22)
        #     pygame.draw.rect(window, colours['boat1'], rect)

        # #blanketed square
        # blanket = tuple(map(lambda x : -x, point2vec[wind]))
        # board[self.x + blanket[0]][self.y - blanket[1]][2] = 'tail'
        # print(blanket)

        # sailPoint = arg2sailing[
        #     proper_arg(card2point[dir] - card2point[wind])]  # ! surely theres some neater way of doing this???
        # if self.spinnaker:
        #     if sailPoint >= 2:
        #         sailPoint += 1
        #     else:
        #         sailPoint = 0
        # board[self.pos] = 'sea'
        # self.pos = tuple(map(lambda x, y: x + y, self.pos, tuple([sailPoint * i for i in card2vec[dir]])))
        # board[self.pos] = 'boat1'


def move(start, wind, point, player):
    relativeWind = (point - wind) % 8
    vec = point2vec[point]
    vecSail = tuple(i * point2sailing[relativeWind] for i in vec)
    if player.spinnaker:
        vecSail = tuple(map(lambda x, y : x + y, vecSail, vec))
    end = tuple(map(lambda x, y: x + y, start, vecSail))
    return end


def valid_points(wind, boat):
    validPoints = [] # true directions
    sailablePoints = [] # sail points relative to wind
    # if p.legCounter == legs:
    #     print('out of legs')
    #     return  validPoints
    # else:
    if board[boat.pos[0]][boat.pos[1]][2] == 'blanketed' or boat.heading == wind:
        return validPoints
    else:
        if boat.tack == 'P':
            if boat.spinnaker:
                sailablePoints = [3, 4]
            else:
                sailablePoints = [1, 2, 3, 4]
        if boat.tack == 'S':
            if boat.spinnaker:
                sailablePoints = [5, 4]
            else:
                sailablePoints = [7, 6, 5, 4]
        for relativeWind in sailablePoints:
            truePoint = (relativeWind + wind) % 8
            if valid_path(boat.pos, move(boat.pos, wind, truePoint, boat)):
               validPoints.append(truePoint)
        return validPoints


def make_path(start, end, option):
    options = {'tail': 0,
               'move': 1
               }
    if option not in options:
        print('wrong option')
        return [] #! dodgy, should be some kind of error handling
    else:
        vec = tuple(map(lambda x, y: x - y, end, start))  # vector of move
        # print('vec', vec)
        norm = max(abs(i) for i in vec)
        # print('norm', norm)
        vecNormed = tuple(int(i / norm) for i in vec)  # normalised vector (i.e. for each step in move)
        path = [tuple(map(lambda x, y: x + (i + options[option]) * y, start, vecNormed)) for i in range(norm)]
        return path


def valid_path(start, end):
    path = make_path(start, end, 'move')
    validPath = True
    for pos in path:
        try:
            if board[pos[0]][pos[1]][0] != 'sea' or board[pos[0]][pos[1]][1] is not None or pos[0] < 0 or pos[1] < 0:
                validPath = False
        except:
            validPath = False
    return validPath


def valid_btns(boat): #! pass current player
    validBtns = [[], []]     # (compass points, sail buttons)
    if boat.legCounter <= legs:
        validBtns[0] = valid_points(wind, boat)
        validBtns[1] = [0, 1]
    return validBtns



class button:

    def __init__(self, text, x, y, size):
        self.text = text
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.colour = colours['btnDisabled']
        self.enabled = True

    def draw(self, window):
        if self.enabled:
            self.colour = colours['btnEnabled']
        else:
            self.colour = colours['btnDisabled']
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("padaukbook", 40)
        text = font.render(self.text, True, (255, 255, 255))
        window.blit(text, (self.x + round(self.width) / 2 - round(text.get_width() / 2),
                           self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height and self.enabled:
            return True
        else:
            return False


def blankets():
    for x in range(len(board)): #clear blankets
        for y in range(len(board[x])):
            board[x][y][2] = None
    for boat in flotilla:
        downWind = tuple(map(lambda x, y : x - y, boat.pos, point2vec[wind]))
        board[downWind[0]][downWind[1]][2] = 'blanketed'
        draw_board()

# def draw_blankets():
#     for x in range(boardSize[0]):
#         for y in range(boardSize[1]):
#
#     downWind = (-point2vec[wind][0], -point2vec[wind][1])
#     for boat in flotilla:
#         board[boat.x + downWind[0]][boat.x + downWind[1]][2]

        # upwind = (x + point2vec[wind][0], y + point2vec[wind][1])  # ! needs tidying
        # try:
        #     upwindBoat = board[upwind[0]][upwind[1]][1]
        #     if not upwindBoat is None:
        #         rect = pygame.Rect(x * blockSize + boardOffset + 1, y * blockSize + boardOffset + 1, blockSize - 2,
        #                            blockSize - 2)
        #         pygame.draw.rect(window, colours['blanket'], rect)
        #         if eval(upwindBoat.spinnnaker):  # ! when more players added, use the flotilla to find spinnakers
        #             rect = pygame.Rect(x * blockSize + boardOffset + 1, y * blockSize + boardOffset + 1, blockSize - 2,
        #                                blockSize - 2)
        #             pygame.draw.rect(window, colours['blanket'], rect)
        # except:
        #     pass


def draw_board():
    for x in range(boardSize[0]):
        for y in range(boardSize[1]):
            # draw terrain
            rect = pygame.Rect(x * blockSize + boardOffset +1 , y * blockSize + boardOffset + 1, blockSize-2, blockSize-2)
            pygame.draw.rect(window, colours[board[x][y][0]], rect)

            try:    # draw blanket / finish line
                if board[x][y][0] == 'sea':
                    rect = pygame.Rect(x * blockSize + boardOffset +1, y * blockSize + boardOffset + 1, blockSize-2, blockSize-2)
                    pygame.draw.rect(window, colours[board[x][y][2]], rect)
            except Exception as e:
                # print(e)
                pass

            try:    # draw boats
                rect = pygame.Rect(x * blockSize + boardOffset +4, y * blockSize + boardOffset + 4, blockSize-8, blockSize-8)
                pygame.draw.rect(window, colours[board[x][y][1]], rect)
            except Exception as e:
                # print(e)
                pass



# ! feels like this should be in a fnc, but then compass rose must be global no?
# compass rose
roseOrigin = (consoleOrigin[0] + consoleWidth / 2, 200)
offsetRoseOrigin = tuple(map(lambda x, y: x + y, roseOrigin, (-25, -25)))
roseOffset = 120
rootAHalf = 0.707
compassRose = [button("N", offsetRoseOrigin[0], offsetRoseOrigin[1] - roseOffset, (50, 50)),
               button("NE", offsetRoseOrigin[0] + rootAHalf * roseOffset, offsetRoseOrigin[1] - rootAHalf * roseOffset,
                      (50, 50)),
               button("E", offsetRoseOrigin[0] + roseOffset, offsetRoseOrigin[1], (50, 50)),
               button("SE", offsetRoseOrigin[0] + rootAHalf * roseOffset, offsetRoseOrigin[1] + rootAHalf * roseOffset,
                      (50, 50)),
               button("S", offsetRoseOrigin[0], offsetRoseOrigin[1] + roseOffset, (50, 50)),
               button("SW", offsetRoseOrigin[0] - rootAHalf * roseOffset, offsetRoseOrigin[1] + rootAHalf * roseOffset,
                      (50, 50)),
               button("W", offsetRoseOrigin[0] - roseOffset, offsetRoseOrigin[1], (50, 50)),
               button("NW", offsetRoseOrigin[0] - rootAHalf * roseOffset, offsetRoseOrigin[1] - rootAHalf * roseOffset,
                      (50, 50))
               ]


sailControls = [button("spinn", consoleOrigin[0] + 100, winSize[1] - 55, (100, 50)),
                button("puff", consoleOrigin[0] + 100, winSize[1] - 165, (100, 50)),
                button("port", consoleOrigin[0] + 100, winSize[1] - 110, (100, 50)),
                button("starboard", consoleOrigin[0] + 205, winSize[1] - 110, (100, 50)),
                ]


def wind_shift(current, shift):
    global wind
    wind = (current + shift) % 8
    draw_wind()
    blankets()


def draw_wind():
    pygame.draw.circle(window, (135, 135, 135), roseOrigin, 70)  # clean wind dial
    rotation = np.array([[np.cos(wind/4*np.pi), -np.sin(wind/4*np.pi)],  # rotation matrix
                         [np.sin(wind/4*np.pi), np.cos(wind/4*np.pi)]])
    rotatedArrow = [tuple(rotation.dot(vertex)) for vertex in assets['windArrow']]  # rotate arrow
    rotatedArrow = [tuple(np.add(vertex, roseOrigin)) for vertex in rotatedArrow]  # shift to compass rose
    pygame.draw.polygon(window, colours['black'], rotatedArrow)  # draw arrow

    # #! make this into a function called on pygame events
    # validPoints = valid_points(wind, p.tack)
    # for btn in compassRose:
    #
    #
    #     btn.draw(window)
    #
    # (validCompassBtns, validSailBtns) = valid_btns()
    # print(validCompassBtns)
    # print(validSailBtns)
    # for btn in compassRose:
    #     btn.enabled = False
    #     if compassRose.index(btn) in validCompassBtns:
    #         btn.enabled = True
    # for btn in sailControls:
    #     btn.enabled = False
    #     if sailControls.index(btn) in validSailBtns:
    #         btn.enabled = True

def draw_console():
    global compassRose, sailControls
    (validCompassBtns, validSailBtns) = valid_btns(p)
    print((validCompassBtns, validSailBtns))
    for btn in compassRose:  #! should be able to write this more succinctly
        btn.enabled = False
        if compassRose.index(btn) in validCompassBtns:
            btn.enabled = True
        btn.draw(window)
    for btn in sailControls:
        btn.enabled = False
        if sailControls.index(btn) in validSailBtns:
            btn.enabled = True
        btn.draw(window)


def roll_dice():
    global wind, legs
    sides = ['P', 'S', 1, 2, 2, 3]
    outcome = random.choices(sides)[0]
    dice.text = str(outcome)
    legs = 0
    if outcome == 'P':
        wind_shift(wind, -1)
    else:
        if outcome == 'S':
            wind_shift(wind, +1)
        else:
            legs = outcome
    print(legs)
    dice.draw(window)


# main
global window
pygame.init()
window = pygame.display.set_mode((winSize[0], winSize[1]))
pygame.display.set_caption("master")

window.fill(colours['grey'])

board = create_map('testMap.csv')

flotilla = []
p = player((5, 5), 'S')
p2 = player((10, 5), 'S')
flotilla.append(p) #!make this hold player class #!it already does o_0
flotilla.append(p2)

#! for testing purposes only
portshift = button("port", consoleOrigin[0] + 55, consoleOrigin[1], (50, 50))
portshift.draw(window)
starshift = button("star", consoleOrigin[0] + 110, consoleOrigin[1], (50, 50))
starshift.draw(window)
nextturn = button("reset", consoleOrigin[0] + 165, consoleOrigin[1], (100, 50))
nextturn.draw(window)

#initialise console
#? should this be elsewhere
pygame.draw.circle(window, colours['black'], roseOrigin, roseOffset + 5)  # draw compass rose ring
pygame.draw.circle(window, (135, 135, 135), roseOrigin, roseOffset - 5)

dice = button("roll", consoleOrigin[0], consoleOrigin[1], (50, 50))
dice.draw(window)

run = True
wind = 0
legs = 100 #!
draw_board()
draw_wind()
blankets()
# roll_dice()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            for btn in compassRose:
                if btn.click(clickPos):
                    p.move(compassRose.index(btn))
                    p.heading = compassRose.index(btn)
                    p.legCounter += 1
                    blankets()
            if dice.click(clickPos):
                roll_dice()
            if portshift.click(clickPos):
                wind_shift(wind, -1)
            if starshift.click(clickPos):
                wind_shift(wind, 1)
            if nextturn.click(clickPos):
                p.legCounter = 0
            if sailControls[0].click(clickPos):
                p.spinnaker = not p.spinnaker
                p.legCounter += 1
                if p.spinnaker:
                    spinn.text = 'lower'
                else:
                    spinn.text = 'raise'
                spinn.draw(window)
            if sailControls[1].click(clickPos):
                p.legCounter += 1
                if p.tack == 'P':
                    p.tack = 'S'
                    sailControls[1].text = 'S'
                else:
                    p.tack = 'P'
                    sailControls[1].text = 'P'
                sailControls[1].draw(window)
            draw_console()
        pygame.display.update()
