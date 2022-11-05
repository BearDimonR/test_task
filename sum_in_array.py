# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:59:22 2022

@author: Okhrimchuk Roman & Maksym Veremchuk
for Sierentz Global Merchants


Test task
"""

"""
Approaches

1. Brute force

Complexity O(n^2), Memory O(1)

Idea: for each element "i" in sorted array, found if there is "s - i" element

2. Binary search

Complexity O(n*logn), Memory O(1) (for iterative implementation)

Idea: for each element "i" in sorted array, found if there is "s-i" element using binary search

3. Two pointers

Complexity O(n), Memory O(1) (for iterative implementation)

Idea: make two pointers and move them to each other in the following conditions:
    - if total value more than S, move right pointer to the left
    - if total value less that S, move left pointer to the right
    - if total value equals S, it is your solution
    - if indexes are equal, there is no solution
    

Let's implement the best of these (which is the last one)
"""

def sum_in_array(sort_array, s):
    left_index = 0
    right_index = len(sort_array) - 1
    if right_index == -1:
        return [-1]
    while left_index != right_index:
        left_val = sort_array[left_index]
        right_val = sort_array[right_index]
        total_val = left_val + right_val
        if total_val > s:
            right_index -= 1
            continue
        elif total_val < s:
            left_index += 1
            continue
        elif total_val == s:
            return [left_val, right_val]
    return [-1]


# tests
tests = [
    ([-3, 1, 4, 6], 7, [1, 6]),
    ([-3, 1, 4, 6], 8, [-1]),
    ([-3, 4, 5], 10, [-1]),
    ([-3, 5, 5], 10, [5, 5]),
    ([-3, 4, 5], 4, [-1]),
    ([], 10, [-1]),
    ([3, 5, 7, 10], 10, [3, 7])
]

for input_arr, s, output in tests:
    result = sum_in_array(input_arr, s)
    string_to_print = f's: {s}, input: {input_arr}, output: {output}, result: {result}'
    print(string_to_print)
    assert result == output, string_to_print
    