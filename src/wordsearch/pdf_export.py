from reportlab.lib.pagesizes import letter as LETTER
from reportlab.pdfgen import canvas
import math


def draw_word_oval(c, start_x, start_y, cell_size, placement):
    start_row, start_col = placement["start"]
    end_row, end_col = placement["end"]

    x1 = start_x + start_col * cell_size + cell_size / 2
    y1 = start_y - start_row * cell_size - cell_size / 2

    x2 = start_x + end_col * cell_size + cell_size / 2
    y2 = start_y - end_row * cell_size - cell_size / 2

    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    dx = x2 - x1
    dy = y2 - y1

    angle = math.degrees(math.atan2(dy, dx))

    word_length = len(placement["word"]) * cell_size
    oval_height = cell_size * 1.25

    c.saveState()
    c.translate(mid_x, mid_y)
    c.rotate(angle)

    c.roundRect(
        -word_length / 2,
        -oval_height / 2,
        word_length,
        oval_height,
        radius=oval_height / 2,
        stroke=1,
        fill=0,
    )

    c.restoreState()


def draw_page_number(c, page_number):
    page_width, _ = LETTER

    c.setFont("Helvetica", 12)
    c.drawRightString(page_width - 45, 18, str(page_number))


def draw_puzzle_page(c, puzzle, page_number):
    page_width, page_height = LETTER

    draw_page_border(c, page_width, page_height)

    title = f"Puzzle {puzzle['id']}: {puzzle['title']}"

    grid = puzzle["grid"]
    words = puzzle["words"]

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(page_width / 2, page_height - 65, title)

    grid_size = len(grid)
    cell_size = 24

    grid_width = grid_size * cell_size
    grid_height = grid_size * cell_size

    start_x = (page_width - grid_width) / 2
    start_y = page_height - 110

    c.setLineWidth(2)
    c.rect(
        start_x,
        start_y - grid_height,
        grid_width,
        grid_height,
        stroke=1,
        fill=0,
    )

    c.setFont("Courier-Bold", 14)

    for row_index, row in enumerate(grid):
        for col_index, grid_letter in enumerate(row):
            x = start_x + col_index * cell_size + 7
            y = start_y - row_index * cell_size - 18
            c.drawString(x, y, grid_letter)

    word_list_y = start_y - grid_height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(90, word_list_y, "Words:")

    c.setFont("Helvetica", 11)

    words_per_column = 5
    column_width = 150

    start_words_x = 90
    start_words_y = word_list_y - 25

    for index, word in enumerate(words):
        column = index // words_per_column
        row = index % words_per_column

        x = start_words_x + column * column_width
        y = start_words_y - row * 18

        c.drawString(x, y, word)

    draw_page_number(c, page_number)

def draw_single_solution(c, puzzle, start_x, start_y, cell_size):
    grid = puzzle["grid"]
    placements = puzzle["placements"]

    title = f"Solution {puzzle['id']}"

    grid_size = len(grid)
    grid_width = grid_size * cell_size
    grid_height = grid_size * cell_size

    c.setFont("Helvetica-Bold", 12)
    c.drawString(start_x, start_y + 15, title)

    c.setLineWidth(1)
    c.rect(
        start_x,
        start_y - grid_height,
        grid_width,
        grid_height,
        stroke=1,
        fill=0,
    )

    c.setFont("Courier-Bold", 8)

    for row_index, row in enumerate(grid):
        for col_index, grid_letter in enumerate(row):
            x = start_x + col_index * cell_size + 3
            y = start_y - row_index * cell_size - 8
            c.drawString(x, y, grid_letter)

    c.setLineWidth(0.75)

    for placement in placements:
        draw_word_oval(c, start_x, start_y, cell_size, placement)


