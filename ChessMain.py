from __future__ import division
import pygame
import ChessEngine
import ChessBot

BLACK_BOT = True
WHITE_BOT = True
WIDTH = 512
HEIGHT = 512
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60 # for animation later on
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main.
'''

def LoadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("pictures/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

    #Note: we can access an image by saying 'IMAGES['wP']'



'''
draw the squares on the board. (top left square is always light.
'''
def drawBoard(screen):
    global colors
    colors = [pygame.Color("antiquewhite1"), pygame.Color("burlywood4")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



'''
draw the pieces on the board using the current GameState.board
'''

def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Responsible for all the graphics withing the current game state/
'''
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) #draw the squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # draw pieces on top of the squares


'''
Highlight square selected and moves for piece selected
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
            #highlight selected square
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparency value -> 0 transparent; 255 opaque
            s.fill(pygame.Color('cyan'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that square
            s.fill(pygame.Color('green'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))




'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)

        #erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pygame.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, endSquare)

        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        #draw the moving piece
        screen.blit(IMAGES[move.pieceMoved], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(60)




def drawText(screen, text):
    font = pygame.font.SysFont("Helvitca", 50, True, False)
    textObject = font.render(text, 0, pygame.Color('dark green'))
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pygame.Color('green'))
    screen.blit(textObject, textLocation.move(2,2))


'''
lets the user choose a promotion for their pawn
'''

def makePromotion(move, screen, board):
    global running
    drawText(screen, "Please choose promotion:")
    pygame.display.flip()
    promoted = False
    while running and not promoted:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'  # turn pawn into a queen
                    promoted = True
                if event.key == pygame.K_b:
                    board[move.endRow][move.endCol] = move.pieceMoved[0] + 'B'  # turn pawn into a bishop
                    promoted = True
                if event.key == pygame.K_n:
                    board[move.endRow][move.endCol] = move.pieceMoved[0] + 'N'  # turn pawn into a knight
                    promoted = True
                if event.key == pygame.K_r:
                    board[move.endRow][move.endCol] = move.pieceMoved[0] + 'R'  # turn pawn into a rook
                    promoted = True



'''
The main driver for our code. This will handle user input and updating the graphics.
'''

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made
    animate = False # flag variable for when we should animate a move
    LoadImages() #Only Once
    global running
    running = True
    sqSelected = () # which square was selected (location of the last click of the user)
    playerClicks = [] ##keep track of the player clicks (two tuples: [(6,4), (4,4)])
    gameOver = False

    while running:
        if (not BLACK_BOT and not gs.whiteToMove) or (not WHITE_BOT and gs.whiteToMove):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                #mouse handler
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not gameOver:
                        location = pygame.mouse.get_pos()
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE



                        if sqSelected == (row, col): #user clicked the same square twice
                            sqSelected = () #deselect
                            playerClicks = [] #clear player clicks

                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected) #append for both 1st and 2nd clicks

                        if len(playerClicks) == 1 and gs.board[sqSelected[0]][sqSelected[1]] == "--":
                            sqSelected = ()  # deselect
                            playerClicks = []  # clear player clicks

                        elif len(playerClicks) == 2: #after 2nd click
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print(move.getChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.make_move(validMoves[i])
                                    if move.isPawnPromotion:
                                        makePromotion(move, screen, gs.board)
                                    moveMade = True
                                    animate = True
                                    sqSelected = () #reset player clicks
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]

                #key handler
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z: #undo when 'z' is pressed
                        gs.undo_move()
                        moveMade = True
                        animate = False
                    if event.key == pygame.K_r:  # reset game when 'r' is pressed
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False

        elif not gameOver and BLACK_BOT and not gs.whiteToMove and not gs.checkMate and not gs.staleMate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            gs.make_move(ChessBot.minimaxBlack(gs, False))  # call bot action
            moveMade = True
            animate = True
        elif not gameOver and WHITE_BOT and gs.whiteToMove and not gs.checkMate and not gs.staleMate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            gs.make_move(ChessBot.minimaxWhite(gs, True))  # call bot action
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False





        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")

        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate")



        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
