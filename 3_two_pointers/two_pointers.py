"""Eight examples of the two pointers technique, with type hints and tests.

Functions that modify lists in place return the same list for convenience.
Complexities use the standard algorithmic model, excluding Python's internal
list-deletion bookkeeping. Sorted-input requirements are noted below.
"""


# 1. Opposite-direction pointers: reverse an array in place.
# Time: O(n), auxiliary space: O(1).
def reverse_array(numbers: list[int]) -> list[int]:
    left = 0
    right = len(numbers) - 1

    while left < right:
        numbers[left], numbers[right] = numbers[right], numbers[left]
        left += 1
        right -= 1

    return numbers


# 2. Opposite-direction pointers: find two values with the target sum.
# Requires ascending sorted input. Time: O(n), auxiliary space: O(1).
def two_sum(numbers: list[int], target: int) -> tuple[int, int] | None:
    left = 0
    right = len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]

        if current_sum == target:
            return numbers[left], numbers[right]
        if current_sum < target:
            left += 1
        else:
            right -= 1

    return None


# 3. Opposite-direction pointers: check a palindrome.
# Case-sensitive, including spaces. Time: O(n), auxiliary space: O(1).
def is_palindrome(text: str) -> bool:
    left = 0
    right = len(text) - 1

    while left < right:
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1

    return True


# 4. Same-direction pointers: remove duplicates from a sorted array in place.
# Time: O(n), algorithmic auxiliary space: O(1).
def remove_duplicates(numbers: list[int]) -> list[int]:
    if not numbers:
        return numbers

    slow = 0

    for fast in range(1, len(numbers)):
        if numbers[fast] != numbers[slow]:
            slow += 1
            numbers[slow] = numbers[fast]

    del numbers[slow + 1:]
    return numbers


# 5. Same-direction pointers: remove all occurrences of a target in place.
# Time: O(n), algorithmic auxiliary space: O(1).
def remove_all(numbers: list[int], target: int) -> list[int]:
    slow = 0

    for fast in range(len(numbers)):
        if numbers[fast] != target:
            numbers[slow] = numbers[fast]
            slow += 1

    del numbers[slow:]
    return numbers


# 6. Same-direction pointers: move zeros to the end in place.
# Preserves the relative order of nonzero elements.
# Time: O(n), auxiliary space: O(1).
def move_zeros(numbers: list[int]) -> list[int]:
    slow = 0

    for fast in range(len(numbers)):
        if numbers[fast] != 0:
            numbers[slow], numbers[fast] = numbers[fast], numbers[slow]
            slow += 1

    return numbers


# 7. Separate-array pointers: merge two ascending sorted arrays.
# Time: O(n + m), space: O(n + m) including the output and slices.
def merge_arrays(first: list[int], second: list[int]) -> list[int]:
    i = j = 0
    result = []

    while i < len(first) and j < len(second):
        if first[i] <= second[j]:
            result.append(first[i])
            i += 1
        else:
            result.append(second[j])
            j += 1

    result.extend(first[i:])
    result.extend(second[j:])
    return result


# 8. Opposite-direction pointers: container with most water.
# Heights must be nonnegative. Time: O(n), auxiliary space: O(1).
def max_area(heights: list[int]) -> int:
    left = 0
    right = len(heights) - 1
    maximum = 0

    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        maximum = max(maximum, width * height)

        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return maximum


def run_tests() -> None:
    assert reverse_array([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]
    assert reverse_array([]) == []
    assert reverse_array([1]) == [1]
    assert two_sum([1, 2, 4, 6, 8, 9, 12], 14) == (2, 12)
    assert two_sum([], 3) is None
    assert two_sum([2], 4) is None
    assert two_sum([-3, 0, 3], 0) == (-3, 3)
    assert two_sum([2, 2], 4) == (2, 2)
    assert is_palindrome('racecar')
    assert not is_palindrome('hello')
    assert is_palindrome('')
    assert remove_duplicates([1, 1, 2, 2, 3, 4, 4]) == [1, 2, 3, 4]
    assert remove_duplicates([]) == []
    assert remove_duplicates([1, 1]) == [1]
    assert remove_all([1, 2, 3, 2, 4, 2, 5], 2) == [1, 3, 4, 5]
    assert remove_all([2, 2], 2) == []
    assert remove_all([], 2) == []
    assert remove_all([1, 3], 2) == [1, 3]
    assert move_zeros([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]
    assert move_zeros([0, 0]) == [0, 0]
    assert move_zeros([]) == []
    assert merge_arrays([1, 3, 5, 7], [2, 4, 6, 8]) == list(range(1, 9))
    assert merge_arrays([], [1]) == [1]
    assert merge_arrays([1, 1], [1, 2]) == [1, 1, 1, 2]
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert max_area([]) == 0
    assert max_area([5]) == 0
    assert max_area([1, 1]) == 1


if __name__ == '__main__':
    print('Reverse array:', reverse_array([1, 2, 3, 4, 5]))
    print('Two sum:', two_sum([1, 2, 4, 6, 8, 9, 12], 14))
    print('Palindrome:', is_palindrome('racecar'))
    print('Remove duplicates:', remove_duplicates([1, 1, 2, 2, 3, 4, 4]))
    print('Remove target:', remove_all([1, 2, 3, 2, 4, 2, 5], 2))
    print('Move zeros:', move_zeros([0, 1, 0, 3, 12]))
    print('Merge arrays:', merge_arrays([1, 3, 5, 7], [2, 4, 6, 8]))
    print('Maximum water area:', max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))
    run_tests()
    print('All tests passed.')
