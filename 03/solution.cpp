#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <numeric>
#include <string>
#include <vector>

template <typename Vector> void print_vector(const Vector &vec) {
  using T = typename Vector::value_type;
  std::copy(std::begin(vec), std::end(vec),
            std::ostream_iterator<T>(std::cout, "\n"));
}

template <typename T> struct read_result {
  int bit_width;
  std::vector<T> vec;
};

template <typename T>
auto read_binary_strings_to_vector(const char *file_path) -> read_result<T> {
  auto file = std::fstream(file_path);
  auto vec = std::vector<T>{};
  vec.reserve(2000);
  auto bit_width = 0;
  for (std::string line; std::getline(file, line);) {
    bit_width = line.length();
    vec.emplace_back(static_cast<T>(std::stoi(line, nullptr, 2)));
  }
  return {bit_width, vec};
}

template <typename T>
auto most_common_bit_in_column(std::vector<T> vec, int col) -> T {
  std::transform(vec.begin(), vec.end(), vec.begin(),
                 [col](auto val) { return (val & (1 << (col))) >> (col); });
  auto col_sum =
      static_cast<double>(std::accumulate(vec.begin(), vec.end(), 0));
  return (vec.size() / col_sum) > 2;
}

template <typename T>
auto all_most_common_bits(std::vector<T> vec, int bit_width) -> std::vector<T> {
  std::vector<T> most_common_bits;
  most_common_bits.reserve(bit_width);
  for (auto i = 0; i < bit_width; ++i) {
    most_common_bits.emplace_back(most_common_bit_in_column(vec, i));
  }
  return most_common_bits;
}

template <typename T>
auto binary_vector_to_number(std::vector<T> bin_vec, int bit_width) {
  auto bin_str = std::string(bin_vec.size(), '0');
  std::transform(bin_vec.rbegin(), bin_vec.rend(), bin_str.begin(),
                 [](auto &val) { return val ? '1' : '0'; });
  auto integer = static_cast<T>(stoi(bin_str, nullptr, 2));
  return integer;
}

auto main() -> int {
  auto read_res = read_binary_strings_to_vector<int>("input.txt");
  auto bit_width = read_res.bit_width;
  auto values = read_res.vec;
  auto most_common_bits = all_most_common_bits(values, bit_width);
  auto gamma = binary_vector_to_number(most_common_bits, bit_width);
  auto mask = (~0u >> ((8 * sizeof(int)) -
                       bit_width)); // mask out all 1s that don't
                                    // belong to the current bit width
  auto epsilon = static_cast<unsigned int>(~gamma) & mask;

  std::cout << "Solution 1: " << gamma * epsilon << "\n";
}
