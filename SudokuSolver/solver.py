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

def solve_grid(grid):
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return grid
    row, column = empty_cell
    for x in range(1,10):
        if is_valid(grid, row, column, x):
            grid[row][column] = str(x)
            if solve_grid(grid):
                return grid
            grid[row][column] = "-"
    return False


def is_valid(board, row, col, num):
    print("Checking validity for number", num, "at position", row, ",", col)
    # Check if the same number already exists in the row
    for x in range(9):
        if board[row][x] == str(num):
            print("Invalid: Number", num, "already exists in the row.")
            return False

    # Check if the same number already exists in the column
    for x in range(9):
        if board[x][col] == str(num):
            print("Invalid: Number", num, "already exists in the column.")
            return False

    # Check if the same number already exists in the 3x3 grid
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == str(num):
                print("Invalid: Number", num, "already exists in the 3x3 grid.")
                return False

    print("Valid: Number", num, "can be placed at position", row, ",", col)
    return True
def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == "-":
                return (i, j)
    return None

if __name__ == '__main__':
    grid = [
        ["4", "7", "-", "-", "-", "2", "1", "-", "-"],
        ["-", "5", "9", "4", "1", "8", "-", "-", "-"],
        ["6", "-", "-", "-", "-", "-", "-", "8", "3"],
        ["-", "-", "6", "2", "5", "-", "-", "1", "9"],
        ["-", "2", "3", "-", "-", "1", "-", "-", "6"],
        ["-", "-", "1", "9", "3", "-", "2", "-", "8"],
        ["8", "-", "-", "-", "-", "-", "9", "6", "-"],
        ["-", "6", "-", "-", "9", "5", "7", "-", "2"],
        ["2", "-", "-", "6", "4", "-", "8", "-", "-"],
    ]
    grid = solve_grid(grid)
    for row in grid:
        print(" ".join(map(str, row)))
