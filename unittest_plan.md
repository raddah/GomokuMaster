# Unit Test Plan for Gomoku Implementation

## Overview

This document outlines the unit testing strategy for the Gomoku game implementation. The goal is to ensure that the enhanced implementation with easyAI maintains the same functionality as the original implementation while adding new features.

## Test Categories

### 1. Basic Game Functionality

- **Initialization Tests**
  - Test that the game initializes correctly with different board sizes and difficulty levels
  - Test that the board is empty at initialization
  - Test that the current player is BLACK at initialization

- **Move Tests**
  - Test making valid moves
  - Test making invalid moves (outside the board, on occupied cells)
  - Test that the current player switches after a move
  - Test that the last move is recorded correctly

- **Game State Tests**
  - Test that the game state is updated correctly after moves
  - Test that the game over flag is set correctly
  - Test that the winner is set correctly

### 2. Win Detection

- **Horizontal Win Tests**
  - Test detecting a horizontal line of 5 stones
  - Test that a horizontal line of 4 stones does not trigger a win

- **Vertical Win Tests**
  - Test detecting a vertical line of 5 stones
  - Test that a vertical line of 4 stones does not trigger a win

- **Diagonal Win Tests**
  - Test detecting a diagonal line of 5 stones (top-left to bottom-right)
  - Test detecting a diagonal line of 5 stones (top-right to bottom-left)
  - Test that diagonal lines of 4 stones do not trigger a win

- **Draw Tests**
  - Test that a full board with no winner is detected as a draw

### 3. AI Functionality

- **AI Move Tests**
  - Test that the AI makes valid moves
  - Test that the AI blocks the opponent's winning moves
  - Test that the AI makes winning moves when possible

- **Difficulty Level Tests**
  - Test that the AI makes different moves at different difficulty levels
  - Test that higher difficulty levels result in stronger play

### 4. easyAI Integration

- **Transposition Table Tests**
  - Test that the transposition table correctly stores and retrieves board states
  - Test that the transposition table improves performance

- **Iterative Deepening Tests**
  - Test that iterative deepening searches deeper when time allows
  - Test that iterative deepening returns a valid move even when interrupted

- **Timeout Tests**
  - Test that the AI returns a move within the specified timeout
  - Test that the AI returns the best move found so far when timeout is reached

## Test Implementation

The tests are implemented in the `test_gomoku.py` file using the Python `unittest` framework. Each test case is a method in the `TestGomoku` class.

### Running Tests

To run all tests:

```
python -m unittest test_gomoku.py
```

To run a specific test:

```
python -m unittest test_gomoku.TestGomoku.test_name
```

### Test Coverage

The tests should cover all public methods of the `Gomoku` class and key internal methods. The goal is to achieve at least 80% code coverage.

## Future Test Improvements

1. **Performance Tests**
   - Add tests to measure the performance of the AI at different difficulty levels
   - Compare the performance of the enhanced implementation with the original implementation

2. **Integration Tests**
   - Add tests to verify that the implementation works correctly with the Flask web server
   - Test the API endpoints to ensure they handle the enhanced implementation correctly

3. **Stress Tests**
   - Test the implementation with large board sizes
   - Test the implementation with many concurrent games

4. **Regression Tests**
   - Add tests for any bugs that are discovered and fixed
   - Ensure that new features don't break existing functionality
