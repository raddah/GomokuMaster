from easyAI import TwoPlayerGame, Negamax, Human_Player, AI_Player

class Gomoku(TwoPlayerGame):
    """The game of Gomoku, also known as Five in a Row."""

    def __init__(self, players=None):
        """Initialize the game."""
        self.board_size = 5
        self.board = [0] * (self.board_size * self.board_size)
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
        for i in range(self.board_size):
            print(
                " ".join(
                    ["." if self.board[i * self.board_size + j] == 0 else
                     ("O" if self.board[i * self.board_size + j] == 1 else "X")
                     for j in range(self.board_size)]
                )
            )

    def scoring(self):
        """Return a score for the current player."""
        return -100 if self.lose() else 0

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

if __name__ == "__main__":
    """Play the game."""
    gomoku = Gomoku()
    gomoku.play()
