
class GameState():
    def __init__(self):
        # Represent the chess board with a list of lists (8x8) with each list representing a row
        # We have used "xx" to represent empty squares - no pieces on that square
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
            ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
            ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
            ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        # Determine whose turn it is
        self.whiteToPlay = True
        # Make the functions for moving pieces and check validity
        self.moveFunctions = {"P": self.pawnMoves,
                              "B": self.bishopMoves,
                              "N": self.knightMoves,
                              "R": self.rookMoves,
                              "Q": self.queenMoves,
                              "K": self.kingMoves}
        # Keep a record of the moves played
        self.moveLog = []

        # For checks thrown to the king, keep track of its location
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        # Keep track of en passant captures
        self.enpassant = ()
        self.enpassantLog=[self.enpassant]
        self.currentCastelingRight = CastleRights(True,True,True,True)
        self.castleRightsLog=[CastleRights(self.currentCastelingRight.wks,self.currentCastelingRight.wqs,
        self.currentCastelingRight.bks,self.currentCastelingRight.bqs)]

    def makeMove(self, move):
        # When we move a piece from (a,b) to (c,d), the piece disappears from initial position (a,b)
        self.board[move.startRow][move.startCol] = "xx"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # Append this move to the log and switch the player
        self.moveLog.append(move)
        self.whiteToPlay = not self.whiteToPlay

        # Update the location of the king after it moves
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.pawnPromotion:
            # Add feature here
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        if move.enpassant:
            self.board[move.startRow][move.endCol] = "xx"
        if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
            self.enpassant = ((move.startRow + move.endRow)//2, move.endCol)
        else:
            self.enpassant = ()

        self.enpassantLog.append(self.enpassant)

        if move.isCastleMove:
            if move.endCol - move.startCol==2: #king side
                if(self.board[move.endRow][move.endCol+1][1]=='R'):
                    self.board[move.endRow][move.endCol-1]=self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1]="xx"
            else:
                if (self.board[move.endRow][move.endCol-2][1]=='R'):
                    self.board[move.endRow][move.endCol+1]=self.board[move.endRow][move.endCol-2]
                    self.board[move.endRow][move.endCol-2]="xx"

        #castling Rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastelingRight.wks,self.currentCastelingRight.wqs,
                self.currentCastelingRight.bks,self.currentCastelingRight.bqs))



    def undoMove(self):
        # Just undo the most recent move
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToPlay = not self.whiteToPlay

            # Update the location of the king after undo
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            if move.enpassant:
                self.board[move.endRow][move.endCol] = "xx"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantLog.pop()
            self.enpassant = self.enpassantLog[-1]

            self.checkmate=False
            self.stalemate=False
            
        
            self.castleRightsLog.pop()
            self.currentCastelingRight= self.castleRightsLog[-1]

            #undo castle Move

            if move.isCastleMove:
                if move.endCol - move.startCol==2: #king side
                        self.board[move.endRow][move.endCol+1]=self.board[move.endRow][move.endCol-1]
                        self.board[move.endRow][move.endCol-1]="xx"
                else:
                        self.board[move.endRow][move.endCol-2]=self.board[move.endRow][move.endCol+1]
                        self.board[move.endRow][move.endCol+1]="xx"  
 

    def updateCastleRights(self,move):
        if move.pieceMoved=="wK":
            self.currentCastelingRight.wks=False
            self.currentCastelingRight.wqs=False
        elif move.pieceMoved=="bK":
            self.currentCastelingRight.bks=False
            self.currentCastelingRight.bqs=False
        
        elif move.pieceMoved=="wR":
            if move.startRow== 7:
                if move.startCol==0:
                    self.currentCastelingRight.wqs=False
                elif move.startCol==7:
                    self.currentCastelingRight.wks=False
        elif move.pieceMoved=="bR":
            if move.startRow==0:
                if move.startCol==0:
                    self.currentCastelingRight.bqs=False
                elif move.startCol==7:
                    self.currentCastelingRight.bks=False
   
    def getAllMoves(self):
        moves = []
        # Nested for loop to check for all pieces position and the squares they are covering
        for row in range(8):
            for col in range(8):
                color = self.board[row][col][0]
                if (color == 'w' and self.whiteToPlay) or (color == 'b' and not self.whiteToPlay):
                    piece = self.board[row][col][1]
                    # Call the function corresponding to the piece
                    self.moveFunctions[piece](row, col, moves)
                    # if piece == 'P':
                    #     self.pawnMoves(row, col, moves)
                    # elif piece == 'N':
                    #     self.knightMoves(row, col, moves)
                    # elif piece == 'B':
                    #     self.bishopMoves(row, col, moves)
                    # elif piece == 'R':
                    #     self.rookMoves(row, col, moves)
                    # elif piece == 'Q':
                    #     self.queenMoves(row, col, moves)
                    # elif piece == 'K':
                    #     self.kingMoves(row, col, moves)
        return moves

    def pawnMoves(self, row, col, moves):
        if self.whiteToPlay:
            # If square in front of us is empty, we can move the pawn there
            if self.board[row-1][col] == "xx":
                moves.append(Move((row, col), (row-1, col), self.board))
                # If pawn on row 6, check if it can move 2 squares
                if row == 6 and self.board[row-2][col] == "xx":
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col-1 >= 0:  # Capture to the left
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
                elif (row-1, col-1) == self.enpassant:
                    moves.append(Move((row, col), (row - 1, col - 1), self.board, enpassant=True))
            if col+1 < 8:  # Capture to the right
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif (row-1, col+1) == self.enpassant:
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, enpassant=True))
        # Black pawn moves
        else:
            # If square below it is empty, we can move the pawn there
            if self.board[row + 1][col] == "xx":
                moves.append(Move((row, col), (row + 1, col), self.board))
                # If pawn on row 1, check if it can move 2 squares
                if row == 1 and self.board[row + 2][col] == "xx":
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:  # Capture to the left
                if self.board[row + 1][col - 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
                elif (row+1, col-1) == self.enpassant:
                    moves.append(Move((row, col), (row + 1, col - 1), self.board, enpassant=True))
            if col + 1 < 8:  # Capture to the right
                if self.board[row + 1][col + 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif (row+1, col+1) == self.enpassant:
                    moves.append(Move((row, col), (row + 1, col + 1), self.board, enpassant=True))

    def bishopMoves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.whiteToPlay:
            opponentColor = "b"
        else:
            opponentColor = "w"
        for d in directions:
            for i in range(1, 8):
                lastRow = row + d[0] * i
                lastCol = col + d[1] * i
                if 0 <= lastRow <= 7 and 0 <= lastCol <= 7:
                    lastPiece = self.board[lastRow][lastCol]
                    if lastPiece == "xx":
                        moves.append(Move((row, col), (lastRow, lastCol), self.board))
                    elif lastPiece[0] == opponentColor:
                        moves.append(Move((row, col), (lastRow, lastCol), self.board))
                        break
                    # Encountered a piece of your own color
                    else:
                        break
                # Break if we go off the board
                else:
                    break

    def knightMoves(self, row, col, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1))
        if self.whiteToPlay:
            opponentColor = "b"
        else:
            opponentColor = "w"
        for direction in directions:
            lastRow = row + direction[0]
            lastCol = col + direction[1]
            if 0 <= lastRow < 8 and 0 <= lastCol < 8:
                lastPiece = self.board[lastRow][lastCol]
                # Check condition below for knight
                if lastPiece[0] == opponentColor or lastPiece[0] == 'x':
                    moves.append(Move((row, col), (lastRow, lastCol), self.board))

    def rookMoves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        if self.whiteToPlay:
            opponentColor = "b"
        else:
            opponentColor = "w"
        for d in directions:
            for i in range(1, 8):
                lastRow = row + d[0] * i
                lastCol = col + d[1] * i
                if 0 <= lastRow <= 7 and 0 <= lastCol <=7:
                    lastPiece = self.board[lastRow][lastCol]
                    if lastPiece == "xx":
                        moves.append(Move((row, col), (lastRow, lastCol), self.board))
                    elif lastPiece[0] == opponentColor:
                        moves.append(Move((row, col), (lastRow, lastCol), self.board))
                        break
                    # Encountered a piece of your own color
                    else:
                        break
                # Break if we go off the board
                else:
                    break

    def queenMoves(self, row, col, moves):
        # A queen is basically a rook and a bishop combined
        self.rookMoves(row, col, moves)
        self.bishopMoves(row, col, moves)

    def kingMoves(self, row, col, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1))
        if self.whiteToPlay:
            sameColor = "w"
        else:
            sameColor = "b"
        for i in range(8):
            lastRow = row + directions[i][0]
            lastCol = col + directions[i][1]
            if 0 <= lastRow < 8 and 0 <= lastCol < 8:
                lastPiece = self.board[lastRow][lastCol]
                # Check condition below for knight
                if lastPiece[0] != sameColor:
                    moves.append(Move((row, col), (lastRow, lastCol), self.board))


    def getCastleMoves(self,r,c,moves):
        if self.squareUnderAttack(r, c):
            return
        
        if (self.whiteToPlay and self.currentCastelingRight.wks) or ( not self.whiteToPlay and self.currentCastelingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        
        if (self.whiteToPlay and self.currentCastelingRight.wqs) or ( not self.whiteToPlay and self.currentCastelingRight.bqs):
            self.getQueensideCastleMoves(r,c,moves)

    def getKingsideCastleMoves(self,r,c,moves):
        if self.board[r][c+1]=='xx' and self.board[r][c+2]=='xx':
            if not self.squareUnderAttack(r, c+1) and  not self.squareUnderAttack(r, c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove=True))

    def getQueensideCastleMoves(self,r,c,moves):
        if self.board[r][c-1]=='xx' and self.board[r][c-2]=='xx' and self.board[r][c-3]=='xx':
            if not self.squareUnderAttack(r, c-1) and  not self.squareUnderAttack(r, c-2):
                moves.append(Move((r,c),(r,c-2),self.board,isCastleMove=True)) 
 

    def findValidMoves(self):
        temp_enpassant = self.enpassant
        #temp_CastleRights = CastleRights(self.currentCastelingRight.wks, self.currentCastelingRight.wqs, self.currentCastelingRight.bks, self.currentCastelingRight.bqs)

        moves = self.getAllMoves()

        # if self.whiteToPlay:
        #     self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        # else:
        #     self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        for i in range(len(moves)-1, -1, -1):
            # Delete moves which are invalid - leading to checks in next move
            self.makeMove(moves[i])
            self.whiteToPlay = not self.whiteToPlay
            if self.inCheck():
                # Remove from valid moves if they attack your king
                moves.remove(moves[i])
            self.whiteToPlay = not self.whiteToPlay
            self.undoMove()
        if len(moves) == 0:
            # This means it is either checkmate or stalemate
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        
        else:
            self.checkmate=False
            self.stalemate=False
            
        self.enpassant = temp_enpassant
        #self.currentCastelingRight = temp_CastleRight
        count=0
        for i in range(8):
            for j in range (8):
                if self.board[i][j]!="xx":
                    count=count+1
        if count<=3:
            self.stalemate=True
        return moves

    # Function to determine if current player is under check
    def inCheck(self):
        if self.whiteToPlay:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # Determines if opponent can attack given square
    def squareUnderAttack(self, row, col):
        # Check from the opponents side if there is an attack on the king
        self.whiteToPlay = not self.whiteToPlay
        opponentMoves = self.getAllMoves()
        # Switch back the turns and return corresponding value
        self.whiteToPlay = not self.whiteToPlay
        for move in opponentMoves:
            if move.endRow == row and move.endCol == col:
                return True
        return False


