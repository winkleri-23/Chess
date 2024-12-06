import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 8
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)
HIGHLIGHT_COLOR = (246, 246, 105, 128)  # Semi-transparent yellow
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Load piece images
PIECES = {
    "b_p": pygame.image.load("images/b_pawn.png"),
    "b_r": pygame.image.load("images/b_rook.png"),
    "b_n": pygame.image.load("images/b_knight.png"),
    "b_b": pygame.image.load("images/b_bishop.png"),
    "b_q": pygame.image.load("images/b_queen.png"),
    "b_k": pygame.image.load("images/b_king.png"),
    "w_p": pygame.image.load("images/w_pawn.png"),
    "w_r": pygame.image.load("images/w_rook.png"),
    "w_n": pygame.image.load("images/w_knight.png"),
    "w_b": pygame.image.load("images/w_bishop.png"),
    "w_q": pygame.image.load("images/w_queen.png"),
    "w_k": pygame.image.load("images/w_king.png"),
}

for key in PIECES:
    PIECES[key] = pygame.transform.scale(PIECES[key], (CELL_SIZE, CELL_SIZE))

# Initial chess board
INITIAL_BOARD = [
    ["b_r", "b_n", "b_b", "b_q", "b_k", "b_b", "b_n", "b_r"],
    ["b_p", "b_p", "b_p", "b_p", "b_p", "b_p", "b_p", "b_p"],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ["w_p", "w_p", "w_p", "w_p", "w_p", "w_p", "w_p", "w_p"],
    ["w_r", "w_n", "w_b", "w_q", "w_k", "w_b", "w_n", "w_r"],
]

# Helper function to copy the board
def copy_board(board):
    return [row[:] for row in board]

def draw_board():
    """Draws the chessboard."""
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(SCREEN, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_pieces(board):
    """Draws the pieces on the board."""
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                SCREEN.blit(PIECES[piece], (col * CELL_SIZE, row * CELL_SIZE))

def draw_highlight(moves):
    """Highlights valid moves."""
    for move in moves:
        row, col = move
        pygame.draw.rect(SCREEN, HIGHLIGHT_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), border_radius=10)

def get_valid_moves(board, piece, pos, check_safety=True):
    """Returns valid moves for the selected piece."""
    moves = []
    row, col = pos
    piece_type = piece[2]
    color = piece[0]

    directions = {
        "p": [(-1, 0)] if color == "w" else [(1, 0)],
        "r": [(-1, 0), (1, 0), (0, -1), (0, 1)],
        "b": [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        "q": [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)],
        "k": [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)],
        "n": [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (2, -1), (2, 1), (1, -2), (1, 2)],
    }

    if piece_type == "p":  # Pawn movement
        direction = directions["p"][0]
        next_row, next_col = row + direction[0], col + direction[1]

        # Single step forward
        if 0 <= next_row < 8 and board[next_row][next_col] is None:
            moves.append((next_row, next_col))

            # Double step forward (only from the starting position)
            start_row = 6 if color == "w" else 1
            next_row_double = next_row + direction[0]
            if row == start_row and board[next_row_double][next_col] is None:
                moves.append((next_row_double, next_col))

        # Diagonal captures
        for attack in [(-1, -1), (-1, 1)] if color == "w" else [(1, -1), (1, 1)]:
            next_row, next_col = row + attack[0], col + attack[1]
            if 0 <= next_row < 8 and 0 <= next_col < 8:
                if board[next_row][next_col] and board[next_row][next_col][0] != color:
                    moves.append((next_row, next_col))
        return filter_safe_moves(board, moves, pos, color) if check_safety else moves

    for d in directions.get(piece_type, []):
        next_row, next_col = row + d[0], col + d[1]
        while 0 <= next_row < 8 and 0 <= next_col < 8:
            if board[next_row][next_col] is None:
                moves.append((next_row, next_col))
            elif board[next_row][next_col][0] != color:
                moves.append((next_row, next_col))
                break
            else:
                break
            if piece_type in ["k", "n"]:
                break
            next_row, next_col = next_row + d[0], next_col + d[1]
    return filter_safe_moves(board, moves, pos, color) if check_safety else moves


def filter_safe_moves(board, moves, pos, color):
    """Filters out moves that would leave the king in check."""
    safe_moves = []
    for move in moves:
        new_board = copy_board(board)
        new_board[pos[0]][pos[1]] = None
        new_board[move[0]][move[1]] = board[pos[0]][pos[1]]
        if not is_check(new_board, color):
            safe_moves.append(move)
    return safe_moves

def is_check(board, color):
    """Checks if the king of the given color is in check."""
    king_pos = None
    for row in range(8):
        for col in range(8):
            if board[row][col] == f"{color}_k":
                king_pos = (row, col)
                break
        if king_pos:
            break

    opponent_color = "b" if color == "w" else "w"
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece[0] == opponent_color:
                if king_pos in get_valid_moves(board, piece, (row, col), check_safety=False):
                    return True
    return False

def is_checkmate(board, color):
    """Checks if the king of the given color is in checkmate."""
    if not is_check(board, color):
        return False
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece[0] == color:
                valid_moves = get_valid_moves(board, piece, (row, col))
                if valid_moves:
                    return False
    return True

def main():
    clock = pygame.time.Clock()
    board = copy_board(INITIAL_BOARD)
    selected_piece = None
    selected_pos = None
    turn = "w"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // CELL_SIZE, y // CELL_SIZE

                if selected_piece:
                    if (row, col) in get_valid_moves(board, selected_piece, selected_pos):
                        board[selected_pos[0]][selected_pos[1]] = None
                        board[row][col] = selected_piece
                        selected_piece = None

                        if is_checkmate(board, "b" if turn == "w" else "w"):
                            print(f"Checkmate! {turn} wins!")
                            pygame.quit()
                            sys.exit()

                        turn = "b" if turn == "w" else "w"
                    else:
                        selected_piece = None
                else:
                    if board[row][col] and board[row][col][0] == turn:
                        selected_piece = board[row][col]
                        selected_pos = (row, col)

        draw_board()
        if selected_piece:
            draw_highlight(get_valid_moves(board, selected_piece, selected_pos))
        draw_pieces(board)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
