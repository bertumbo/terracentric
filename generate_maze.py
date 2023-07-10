import numpy as np

rows = n = 3
columns = m = 60

# Create a zeros array
arr = np.zeros((n, m), dtype=object)

# Function to check if a position is valid and has a neighboring non-zero entry
def is_valid_position(row, col):
    if row >= 0 and row < n and col >= 0 and col < m:
        if (row - 1 >= 0 and arr[row - 1, col] != 0) or \
           (row + 1 < n and arr[row + 1, col] != 0) or \
           (col - 1 >= 0 and arr[row, col - 1] != 0) or \
           (col + 1 < m and arr[row, col + 1] != 0):
            return True
    return False

# Randomly choose an entry and change it to 1
row, col = np.random.randint(0, n), np.random.randint(0, m)
arr[row, col] = 1

# Repeat until there are no more zero entries with a neighboring non-zero entry
while np.any(arr == 0):
    zero_positions = np.argwhere(arr == 0)  # Get all zero positions
    np.random.shuffle(zero_positions)  # Shuffle the positions randomly
    for pos in zero_positions:
        row, col = pos
        if is_valid_position(row, col):
            valid_directions = []
            if row - 1 >= 0 and arr[row - 1, col] != 0:
                valid_directions.append("up")
            if row + 1 < n and arr[row + 1, col] != 0:
                valid_directions.append("down")
            if col - 1 >= 0 and arr[row, col - 1] != 0:
                valid_directions.append("left")
            if col + 1 < m and arr[row, col + 1] != 0:
                valid_directions.append("right")
            direction = np.random.choice(valid_directions)  # Randomly choose a valid direction
            if direction == "up":
                arr[row, col] = "up"
            elif direction == "down":
                arr[row, col] = "down"
            elif direction == "left":
                arr[row, col] = "left"
            elif direction == "right":
                arr[row, col] = "right"
            break  # Move to the next iteration of the while loop

np.set_printoptions(linewidth=250)

#print(arr)



# Print the final array
rows, columns = arr.shape
for row in range(rows):
    for column in range(columns):
        try:
            print(arr[row, column][0], end=" ")
        except:
            print(1, end=" ")
    print()

