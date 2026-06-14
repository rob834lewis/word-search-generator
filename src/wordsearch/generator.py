import json
import random
import string

DIRECTIONS = {
    "horizontal": (0, 1),
    "vertical": (1, 0),
    "diagonal_down": (1, 1),
    "horizontal_back": (0, -1),
    "vertical_up": (-1, 0),
    "diagonal_up": (-1, 1),
}


def generate_grid(grid_size=15):
    return [["." for _ in range(grid_size)] for _ in range(grid_size)]


def load_puzzle(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
    
    
def can_place_word(grid, row, col, word, direction):
    grid_size = len(grid)

    if direction not in DIRECTIONS:
        raise ValueError(f"Invalid direction: {direction}")

    row_step, col_step = DIRECTIONS[direction]

    end_row = row + row_step * (len(word) - 1)
    end_col = col + col_step * (len(word) - 1)

    if end_row < 0 or end_row >= grid_size:
        return False

    if end_col < 0 or end_col >= grid_size:
        return False

    for i, letter in enumerate(word):
        current_row = row + row_step * i
        current_col = col + col_step * i

        existing_letter = grid[current_row][current_col]

        if existing_letter != "." and existing_letter != letter:
            return False

    return True


def place_word(grid, row, col, word, direction):
    if not can_place_word(grid, row, col, word, direction):
        raise ValueError("Cannot place word at the specified position and direction.")

    row_step, col_step = DIRECTIONS[direction]

    coordinates = []

    for i, letter in enumerate(word):
        current_row = row + row_step * i
        current_col = col + col_step * i

        grid[current_row][current_col] = letter
        coordinates.append((current_row, current_col))

    return {
        "word": word,
        "direction": direction,
        "start": (row, col),
        "end": coordinates[-1],
        "coordinates": coordinates,
    }

def place_words_randomly(grid, words, max_attempts=1000):
    directions = list(DIRECTIONS.keys())
    placements = []

    words = sorted(words, key=len, reverse=True)

    for word in words:
        placed = False

        for _ in range(max_attempts):
            row = random.randint(0, len(grid) - 1)
            col = random.randint(0, len(grid) - 1)
            direction = random.choice(directions)

            if can_place_word(grid, row, col, word, direction):
                placement = place_word(grid, row, col, word, direction)
                placements.append(placement)
                placed = True
                break

        if not placed:
            raise ValueError(f"Could not place word: {word}")

    return placements

def fill_empty_spaces(grid):
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == ".":
                grid[row][col] = random.choice(string.ascii_uppercase)


def generate_solution_grid(grid, placements):
    solution_grid = [["." for _ in range(len(grid))] for _ in range(len(grid))]

    for placement in placements:
        for row, col in placement["coordinates"]:
            solution_grid[row][col] = grid[row][col]

    return solution_grid