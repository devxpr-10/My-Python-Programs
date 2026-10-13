from typing import Literal

elements = {
    'X' : 1,
    ' ' : 0,
    'O' : -1
}

def change_nature(element: Literal["X", "O", " ", 1, -1, 0]) -> str | int:
    """Converts the given element into its respective alterntive in another type.
    \nFor Example:
    - element : X, output -> 1
    \nSimilarly,
    - element : -1, output -> O
    """
    if element in elements:
        return elements[element]

    int_to_str = {}
    for val in elements:
        int_to_str[elements[val]] = val
    
    if element in int_to_str:
        return int_to_str[element]

class Board:
    def __init__(self, x_minimizing: bool = True):
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.minimizing = -1 if x_minimizing else 1
        self.maximizing = -self.minimizing

    def convert_location(self, location: tuple | str) -> str | tuple:
        alpha = [chr(i) for i in range(97, 123)]
        if isinstance(location, tuple):
            return f"{alpha[location[0]]}{location[1]+1}"
        elif isinstance(location, str):
            return (alpha.index(location[0]), int(location[1]) - 1)

    def fill(self, element: Literal["X", "O", " "]) -> None:
        for i in range(3):
            for j in range(3):
                self.put((i, j), element)

    def put(self, location: str | tuple, element: Literal["X", "O", " "]) -> None:
        element = change_nature(element) if isinstance(element, int) else element
        loc = self.convert_location(location) if isinstance(location, str) else location
        self.board[loc[0]][loc[1]] = change_nature(element)

    def validity(self, loc: str | tuple) -> tuple[bool]:
        """Returns if the given location is a valid location and if it's occupied"""
        try:
            loc = self.convert_location(loc) if isinstance(loc, str) else loc
            legal = -1 < loc[0] < 4 and -1 < loc[1] < 4
            occupied = self.board[loc[0]][loc[1]] != 0
        except (ValueError, TypeError, IndexError):
            legal, occupied = False, False
        return (legal, occupied)

    def empty_locations(self) -> list[tuple]:
        return  [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == 0]

    def state(self) -> Literal[1, 0, -1] | None:
        """Returns '0' if draw, '1' if 'X' wins, '-1' if 'O' otherwise 'None'"""
        vertical = [sum(row) for row in self.board]
        horizontal = [sum(col) for col in zip(*self.board)]
        diags = [sum([self.board[i][i] for i in range(3)]),
                sum([self.board[i][len(self.board)-1-i] for i in range(3)])]
        boundaries = [*vertical, *horizontal, *diags]

        if 3 in [abs(x) for x in boundaries]:
            for i in [-3, 3]:
                if i in boundaries:
                    winner = i // 3
                    break
            return winner
        
        elif all([True if 0 not in row else False for row in self.board]):
            return 0

        return None

    def __str__(self):
        s, newline = '', ''
        for cn, row in enumerate(self.board):
            newline = '' if cn == len(self.board) - 1 else '\n'
            s += ' | '.join([' X' if i == change_nature('X') else ' O' if i == change_nature('O') else self.convert_location((cn, rn)) for rn, i in enumerate(row)]) + newline
        return s