def draw_solution_pages(c, puzzles, start_page_number):
    page_width, page_height = LETTER

    cell_size = 17

    positions = [
        (35, page_height - 50),
        (page_width / 2 + 10, page_height - 50),
        (35, page_height / 2 + 10),
        (page_width / 2 + 10, page_height / 2 + 10),
    ]

    page_number = start_page_number

    for puzzle_index, puzzle in enumerate(puzzles):
        position_index = puzzle_index % 4

        if puzzle_index > 0 and position_index == 0:
            draw_page_number(c, page_number)
            c.showPage()
            page_number += 1

        draw_single_solution(
            c=c,
            puzzle=puzzle,
            start_x=positions[position_index][0],
            start_y=positions[position_index][1],
            cell_size=cell_size,
        )

    draw_page_number(c, page_number)

def draw_database_icon(c, x, y):
    c.ellipse(x, y + 20, x + 35, y + 30, stroke=1, fill=0)
    c.line(x, y + 25, x, y)
    c.line(x + 35, y + 25, x + 35, y)
    c.ellipse(x, y - 5, x + 35, y + 5, stroke=1, fill=0)


def draw_cloud_icon(c, x, y):
    c.circle(x + 12, y + 12, 8, stroke=1, fill=0)
    c.circle(x + 23, y + 17, 10, stroke=1, fill=0)
    c.circle(x + 35, y + 12, 8, stroke=1, fill=0)
    c.line(x + 8, y + 5, x + 40, y + 5)


def draw_code_icon(c, x, y):
    c.setFont("Courier-Bold", 18)
    c.drawString(x, y, "</>")


def draw_nodes_icon(c, x, y):
    points = [
        (x + 5, y + 5),
        (x + 30, y + 20),
        (x + 45, y + 5),
    ]

    c.line(points[0][0], points[0][1], points[1][0], points[1][1])
    c.line(points[1][0], points[1][1], points[2][0], points[2][1])

    for px, py in points:
        c.circle(px, py, 4, stroke=1, fill=0)

def draw_page_border(c, page_width, page_height):
    margin = 30
    icon_offset = 18

    c.setLineWidth(2)
    c.rect(
        margin,
        margin,
        page_width - margin * 2,
        page_height - margin * 2,
        stroke=1,
        fill=0,
    )

    c.setLineWidth(0.75)
    c.rect(
        margin + 8,
        margin + 8,
        page_width - (margin + 8) * 2,
        page_height - (margin + 8) * 2,
        stroke=1,
        fill=0,
    )

    c.setFont("Courier-Bold", 18)

    # Top left
    c.drawString(margin + icon_offset, page_height - margin - 28, "</>")

    # Top right
    c.drawRightString(page_width - margin - icon_offset, page_height - margin - 28, "{ }")

    # Bottom left
    c.drawString(margin + icon_offset, margin + 18, "[ ]")

    # Bottom right
    c.drawRightString(page_width - margin - icon_offset, margin + 18, "( )")


def draw_contents_page(c, puzzles, solutions_start_page):
    page_width, page_height = LETTER

    draw_page_border(c, page_width, page_height)

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(page_width / 2, page_height - 80, "Contents")

    c.setFont("Helvetica", 13)

    y = page_height - 130

    for puzzle in puzzles:
        line = f"Puzzle {puzzle['id']}: {puzzle['title']}"
        page = str(puzzle["page_number"])

        c.drawString(80, y, line)
        c.drawRightString(page_width - 80, y, page)

        y -= 24

    y -= 12

    c.setFont("Helvetica-Bold", 13)
    c.drawString(80, y, "Solutions")
    c.drawRightString(page_width - 80, y, str(solutions_start_page))

    draw_page_number(c, 1)


def export_book_pdf(puzzles, output_path):
    c = canvas.Canvas(output_path, pagesize=LETTER)

    contents_page_number = 1
    first_puzzle_page = 2

    for index, puzzle in enumerate(puzzles):
        puzzle["page_number"] = first_puzzle_page + index

    solutions_start_page = first_puzzle_page + len(puzzles)

    draw_contents_page(c, puzzles, solutions_start_page)
    c.showPage()

    for puzzle in puzzles:
        draw_puzzle_page(c, puzzle, puzzle["page_number"])
        c.showPage()

    draw_solution_pages(
        c,
        puzzles,
        start_page_number=solutions_start_page,
    )

    c.save()