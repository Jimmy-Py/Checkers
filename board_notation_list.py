letters = ["a","b","c","d","e","f","g","h"]


board = []

row = 1
number = 1
while row <= 8:
    for letter in letters:
        board.append(letter + str(number))
        if number == 9:
            number = 1
    row += 1
    number += 1
print(board)