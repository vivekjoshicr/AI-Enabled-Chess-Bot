
# File for handling user input and displaying current game state
import pygame as p
import chessEngine , SmartMoveFinder 
# Define some constants
# Initialise our pygame package
p.init()
WIDTH = 500
HEIGHT = 500
MOVE_LOG_PANEL_WIDTH=250
MOVE_LOG_PANEL_HEIGHT=500
DIMENSION = 8
SQUARE_SIZE = WIDTH // DIMENSION
# Do not load the images for every operation - load once and save it once as key-value pairs
IMAGES = {}


def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bK', 'bQ', 'bP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'wP']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def drawBoard(screen):
    # Play around with the color scheme
    colors = [p.Color("burlywood"), p.Color("darkorange4")]
    # The top left of the board is always a light square
    # Starting from 0,0 - all light squares are divisible by 2 when you add their row and column
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col)%2)]
            p.draw.rect(screen, color, p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # Based on the value we are taking from the board in engine.py put the corresponding image
            piece = board[row][col]
            if piece != "xx":
                # Image needs to be added in these squares
                screen.blit(IMAGES[piece], p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected !=():
        r,c = sqSelected
        if gs.board[r][c][0]==('w' if gs.whiteToPlay else 'b'):
            s=p.Surface((SQUARE_SIZE,SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQUARE_SIZE,r*SQUARE_SIZE))
            s.fill(p.Color('yellow'))

            for move in validMoves:

                if move.startRow==r and move.startCol==c:
                    screen.blit(s,(move.endCol*SQUARE_SIZE,move.endRow*SQUARE_SIZE))



def drawGameState(screen, gs,validMoves,sqSelected,moveLogFont):
    # First draw board, then pieces since the pieces get covered if done the other way around
    # Draw the squares on the chessboard
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    # Add the piece images onto the board
    drawPieces(screen, gs.board)
    drawMoveLog(screen,gs,moveLogFont)

def drawEndGameText(screen,text):
    font=p.font.SysFont("Arial",32,True,False)
    textObject=font.render(text,0,p.Color('Black'))
    textLocation=p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2,HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject=font.render(text,0,p.Color('Gray'))
    screen.blit(textObject,textLocation.move(2,2))

def drawMoveLog(screen,gs,font):
    moveLogRect = p.Rect(WIDTH,0,MOVE_LOG_PANEL_WIDTH,MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen,p.Color('black'),moveLogRect)
    moveLog=gs.moveLog
    moveTexts = []
    for i in range (0,len(moveLog),2):
        moveString = str(i//2 + 1)+". "+str(moveLog[i])+" "
        if i+1 <len(moveLog): #To ensure Black made a move
            moveString+=str(moveLog[i+1])
        moveTexts.append(moveString)

    padding =5
    textY=padding
    lineSpacing=2
    movesPerRow=3

    for i in range (0,len(moveTexts),movesPerRow):

        text=""
        for j in range(movesPerRow):
            if i+j<len(moveTexts):
                text+=moveTexts[i+j]+" "

        textObject=font.render(text,True,p.Color('white'))
        textLocation=moveLogRect.move(padding ,textY)
        screen.blit(textObject,textLocation)
        textY+= textObject.get_height() + lineSpacing
def main():
    screen = p.display.set_mode((WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    # Get the list of all the valid moves
    validMoves = gs.findValidMoves()
    moveMade = False
    loadImages()
    # print(gs.board) works!
    # Keep track of selected square - row and column
    selected_square = ()
    # 2 tuples containing the selected piece's current location and where the user moves it to
    player_clicks = []

    playerOne=True #True When it is Human for White
    playerTwo=False #False when AI is playing for Black

    moveLogFont=p.font.SysFont("Helvitca",20,False,False)

    flag = True

    gameOver=False
    while flag:
        humanTurn = (gs.whiteToPlay and playerOne) or (not gs.whiteToPlay and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                flag = False
            elif e.type == p.KEYDOWN:
                # Undo functionality - press z key
                if e.key == p.K_z:
                    gs.undoMove()
                    if not playerTwo :
                        gs.undoMove()
                    moveMade = True
                    gameOver=False
                
                if e.key == p.K_r: #for reset
                    gs=chessEngine.GameState()
                    validMoves=gs.findValidMoves()
                    selected_square=()
                    player_clicks=[]
                    moveMade=False
                    gameOver=False

            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    # Grab the mouse location to move the piece
                    location = p.mouse.get_pos()
                    col = location[0]//SQUARE_SIZE
                    row = location[1]//SQUARE_SIZE
                    # Do not let the user click the same square twice
                    # If the action occurs, undo the move
                    if selected_square == (row, col) or col>=8:
                        selected_square = ()
                        player_clicks = []
                    else:
                        selected_square = (row, col)
                        player_clicks.append(selected_square)

                    # After the second click, perform the move and reset the player_clicks
                    if len(player_clicks) == 2:
                        move = chessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                            # if move in validMoves:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                # Reset the move clicks so length becomes 0 again
                                selected_square = ()
                                player_clicks = []
                        if not moveMade:
                            player_clicks = [selected_square]

        #AI Move Finder Logic

        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMoveMinMax(gs, validMoves)
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)

            gs.makeMove(AIMove)
            moveMade = True

        if moveMade:
            # Generate a new set of valid moves after move is made
            validMoves = gs.findValidMoves()
            moveMade = False


        drawGameState(screen, gs,validMoves,selected_square,moveLogFont)

        if gs.checkmate:
            gameOver=True
            if gs.whiteToPlay:
                drawEndGameText(screen,'BLACK WINS by CHECKMATE')
            else:
                drawEndGameText(screen,'WHITE WINS by CHECKMATE')
        elif gs.stalemate:
            gameOver=True
            drawEndGameText(screen,'Draw By STALEMATE')

        clock.tick(20) # Kept 20 Frames per second
        p.display.flip()



if __name__ == "__main__":
    main()