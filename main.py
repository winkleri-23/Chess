import pygame
import sys

# Inicializace Pygame
pygame.init()

# Konstanty
WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 8
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Šachy")

# Načtení obrázků figurek
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

# Základní šachovnice
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

# Funkce pro vykreslení šachovnice
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(SCREEN, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Funkce pro vykreslení figurek
def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                SCREEN.blit(PIECES[piece], (col * CELL_SIZE, row * CELL_SIZE))

# Hlavní smyčka hry
def main():
    clock = pygame.time.Clock()
    board = [row[:] for row in INITIAL_BOARD]
    selected_piece = None
    selected_pos = None
    turn = "w"  # bílý začíná

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // CELL_SIZE, y // CELL_SIZE

                if selected_piece:
                    # Přesun figury
                    if (row, col) != selected_pos:
                        board[selected_pos[0]][selected_pos[1]] = None
                        board[row][col] = selected_piece
                        turn = "b" if turn == "w" else "w"  # střídání hráčů
                    selected_piece = None
                else:
                    # Výběr figury
                    if board[row][col] and board[row][col][0] == turn:
                        selected_piece = board[row][col]
                        selected_pos = (row, col)

        # Vykreslení
        draw_board()
        draw_pieces(board)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
