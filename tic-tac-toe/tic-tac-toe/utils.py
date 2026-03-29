import copy


PLAYER_X = "X"
PLAYER_O = "O"


def is_free_to_mark(board, movement):
    if board[movement[1]][movement[0]] == None:
        return True
    else:        
        return False


def players(board):
    """
    Returns the player who must move in state s
    """
    contar = 0
    for i in board:
        for j in i:
            if j != None:
                contar += 1
    if contar % 2 == 0 or contar == 0:
        return PLAYER_X
    else:        
        return PLAYER_O    


def actions(board):
    """
    Returns the legal moves in state s
    """
    Lista = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == None:
                Lista.append((j, i))
    return Lista


def result(board, action):
    """
    Returns the state after taking action a in state s
    """
    board = copy.deepcopy(board)
    board[action[1]][action[0]] = players(board)
    return board


def terminal(board):
    """
    Checks whether state s is a terminal state
    """
    # diagonales 
    if board[0][0] == PLAYER_X and board[1][1] == PLAYER_X and board[2][2] == PLAYER_X:
        return True
    if board[0][0] == PLAYER_O and board[1][1] == PLAYER_O and board[2][2] == PLAYER_O:
        return True
    if board[0][2] == PLAYER_X and board[1][1] == PLAYER_X and board[2][0] == PLAYER_X:
        return True
    if board[0][2] == PLAYER_O and board[1][1] == PLAYER_O and board[2][0] == PLAYER_O:
        return True
    count = 0
    for i in board:
        if board[0][count] == PLAYER_X and board[1][count] == PLAYER_X and board[2][count] == PLAYER_X:
            return True 
        if board[0][count] == PLAYER_O and board[1][count] == PLAYER_O and board[2][count] == PLAYER_O:
            return True
        count += 1
        if i[0] == PLAYER_X and i[1] == PLAYER_X and i[2] == PLAYER_X:
            return True
        if i[0] == PLAYER_O and i[1] == PLAYER_O and i[2] == PLAYER_O:
            return True
    for i in board:
        for j in i:
            if j == None:
                return False   
    return True 


def utility(board):
    """
    Final numeric value for terminal state s
    """
    # diagonales 
    if board[0][0] == PLAYER_X and board[1][1] == PLAYER_X and board[2][2] == PLAYER_X:
        return 1
    if board[0][0] == PLAYER_O and board[1][1] == PLAYER_O and board[2][2] == PLAYER_O:
        return -1
    if board[0][2] == PLAYER_X and board[1][1] == PLAYER_X and board[2][0] == PLAYER_X:
        return 1
    if board[0][2] == PLAYER_O and board[1][1] == PLAYER_O and board[2][0] == PLAYER_O:
        return -1
    count = 0
    for i in board:
        if board[0][count] == PLAYER_X and board[1][count] == PLAYER_X and board[2][count] == PLAYER_X:
            return 1 
        if board[0][count] == PLAYER_O and board[1][count] == PLAYER_O and board[2][count] == PLAYER_O:
            return -1
        count += 1
        if i[0] == PLAYER_X and i[1] == PLAYER_X and i[2] == PLAYER_X:
            return 1
        if i[0] == PLAYER_O and i[1] == PLAYER_O and i[2] == PLAYER_O:
            return -1

    return 0