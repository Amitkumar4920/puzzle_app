import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 400
GRID_SIZE = 3
TILE_SIZE = WINDOW_SIZE // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
FONT_SIZE = 36

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sliding Puzzle")
font = pygame.font.Font(None, FONT_SIZE)

class PuzzleGame:
    def __init__(self):
        self.board = list(range(GRID_SIZE * GRID_SIZE))
        self.empty_cell = GRID_SIZE * GRID_SIZE - 1
        self.shuffle()

    def shuffle(self):
        # Shuffle the board while ensuring it's solvable
        moves = 1000
        for _ in range(moves):
            possible_moves = self.get_possible_moves()
            if possible_moves:
                move = random.choice(possible_moves)
                self.move(move)

    def get_possible_moves(self):
        moves = []
        empty_row = self.empty_cell // GRID_SIZE
        empty_col = self.empty_cell % GRID_SIZE

        # Check all possible moves (up, down, left, right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row = empty_row + dr
            new_col = empty_col + dc
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                moves.append(new_row * GRID_SIZE + new_col)
        return moves

    def move(self, position):
        if position in self.get_possible_moves():
            self.board[self.empty_cell], self.board[position] = self.board[position], self.board[self.empty_cell]
            self.empty_cell = position
            return True
        return False

    def is_solved(self):
        return self.board == list(range(GRID_SIZE * GRID_SIZE))

    def draw(self, screen):
        screen.fill(WHITE)
        for i in range(len(self.board)):
            if i != self.empty_cell:
                row = i // GRID_SIZE
                col = i % GRID_SIZE
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                
                pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE - 2, TILE_SIZE - 2))
                number = str(self.board[i] + 1)
                text = font.render(number, True, BLACK)
                text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text, text_rect)

def main():
    game = PuzzleGame()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                position = row * GRID_SIZE + col
                game.move(position)

                if game.is_solved():
                    print("Congratulations! Puzzle solved!")

        game.draw(screen)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
