import numpy as np

if __name__ == "__main__":
    drawn_numbers = np.loadtxt("input.txt", delimiter=",", max_rows=1, dtype=int)
    boards = np.loadtxt("input.txt", skiprows=1, dtype=int)
    boards = boards.reshape((100, 5, 5)).astype(complex)
    finish = False
    winning_board = None
    winning_number = 0
    for num in drawn_numbers:
        boards[(boards == num) & (np.imag(boards) == 0)] += 1j
        for board in boards:
            if np.any(np.imag(np.sum(board, axis=0)) == 5) or np.any(
                np.imag(np.sum(board, axis=1)) == 5
            ):
                winning_board = board
                winning_number = num
                finish = True
                break
        if finish:
            break

    print(np.sum(winning_board[np.imag(winning_board) == 0]) * winning_number)
