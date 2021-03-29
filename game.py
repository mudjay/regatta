import pygame
import numpy as np
import random
import csv

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
           'white': (255, 255, 255),
           'tail': (0, 200, 0),
           'blanketed': (64, 144, 204),
           'clientBackground': (150, 150, 150),
           'starboard': (30, 120, 30),
           'port': (180, 50, 40)
           }

boatColours = {'red': (200, 0, 0),
               'orange': (220, 125, 0),
               'yellow': (255, 250, 80),
               'darkGreen': (70, 110, 60),
               'turquoise': (50, 200, 180),
               'darkBlue': (20, 20, 100),
               'purple': (130, 40, 180),
               }

assets = {'windArrow': [(0, -64), (15, -40), (15, 40), (-15, 40), (-15, -40)],
          'boat': [(0, -50), (20, -15), (20, 40), (8, 50), (-8, 50), (-20, 40), (-20, -15)],
          'bouy': [(-54, 46), (46, 46), (48, 24), (33, 23), (33, -42), (-26, -48), (-36, 17), (-51, 16)]
          }

point2sailing = {0: 0,
                 1: 1,
                 2: 2,
                 3: 3,
                 4: 2,
                 5: 3,
                 6: 2,
                 7: 1
                 }

point2vec = {0: (0, -1),
             1: (1, -1),
             2: (1, 0),
             3: (1, 1),
             4: (0, 1),
             5: (-1, 1),
             6: (-1, 0),
             7: (-1, -1)
             }

class Dice:
    def __init__(self, faces):
        self.faces = faces
        self.outcome = random.choices(self.faces)[0]

    def roll(self):
        self.outcome = random.choices(self.faces)[0]
        return self.outcome

class Player:
    def __init__(self, pos, tack, heading, colour, boatId):
        global board
        self.pos = pos
        self.currentTack = tack
        self.heading = heading
        self.colour = colour
        self.boatId = boatId
        board[self.pos[0]][self.pos[1]][1] = boatId

        self.spinnaker = False
        self.puff = False
        self.puffCounter = 2
        self.legCounter = 0

    def tack(self):
        if self.currentTack == 'P':
            self.currentTack = 'S'
            self.heading = (wind + 1) % 8
        if self.currentTack == 'S':
            self.currentTack = 'P'
            self.heading = (wind - 1) % 8

    def move(self, point):
        self.heading = point
        board[self.pos[0]][self.pos[1]][1] = None
        self.pos = move(self, wind, point, self.pos)
        board[self.pos[0]][self.pos[1]][1] = self.boatId


class Board:
    def __init__(self, file):
        terrainKey = {'0': 'sea',
                      '1': 'land',
                      '2': 'bouy'
                      }
        with open(file, newline='') as f:
            reader = csv.reader(f)
            terrain = list(reader)
        self.size = (len(terrain[0]), len(terrain))
        self.board = []
        for x in range(self.size[0]):  # ! using list comprehension would be nicer
            self.board.append([])
            for y in range(self.size[1]):
                if terrainKey[terrain[y][x]] == 'bouy':
                    board[x].append(['sea', 'bouy', None])
                else:
                    board[x].append([terrainKey[terrain[y][x]], None, None])

    def get_square(self, pos):
        return self.board[pos[0]][pos[1]]

    def is_clear(self, pos):
        if self.get_square(pos)[0] == 'sea' and self.get_square(pos)[1] is None:
            return True
        else:
            return False


def move(boat, wind, point, start):
    relativeWind = (point - wind) % 8
    vec = point2vec[point]
    vecSail = tuple(i * point2sailing[relativeWind] for i in vec)
    if boat.spinnaker or boat.puff:
        vecSail = tuple(map(lambda x, y: x + y, vecSail, vec))
    end = tuple(map(lambda x, y: x + y, start, vecSail))
    return end
