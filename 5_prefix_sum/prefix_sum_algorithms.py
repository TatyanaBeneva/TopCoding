"""Prefix sum algorithms: five educational implementations.

All range endpoints are zero-based and inclusive. Input arrays are not
modified, except for explicit updates to a difference array.
Complexities assume constant-time integer arithmetic.
"""


# 1. SIMPLE PREFIX SUM ARRAY

def prefix_sum(numbers: list[int]) -> list[int]:
    """Build padded cumulative sums. Time O(n), space O(n)."""
    prefix = [0]
    for number in numbers:
        prefix.append(prefix[-1] + number)
    return prefix


def range_sum(prefix: list[int], left: int, right: int) -> int:
    """Sum original elements left through right. Time/space O(1)."""
    if not 0 <= left <= right < len(prefix) - 1:
        raise IndexError("Invalid range")
    return prefix[right + 1] - prefix[left]


# 2. 2D PREFIX SUM ARRAY (SUMMED-AREA TABLE)

def prefix_sum_2d(matrix: list[list[int]]) -> list[list[int]]:
    """Build a padded summed-area table. Time/space O(rows * cols)
    for nonempty matrices with at least one column.
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    if any(len(row) != cols for row in matrix):
        raise ValueError("Matrix must be rectangular")
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            # Subtract the overlapping region counted twice.
            prefix[r + 1][c + 1] = (
                matrix[r][c] + prefix[r][c + 1]
                + prefix[r + 1][c] - prefix[r][c]
            )
    return prefix


def rectangle_sum(prefix: list[list[int]], top: int, left: int,
                  bottom: int, right: int) -> int:
    """Sum an inclusive rectangle. Time/space O(1)."""
    if not (prefix and 0 <= top <= bottom < len(prefix) - 1
            and 0 <= left <= right < len(prefix[0]) - 1):
        raise IndexError("Invalid rectangle")
    return (prefix[bottom + 1][right + 1] - prefix[top][right + 1]
            - prefix[bottom + 1][left] + prefix[top][left])


# 3. MODULAR PREFIX SUM ARRAY

def modular_prefix_sum(numbers: list[int], modulus: int) -> list[int]:
    """Store cumulative sums modulo a positive integer. Time/space O(n)."""
    if modulus <= 0:
        raise ValueError("Modulus must be positive")
    prefix = [0]
    for number in numbers:
        prefix.append((prefix[-1] + number) % modulus)
    return prefix


def modular_range_sum(prefix: list[int], left: int, right: int,
                      modulus: int) -> int:
    """Range sum modulo the same modulus used to build prefix. O(1)."""
    if modulus <= 0:
        raise ValueError("Modulus must be positive")
    return range_sum(prefix, left, right) % modulus


def count_divisible_subarrays(numbers: list[int], modulus: int) -> int:
    """Count nonempty subarrays whose sums are divisible by modulus.
    Equal prefix remainders identify a divisible subarray.
    Time O(n) expected, space O(min(n + 1, modulus)).
    """
    if modulus <= 0:
        raise ValueError("Modulus must be positive")
    frequencies = {0: 1}
    remainder = total = 0
    for number in numbers:
        remainder = (remainder + number) % modulus
        total += frequencies.get(remainder, 0)
        frequencies[remainder] = frequencies.get(remainder, 0) + 1
    return total


# 4. PREFIX XOR ARRAY

def prefix_xor(numbers: list[int]) -> list[int]:
    """Build cumulative bitwise XOR values. Time/space O(n)."""
    prefix = [0]
    for number in numbers:
        prefix.append(prefix[-1] ^ number)
    return prefix


def range_xor(prefix: list[int], left: int, right: int) -> int:
    """XOR of original elements left through right. Time/space O(1)."""
    if not 0 <= left <= right < len(prefix) - 1:
        raise IndexError("Invalid range")
    # x ^ x == 0, so the common prefix cancels out.
    return prefix[right + 1] ^ prefix[left]


# 5. DIFFERENCE ARRAY (DELTA ARRAY)

def difference_array(numbers: list[int]) -> list[int]:
    """Build differences, plus one sentinel slot. Time/space O(n)."""
    diff = [0] * (len(numbers) + 1)
    for i, number in enumerate(numbers):
        diff[i] = number - (numbers[i - 1] if i else 0)
    if numbers:
        diff[-1] = -numbers[-1]
    return diff


def range_update(diff: list[int], left: int, right: int, value: int) -> None:
    """Add value to an inclusive range in place. Time/space O(1)."""
    if not 0 <= left <= right < len(diff) - 1:
        raise IndexError("Invalid range")
    diff[left] += value
    diff[right + 1] -= value


def reconstruct_array(diff: list[int]) -> list[int]:
    """Apply accumulated updates with a prefix sum. Time/space O(n)."""
    result = []
    current = 0
    for i in range(len(diff) - 1):
        current += diff[i]
        result.append(current)
    return result


def run_tests() -> None:
    """Check normal cases, empty inputs, negatives and boundary ranges."""
    from itertools import accumulate
    from operator import xor
    from functools import reduce
    from random import Random

    assert prefix_sum([]) == [0]
    assert prefix_sum_2d([]) == [[0]]
    assert prefix_sum_2d([[], []]) == [[0], [0], [0]]
    assert modular_prefix_sum([], 3) == [0]
    assert count_divisible_subarrays([], 3) == 0
    assert prefix_xor([]) == [0]
    assert reconstruct_array(difference_array([])) == []
    rng = Random(42)
    for n in range(1, 21):
        numbers = [rng.randint(-10, 10) for _ in range(n)]
        p = prefix_sum(numbers)
        x = prefix_xor(numbers)
        assert p == [0, *accumulate(numbers)]
        for modulus in (1, 3, 7):
            m = modular_prefix_sum(numbers, modulus)
            count = 0
            for left in range(n):
                for right in range(left, n):
                    segment = numbers[left:right + 1]
                    assert range_sum(p, left, right) == sum(segment)
                    assert modular_range_sum(m, left, right, modulus) == sum(segment) % modulus
                    assert range_xor(x, left, right) == reduce(xor, segment, 0)
                    count += sum(segment) % modulus == 0
            assert count_divisible_subarrays(numbers, modulus) == count
        diff = difference_array(numbers)
        expected = numbers.copy()
        assert reconstruct_array(diff) == expected
        for _ in range(10):
            left = rng.randrange(n)
            right = rng.randrange(left, n)
            value = rng.randint(-10, 10)
            range_update(diff, left, right, value)
            for i in range(left, right + 1):
                expected[i] += value
            assert reconstruct_array(diff) == expected
    matrix = [[1, -2, 3], [4, 5, 6], [7, 8, 9]]
    p2 = prefix_sum_2d(matrix)
    for top in range(3):
        for bottom in range(top, 3):
            for left in range(3):
                for right in range(left, 3):
                    assert rectangle_sum(p2, top, left, bottom, right) == sum(
                        sum(row[left:right + 1]) for row in matrix[top:bottom + 1]
                    )
    for call, error in (
        (lambda: range_sum([0], 0, 0), IndexError),
        (lambda: range_xor([0], -1, 0), IndexError),
        (lambda: rectangle_sum([[0]], 0, 0, 0, 0), IndexError),
        (lambda: range_update([0], 0, 0, 1), IndexError),
        (lambda: prefix_sum_2d([[1], [2, 3]]), ValueError),
        (lambda: modular_prefix_sum([1], 0), ValueError),
        (lambda: modular_range_sum([0, 1], 0, 0, -1), ValueError),
        (lambda: count_divisible_subarrays([1], 0), ValueError),
    ):
        try:
            call()
        except error:
            pass
        else:
            raise AssertionError(f"Expected {error.__name__}")
    print("All tests passed.")


if __name__ == "__main__":
    numbers = [2, 4, 6, 8, 10]
    p = prefix_sum(numbers)
    print("1. Prefix sum:", p, "| range [1, 3]:", range_sum(p, 1, 3))
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    p2 = prefix_sum_2d(matrix)
    print("2. 2D prefix:", p2, "| rectangle:", rectangle_sum(p2, 1, 1, 2, 2))
    m = modular_prefix_sum(numbers, 5)
    print("3. Modular prefix:", m, "| range mod 5:", modular_range_sum(m, 1, 3, 5))
    print("   Divisible subarrays:", count_divisible_subarrays([4, 5, 0, -2, -3, 1], 5))
    x = prefix_xor(numbers)
    print("4. Prefix XOR:", x, "| range XOR:", range_xor(x, 1, 3))
    diff = difference_array(numbers)
    print("5. Difference array:", diff)
    range_update(diff, 1, 3, 5)
    print("   Updated array:", reconstruct_array(diff))
    run_tests()
