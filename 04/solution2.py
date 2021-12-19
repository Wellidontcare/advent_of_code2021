import numpy as np

if __name__ == "__main__":
    drawn_numbers = np.loadtxt("input.txt", delimiter=",", max_rows=1, dtype=int)
    print(drawn_numbers)
    boards = np.loadtxt("input.txt", skiprows=1, dtype=int)
    boards = boards.reshape((100, 5, 5)).astype(complex)
    finish = False
    for num in drawn_numbers:
        winning_board = None
        winning_number = 0
        boards[(boards == num) & (np.imag(boards) == 0)] += 1j
        boards = [b for b in boards]
        winning_boards = []
        for board in boards:
            if np.any(np.imag(np.sum(board, axis=0)) == 5) or np.any(
                np.imag(np.sum(board, axis=1)) == 5
            ):
                # __import__("pudb").set_trace()
                winning_board = board
                winning_number = num
                winning_boards.append(winning_board)

        for wb in winning_boards:
            boards = [b for b in boards if not (np.all(b == wb))]

        if len(boards) == 0:
            print(winning_boards)
            print(winning_number)
            print(np.sum(winning_boards[0][np.imag(winning_board) == 0]))
            print(
                np.sum(winning_boards[0][np.imag(winning_board) == 0]) * winning_number
            )
            break
        boards = np.array(boards)
