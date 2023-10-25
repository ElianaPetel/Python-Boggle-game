import math
from typing import List, Tuple, Iterable, Optional, Any


Board = List[List[str]]
Path = List[Tuple[int, int]]

# color constants
VERY_LIGHT_GREEN = "#e5f5e0"
LIGHT_GREEN = "#c7e9c0"
INTER_LIGHT = "#a1d99b"
INTER_DARK = "#74c476"
DARK_GREEN = "#238b45"
VERY_DARK_GREEN = "#005a32"
LIGHT_YELLOW = "#ffe64e"
DARKER_YELLOW = "#ffdf18"
LIGHT_RED = "#ff6767"

# GUI constants
SPLIT = 0.15


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """Function that checks if a given path is considered valid on the board.
    Returns the word formed by the path if its considered valid and None otherwise.
    :param board: 2d list representing a boggle board.
    :param path: List of coordinates on the board.
    :param words: Iterable object that contains all the possible words in the game.
    """
    if is_same_cube(path):  # if there is same positions in path
        return None
    # if next pos is further than 1 cell (from all the 8 possible moves)
    if not legal_move(path):
        return None
    word = ""  # variable to hold the word represented as a path
    for pos in path:  # iterate over all the path to extricate word
        if 0 <= pos[0] < len(board) and 0 <= pos[1] < len(board[0]):
            word += board[pos[0]][pos[1]]
        else:
            return None
    if word in words:  # check if the word is presented in dictionary
        return word
    else:
        return None


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """function that finds all the possible paths of length n on a given board.
    :param n: an integer representing the length of the path.
    :param board: 2d list representing a boggle board.
    :param words: Iterable object that contains all the possible words in the game.
    """
    return find_paths(board, words, n)


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """Function that finds all the possible paths that form words of length n.
    :param n: an integer representing the length of the words.
    :param board: 2d list representing a boggle board.
    :param words: Iterable object that contains all the possible words in the game.
    """
    return find_paths(board, words, n)


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """Function that finds the paths that maximize the score.
    :param board: 2d list representing a boggle board.
    :param words: Iterable object that contains all the possible words in the game.
    """
    return find_paths(board, words, None, score=True)


def find_paths(board, words, n, score=False):
    """Function that finds all the possible paths of a given board,
    given certain conditions.
    :param board: 2d list representing a boggle board.
    :param words: Iterable object that contains all the possible words in the game.
    """
    ans = []
    words_dict = {}

    def find_recursive_path(path, y, x):
        # if the function needs to find paths that maximize the score
        if score:
            word_length = words_length(path, board)
            if word_length >= 3:
                prefix = create_word(path, board)
                if not is_word_in_dict(prefix, words):
                    return
                else:
                    if is_word_in_dict(prefix, words):
                        if prefix in words_dict and len(path) > len(words_dict[prefix]):
                            ans.remove(words[prefix])
                            ans.append(path)
                            words_dict[prefix] = path
                        else:
                            ans.append(path)
                            words_dict[prefix] = path
        else:
            if len(path) == n:
                word = create_word(path, board)
                if is_word_in_dict(word, words):
                    ans.append(path)
                return

        neighbors = find_neighboring_values(board, y, x)
        for neighbor in neighbors:
            if neighbor not in path:
                new_path = path.copy()
                new_path.append(neighbor)
                new_y, new_x = neighbor
                # find all possible paths from this cell
                find_recursive_path(new_path, new_y, new_x)

    # iterates through each cell
    for r in range(len(board)):
        for c in range(len(board[0])):
            sub_path = [(r, c)]
            # find all possible paths from this cell
            find_recursive_path(sub_path, r, c)

    return ans


def words_length(path, board):
    length = 0
    for pos in path:
        y_pos, x_pos = pos
        length += len(board[y_pos][x_pos])
    return length


def is_same_cube(path: Path):
    """gets a list of path and returns True if the same Tuple is showing
    twice and False otherwise. this will indicate if one of the illegal moves
    was provided: going over the same letter cube"""
    return len(path) != len(set(path))


def legal_move(path: Path):
    """get a list of Path representing all the pos steps that being used
    from left to right and checks if the progress of the steps is legal.
    returns True if all the steps are valid, otherwise False.
    illegal step may be step forward to a cell that is not near one of the
    8 nearby cells in the board"""
    index = 1
    for cur_pos in range(len(path) - 1):
        next_pos = path[index]  # next pos in path
        # if the rows or the col of the current & next pos are the same
        # the distance between the two should be 1 to be valid
        if path[cur_pos][0] == next_pos[0] or path[cur_pos][1] == next_pos[1]:
            if math.dist(path[cur_pos], next_pos) != 1:
                return False
        # the other option for moving is diagonal and the distance should
        # be as presented below
        else:
            if math.dist(path[cur_pos], next_pos) != 1.4142135623730951:
                return False
        # making sure we move next pos one step forward from current pos
        index += 1
    return True


def is_word_in_dict(word: str, words: Iterable[str]) -> bool:
    """helper function that receives a string and returns True
    if the string corresponds to a word in the dictionary
    and False otherwise."""
    return word in words


def create_word(path: Path, board: Board) -> str:
    """Helper function that receives a path and a board
    and creates the word formed by that given path"""
    ans = ""
    for element in path:
        y, x = element
        ans += board[y][x]
    return ans


def find_neighboring_values(board: Board, y: int, x: int) -> list[Any]:
    """Helper function that receives a board and the coordinates
    of a cell and returns a list of all the valid cells the player
    could select from that given cell."""
    # All 8 theoretical cells the player could select
    neighbors = [
        (y + 1, x),
        (y - 1, x),
        (y, x + 1),
        (y, x - 1),
        (y + 1, x + 1),
        (y + 1, x - 1),
        (y - 1, x + 1),
        (y - 1, x - 1),
    ]
    for element_index in range(len(neighbors) - 1, -1, -1):
        y_element, x_element = neighbors[element_index]
        # If not within game borders, remove this possibility
        if not (0 <= y_element < len(board) and 0 <= x_element < len(board[0])):
            neighbors.remove(neighbors[element_index])
    return neighbors
