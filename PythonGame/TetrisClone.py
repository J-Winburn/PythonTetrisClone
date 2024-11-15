#This program is my first game built in programming, I thought why not go with a classic - TETRIS
#This is a Tetris clone
#Built by the helpful resource 'Making Games with Python & Pygame By Al Swegart' 


from re import L
import random, time, pygame, sys
import pygame.font
from pygame.locals import *

FPS = 30
WindowWidth = 640
WindowHeight = 480
BoxSize = 20
BoardWidth = 10
BoardHeight = 20
Blank = '.'  # used to represent blank spots in board datastruct

#Timing constraints

SidewaysFreq = .15
DownFreq = .1

XMargin = int((WindowWidth - BoardWidth * BoxSize) /2)
Topmargin = WindowHeight - (BoardHeight * BoxSize) -5

#colors we can use 
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = ( 0, 0, 0)
RED = (155, 0, 0)
LIGHTRED = (175, 20, 20)
GREEN = ( 0, 155, 0)
LIGHTGREEN = ( 20, 175, 20)
BLUE = ( 0, 0, 155)
LIGHTBLUE = ( 20, 20, 175)
YELLOW = (155, 155, 0)
LIGHTYELLOW = (175, 175, 20)
#game board colors
BorderColor = BLUE
BackgroundColor = BLACK
TextColor = WHITE
TextShadow = GRAY
#Colors for the shapes and their shadows 
Colors = (BLUE,GREEN,RED,YELLOW)
LightColors = (LIGHTBLUE,LIGHTGREEN,LIGHTRED,LIGHTYELLOW)

assert len(Colors) == len(LightColors)

#TEMPLATES FOR GAME PIECES 

TemplateWidth = 5
TemplateHeight = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

def main ():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WindowWidth, WindowHeight))
    BASICFONT = pygame.font.Font('freesansbold.ttf',18)
    BIGFONT = pygame.font.Font('freesansbold.ttd', 100)
    pygame.display.set_caption('Jareds Tetris Clone')

    showTextScreen('Jareds Tetris Clone')

    while True:
        if random.randint(0,1) == 0:
            pygame.mixer.music.load('tetrisb.mid')
        else:
            pygame.mixer.music.play(-1,.0)
            runGame()
            pygame.mixer.music.stop()
            showTextScreen('Game Over')

def runGame():

    # Game Start Variables and Initilization

    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True:
        if fallingPiece == none: #Start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() #Reset

            if not isValidPosition(board, fallingPiece):
                return # When a piece can no longer fit in the board then the game is over 

        checkForQuit()

        for event in pygame.event.get():
            if event.type == KEYUP:
                if (event.key == K_p):
                    DISPLAYSURF.fill(BackgroundColor) # if player pauses, we fill the board so they can not cheat
                    pygame.mixer.music.stop()
                    showTextScreen('Paused')
                    pygame.mixer.music.plat(-1,.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif(event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif(event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif(event.key == K_DOWN or event.key == K_s):
                    movingDown = False
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX = -1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()






