import pygame
import numpy as np
from game import colours, boatColours, assets
import subprocess
from network import Network


class Button:
    def __init__(self, text, pos, size, colourRange=(colours['btnEnabled'], colours['btnDisabled']), border=0):
        self.text = text
        self.pos = pos
        self.size = size
        self.colourRange = colourRange  # (enabled colour, disabled colour)
        self.colour = colourRange[0]    # start button enabled
        self.border = border
        self.enabled = True
        self.visible = True

    def draw(self, window):
        if self.visible:
            if self.enabled:
                self.colour = self.colourRange[0]
            else:
                self.colour = self.colourRange[1]
            pygame.draw.rect(window, self.colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), self.border)
            font = pygame.font.SysFont("freesans", 40)
            text = font.render(self.text, True, (255, 255, 255))
            window.blit(text, (self.pos[0] + round(self.size[0]) / 2 - round(text.get_width() / 2),
                               self.pos[1] + round(self.size[1] / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.pos[0] <= x1 <= self.pos[0] + self.size[0] and self.pos[1] <= y1 <= self.pos[1] + self.size[1] and self.enabled:
            return True
        else:
            return False


class Text:
    def __init__(self, text, pos, size, colour=colours['black'], bold=False, italic=False):
        self.text = text
        self.pos = pos
        self.size = size
        self.colour = colour
        self.bold = bold
        self.italic = italic

    def draw(self, window):
        font = pygame.font.SysFont("freesans", self.size, bold=self.bold, italic=self.italic)
        window.blit(font.render(self.text, True, self.colour), self.pos)



def draw_asset(asset, centre, scale, rotation, colour=colours['black'], lineWidth=0):
    imgOut = []
    rotImg = []
    rotMatrix = np.array([[np.cos(rotation), -np.sin(rotation)],  # rotation matrix
                          [np.sin(rotation), np.cos(rotation)]])
    for vertex in asset:
        imgOut.append(np.add(rotMatrix.dot(vertex) * scale, centre))
    pygame.draw.polygon(window, colour, imgOut, width=lineWidth)


def welcome_screen():
    global connected, running
    window.fill(colours['clientBackground'])
    # while True:
    texts = [Text("welcome to..", (4,0), 20, bold=True, italic=True),
         Text("Regatta 0.2", (4, 16), 40, bold=True, italic=True)]
    for text in texts:
        text.draw(window)

    BTNconnect = Button("connect", (winSize[0]/2 - 90, winSize[1]/2 - 20), (180, 40))
    BTNconnect.draw(window)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                if BTNconnect.click(clickPos):
                    #try and connect
                    print("connecting")
                    connected = True
                    if connected:
                        return connected
                    else:
                        print("connection failed, retry")

        pygame.display.update()


def lobby_screen():
    def draw_flotilla(flotilla, pos):
        xShift = 0
        for boat in flotilla:
            if boat == 1:
                scale = 0.6
            else:
                scale = 0.4
            draw_asset(assets['boat'], (pos[0] + xShift, pos[1]), scale, 0, boatColours['orange'])
            xShift += 40

    global connected
    boatID = 10
    run = True
    window.fill(colours['clientBackground'])
    texts = [Text("Game Lobby", (0, 0), 40, bold=True, italic=True),
             Text("sail number:", (5, 55), 20),
             Text(str(boatID), (40, 75), 30),
             Text("pick boat colour:", (160, 55), 20),
             Text("flotilla:", (5, 120), 20),
             Text("ready?", (5, 350), 20)
             ]
    for text in texts:
        text.draw(window)

    colourBtns = []
    x = 0
    for colour in boatColours:
        colourBtns.append(Button("", (190 + x, 78), (20, 20), (colour, colours['btnDisabled'])))
        x += 22
    for btn in colourBtns:
        btn.draw(window)

    flotilla = [1,2,3,4]
    draw_flotilla(flotilla, (60, 175))

    BTNready = Button("ready", (200, 300), (100, 50))
    BTNready.draw(window)

    while run and connected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                for btn in colourBtns:
                    if btn.click(clickPos):
                        # n.send(btn.colour)
                        print(btn.colour)
                if BTNready.click(clickPos):
                    run = False

        pygame.display.update()


def console_screen():
    subprocess.Popen(['python', 'boardViewer.py'])  # should pass it a game id
    global connected
    run = True
    window.fill(colours['clientBackground'])



    # compass rose
    roseCentre = (150, 250)
    offsetRoseCentre = tuple(i - 25 for i in roseCentre)
    roseRadius = 120
    rootHalf =0.707
    compassRose = [Button("N", (offsetRoseCentre[0], offsetRoseCentre[1] - roseRadius), (50, 50)),
                   Button("NE", (offsetRoseCentre[0] + roseRadius*rootHalf, offsetRoseCentre[1] - roseRadius*rootHalf), (50, 50)),
                   Button("E", (offsetRoseCentre[0] + roseRadius, offsetRoseCentre[1]), (50, 50)),
                   Button("SE", (offsetRoseCentre[0] + roseRadius*rootHalf, offsetRoseCentre[1] + roseRadius*rootHalf), (50, 50)),
                   Button("S", (offsetRoseCentre[0], offsetRoseCentre[1] + roseRadius), (50, 50)),
                   Button("SW", (offsetRoseCentre[0] - roseRadius*rootHalf, offsetRoseCentre[1] + roseRadius*rootHalf), (50, 50)),
                   Button("W", (offsetRoseCentre[0] - roseRadius, offsetRoseCentre[1]), (50, 50)),
                   Button("NW", (offsetRoseCentre[0] - roseRadius*rootHalf, offsetRoseCentre[1] - roseRadius*rootHalf), (50, 50))
                   ]
    pygame.draw.circle(window, colours['black'], roseCentre, roseRadius + 5)  # draw compass rose ring
    pygame.draw.circle(window, colours['clientBackground'], roseCentre, roseRadius - 5)
    for btn in compassRose:
        btn.draw(window)
    draw_asset(assets['windArrow'], roseCentre, 1, 0)

    #sail controls
    sailControls = [Button("spin.", (42, 410), (100, 50)),
                    Button("puff", (147, 410), (100, 50)),
                    Button("port", (42, 465), (100, 50), colourRange=(colours['port'], colours['btnDisabled'])),
                    Button("star.", (147, 465), (100, 50), colourRange=(colours['starboard'], colours['btnDisabled']))
                    ]

    for btn in sailControls:
        btn.draw(window)

    #? maybe group dice with other buttons

    btnDice = Button("dice", (5,5), (100, 50))
    btnDice.draw(window)


    texts = [Text("puffs left: " + str(2), (195, 8), 20),
             Text("legs left: " + str(5), (203, 30), 20)]
    for text in texts:
        text.draw(window)


    while connected and run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        pygame.display.update()


def main():
    global connected
    global connected, running, winSize, window
    while not connected:
        welcome_screen()
    connected = True
    lobby_screen()
    console_screen()

########################################################################################################################
pygame.init()
winSize = (300, 520)
window = pygame.display.set_mode(winSize)
pygame.display.set_caption("client")
window.fill(colours['clientBackground'])
connected = False
running = True
main()