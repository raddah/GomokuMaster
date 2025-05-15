from easyAI import TwoPlayerGame, Negamax, Human_Player, AI_Player

class Gomoku(TwoPlayerGame):
    """The game of Gomoku, also known as Five in a Row."""

    def __init__(self, players=None):
        """Initialize the game."""
        self.board_size = 5
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.players = players or [Human_Player(), AI_Player(Negamax(5))]
        self.current_player = 1  # Player 1 starts

    def possible_moves(self):
        """Return a list of possible moves (empty cells)."""
        return [i + 1 for i, v in enumerate(self.board) if v == 0]

    def make_move(self, move):
        """Apply a move to the board."""
        self.board[int(move) - 1] = self.current_player

    def unmake_move(self, move):
        """Undo a move from the board."""
        self.board[int(move) - 1] = 0

    def lose(self):
        """Has the opponent formed a five-in-a-row?"""
        return self.five_in_a_row(opponent=self.current_player)

    def is_over(self):
        """Is the game over?"""
        return self.lose() or not self.possible_moves()

    def show(self):
        """Print the board."""
        for row in self.board:
            print(" ".join(["." if cell == 0 else ("O" if cell == 1 else "X") for cell in row]))

    def scoring(self):
        """Return a score for the current player."""
        score = -100 if self.lose() else 0
        print(f"Scoring: Player {self.current_player}, Score: {score}")
        return score

    def five_in_a_row(self, opponent):
        """Check if the opponent has five in a row."""
        size = self.board_size
        board = self.board

        # Check rows
        for i in range(size):
            for j in range(size - 4):
                if all(board[i * size + j + k] == opponent for k in range(5)):
                    return True

        # Check columns
        for j in range(size):
            for i in range(size - 4):
                if all(board[(i + k) * size + j] == opponent for k in range(5)):
                    return True

        # Check diagonals (top-left to bottom-right)
        for i in range(size - 4):
            for j in range(size - 4):
                if all(board[(i + k) * size + j + k] == opponent for k in range(5)):
                    return True

        # Check diagonals (top-right to bottom-left)
        for i in range(size - 4):
            for j in range(4, size):
                if all(board[(i + k) * size + j - k] == opponent for k in range(5)):
                    return True

        return False

    def play(self, verbose=True):
        """Play the game."""
        if verbose:
            print("Welcome to Gomoku!")
            print("The goal is to get five in a row (horizontally, vertically, or diagonally).")
            print("Players take turns placing their stones on the board.")
            print("Player 1: O, Player 2: X")
            print("To make a move, enter the row and column number (1-5), separated by a space.")
            print(self)

        while not self.is_over():
            pass

if __name__ == "__main__":
    """Play the game."""
    gomoku = Gomoku()
    gomoku.play()
