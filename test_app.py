import pytest
from app import app, PuzzleGame
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def game():
    return PuzzleGame()

def test_index_route(client):
    """Test if the index route returns the game page"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Sliding Puzzle' in response.data

def test_new_game_route(client):
    """Test if new game route returns valid game state"""
    response = client.get('/new-game')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'puzzle' in data
    assert 'moves' in data
    assert 'time' in data
    assert 'difficulty' in data
    assert data['moves'] == 0

def test_move_route(client):
    """Test if move route handles valid moves"""
    # First get a new game state
    response = client.get('/new-game')
    data = json.loads(response.data)
    
    # Find empty tile and a valid adjacent position
    empty_pos = data['puzzle'].index(None)
    # Make a move to position 0 (if possible)
    response = client.get('/move/0')
    assert response.status_code == 200
    new_data = json.loads(response.data)
    assert 'puzzle' in new_data
    assert 'moves' in new_data

def test_game_initialization():
    """Test PuzzleGame class initialization"""
    game = PuzzleGame()
    assert game.size == 3
    assert game.moves == 0
    assert game.difficulty == "medium"
    assert len(game.board) == 9
    assert None in game.board

def test_game_difficulty_setting(game):
    """Test difficulty level setting"""
    game.set_difficulty("easy")
    assert game.difficulty == "easy"
    assert game.moves == 0
    
    game.set_difficulty("hard")
    assert game.difficulty == "hard"
    assert game.moves == 0

def test_game_move_mechanics(game):
    """Test game movement mechanics"""
    initial_board = game.board.copy()
    empty_pos = game.board.index(None)
    
    # Get possible moves
    possible_moves = game.get_possible_moves(empty_pos)
    
    # Try a valid move
    if possible_moves:
        move_pos = possible_moves[0]
        initial_value = game.board[move_pos]
        
        # Make the move
        success = game.make_move(move_pos)
        assert success
        assert game.moves == 1
        assert game.board[empty_pos] == initial_value
        assert game.board[move_pos] is None

def test_game_solved_state():
    """Test win condition detection"""
    game = PuzzleGame()
    # Set up a solved board
    game.board = list(range(1, 9)) + [None]
    assert game.is_solved()
    
    # Modify board to be unsolved
    game.board[0], game.board[1] = game.board[1], game.board[0]
    assert not game.is_solved()

def test_invalid_difficulty(game):
    """Test setting invalid difficulty level"""
    original_difficulty = game.difficulty
    game.set_difficulty("invalid")
    assert game.difficulty == original_difficulty

def test_elapsed_time(game):
    """Test elapsed time calculation"""
    initial_time = game.get_elapsed_time()
    assert isinstance(initial_time, int)
    assert initial_time >= 0
