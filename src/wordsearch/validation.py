def validate_puzzles(puzzles, grid_size=15, expected_word_count=15):

    all_words = {}
    errors = []

    seen_ids = set()
    seen_titles = set()

    for puzzle in puzzles:
        puzzle_id = puzzle.get("id")
        title = puzzle.get("title")
        words = puzzle.get("words")

        if puzzle_id in seen_ids:
            errors.append(f"Duplicate puzzle id: {puzzle_id}")
        seen_ids.add(puzzle_id)

        if title in seen_titles:
            errors.append(f"Duplicate puzzle title: {title}")
        seen_titles.add(title)

        if not isinstance(words, list):
            errors.append(f"Puzzle {puzzle_id} has no valid word list")
            continue

        if len(words) != expected_word_count:
            errors.append(
                f"Puzzle {puzzle_id} has {len(words)} words, expected {expected_word_count}"
            )

        seen_words = set()

        for word in words:
            if not isinstance(word, str):
                errors.append(f"Puzzle {puzzle_id} contains a non-string word: {word}")
                continue

            if word != word.upper():
                errors.append(f"Puzzle {puzzle_id} word is not uppercase: {word}")

            if " " in word:
                errors.append(f"Puzzle {puzzle_id} word contains a space: {word}")

            if len(word) > grid_size:
                errors.append(
                    f"Puzzle {puzzle_id} word is too long for grid: {word}"
                )

            if word in seen_words:
                errors.append(f"Puzzle {puzzle_id} has duplicate word: {word}")

            seen_words.add(word)
            if word in all_words:
                errors.append(
                    f"Word appears in multiple puzzles: {word} "
                    f"(Puzzle {all_words[word]} and Puzzle {puzzle_id})"
                )
            else:
                all_words[word] = puzzle_id

    if errors:
        error_message = "\n".join(errors)
        raise ValueError(f"Puzzle validation failed:\n{error_message}")