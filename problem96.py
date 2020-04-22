boards = []

# Print array row by row
def parray(arr):
    for row in arr:
        print(row)


# Convenience function to check if a board is correct (Unused)
def correct(board):

    # Check rows for duplicates
    for row in board:
        no0 = [x for x in row if x]
        if sorted(list(set(no0))) != sorted(no0):
            return False

    # Check for column duplicates
    for i in range(9):
        no0 = [y[i] for y in board if y[i]]
        if sorted(list(set(no0))) != sorted(no0):
            return False

        # While on columns, check for 'square' duplicates
        if i % 3 == 0:
            for j in range(0,9,3):
                no0 = [qq for q in board[i:i+3] for qq in q[j:j+3] if qq]
                if sorted(list(set(no0))) != sorted(no0):
                    return False
    
    # Nothing failed, return True
    return True


# Return a list of possible values for a coordinate on a board
def possibles(coord, board):

    # Grab all non 0 row values
    p = [x for x in board[coord[1]] if x]

    # Grab all non 0 column values
    p.extend([y[coord[0]] for y in board if y[coord[0]]])

    # Locate the top left of the 'square' the coord belongs to
    y = (coord[1] // 3) * 3
    x = (coord[0] // 3) * 3
    # Grab all non 0 values from the 'square'
    p.extend([qq for q in board[y:y+3] for qq in q[x:x+3] if qq])

    # Return all 1-9 values that ARENT in the list we've made
    return [i for i in range(1,10) if i not in p]


# Return a solved board from a given unfinished board
def solve(board):

    # Make a deep copy of the given board
    solved = [l[:] for l in board]

    # Make a grid of possible solutions for each position
    solutions = []

    # Check if the board we were given is already solved
    if 0 not in [qq for q in board for qq in q]:
        return solved
    
    # Go through each position and get its possible solutions
    for y in range(9):
        solutions_y = []
        for x in range(9):
            c = (x, y)

            if not board[y][x]:
                p = possibles(c, board)
                if not p: raise Exception(f'{c}')

                # Add the possible solutions to the row
                solutions_y.append(p)

                # If there's only one possibility, use it
                if len(p) == 1:
                    solved[y][x] = p[0]
                    # Solve for the next empty square
                    return solve(solved)
            else:
                solutions_y.append(0)
        
        # Add the possible solutions to the grid
        solutions.append(solutions_y)
    
    # If we got here, that means no immidiate solution exists

    # Make a list of boards that are possible branches to the final solution
    branches = []

    # Go through all positions to look for the first empty slot
    for y in range(9):
        if branches: break  # If branches has been filled, we don't need more
        for x in range(9):

            # If we found an empty space and we have exactly 2 solutions for it
            #   The 2 is just to trim the probability space
            if not board[y][x] and solutions[y][x] and len(solutions[y][x]) == 2:

                # Make a board for each of the possible solutions
                for p in solutions[y][x]:
                    branches.append([l[:] for l in board])
                    branches[-1][y][x] = p
                break

    # Try to solve each branch
    for branch in branches:
        try:
            return solve(branch)
        except:
            pass

    raise Exception('Cant solve')

# Open the file and populate the list of all boards
with open('p096_sudoku.txt','r') as f:
    lines = list(map(lambda l: l.strip(), f.readlines()))
    for i in range(0, len(lines), 10):
        boards.append([list(map(int, l)) for l in lines[i+1:i+10]])

total = 0

# Calculate the total
for board in boards:
    solved = solve(board)
    parray(solved)
    total += int(''.join(map(str, solved[0][:3])))
    print('~='*8)

print(total)
