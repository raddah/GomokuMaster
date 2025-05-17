<<<<<<< HEAD
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Benchmark script for comparing the performance of the Gomoku AI implementations
"""

import time
import random
from gomoku import Gomoku, Player

def benchmark_ai_move(board_size=15, difficulty=3, num_trials=5):
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
    
    for trial in range(num_trials):
        # Create a new game
        game = Gomoku(board_size=board_size, difficulty=difficulty)
        
        # Make some random moves to create a non-empty board
        num_moves = min(5, board_size * board_size // 4)  # Make at most 25% of the board filled
        
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
            print(f"  Trial {trial + 1}: {move_time:.4f} seconds")
        except Exception as e:
            print(f"  Trial {trial + 1}: Error - {str(e)}")
            # Skip this trial
            continue
    
    # Calculate the average time
    avg_time = total_time / num_trials
    print(f"Average time: {avg_time:.4f} seconds")
    
    return avg_time

def run_benchmarks():
    """Run benchmarks for different board sizes and difficulty levels"""
    results = {}
    
    # Test different board sizes
    for board_size in [9, 15, 19]:
        # Test different difficulty levels
        for difficulty in [1, 3, 5]:
            key = f"board_size={board_size}, difficulty={difficulty}"
            results[key] = benchmark_ai_move(board_size=board_size, difficulty=difficulty)
            print()  # Add a blank line between benchmarks
    
    # Print summary
    print("\nBenchmark Summary:")
    print("-----------------")
    for key, value in results.items():
        print(f"{key}: {value:.4f} seconds")

if __name__ == "__main__":
    run_benchmarks()
=======
"""
Benchmark script for Gomoku AI algorithms.

