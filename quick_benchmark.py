#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick benchmark script for comparing the performance of the Gomoku AI implementations
Uses fewer trials and lower difficulty levels for faster results
"""

import time
import random
from gomoku import Gomoku, Player

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
        # Create a new game
        game = Gomoku(board_size=board_size, difficulty=difficulty)
        
        # Make some random moves to create a non-empty board
        num_moves = min(3, board_size * board_size // 4)  # Make at most 25% of the board filled
        
        for _ in range(num_moves):
            empty_cells = []
            for i in range(board_size):
                for j in range(board_size):
                    if game.board[i][j] == Player.NONE:
                        empty_cells.append((i, j))
            
            if not empty_cells:
                break
                
            row, col = random.choice(empty_cells)
            try:
                game.make_move(row, col)
            except Exception:
                # If the move is invalid, try again
                continue
        
        # Make sure it's AI's turn
        if game.current_player != Player.WHITE:
            try:
                # Make one more move to switch to AI's turn
                empty_cells = []
                for i in range(board_size):
                    for j in range(board_size):
                        if game.board[i][j] == Player.NONE:
                            empty_cells.append((i, j))
                
                if empty_cells:
                    row, col = random.choice(empty_cells)
                    game.make_move(row, col)
            except Exception:
                # If the move is invalid, skip this trial
                continue
        
        # Measure the time it takes for the AI to make a move
        start_time = time.time()
        try:
            game.ai_move()
            end_time = time.time()
            move_time = end_time - start_time
            total_time += move_time
            successful_trials += 1
            print(f"  Trial {trial + 1}: {move_time:.4f} seconds")
        except Exception as e:
            print(f"  Trial {trial + 1}: Error - {str(e)}")
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