class CastleRights():
    def __init__(self,wks,wqs,bks,bqs):
        self.wks=wks
        self.wqs=wqs
        self.bks=bks
        self.bqs=bqs


class Move():
    # In chess, horizontal rows are called ranks - 6th rank, 3rd rank, etc.
    # Vertical columns are called files - d file, a file
    # toRanks = {"0": 8, "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1}
    # toFiles = {"0": "a", "1": "b", "2": "c", "3": "d", "4": "e", "5": "f", "6": "g", "7": "h"}
    # Get corresponding array row number from rank
    toRows = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7}
    # Get corresponding array column number from file
    toCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    # Get corresponding chess rank notation from array
    toRanks = {values: keys for keys, values in toRows.items()}
    # Get corresponding chess file notation from array
    toFiles = {values: keys for keys, values in toCols.items()}

    def __init__(self, initial_pos, final_pos, board, enpassant=False,isCastleMove=False):
        # Grab the 4 positions in play
        self.startRow = initial_pos[0]
        self.startCol = initial_pos[1]
        self.endRow = final_pos[0]
        self.endCol = final_pos[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.pawnPromotion = False
        if (self.pieceMoved == "wP" and self.endRow == 0) or (self.pieceMoved == "bP" and self.endRow == 7):
            # Pawn needs to be promoted
            self.pawnPromotion = True

        self.enpassant = enpassant
        if self.enpassant:
            if self.pieceMoved == "bP":
                self.pieceCaptured = "wP"
            else:
                self.pieceCaptured = "bP"
        # enpassant Bug fixed

        self.isCastleMove=isCastleMove

        # MoveID generated like a hash function
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol * 1
        # print(self.moveID)
        self.iscapture = self.pieceCaptured!="xx"

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def __str__(self):

        endSquare = self.getRankAndFile(self.endRow, self.endCol)
        
        #pawn Moves

        if self.pieceMoved[1]=='P':
            if self.iscapture:
                return self.toFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare
        
        moveString=self.pieceMoved[1]
        if self.iscapture:
            moveString+='x'
        return moveString + endSquare

    def getChessNotation(self):
        # Modify this to real chess notation
        return self.getRankAndFile(self.startRow, self.startCol) + self.getRankAndFile(self.endRow, self.endCol)

    def getRankAndFile(self, row, col):
        return self.toFiles[col] + self.toRanks[row]