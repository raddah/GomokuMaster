#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick benchmark script for comparing the performance of the Gomoku AI implementations
Uses fewer trials and lower difficulty levels for faster results
"""

import time
import random
from gomoku import Gomoku

def benchmark_ai_move(board_size=15, difficulty=3, num_trials=3):
    """
    Benchmark the AI move performance
    
    Args:
        board_size (int): Size of the board
        difficulty (int): AI difficulty level
        num_trials (int): Number of trials to run
        
    Returns:
        float: Average time per move in seconds
    """
    print(f"Benchmarking AI move (board_size={board_size}, difficulty={difficulty}, trials={num_trials})...")
    
    total_time = 0
    successful_trials = 0
    
    for trial in range(num_trials):
        try:
            # Create a new game
            print(f"  Creating game with board_size={board_size}, difficulty={difficulty}")
            game = Gomoku(board_size=board_size, difficulty=difficulty)
            print(f"  Game created successfully. Current player: {game.current_player}")
        except Exception as e:
            print(f"  Error creating game: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
        
        # Make some random moves to create a non-empty board
        num_moves = min(3, board_size * board_size // 4)  # Make at most 25% of the board filled
        print(f"  Making {num_moves} random moves")
        
        moves_made = 0
        for _ in range(num_moves):
            empty_cells = []
            for i in range(board_size):
                for j in range(board_size):
                    if game.board[i][j] == 0:  # 0 represents an empty cell
                        empty_cells.append((i, j))
            
            if not empty_cells:
                print("  No empty cells found")
                break
                
            row, col = random.choice(empty_cells)
            try:
                print(f"  Making move at ({row}, {col})")
                game.make_move((row, col))  # Pass as tuple
                moves_made += 1
                print(f"  Move made successfully. Current player: {game.current_player}")
            except Exception as e:
                print(f"  Error making move: {str(e)}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"  Made {moves_made} random moves")
        
        # Make sure it's AI's turn
        print(f"  Checking if it's AI's turn. Current player: {game.current_player}")
        if game.current_player != 2:  # 2 represents the AI player
            try:
                print("  It's not AI's turn. Making one more move to switch to AI's turn.")
                # Make one more move to switch to AI's turn
                empty_cells = []
                for i in range(board_size):
                    for j in range(board_size):
                        if game.board[i][j] == 0:  # 0 represents an empty cell
                            empty_cells.append((i, j))
                
                if empty_cells:
                    row, col = random.choice(empty_cells)
                    print(f"  Making move at ({row}, {col}) to switch to AI's turn")
                    game.make_move((row, col))  # Pass as tuple
                    print(f"  Move made successfully. Current player: {game.current_player}")
                else:
                    print("  No empty cells found to make a move")
                    continue
            except Exception as e:
                print(f"  Error making move to switch to AI's turn: {str(e)}")
                import traceback
                traceback.print_exc()
                # If the move is invalid, skip this trial
                continue
        
        # Measure the time it takes for the AI to make a move
        start_time = time.time()
        try:
            print(f"  Getting AI move. Players: {game.players}")
            # Get AI move using the AI player's ask_move method
            ai_move = game.players[1].ask_move(game)
            print(f"  AI move: {ai_move}")
            # Make the AI move
            game.make_move(ai_move)
            end_time = time.time()
            move_time = end_time - start_time
            total_time += move_time
            successful_trials += 1
            print(f"  Trial {trial + 1}: {move_time:.4f} seconds")
        except Exception as e:
            print(f"  Trial {trial + 1}: Error - {str(e)}")
            import traceback
            traceback.print_exc()  # Print the full traceback for debugging
            # Skip this trial
            continue
    
    # Calculate the average time
    if successful_trials > 0:
        avg_time = total_time / successful_trials
        print(f"Average time: {avg_time:.4f} seconds")
        return avg_time
    else:
        print("No successful trials")
        return None

def run_benchmarks():
    """Run benchmarks for different board sizes and difficulty levels"""
    results = {}
    
    # Test different board sizes with lower difficulty levels
    for board_size in [9, 15]:
        # Test different difficulty levels
        for difficulty in [1, 2, 3]:
            key = f"board_size={board_size}, difficulty={difficulty}"
            results[key] = benchmark_ai_move(board_size=board_size, difficulty=difficulty, num_trials=3)
            print()  # Add a blank line between benchmarks
    
    # Print summary
    print("\nBenchmark Summary:")
    print("-----------------")
    for key, value in results.items():
        if value is not None:
            print(f"{key}: {value:.4f} seconds")
        else:
            print(f"{key}: No successful trials")

if __name__ == "__main__":
    run_benchmarks()
