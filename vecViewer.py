import pygame
import numpy as np


class button:
    def __init__(self, text, corner, size):
        self.text = text
        self.x, self.y = corner
        self.width = size[0]
        self.height = size[1]
        self.colour = colours['black']

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("padaukbook", 40)
        text = font.render(self.text, True, (255, 255, 255))
        window.blit(text, (self.x + round(self.width) / 2 - round(text.get_width() / 2),
                           self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


################################
img = [(0, -50), (20, -15), (20, 40), (8, 50), (-8, 50), (-20, 40), (-20, -15)]

# img = [(-54, 46),
#        (46, 46),
#        (48, 24),
#        (33, 23),
#        (33, -42),
#        (-26, -48),
#        (-36, 17),
#        (-51, 16)]

##############################
colours = {'black': (0, 0, 0),
           'red': (255, 0, 0)
           }

boundBox = [(-10, -10),
            (10, -10),
            (10, 10),
            (-10, 10)]



def draw_asset(asset, centre, scale, rotation, colour, lineWidth):
    imgOut = []
    rotImg = []
    rotMatrix = np.array([[np.cos(rotation), -np.sin(rotation)],  # rotation matrix
                          [np.sin(rotation), np.cos(rotation)]])
    for vertex in asset:
        imgOut.append(np.add(rotMatrix.dot(vertex) * scale, centre))
    pygame.draw.polygon(window, colour, imgOut, width=lineWidth)
    print(imgOut)


def draw_window():
    window.fill((255, 255, 255))

    zoomIn.draw(window)
    zoomOut.draw(window)
    rotW.draw(window)
    rotC.draw(window)
    zoomScale.draw(window)


winSize = (600, 600)
winCentre = tuple(i * 0.5 for i in winSize)
zoomIn = button("+", (winCentre[0] - 45, 0), (30, 30))
zoomScale = button("s", (winCentre[0] - 15, 0), (30, 30))
zoomOut = button("-", (winCentre[0] + 15, 0), (30, 30))
rotW = button("w", (winCentre[0] - 75, 0), (30, 30))
rotC = button("c", (winCentre[0] + 45, 0), (30, 30))


def main():
    global window, scale
    pygame.init()
    window = pygame.display.set_mode(winSize)
    window.fill((255, 255, 255))

    scale = 1
    rotation = 0
    draw_window()
    draw_asset(img, winCentre, scale, rotation, colours['black'], 0)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                draw_window()
                if zoomIn.click(clickPos):
                    scale *= 1.5
                if zoomScale.click(clickPos):
                    assetBound = (max(vertex[0] for vertex in img) - min(vertex[0] for vertex in img),
                                  max(vertex[1] for vertex in img) - min(vertex[1] for vertex in img))
                    scale = 20 / max(assetBound)
                    print(scale)
                    draw_asset(boundBox, winCentre, 1, 0, colours['red'], 1)
                if zoomOut.click(clickPos):
                    scale *= 0.5
                if rotC.click(clickPos):
                    rotation += np.pi / 4
                if rotW.click(clickPos):
                    rotation -= np.pi / 4
                draw_asset(img, winCentre, scale, rotation, colours['black'], 0)
        pygame.display.update()


main()
