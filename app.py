from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Import the game module
from gomoku import Gomoku, Player

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
        result = game.make_move(row, col)
        
        response = {
            'valid': True,
            'board': [[cell.value for cell in row] for row in game.board],
            'gameOver': game.game_over,
            'winner': game.winner.value if game.winner else None,
            'message': 'Move successful'
        }
        
        # If playing against AI and the game is not over, make AI move
        if data.get('opponent') == 'ai' and not game.game_over:
            ai_row, ai_col = game.ai_move()
            response['aiMove'] = {'row': ai_row, 'col': ai_col}
            response['board'] = [[cell.value for cell in row] for row in game.board]
            response['gameOver'] = game.game_over
            response['winner'] = game.winner.value if game.winner else None
        
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting Gomoku Master server on port {port}")
    print(f"Open http://localhost:{port} in your browser to play")
    app.run(host='0.0.0.0', port=port, debug=True)
