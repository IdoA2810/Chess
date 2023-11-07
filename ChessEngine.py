DIMENSION = 8
import sys
values = {'P' : 10, 'N' : 30, 'B' : 30, 'R' : 50, 'Q' : 90, 'K' : 900, '-' : 0, 'w' : 1, 'b' : -1}

#tables for board evaluation
pawn_table =[
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]
knight_table = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50],
]
bishop_table = [
[-20,-10,-10,-10,-10,-10,-10,-20],
[-10,  0,  0,  0,  0,  0,  0,-10],
[-10,  0,  5, 10, 10,  5,  0,-10],
[-10,  5,  5, 10, 10,  5,  5,-10],
[-10,  0, 10, 10, 10, 10,  0,-10],
[-10, 10, 10, 10, 10, 10, 10,-10],
[-10,  5,  0,  0,  0,  0,  5,-10],
[-20,-10,-10,-10,-10,-10,-10,-20],
]
rook_table = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]
]
queen_table = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [  0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]
king_table = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20]
]

class GameState:
    def __init__(self):
        #board is and 8x8 2d list, each element of the list has 2 characters.
        #the first character represents the color of the piece
        #the second character represents the type of the piece
        #"--" represents an empty space.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]

        ]

        '''self.board = [
            ["--", "--", "--", "--", "bK", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "wB", "--"],
            ["--", "--", "--", "--", "--", "wQ", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]

        ]'''


        self.moveFunctions = {'P' : self.getPawnMoves, 'R' : self.getRookMoves, 'N' : self.getKnightMoves,
                              'B' : self.getBishopMoves, 'Q' : self.getQueenMoves, 'K' : self.getKingMoves}

        self.evaluationTables = {'P' : pawn_table, 'R' : rook_table, 'N' : knight_table, 'B' : bishop_table,
                                  'Q' : queen_table, 'K' : king_table}

        self.whiteToMove = True
        self.moveLog = []
        self.sockets = {}
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False # no valid moves and the king is in check
        self.staleMate = False # no valid moves and the king is not in check
        self.enpassantPossible = () #coordinates for the square where an en passant capture is possible
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]
        self.started = False
        self.NumPlayers = 0
        self.whiteTaken = False

        #self.inCheck = False
        #self.pins = []
        #self.checks = []

    # return value of board for the bot

    def add_player(self, socket, color):
        if not self.started:
            self.NumPlayers += 1
            if self.NumPlayers == 2:
                self.started = True
            self.whiteTaken = True
            self.sockets[color] = socket
    def remove_player(self, color):
        self.NumPlayers -= 1
        self.started = False
        if color == "w":
            self.whiteTaken = False
        del self.sockets[color]

    '''
    a positive score is good for white, a negative score is good for black
    '''
    def boardValue(self):
        if self.checkMate:
            if self.whiteToMove:
                return -100000
            else:
                return 100000
        value = 0
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                value += values[self.board[i][j][0]] * values[self.board[i][j][1]]
        return value

    def boardValue2(self):
        if self.checkMate:
            if self.whiteToMove:
                return -100000
            else:
                return 100000
        value = 0
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if self.board[i][j] != "--":
                    if self.board[i][j][0] == 'w':
                        line = i
                    else:
                        line = 7 - i # for black pieces we need to mirror the piece-table
                    value += self.evaluationTables[self.board[i][j][1]][line][j] * values[self.board[i][j][0]]
        return value


    def make_move(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove # swap players (next turn)
        #update the king's location if moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion (choosing a specific promotion is done from main)
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q' # turn pawn into a queen

        #enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' #capturing the pawn

        #update the enpassantPossible variable (check if enpassant is possible)
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2: # only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

        #castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle move
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] # move the rook to it's new square
                self.board[move.endRow][move.endCol + 1] = '--' #erase old rook


            else: #queenside castle move
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # move the rook to it's new square
                self.board[move.endRow][move.endCol - 2] = '--' #erase old rook


        #update castling rights - whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))








    '''
    undo the last move that was made
    '''
    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # swap players (previous turn)
            # update the king's location if moved
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo en passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)

            #undo a 2 square pawn advance
            if move.pieceMoved[1] == 'P' and abs(move.endRow - move.startRow) == 2:
                self.enpassantPossible = ()


            #undo castling rights
            self.castleRightsLog.pop() # get rid of the new castle rights from the move we are undoing
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRights = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]  # move the rook to it's old square
                    self.board[move.endRow][move.endCol - 1] = '--'  # erase new rook
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]  # move the rook to it's old square
                    self.board[move.endRow][move.endCol + 1] = '--'  # erase old rook



    '''
    update the castle rights given the move
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: # left rook
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRights.bks = False


    '''
    all moves considering checks
    '''

    def getValidMoves(self):
        '''moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1: #only 1 check, block check or move the king
                moves = self.getAllPossibleMoves()
                #to block a check you must move a piece into one of the squares between the enemy piece and the king
                check = self.checks[0] # check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] # enemy piece causing the check
                validSquares = [] # squares that pieces can move to
                # if knight, must capture knight or move king other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) # check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: #once you get to piece end checks
                            break
                #get rid of any moves that don't block check or move the king
                for i in range(len(moves) - 1, -1, -1): # go through backwards when you are removing from a list as iterating
                    if moves[i].pieceMoved[[1]] != 'K' : # move dosen't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: #move doesn't block check or capture piece
                            moves.remove(moves[i])

            else: # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: # not in check so every possible move is fine
            moves = self.getAllPossibleMoves()

        return moves'''




        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                        self.currentCastlingRights.wqs, self.currentCastlingRights.bqs) #copy the current castling rights
        #1.) generate all possible moves
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        #2.) for each move, make the move
        for i in range (len(moves) - 1, -1, -1): #when removing from a list go backwards through that list
            self.make_move(moves[i])
            #3.) generate all opponent's moves
            #4.) for each of your opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove # need to switch the turns back because make_move switches turns
            if self.inCheck():
                moves.remove(moves[i]) #5.) if they do attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove # swap turns back
            self.undo_move()

        if len(moves) == 0: #either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRights = tempCastleRights
        return moves

    '''
    determine if the current player is in check
    '''

    def checkForPinsAndChecks(self):
        pins = [] # squares where the allied pinned piece is and direction pinned from
        checks = [] #squares where the enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        #check outward from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () # reset possible pins
            for i in range (1, DIMENSION):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < DIMENSION and 0 <= endCol < DIMENSION:
                    endPiece  = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == (): #1st allied piece would be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: #2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece == enemyColor:
                        type = endPiece[1]
                        #5 possibilities here in this complex conditional
                        #1.) orthogonally away from the king is a rook
                        #2.) diagonally away from the king is a bishop
                        #3.) 1 square away diagonally away from the king and piece is a pawn
                        #4.) any direction and the piece is a queen
                        #5.) any direction one square away and the piece is a king (this is necessary to prevent a king move to a square controlled by another king)
                        if (0 <= j <=3 and type == 'R') or (4 <= j <= 7 and type == 'B') or \
                            (i == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4<= j <= 5))) or \
                            (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): #no piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: #piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else: # enemy piece not applying check
                            break
                else:
                    break # off board
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0<= endRow <8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N' : #enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks






    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    determine if the enemy can attack the square r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: # square is under attack
                return True
        return False


    '''
        all moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): # number of cols
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # calls the appropriate move function based on piece types


        return moves

    '''
    get all the possible moves for the given pawn
    '''

    def getPawnMoves(self, r, c, moves):
        #piecePinned = False
        #pinDirection = ()
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))

            if c - 1 >= 0: #capture to the left
                if self.board[r - 1][c - 1][0] == 'b':  # capture to the left
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))


            if c + 1 < DIMENSION: #capture to the right
                if self.board[r - 1][c + 1][0] == 'b':  # capture to the right
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))

        else: #black pawn moves
            if self.board[r+1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))

            if c - 1 >= 0: #capture to the left
                if self.board[r + 1][c - 1][0] == 'w':  # capture to the left
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))

            if c + 1 < DIMENSION: #capture to the right
                if self.board[r + 1][c + 1][0] == 'w':  # capture to the right
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))

            # add pawm promotions later
    '''
        get all the possible moves for the selected rook
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, DIMENSION):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < DIMENSION and 0 <= endCol < DIMENSION:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: #off board
                    break
            '''if self.whiteToMove:  # white pawn moves
            for i in range(r - 1, -1, -1): # check up movement
                if self.board[i][c] == "--" or self.board[i][c][0] == 'b':
                    moves.append(Move((r, c), (i, c), self.board))
                if self.board[i][c] != '--':
                    break
            for i in range(r + 1, len(self.board)): # check down movement
                if self.board[i][c] == "--" or self.board[i][c][0] == 'b':
                    moves.append(Move((r, c), (i, c), self.board))
                if self.board[i][c] != '--':
                    break
            for i in range(c - 1, -1, -1): # check left movement
                if self.board[r][i] == "--" or self.board[r][i][0] == 'b':
                    moves.append(Move((r, c), (r, i), self.board))
                if self.board[r][i] != '--':
                    break
            for i in range(c + 1, len(self.board[r])): # check right movement
                if self.board[r][i] == "--" or self.board[r][i][0] == 'b':
                    moves.append(Move((r, c), (r, i), self.board))
                if self.board[r][i] != '--':
                    break

        else:  # black pawn moves
            for i in range(r - 1, -1, -1):  # check up movement
                if self.board[i][c] == "--" or self.board[i][c][0] == 'w':
                    moves.append(Move((r, c), (i, c), self.board))
                if self.board[i][c] != '--':
                    break
            for i in range(r + 1, len(self.board)):  # check down movement
                if self.board[i][c] == "--" or self.board[i][c][0] == 'w':
                    moves.append(Move((r, c), (i, c), self.board))
                if self.board[i][c] != '--':
                    break
            for i in range(c - 1, -1, -1):  # check left movement
                if self.board[r][i] == "--" or self.board[r][i][0] == 'w':
                    moves.append(Move((r, c), (r, i), self.board))
                if self.board[r][i] != '--':
                    break
            for i in range(c + 1, len(self.board[r])):  # check right movement
                if self.board[r][i] == "--" or self.board[r][i][0] == 'w':
                    moves.append(Move((r, c), (r, i), self.board))
                if self.board[r][i] != '--':
                    break'''

    '''
            get all the possible moves for the selected knight
    '''

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < DIMENSION and 0 <= endCol < DIMENSION:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
            get all the possible moves for the selected bishop
    '''

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, DIMENSION):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < DIMENSION and 0 <= endCol < DIMENSION:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

    '''
            get all the possible moves for the selected queen
    '''

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
            get all the possible moves for the selected king
    '''

    def getKingMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < DIMENSION and 0 <= endCol < DIMENSION:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    '''
    generate all valid castle moves for the king at (r,c) and add them to the list of moves
    '''

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return #can't castle while we are in check
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(r, c, moves)


    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r,c), (r, c + 2), self.board, isCastleMove = True))


    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))



class Move:

    #maps keys to values
    #keys: value

    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowsToRanks = {v : k for k, v in ranksToRows.items()}

    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):

        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        #pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)

        #en passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'

        #castle move
        self.isCastleMove = isCastleMove

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]



class CastleRights: # store the current state of the castling rights
    def __init__(self, wks, bks, wqs ,bqs):
        self.wks = wks #white king side
        self.bks = bks #black king side
        self.wqs = wqs #white queen side
        self.bqs = bqs #black queen side