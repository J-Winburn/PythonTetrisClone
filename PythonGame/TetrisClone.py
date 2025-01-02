#This program is my first game built in programming, I thought why not go with a classic - TETRIS
#This is a Tetris clone
#Built by the helpful resource 'Making Games with Python & Pygame By Al Swegart' 


import random, time, pygame, sys
from pygame.locals import *

FPS = 25
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

SHAPES = {'S': S_SHAPE_TEMPLATE,
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
    BASICFONT = pygame.font.Font('freesansbold.ttf',12)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 50)
    pygame.display.set_caption('Jareds Tetris Clone')

    showTextScreen('Jareds Tetris Clone')

    while True:
        if random.randint(0,1) == 0:
            pygame.mixer.music.load('tetrisb.mid')
        else:
            pygame.mixer.music.load('tetrisb.mid')
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

    while True: #Main game loop 
        if fallingPiece == None: #Start a new piece at the top if there is no piece already falling
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() #Reset

            if not isValidPosition(board, fallingPiece):
                return # When a piece can no longer fit in the board then the game is over 

        checkForQuit()

        for event in pygame.event.get(): #event handeling 
            if event.type == KEYUP:
                if (event.key == K_p):
                    DISPLAYSURF.fill(BackgroundColor) # if player pauses, we fill the board so they can not cheat
                    pygame.mixer.music.stop()
                    showTextScreen('Paused')
                    pygame.mixer.music.play(-1, 0.0)
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
                    #handling moving left
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX =-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()
                    #handling moving right
                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX = 1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation']+1) % len(SHAPES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation']-1) % len(SHAPES[fallingPiece['shape']])
                elif (event.key == K_q):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['roatation'] = (fallingPiece['rotation']+1) % len(SHAPES[fallingPiece['shape']])
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BoardHeight):
                        if not isValidPosition(board, fallingPiece, adjY=1):
                            break
                    fallingPiece['y'] += i-1 

        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > SidewaysFreq:
            if movingLeft and isValidPosition(board, fallingPiece, adjX =-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board,fallingPiece,adjX =1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()
        if movingDown and time.time() - lastMoveDownTime > DownFreq and isValidPosition(board, fallingPiece, adjY =1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()
        if time.time() - lastFallTime > fallFreq:
            if not isValidPosition(board, fallingPiece, adjY =1):
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        DISPLAYSURF.fill(BackgroundColor) #drawing items on screen
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def terminate():
    pygame.quit
    sys.exit

def checkForKeyPress():
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def showTextScreen(text): #displays large text until a key is pressed

    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TextShadow)
    titleRect.center = (int(WindowWidth / 2), int(WindowHeight / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TextColor)
    titleRect.center = (int(WindowWidth / 2 ) - 3 , int(WindowHeight / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    pressKeySurf,pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TextColor)
    pressKeyRect.center = (int(WindowWidth / 2), int(WindowHeight / 2 ) + 100)
    
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def checkForQuit():
    for event in pygame.event.get(QUIT): # gathering all quit events
        terminate()
    for event in pygame.event.get(KEYUP): # gather keyup events
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def calculateLevelAndFallFreq(score):
    #based on the score return the players level

    level = int(score / 10 ) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getNewPiece():
    shape = random.choice(list(SHAPES.keys()))
    newPiece = {'shape': shape, 'rotation': random.randint(0, len(SHAPES[shape]) -1),
                'x': int(BoardWidth/ 2) - int(TemplateWidth / 2),
                'y': -2,
                'color':random.randint(0,len(Colors) - 1 )}

    return newPiece

def addToBoard(board, piece):
    for x in range(TemplateWidth):
        for y in range(TemplateHeight):
            if SHAPES[piece['shape']][piece['rotation']][y][x] != Blank:
                board[x+piece['x']][y+piece['y']] = piece['color']

def getBlankBoard():
    board = []
    for i in range(BoardWidth):
        board.append([Blank]*BoardHeight)
    return board

def isOnBoard(x, y):

    return x >= 0 and x < BoardWidth and y < BoardHeight

def isValidPosition(board, piece, adjX=0, adjY=0):
    for x in range(TemplateWidth):
        for y in range(TemplateHeight):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or SHAPES[piece['shape']][piece['rotation']][y][x] == Blank:
                continue
            if not isOnBoard(x + piece['x']+ adjX, y + piece['y']+adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != Blank:
                return False
    return True

def isCompleteLine(board, y): # returns true if the line is filled with no gaps
    for x in range(BoardWidth):
        if board[x][y] == Blank:
            return False
    return True

def removeCompleteLines(board):
    numLinesRemoved = 0

    y = BoardHeight - 1 # starting at bottom of board

    while y >= 0:
        if isCompleteLine(board, y):
            for pullDownY in range (y, 0, -1):
                for x in range(BoardWidth):
                    board[x][pullDownY] = board[x][pullDownY - 1]
            for x in range(BoardWidth):
                board[x][0] = Blank
            numLinesRemoved += 1

        else:
            y -= 1

    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    return (XMargin + (boxx * BoxSize)), (Topmargin + (boxy * BoxSize))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):

    if color == Blank:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)

    pygame.draw.rect(DISPLAYSURF, Colors[color], (pixelx + 1, pixely + 1, BoxSize -1, BoxSize -1))

    pygame.draw.rect(DISPLAYSURF, LightColors[color], (pixelx + 1, pixely + 1, BoxSize - 4, BoxSize -4))


def drawBoard(board):

    pygame.draw.rect(DISPLAYSURF, BorderColor, (XMargin - 3, Topmargin - 7, (BoardWidth * BoxSize)+8, (BoardHeight * BoxSize) + 8), 5) #Border color

    pygame.draw.rect(DISPLAYSURF, BackgroundColor, (XMargin, Topmargin, BoxSize * BoardWidth, BoxSize * BoardHeight))  #BG color

    for x in range(BoardWidth):
        for y in range(BoardHeight):
            drawBox(x,y,board[x][y])

def drawStatus(score, level):
    #Score Text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TextColor)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WindowWidth - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    #Level Text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TextColor)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WindowWidth - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    for x in range(TemplateWidth):
        for y in range(TemplateHeight):
            if shapeToDraw[y][x] != Blank:
                drawBox(None, None, piece['color'], pixelx + (x *BoxSize), pixely + (y*BoxSize))


def drawNextPiece(piece):
    NextSurf = BASICFONT.render('Next:',True, TextColor)
    nextRect = NextSurf.get_rect()
    nextRect.topleft = (WindowWidth - 120, 80)
    DISPLAYSURF.blit(NextSurf,nextRect)

    drawPiece(piece,pixelx = WindowWidth -120, pixely = 100)

if __name__ == '__main__':
    main()