This script measures the performance of different AI algorithms for the Gomoku game.
It generates graphs and reports to visualize the performance data.
"""

import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from gomoku import Gomoku, Negamax, AI_Player, Human_Player
from easyAI import TranspositionTable

def benchmark_algorithm(algorithm_name, algorithm, board_size=9, num_moves=10, num_runs=3):
    """
    Benchmark an AI algorithm.
    
    Args:
        algorithm_name: The name of the algorithm.
        algorithm: The algorithm to benchmark.
        board_size: The size of the board.
        num_moves: The number of moves to make.
        num_runs: The number of runs to average over.
        
    Returns:
        dict: A dictionary containing the benchmark results.
    """
    print(f"Benchmarking {algorithm_name}...")
    
    # Initialize results
    results = {
        'algorithm': algorithm_name,
        'board_size': board_size,
        'num_moves': num_moves,
        'num_runs': num_runs,
        'move_times': [],
        'total_time': 0,
        'avg_time_per_move': 0,
        'nodes_evaluated': 0,
        'avg_nodes_per_move': 0,
    }
    
    # Run the benchmark multiple times and average the results
    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs}...")
        
        # Create a new game
        ai_player = AI_Player(algorithm)
        human_player = Human_Player(name="Benchmark")
        game = Gomoku(board_size=board_size, players=[human_player, ai_player])
        
        # Make moves
        move_times = []
        for move_num in range(num_moves):
            # Skip if the game is over
            if game.is_over():
                break
                
            # Make a random move for the human player
            human_moves = game.possible_moves()
            if human_moves:
                human_move = human_moves[np.random.randint(0, len(human_moves))]
                game.make_move(human_move)
                game.current_player = 3 - game.current_player
            
            # Skip if the game is over after the human move
            if game.is_over():
                break
                
            # Measure the time it takes for the AI to make a move
            start_time = time.time()
            ai_move = ai_player.ask_move(game)
            end_time = time.time()
            
            # Record the time
            move_time = end_time - start_time
            move_times.append(move_time)
            
            # Make the AI move
            game.make_move(ai_move)
            game.current_player = 3 - game.current_player
        
        # Add the results from this run
        results['move_times'].extend(move_times)
        results['total_time'] += sum(move_times)
        
        # Get the number of nodes evaluated if available
        if hasattr(algorithm, 'tt') and algorithm.tt is not None:
            results['nodes_evaluated'] += len(algorithm.tt)
    
    # Calculate averages
    if results['move_times']:
        results['avg_time_per_move'] = results['total_time'] / len(results['move_times'])
    if results['nodes_evaluated'] > 0:
        results['avg_nodes_per_move'] = results['nodes_evaluated'] / len(results['move_times'])
    
    return results

def run_benchmarks():
    """Run benchmarks for different algorithms and board sizes."""
    # Define the algorithms to benchmark
    algorithms = [
        ('Negamax (depth=1)', Negamax(depth=1, timeout=10)),
        ('Negamax (depth=2)', Negamax(depth=2, timeout=10)),
        ('Negamax (depth=3)', Negamax(depth=3, timeout=10)),
        ('Negamax (depth=4)', Negamax(depth=4, timeout=10)),
        ('Negamax (depth=5)', Negamax(depth=5, timeout=10)),
    ]
    
    # Focus on 9x9 board size for initial benchmarks
    board_sizes = [9]
    
    # Run the benchmarks with fewer runs
    results = []
    for board_size in board_sizes:
        for algorithm_name, algorithm in algorithms:
            result = benchmark_algorithm(
                algorithm_name=algorithm_name,
                algorithm=algorithm,
                board_size=board_size,
                num_moves=5,  # Reduced from 10
                num_runs=1    # Reduced from 3
            )
            results.append(result)
    
    return results

def generate_report(results):
    """
    Generate a report from the benchmark results.
    
    Args:
        results: A list of dictionaries containing the benchmark results.
    """
    # Create a DataFrame from the results
    df = pd.DataFrame(results)
    
    # Print the results
    print("\nBenchmark Results:")
    print(df[['algorithm', 'board_size', 'avg_time_per_move', 'avg_nodes_per_move']])
    
    # Save the results to a CSV file
    df.to_csv('benchmark_results.csv', index=False)
    print("\nResults saved to benchmark_results.csv")
    
    # Generate graphs
    generate_graphs(df)

def generate_graphs(df):
    """
    Generate graphs from the benchmark results.
    
    Args:
        df: A DataFrame containing the benchmark results.
    """
    # Create a figure with multiple subplots
    fig, axes = plt.subplots(2, 1, figsize=(10, 12))
    
    # Plot average time per move vs. algorithm for different board sizes
    for board_size in df['board_size'].unique():
        subset = df[df['board_size'] == board_size]
        axes[0].plot(subset['algorithm'], subset['avg_time_per_move'], marker='o', label=f'Board Size {board_size}')
    
    axes[0].set_title('Average Time per Move vs. Algorithm')
    axes[0].set_xlabel('Algorithm')
    axes[0].set_ylabel('Average Time per Move (seconds)')
    axes[0].legend()
    axes[0].grid(True)
    axes[0].set_xticklabels(df['algorithm'].unique(), rotation=45, ha='right')
    
    # Plot average nodes per move vs. algorithm for different board sizes
    for board_size in df['board_size'].unique():
        subset = df[df['board_size'] == board_size]
        axes[1].plot(subset['algorithm'], subset['avg_nodes_per_move'], marker='o', label=f'Board Size {board_size}')
    
    axes[1].set_title('Average Nodes Evaluated per Move vs. Algorithm')
    axes[1].set_xlabel('Algorithm')
    axes[1].set_ylabel('Average Nodes Evaluated per Move')
    axes[1].legend()
    axes[1].grid(True)
    axes[1].set_xticklabels(df['algorithm'].unique(), rotation=45, ha='right')
    
    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig('benchmark_results.png')
    print("Graphs saved to benchmark_results.png")
    
    # Show the figure
    plt.show()

if __name__ == "__main__":
    print("Running Gomoku AI Algorithm Benchmarks...")
    results = run_benchmarks()
    generate_report(results)
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
