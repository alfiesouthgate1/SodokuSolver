import random
from solver import solve_grid

grid = [
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
]
def generate_grid(grid):
    rows = [0,1,2,3,4,5,6,7,8]
    numbers = ["1","2","3","4","5","6","7","8","9"]
    # Places numbers 1-9 in random rows and random columns
    for i in range(9):
        row = random.choice(rows)
        number = random.choice(numbers)
        grid[row][random.randint(0,8)] = number
        numbers.remove(number)
        rows.remove(row)
    # Solves the grid to generate a board
    grid = solve_grid(grid, False)
    return grid
# These functions work by removing a set amount of numbers from a board that is generated above
def easy(grid):
    staying = random.sample(range(80), random.randint(33,40))
    counter = 1
    for row in range(9):
        for col in range(9):
            if counter not in staying:
                grid[row][col] = "-"
            counter+=1
    return grid
def medium(grid):
    staying = random.sample(range(80), random.randint(26,32))
    counter = 1
    for row in range(9):
        for col in range(9):
            if counter not in staying:
                grid[row][col] = "-"
            counter+=1
    return grid
def hard(grid):
    staying = random.sample(range(80), random.randint(17,25))
    counter = 1
    for row in range(9):
        for col in range(9):
            if counter not in staying:
                grid[row][col] = "-"
            counter+=1
    return grid


grid = generate_grid(grid)
grid = easy(grid)
for row in grid:
    print(" ".join(row))