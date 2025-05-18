from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Import the game module - use explicit import with full path
import gomoku
from gomoku import Gomoku

app = Flask(__name__, static_folder='static')
CORS(app)

# Store active games
games = {}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/new_game', methods=['POST'])
def new_game():
    data = request.json
    board_size = data.get('boardSize', 15)
    difficulty = data.get('difficulty', 3)
    
    game_id = str(len(games) + 1)
    games[game_id] = Gomoku(board_size=board_size, difficulty=difficulty)
    
    return jsonify({
        'gameId': game_id,
        'boardSize': board_size,
        'message': 'Game created successfully'
    })

@app.route('/api/make_move', methods=['POST'])
def make_move():
    data = request.json
    game_id = data.get('gameId')
    row = data.get('row')
    col = data.get('col')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    # Make the player's move
    try:
        # In gomoku.py, make_move expects a tuple (row, col)
        game.make_move((row, col))
        
        # Check if the game is over after the player's move
        game_over = game.is_over()
        # Determine the winner (if any)
        winner = None
        if game_over and game.lose():  # If the game is over and the current player lost
            winner = 3 - game.current_player  # The winner is the other player
        
        response = {
            'valid': True,
            'board': [[cell for cell in row] for row in game.board],  # Board is a 2D array of integers
            'gameOver': game_over,
            'winner': winner,
            'message': 'Move successful'
        }
        
        # If playing against AI and the game is not over, make AI move
        if data.get('opponent') == 'ai' and not game_over:
            # Switch to AI player (player 2)
            game.current_player = 2
            # Get AI move using the AI player's ask_move method
            ai_move = game.players[1].ask_move(game)
            ai_row, ai_col = ai_move
            # Make the AI move
            game.make_move(ai_move)
            
            # Check if the game is over after the AI's move
            game_over = game.is_over()
            # Determine the winner (if any)
            winner = None
            if game_over and game.lose():  # If the game is over and the current player lost
                winner = 3 - game.current_player  # The winner is the other player
            
            response['aiMove'] = {'row': ai_row, 'col': ai_col}
            response['board'] = [[cell for cell in row] for row in game.board]
            response['gameOver'] = game_over
            response['winner'] = winner
            
            # Switch back to player 1 for the next move
            game.current_player = 1
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'valid': False, 'message': str(e)}), 400

@app.route('/api/reset', methods=['POST'])
def reset_game():
    data = request.json
    game_id = data.get('gameId')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    board_size = data.get('boardSize', 15)
    difficulty = data.get('difficulty', 3)
    
    games[game_id] = Gomoku(board_size=board_size, difficulty=difficulty)
    
    return jsonify({
        'message': 'Game reset successfully',
        'boardSize': board_size
    })

import socket

def find_free_port(start_port=5002, max_attempts=10):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No free port found in range {start_port}-{start_port + max_attempts - 1}")

if __name__ == '__main__':
    # Try to get port from environment, else find a free one
    port = int(os.environ.get('PORT', 0))
    if port == 0:
        try:
            port = find_free_port(5002, 10)
        except RuntimeError as e:
            print(str(e))
            sys.exit(1)
    print(f"Starting Gomoku Master server on port {port}")
    print(f"Open http://localhost:{port} in your browser to play")
    app.run(host='0.0.0.0', port=port, debug=True)
