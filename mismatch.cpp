// clang++ -Wall -std=c++17 -o mismatch mismatch.cpp
#include <algorithm>
#include <iostream>
#include <string>

bool has_prefix(const std::string& prefix, const std::string& str)
{
	return std::mismatch(prefix.begin(), prefix.end(), str.begin()).first == prefix.end();
}

bool has_suffix(const std::string& suffix, const std::string& str)
{
	return std::mismatch(suffix.rbegin(), suffix.rend(), str.rbegin()).first == suffix.rend();
}

int main()
{
	using namespace std;

	const string prefix = "prefix";
	string has_the_prefix= "prefix this string has it";

	const string suffix = "suffix";
	string has_the_suffix = "this string has the suffix";

	const string empty = "";

	assert(has_prefix(prefix, has_the_prefix));
	assert(has_prefix(empty, has_the_prefix));
	assert(!has_prefix(prefix, has_the_suffix));

	assert(has_suffix(suffix, has_the_suffix));
	assert(has_suffix(empty, has_the_suffix));
	assert(!has_suffix(suffix, has_the_prefix));
	return 0;
}
