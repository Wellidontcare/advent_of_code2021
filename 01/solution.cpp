#include <algorithm>
#include <initializer_list>
#include <iterator>
#include <numeric>
#include <string>
#include <typeinfo>
#include <valarray>
#include <vector>
#include <iostream>
#include <fstream>


template<typename T>
auto string_to_number(const std::string& str) -> T;

template<>
auto string_to_number<int>(const std::string& str) -> int{
	return std::stoi(str);
}

template<>
auto string_to_number<int64_t>(const std::string& str) -> int64_t{
	return std::stoi(str);
}

template<>
auto string_to_number<double>(const std::string& str) -> double {
	return std::stod(str);
}


template<typename T>
auto read_data_to_vector(const char* file_path) -> std::vector<T>{
	std::fstream file(file_path);
	std::vector<T> data;
	data.reserve(2000);
	std::string line;
	int64_t count = 0;
	for(std::string line; std::getline(file, line);){
		data.emplace_back(string_to_number<T>(line));
		count++;
	}
	std::cout << "Read " << count << " lines\n";
	return data;
}


template<typename Container>
auto count_increase(Container data) -> Container::value_type {
	Container diff(data.size());
	std::adjacent_difference(data.begin(), data.end(), diff.begin());
	return std::count_if(diff.begin()+1, diff.end(), [](auto value){return value > 0;});
}

template<typename Container>
auto correlate_valid(const Container& left, const Container& right) -> Container{
	using T = Container::value_type;

	auto valid_size = left.size() - right.size() + 1;
	Container convolved(valid_size);
	auto data_array = std::valarray<T>(left.size());
	std::copy(left.begin(), left.end(), std::begin(data_array));
	auto mask = std::valarray<T>(right.size());
	std::copy(right.begin(), right.end(), std::begin(mask));
	auto slice_size = right.size();
	for(auto start_index = 0ull; start_index < valid_size; start_index++){
		std::valarray<T> multiplied = std::valarray<T>(data_array[std::slice(start_index, slice_size, 1)]) * mask;
		convolved[start_index] = multiplied.sum();
	}
	return convolved;
}

auto main() -> int{
	auto data = read_data_to_vector<double>("input.txt");
	std::cout << "Solution 1: " << count_increase(data) << "\n";
	std::cout << "Solution 2: " << count_increase(correlate_valid(data, {1, 1, 1})) << "\n";
}
