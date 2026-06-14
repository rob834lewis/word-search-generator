import json

from src.wordsearch.generator import (
    generate_grid,
    place_words_randomly,
    fill_empty_spaces,
)

from src.wordsearch.pdf_export import (
    export_book_pdf,
)

from src.wordsearch.validation import validate_puzzles

def load_puzzles(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def build_single_puzzle(puzzle, max_grid_attempts=50):
    for attempt in range(max_grid_attempts):
        grid = generate_grid()

        try:
            placements = place_words_randomly(grid, puzzle["words"])
            fill_empty_spaces(grid)

            return {
                "id": puzzle["id"],
                "title": puzzle["title"],
                "words": puzzle["words"],
                "grid": grid,
                "placements": placements,
            }

        except ValueError:
            continue

    raise ValueError(f"Could not build puzzle after {max_grid_attempts} attempts: {puzzle['title']}")

def build_puzzles(puzzle_data):
    return [build_single_puzzle(puzzle) for puzzle in puzzle_data]


if __name__ == "__main__":
    puzzle_data = load_puzzles("data/data_engineering.json")

    validate_puzzles(puzzle_data)

    built_puzzles = build_puzzles(puzzle_data)

    export_book_pdf(
        puzzles=built_puzzles,
        output_path="output/data_engineering_word_search.pdf",
    )