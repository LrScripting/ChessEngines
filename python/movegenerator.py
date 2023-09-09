from copy import deepcopy


class cockFish:
    def __init__(self):
        self.board = [
        [{'square': 'black', 'piece': 'brook'}, {'square': 'white', 'piece': 'bknight'}, {'square': 'black', 'piece': 'bbishop'}, {'square': 'white', 'piece': 'bqueen'}, {'square': 'black', 'piece': 'bking'}, {'square': 'white', 'piece': 'bbishop'}, {'square': 'black', 'piece': 'bknight'}, {'square': 'white', 'piece': 'brook'}],
        [{'square': 'white', 'piece': 'bpawn'}, {'square': 'black', 'piece': 'bpawn'}, {'square': 'white', 'piece': 'bpawn'}, {'square': 'black', 'piece': 'bpawn'}, {'square': 'white', 'piece': 'bpawn'}, {'square': 'black', 'piece': 'bpawn'}, {'square': 'white', 'piece': 'bpawn'}, {'square': 'black', 'piece': 'bpawn'}],
        [{'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}],
        [{'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}],
        [{'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}],
        [{'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'empty'}],
        [{'square': 'black', 'piece': 'wpawn'}, {'square': 'white', 'piece': 'wpawn'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'wpawn'}, {'square': 'black', 'piece': 'wpawn'}, {'square': 'white', 'piece': 'wpawn'}, {'square': 'black', 'piece': 'wpawn'}, {'square': 'white', 'piece': 'wpawn'}],
        [{'square': 'white', 'piece': 'wrook'}, {'square': 'black', 'piece': 'wknight'}, {'square': 'white', 'piece': 'wbishop'}, {'square': 'black', 'piece': 'wqueen'}, {'square': 'white', 'piece': 'wking'}, {'square': 'black', 'piece': 'empty'}, {'square': 'white', 'piece': 'empty'}, {'square': 'black', 'piece': 'wrook'}]
        ]
        self.lastMove = None

        self.possibleMoves = []
        self.inCheck = False
        self.castle = {"king": True, "leftRook": True, "rightRook": True}

    def flipboard(self, board):
        flipped = []
        for i in range(8):
            flipped.append(list(reversed(board[7-i])))
        return flipped
    
    

    def getPawnRange(self, board, color, pos):
        moves = []

        #define player starting pieces
        playerDirection = -1 if color == 'w' else 1
        enemyColor = 'b' if color == 'w' else 'w'
        startRow = 6 if color == 'w' else 1

        if 0 <= pos[0] + playerDirection < 8 and board[pos[0]+playerDirection][pos[1]]['piece'] == "empty":
            moves.append([pos, [pos[0]+playerDirection, pos[1]]])

            # 2 squarer  
            if pos[0] == startRow and 0 <= pos[0] + 2*playerDirection < 8 and board[pos[0]+2*playerDirection][pos[1]]['piece'] == "empty":
                moves.append([pos, [pos[0]+2*playerDirection, pos[1]]])

        # Capture moves
        for delta in [-1, 1]:
            diagonalColumn = pos[1] + delta
            if 0 <= diagonalColumn< 8 and board[pos[0]+playerDirection][diagonalColumn]['piece'].startswith(enemyColor):
                moves.append([pos, [pos[0]+playerDirection, diagonalColumn]])

        # avant Garde
        if self.lastMove:
            moveDiff = self.lastMove[1] - self.lastMove[0]
            expectedDiff = 2 if color == 'w' else - 2
            if moveDiff == expectedDiff and self.lastMove[2] == enemyColor + 'Pawn':
                if self.lastMove[3] == pos[1]-1:
                    moves.append([pos, [pos[0]+playerDirection, pos[1]-1]])
                if self.lastMove[3] == pos[1]+1:
                    moves.append([pos, [pos[0]+playerDirection, pos[1]+1]])


        return moves
        
    #pos is an array of row and column pos
    #player color is 'w' or 'b'
    def getHorseRange(self, pos, board, playerColor):
        moves = []
        squares = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]  # Possible moves for the knight
        for square in squares:
            newRow = pos[0] + square[0]
            newCol = pos[1] + square[1]
            if 0 <= newRow < 8 and 0 <= newCol < 8 and board[newRow][newCol]['piece'][0] != playerColor:
                moves.append([pos, [newRow, newCol]])
        return moves
    
    def getRookRange(self, pos, board, playerColor):
        moves = []

        # Moving up
        for i in range(pos[0] - 1, -1, -1):
            if board[i][pos[1]]['piece'] == 'empty':
                moves.append([pos,[i, pos[1]]])
            elif board[i][pos[1]]['piece'][0] != playerColor:
                moves.append([pos, [i, pos[1]]])
                break
            else:
                break

        # Moving down
        for i in range(pos[0] + 1, 8):
            if board[i][pos[1]]['piece'] == 'empty':
                moves.append([pos, [i, pos[1]]])
            elif board[i][pos[1]]['piece'][0] != playerColor:
                moves.append([pos, [i, pos[1]]])
                break
            else:
                break

        # Moving left
        for i in range(pos[1] - 1, -1, -1):
            if board[pos[0]][i]['piece'] == 'empty':
                moves.append([pos, [pos[0], i]])
            elif board[pos[0]][i]['piece'][0] != playerColor:
                moves.append([pos, [pos[0], i]])
                break
            else:
                break

        # Moving right
        for i in range(pos[1] + 1, 8):
            if board[pos[0]][i]['piece'] == 'empty':
                moves.append([pos, [pos[0], i]])
            elif board[pos[0]][i]['piece'][0] != playerColor:
                moves.append([pos, [pos[0], i]])
                break
            else:
                break

        return moves
    def getQueenRange(self, pos, board, playerColor):
        moves = []
        i, j = pos[0] - 1, pos[1] - 1
        while i >= 0 and j >= 0:
            if board[i][j]['piece'] == 'empty':
                moves.append([pos, [i, j]])
            elif board[i][j]['piece'][0] != playerColor:
                moves.append([pos, [i, j]])
                break
            else:
                break
            i -= 1
            j -= 1

        # Moving up and to the right
        i, j = pos[0] - 1, pos[1] + 1
        while i >= 0 and j < 8:
            if board[i][j]['piece'] == 'empty':
                moves.append([pos, [i, j]])
            elif board[i][j]['piece'][0] != playerColor:
                moves.append([pos, [i, j]])
                break
            else:
                break
            i -= 1
            j += 1

        # Moving down and to the left
        i, j = pos[0] + 1, pos[1] - 1
        while i < 8 and j >= 0:
            if board[i][j]['piece'] == 'empty':
                moves.append([pos, [i, j]])
            elif board[i][j]['piece'][0] != playerColor:
                moves.append([pos, [i, j]])
                break
            else:
                break
            i += 1
            j -= 1

        # Moving down and to the right
        i, j = pos[0] + 1, pos[1] + 1
        while i < 8 and j < 8:
            if board[i][j]['piece'] == 'empty':
                moves.append([pos, [i, j]])
            elif board[i][j]['piece'][0] != playerColor:
                moves.append([pos, [i, j]])
                break
            else:
                break
            i += 1
            j += 1
        # Moving up
        for i in range(pos[0] - 1, -1, -1):
            if board[i][pos[1]]['piece'] == 'empty':
                moves.append([pos, [i, pos[1]]])
            elif board[i][pos[1]]['piece'][0] != playerColor:
                moves.append([pos, [i, pos[1]]])
                break
            else:
                break

        # Moving down
        for i in range(pos[0] + 1, 8):
            if board[i][pos[1]]['piece'] == 'empty':
                moves.append([pos, [i, pos[1]]])
            elif board[i][pos[1]]['piece'][0] != playerColor:
                moves.append([pos, [i, pos[1]]])
                break
            else:
                break

        # Moving left
        for i in range(pos[1] - 1, -1, -1):
            if board[pos[0]][i]['piece'] == 'empty':
                moves.append([pos, [pos[0], i]])
            elif board[pos[0]][i]['piece'][0] != playerColor:
                moves.append([pos, [pos[0], i]])
                break
            else:
                break

        # Moving right
        for i in range(pos[1] + 1, 8):
            if board[pos[0]][i]['piece'] == 'empty':
                moves.append([pos, [pos[0], i]])
            elif board[pos[0]][i]['piece'][0] != playerColor:
                moves.append([pos, [pos[0], i]])
                break
            else:
                break

        return moves
    def getBishopRange(self, pos, board, playerColor):
        moves = []

        # Bishop-style movements (diagonal)

        # Moving up and to the left
        i, j = pos[0] - 1, pos[1] - 1
        while i >= 0 and j >= 0:
            if board[i][j]['piece'] == 'empty':
                moves.append([pos, [i, j]])
            elif board[i][j]['piece'][0] != playerColor:
                moves.append([pos, [i, j]])
                break
            else:
                break
            i -= 1
            j -= 1

        # Moving up and to the right
        i, j = pos[0] - 1, pos[1] + 1
        while i >= 0 and j < 8:
            if board[i][j]['piece'] == 'empty':
                moves.append([pos, [i, j]])
            elif board[i][j]['piece'][0] != playerColor:
                moves.append([pos, [i, j]])
                break
            else:
                break
            i -= 1
            j += 1

        # Moving down and to the left
        i, j = pos[0] + 1, pos[1] - 1
        while i < 8 and j >= 0:
            if board[i][j]['piece'] == 'empty':
                moves.append([pos, [i, j]])
            elif board[i][j]['piece'][0] != playerColor:
                moves.append([pos, [i, j]])
                break
            else:
                break
            i += 1
            j -= 1

        # Moving down and to the right
        i, j = pos[0] + 1, pos[1] + 1
        while i < 8 and j < 8:
            if board[i][j]['piece'] == 'empty':
                moves.append([pos, [i, j]])
            elif board[i][j]['piece'][0] != playerColor:
                moves.append([pos, [i, j]])
                break
            else:
                break
            i += 1
            j += 1

        return moves

    def getKingRange(self, pos, leftCastlePos, rightCastlePos,  board, playerColor):
        moves = []
        print(pos)
        potentialMoves = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1, 1), (1, -1), (-1,-1)]
        for move in potentialMoves:
            newRow, newCol = pos[0] + move[0], pos[1] + move[1]
            print(f"newcol:  {newCol} newRow: {newRow} currentRow{pos[0]}, currentCol {pos[1]}")
            if 0 <= newRow < 8 and 0 <= newCol < 8:  # Ensure the move is within the board
                if board[newRow][newCol]["piece"] == 'empty' or board[newRow][newCol]['piece'][0] != playerColor:
                    moves.append([pos, [newRow, newCol]])

        #castle logic 
        if self.castle['king'] and self.castle['leftRook']  and (board[leftCastlePos[0]][leftCastlePos[1]+1]['piece'] == "empty" and board[leftCastlePos[0]][leftCastlePos[1]+2]['piece'] == 'empty'):
            moves.append([[pos, [pos[0], pos[1]-2]], [leftCastlePos, [leftCastlePos[0], leftCastlePos[1] +3]]])
        if self.castle['king'] and self.castle['rightRook'] and [board[rightCastlePos[1]-1], board[rightCastlePos[1]-2]] not in self.getPossibleMoves(self.flipboard(board), 'w' if playerColor=="w" else 'b') and (board[rightCastlePos[0]][rightCastlePos[1]-1]['piece'] == "empty" and board[rightCastlePos[0]][rightCastlePos[1]-2]['piece'] == 'empty'): 
            moves.append([[pos, [pos[0], pos[1]+2]], [rightCastlePos, [rightCastlePos[0], rightCastlePos[1] -3]]])
        return moves

        # when you call possible moves move to class variable 
    def getPossibleMoves(self, board, playerColor):
        possibleMoves = []


        for i in range(8):
            for j in range(8):
                if board[i][j]['piece'].startswith(playerColor):
                    if "pawn" in board[i][j]['piece']:
                        possibleMoves.extend(self.getPawnRange(self.board, playerColor, [i, j]))
                    elif "rook" in board[i][j]['piece']:
                        possibleMoves.extend(self.getRookRange([i, j], board, playerColor))
                    elif "bishop" in board[i][j]['piece']:
                        possibleMoves.extend(self.getBishopRange([i, j], board, playerColor))
                    elif "queen" in board[i][j]['piece']:
                        possibleMoves.extend(self.getQueenRange([i, j], board, playerColor))
                    elif "knight" in board[i][j]['piece']:
                        possibleMoves.extend(self.getHorseRange([i, j], board, playerColor))

        return possibleMoves

    def filterIllegal(self, board, potentialMoves, playerColor, kingPos):
        illegalMoves = []
        for move in potentialMoves:
            
            # Create a deep copy of the board for hypothetical moves
            checkBoard = deepcopy(board)
            pieceMoved = checkBoard[move[0][0]][move[0][1]]['piece']
            checkBoard[move[0][0]][move[0][1]]['piece'] = "empty"
            checkBoard[move[1][0]][move[1][1]]['piece'] = pieceMoved

            # Generate enemy moves based on the hypothetical board
            enemyMoves = self.getPossibleMoves(self.flipboard(checkBoard), "w" if playerColor=="b" else "w")

            # Check if any enemy move can capture the king
            for enemyMove in enemyMoves:
                if kingPos == enemyMove[1]:
                    illegalMoves.append(move)
                    break

        # Remove the illegal moves from the list of potential moves
        for illegalMove in illegalMoves:
            potentialMoves.remove(illegalMove)
        return potentialMoves
    
    def filterKingMoves(self, board, potentialMoves):
        pass

    def generateAndFilter(self):

        possibleMoves = self.getPossibleMoves(self.board, 'w')
        possibleKingMoves = self.getKingRange()
