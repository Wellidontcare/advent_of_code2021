#include <algorithm>
#include <array>
#include <fstream>
#include <initializer_list>
#include <iostream>
#include <iterator>
#include <map>
#include <numeric>
#include <sstream>
#include <string>
#include <string_view>
#include <valarray>
#include <vector>

enum class direction { FORWARD = 0, DOWN, UP, INC_AIM, DEC_AIM };
enum class state { HORIZONTAL_POS = 0, VERTICAL_POS, AIM };

const std::array<std::valarray<int>, 5> direction_to_submarine_movement = {
    {{1, 0, 0}, {0, 1, 0}, {0, -1, 0}, {0, 0, 1}, {0, 0, -1}}};

const std::map<std::string, direction> direction_string_to_direction_simple{
    {"forward", direction::FORWARD},
    {"down", direction::DOWN},
    {"up", direction::UP}};

const std::map<std::string, direction> direction_string_to_direction_extended{
    {"forward", direction::FORWARD},
    {"down", direction::INC_AIM},
    {"up", direction::DEC_AIM}};

template <typename Vector> void print_vector(const Vector &vec) {
  using T = Vector::value_type;
  std::copy(std::begin(vec), std::end(vec), std::ostream_iterator<T>(std::cout, "\n"));
}

struct submarine_input {
  direction dir;
  int ammount;
};

struct raw_submarine_input{
  std::string dir;
  int ammount;
};

struct submarine_position{
  int x, y, aim;
};

auto read_input(const char *file_path) -> std::vector<raw_submarine_input> {
  std::fstream file(file_path);
  std::vector<raw_submarine_input> input;
  input.reserve(2000);
  for (std::string line; std::getline(file, line);) {
    auto line_stream = std::stringstream(line);
    std::string dir;
    int ammount;
    line_stream >> dir;
    line_stream >> ammount;
    input.emplace_back(dir, ammount);
  }
  return input;
}

auto parse_input_simple(const std::vector<raw_submarine_input> &input)
    -> std::vector<submarine_input> {
  std::vector<submarine_input> directions;
  for (auto [dir, ammount] : input) {
    directions.emplace_back(direction_string_to_direction_simple.at(dir),
                            ammount);
  }
  return directions;
}

auto parse_input_extended(const std::vector<raw_submarine_input> &input)
    -> std::vector<submarine_input> {
  std::vector<submarine_input> directions;
  for (auto [dir, ammount] : input) {
    directions.emplace_back(direction_string_to_direction_extended.at(dir),
                            ammount);
  }
  return directions;
}

auto calculate_submarine_position_simple(
    const std::vector<submarine_input> &directions) -> submarine_position {
  auto position = std::valarray<int>{0, 0, 0};
  for (auto [direction, ammount] : directions) {
    position += direction_to_submarine_movement.at(static_cast<int>(direction)) * ammount;
  }
  return {position[0], position[1], position[2]};
}

auto calculate_submarine_position_extended(
    const std::vector<submarine_input> &directions) -> submarine_position {
	auto position = std::valarray<int>{0, 0, 0};
	for(auto [direction, ammount] : directions){
          position +=
              direction_to_submarine_movement.at(static_cast<int>(direction)) *
              ammount;

          // no branching
          position[1] += position[2] * ammount *
                         static_cast<int>(!static_cast<bool>(
                             direction)) /*1 if FORWARD 0 otherwise*/;
        }
        return {position[0], position[1], position[2]};
}

auto main() -> int {
  auto raw_submarine_inputs = read_input("input.txt");
  {
    auto submarine_inputs = parse_input_simple(raw_submarine_inputs);
    auto [x, y, aim] = calculate_submarine_position_simple(submarine_inputs);
    std::cout << "Solution 1:  "
              << "X: " << x << " Y: " << y << " | "
              << "X*Y: " << x * y << "\n";
  }
  {
    auto submarine_inputs = parse_input_extended(raw_submarine_inputs);
    auto [x, y, aim] = calculate_submarine_position_extended(submarine_inputs);
    std::cout << "Solution 2:  "
              << "X: " << x << " Y " << y << " | "
              << "X*Y: " << x * y << "\n";
  }
}
