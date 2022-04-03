#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <numeric>
#include <string>
#include <vector>
#include <list>

template <typename Vector> void print_vector(const Vector &vec) {
  using T = typename Vector::value_type;
  std::copy(std::begin(vec), std::end(vec),
            std::ostream_iterator<T>(std::cout, "\n"));
}

template <typename T>
constexpr T bit_at(T value, unsigned index, unsigned bit_width) {
  return static_cast<T>(static_cast<bool>(value & (1 << (bit_width - index - 1))));
}

template <typename T> struct read_result {
  int bit_width;
  std::vector<T> vec;
};

template <typename T>
auto read_binary_strings_to_vector(const char *file_path) -> read_result<T> {
  auto file = std::ifstream(file_path);
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
auto most_common_bit_in_column(std::vector<T> vec, int col, unsigned bit_width)
    -> T {
  std::transform(vec.begin(), vec.end(), vec.begin(),
                 [=](auto val) { return bit_at(val, col, bit_width); });
  auto col_sum =
      static_cast<double>(std::accumulate(vec.begin(), vec.end(), 0));
  return col_sum >= (vec.size() / 2.0);
}

template <typename T>
auto all_most_common_bits(std::vector<T> vec, unsigned bit_width)
    -> std::vector<T> {
  std::vector<T> most_common_bits;
  most_common_bits.reserve(bit_width);
  for (auto i = 0; i < bit_width; ++i) {
    most_common_bits.emplace_back(most_common_bit_in_column(vec, i, bit_width));
  }
  return most_common_bits;
}


enum class device_type { OXYGEN_GENERATOR, CO2_SCRUBBER };

template <typename T>
auto device_rating(const std::vector<T> &vec, unsigned bit_width,
                   device_type type) {
  auto numbers = std::list<T>{};
  std::copy(vec.begin(), vec.end(), std::back_inserter(numbers));
  auto cur_col = 0u;
  while (numbers.size() != 1) {
    auto temp_vec = std::vector<T>{};
    temp_vec.reserve(numbers.size());
    std::copy(numbers.begin(), numbers.end(), std::back_inserter(temp_vec));
    T test_bit = 0;
    switch (type) {
    case device_type::OXYGEN_GENERATOR:
      test_bit = most_common_bit_in_column(temp_vec, cur_col, bit_width);
      break;
    case device_type::CO2_SCRUBBER:
      test_bit = !most_common_bit_in_column(temp_vec, cur_col, bit_width);
      break;
    }

    numbers.remove_if([&](auto n) {
      auto cur_bit = bit_at(n, cur_col, bit_width);
      return cur_bit != test_bit;
    });
    cur_col++;
  }
  return numbers.front();
}

template <typename T>
auto binary_vector_to_number(const std::vector<T>& bin_vec, int bit_width) {
  auto bin_str = std::string(bin_vec.size(), '0');
  std::transform(bin_vec.begin(), bin_vec.end(), bin_str.begin(),
                 [](auto &val) { return val ? '1' : '0'; });
  auto integer = static_cast<T>(stoi(bin_str, nullptr, 2));
  return integer;
}

template <typename T> std::string to_binary(T number, unsigned bit_width) {
  std::string binary(bit_width, '0');
  auto cur_col = 0;
  std::transform(binary.begin(), binary.end(), binary.begin(),
                 [&](auto &c) { return bit_at(c, cur_col++, bit_width); });
  return binary;
}

auto main() -> int {
  auto [bit_width, values] =
      read_binary_strings_to_vector<unsigned int>("input.txt");
  auto most_common_bits = all_most_common_bits(values, bit_width);
  auto gamma = binary_vector_to_number(most_common_bits, bit_width);
  auto mask = (~0u >> ((8 * sizeof(int)) -
                       bit_width)); // mask out all 1s that don't
                                    // belong to the current bit width
  auto epsilon = static_cast<unsigned int>(~gamma) & mask;

  std::cout << "Solution 1: " << gamma * epsilon << "\n";
  auto oxygen_rating =
      device_rating(values, bit_width, device_type::OXYGEN_GENERATOR);
  auto co2_scrubber_rating =
      device_rating(values, bit_width, device_type::CO2_SCRUBBER);
  std::cout << "Solution 2: " << oxygen_rating * co2_scrubber_rating << "\n";
}
