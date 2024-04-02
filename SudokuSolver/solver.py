#Make Console Board

def take_user_input():
    column1 = input("Enter a column to change (A-I): ").upper()
    column = ord(column1) - 65
    row = int(input("Enter a row change (1-9): "))
    row -= 1
    new_value = input("Enter the number you want to enter: ")
    return row, column, new_value

def update_grid(grid, row, column, newvalue):
    grid[row][column] = newvalue
    return grid

def initialise_grid(grid):
    done = False
    i = 0
    letters = ["  A B C D E F G H I"]
    while not done:
        end = input("Are you done inputting numbers (Y/N): ")
        if end == "Y":
            break
        inputs = take_user_input()
        grid = update_grid(grid, inputs[0], inputs[1], inputs[2])
        print(" ".join(letters))
        for row in grid:
            print(i, " ".join(row))
            i+=1
    return grid

def solve_grid(grid, initial_check):
    if initial_check == False:
        if not check_if_initially_valid(grid):
            return None
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return grid
    row, column = empty_cell
    for x in range(1,10):
        if is_valid(grid, row, column, x):
            grid[row][column] = str(x)
            if solve_grid(grid, True):
                return grid
            grid[row][column] = "-"
    return None
def check_if_initially_valid(grid):
        def is_valid_unit(unit):
            unit = [x for x in unit if x != '-']
            return len(set(unit)) == len(unit)

        for i in range(9):
            if not is_valid_unit(grid[i]) or not is_valid_unit([grid[j][i] for j in range(9)]):
                return False

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if not is_valid_unit([grid[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]):
                    return False

        return True

def is_valid(board, row, col, num):
    # print("Checking validity for number", num, "at position", row, ",", col)
    # Check if the same number already exists in the row
    for x in range(9):
        if board[row][x] == str(num):
            # print("Invalid: Number", num, "already exists in the row.")
            return False

    # Check if the same number already exists in the column
    for x in range(9):
        if board[x][col] == str(num):
            # print("Invalid: Number", num, "already exists in the column.")
            return False

    # Check if the same number already exists in the 3x3 grid
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == str(num):
                # print("Invalid: Number", num, "already exists in the 3x3 grid.")
                return False

    # print("Valid: Number", num, "can be placed at position", row, ",", col)
    return True
def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == "-":
                return (i, j)
    return None

if __name__ == '__main__':
    grid = [
        ["-", "3", "3", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "1", "9", "5", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "6", "-", "-", "-", "3"],
        ["-", "-", "-", "8", "-", "3", "-", "-", "1"],
        ["-", "-", "-", "-", "2", "-", "-", "-", "6"],
        ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "4", "1", "9", "-", "-", "5"],
        ["-", "-", "-", "-", "8", "-", "-", "7", "9"]
    ]
    grid = solve_grid(grid, False)
    if grid is None:
        print("No solution exists.")
    else:
        print("Solution:")
        for row in grid:
            print(" ".join(row))
