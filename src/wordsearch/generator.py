import random
import string

def generate_grid(grid_size=15):
    grid = []
    for _ in range(grid_size):
        row = [random.choice(string.ascii_uppercase) for _ in range(grid_size)]
        grid.append(row)
    return grid



x = generate_grid()

    

print_grid()