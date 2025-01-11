from flask import Flask, render_template, jsonify, request
import random
import time

app = Flask(__name__)

class PuzzleGame:
    def __init__(self):
        self.size = 3
        self.board = None
        self.moves = 0
        self.start_time = None
        self.difficulty = "medium"
        self.new_game()

    def new_game(self):
        self.board = list(range(1, self.size * self.size)) + [None]
        self.moves = 0
        self.start_time = time.time()
        self.shuffle()

    def shuffle(self):
        moves = {"easy": 20, "medium": 40, "hard": 100}
        shuffle_moves = moves.get(self.difficulty, 40)
        
        # Get the empty tile position
        empty_pos = len(self.board) - 1
        
        for _ in range(shuffle_moves):
            possible_moves = self.get_possible_moves(empty_pos)
            if possible_moves:
                move = random.choice(possible_moves)
                # Swap empty tile with chosen position
                self.board[empty_pos], self.board[move] = self.board[move], self.board[empty_pos]
                empty_pos = move

    def get_possible_moves(self, empty_pos):
        moves = []
        row = empty_pos // self.size
        col = empty_pos % self.size

        # Check all adjacent positions (up, down, left, right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row = row + dr
            new_col = col + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                moves.append(new_row * self.size + new_col)
        return moves

    def make_move(self, position):
        empty_pos = self.board.index(None)
        if position in self.get_possible_moves(empty_pos):
            self.board[empty_pos], self.board[position] = self.board[position], self.board[empty_pos]
            self.moves += 1
            return True
        return False

    def is_solved(self):
        solution = list(range(1, self.size * self.size)) + [None]
        return self.board == solution

    def get_elapsed_time(self):
        if self.start_time:
            return int(time.time() - self.start_time)
        return 0

    def set_difficulty(self, difficulty):
        if difficulty in ["easy", "medium", "hard"]:
            self.difficulty = difficulty
            self.new_game()

# Create a global game instance
game = PuzzleGame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new-game')
def new_game():
    difficulty = request.args.get('difficulty', 'medium')
    game.set_difficulty(difficulty)
    return get_game_state()

@app.route('/move/<int:position>')
def make_move(position):
    game.make_move(position)
    return get_game_state()

@app.route('/state')
def get_game_state():
    return jsonify({
        'puzzle': game.board,
        'moves': game.moves,
        'time': game.get_elapsed_time(),
        'solved': game.is_solved(),
        'difficulty': game.difficulty
    })

if __name__ == '__main__':
    app.run(debug=True)
