import math
import sys
import pygame
import ChessEngine
from ChessEngine import GameState
MAX_DEPTH = 2
values = {'P' : 10, 'N' : 30, 'B' : 30, 'R' : 50, 'Q' : 90}


def minimaxWhite(gameState, maximizingPlayer,  depth = 0, alpha = -sys.maxsize, beta = sys.maxsize):
    pygame.event.get()
    bestMove = None
    moves = gameState.getValidMoves()
    value = gameState.boardValue2()
    if gameState.checkMate or gameState.staleMate or depth > MAX_DEPTH:
        return value
    if maximizingPlayer:
        maxEval = -sys.maxsize
        for move in moves:
            gameState.make_move(move)
            eval = minimaxWhite(gameState, False, depth + 1, alpha, beta)
            gameState.undo_move()
            if eval > maxEval:
                maxEval = eval
                bestMove = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        if depth == 0:
            return bestMove
        return maxEval
    else:
        minEval = sys.maxsize
        for move in moves:
            gameState.make_move(move)
            eval = minimaxWhite(gameState, True, depth + 1, alpha, beta)
            gameState.undo_move()
            minEval = min(eval, minEval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def minimaxBlack(gameState, maximizingPlayer,  depth = 0, alpha = -sys.maxsize, beta = sys.maxsize):
    pygame.event.get()
    bestMove = None
    moves = gameState.getValidMoves()
    value = gameState.boardValue() # trying new evaluation
    if gameState.checkMate or gameState.staleMate or depth > MAX_DEPTH: #change for different level bots
        return value
    if maximizingPlayer:
        maxEval = -sys.maxsize
        for move in moves:
            gameState.make_move(move)
            eval = minimaxBlack(gameState, False, depth + 1, alpha, beta)
            gameState.undo_move()
            maxEval = max(eval, maxEval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = sys.maxsize
        for move in moves:
            gameState.make_move(move)
            eval = minimaxBlack(gameState, True, depth + 1, alpha, beta)
            gameState.undo_move()
            if eval < minEval:
                minEval = eval
                bestMove = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        if depth == 0:
            return bestMove
        return minEval



