#include <algorithm>
#include <complex>
#include <fstream>
#include <iostream>
#include <iterator>
#include <list>
#include <memory>
#include <numeric>
#include <sstream>
#include <string>
#include <valarray>
#include <vector>
#include <functional>

using board_entry_t = std::complex<int>;

constexpr auto BOARD_WIDTH = 5;
constexpr auto BOARD_HEIGHT = 5;
constexpr auto BOARD_SIZE = BOARD_WIDTH*BOARD_HEIGHT;
constexpr auto tag = board_entry_t(0, 1);

template <typename Vector> void print_vector(const Vector &vec) {
  using T = typename Vector::value_type;
  std::copy(std::begin(vec), std::end(vec),
            std::ostream_iterator<T>(std::cout, "\n"));
}

struct bingo_input_t {
  std::vector<int> drawn_numbers;
  std::valarray<board_entry_t> boards;
  int board_count;
};

auto read_input(const char *file_path) -> bingo_input_t {
  auto file = std::ifstream(file_path);
  auto drawn_numbers = std::vector<int>{};
  drawn_numbers.reserve(2000);
  auto bit_width = 0;
  {
    std::string line;
    std::getline(file, line);
    std::stringstream line_ss(line);
    while (line_ss.good()) {
      std::string num;
      std::getline(line_ss, num, ',');
      drawn_numbers.emplace_back(std::stoi(num));
    }
  }
  auto boards_vec = std::vector<board_entry_t>{};
  boards_vec.reserve(2000);
  int board_count = 0;
  while (!file.eof()) {
    for (int i = 0; i < 5; ++i) {
      auto line = std::string{};
      std::getline(file, line);
      auto line_ss = std::stringstream(line);
      auto ss_iterator = std::istream_iterator<int>(line_ss);
      std::copy(ss_iterator, std::istream_iterator<int>{},
                std::back_inserter(boards_vec));
    }
    board_count++;
  }
  auto boards =
      std::valarray<board_entry_t>(boards_vec.data(), boards_vec.size());
  return {drawn_numbers, boards, board_count};
}

struct winner_t {
  int sum_of_board;
  int winning_number;
};

auto get_winning_board(const bingo_input_t &input) -> winner_t {
  auto [drawn_numbers, boards, board_count] = input;
  auto winning_number = 0;
  auto winning_board_sum = 0;
  for (auto num : drawn_numbers) {
    std::transform(std::begin(boards), std::end(boards), std::begin(boards),
                   [num](auto entry) {
                     if ((entry.real()) == num)
                       return entry + tag;
                     return entry;
                   });
    for (int i = 0; i < board_count; ++i) {
      std::valarray<board_entry_t> board = boards[std::gslice(
          i * BOARD_SIZE, {BOARD_WIDTH, BOARD_HEIGHT}, {BOARD_WIDTH, 1})];
      for (int row = 0; row < BOARD_HEIGHT; ++row) {
        auto sum = std::valarray<board_entry_t>(
                       board[std::slice(row * BOARD_WIDTH, BOARD_WIDTH, 1)])
                       .sum();
        if (sum.imag() == BOARD_WIDTH) {
          winning_number = num;
          winning_board_sum =
              std::accumulate(std::begin(board), std::end(board),
                              board_entry_t{},
                              [](board_entry_t a, board_entry_t b) {
                                return (a.imag() | b.imag()) == 0 ? a + b : a;
                              })
                  .real();
          goto exit;
        }
      }
      for (int col = 0; col < BOARD_HEIGHT; ++col) {
        auto sum =
            std::valarray<board_entry_t>(
                board[std::gslice(col, {BOARD_HEIGHT, 1}, {BOARD_WIDTH, 1})])
                .sum();
        if (sum.imag() == BOARD_WIDTH) {
          winning_number = num;
          winning_board_sum =
              std::accumulate(std::begin(board), std::end(board),
                              board_entry_t{},
                              [](board_entry_t a, board_entry_t b) {
                                return (a.imag() | b.imag()) == 0 ? a + b : a;
                              })
                  .real();
          goto exit;
        }
      }

      // for (int y = 0; y < BOARD_HEIGHT; ++y) {
      // for (int x = 0; x < BOARD_WIDTH; ++x) {
      // std::cout << board[x + BOARD_WIDTH * y] << " ";
      //}
      // std::cout << "\n";
      //}
      // std::cout << "\n";
    }
  }
exit:
  return {winning_board_sum, winning_number};
  return {0, 0};
}

auto main() -> int {
  auto input = read_input("input.txt");
  auto [board_sum, winning_board] = get_winning_board(input);
  std::cout << "Solution 1: " << board_sum * winning_board << "\n";
}
