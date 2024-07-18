import random

pieceScore={'K':0,'Q':10,'R':5,'B':3,'N':3,'P':1}
CHECKMATE=1000
STALEMATE=0
DEPTH=2

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

def findBestMove(gs,validMoves):
    turnMultiplier = 1 if gs.whiteToPlay else -1
    opponentMinMaxScore=CHECKMATE #Opponent's Min of all Max Scores
    bestMove=None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves=gs.findValidMoves()
        if gs.stalemate:
            opponentMaxScore=STALEMATE
        elif gs.checkmate:
            opponentMaxScore=-CHECKMATE
        else:
            opponentMaxScore=-CHECKMATE
            for opponentMove in opponentsMoves:

                gs.makeMove(opponentMove)
                #gs.findValidMoves()
                if gs.checkmate:
                    score= CHECKMATE
                elif gs.stalemate:
                    score= STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if(score>opponentMaxScore):
                    opponentMaxScore=score
                gs.undoMove()
        if opponentMaxScore<opponentMinMaxScore:
            opponentMinMaxScore=opponentMaxScore
            bestMove=playerMove
        gs.undoMove()
    return bestMove

def findBestMoveMinMax(gs,validMoves):
    global nextMove
    nextMove=None
    random.shuffle(validMoves)
    #findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToPlay)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.whiteToPlay else -1)
    return nextMove

def findMoveMinMax(gs,validMoves,depth,whiteToPlay):
    global nextMove
    if depth==0:
        return scoreMaterial(gs.board)

    if whiteToPlay:
        maxScore=-CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves=gs.findValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, not whiteToPlay)
            if score > maxScore:
                maxScore=score
                if depth==DEPTH:
                    nextMove=move
            gs.undoMove()
        return maxScore
    else:
        minScore=CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves=gs.findValidMoves()
            score=findMoveMinMax(gs, nextMoves, depth-1, not whiteToPlay)
            if score < minScore:
                minScore=score
                if depth==DEPTH:
                    nextMove=move
            gs.undoMove()
        return minScore


def findMoveNegaMax(gs,validMoves,depth,turnMultiplier):
    global nextMove
    if depth ==0:
        return turnMultiplier*scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.findValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore=score
            if depth == DEPTH:
                nextMove=move
        gs.undoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs,validMoves,depth,alpha,beta,turnMultiplier):
    global nextMove
    if depth ==0:
        return turnMultiplier*scoreBoard(gs)
    

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.findValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1,-beta,-alpha, -turnMultiplier)
        if score > maxScore:
            maxScore=score
            if depth == DEPTH:
                nextMove=move
        gs.undoMove()
        if maxScore > alpha:
            alpha=maxScore
        
        if alpha >= beta:
            break
    return maxScore



def scoreBoard(gs):

    if gs.checkmate:
        if gs.whiteToPlay:
            return -CHECKMATE
        else:
            return CHECKMATE
    
    elif gs.stalemate:
        return STALEMATE

    score=0
    for row in gs.board:
        for square in row:
            if square[0]=='w':
                score+=pieceScore[square[1]]
            elif square[0]=='b':
                score+=pieceScore[square[1]]
    return score



def scoreMaterial(board):
    score=0

    for row in board:
        for square in row:
            if square[0]=='w':
                score+=pieceScore[square[1]]
            elif square[0]=='b':
                score+=pieceScore[square[1]]
    return score