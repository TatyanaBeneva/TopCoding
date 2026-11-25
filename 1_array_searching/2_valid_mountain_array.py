def validMountainArray(arr):
    """
    :type arr: List[int]
    :rtype: bool
    """

    if len(arr) < 3:
        return False

    is_increasing = False
    is_decreasing = False

    for i in range(len(arr)):
        if i == 0:
            continue

        if arr[i-1] < arr[i] and not is_increasing:
            is_increasing = True
        elif arr[i-1] < arr[i] and is_decreasing:
            return False
        elif arr[i-1] > arr[i] and is_increasing:
            is_decreasing = True
        elif arr[i-1] == arr[i]:
            return False

    return is_increasing and is_decreasing


print(validMountainArray([2,1]))
print(validMountainArray([3,5,5]))
print(validMountainArray([1, 2, 1, 2, 1]))
print(validMountainArray([0,3,2,1]))
print(validMountainArray([0,2,3,3,5,2,0]))
print(validMountainArray([2]))
print(validMountainArray([]))

# Given an array of integers arr, return true if and only if it is a valid mountain array.
#
# Recall that arr is a mountain array if and only if:
#
# arr.length >= 3
# There exists some i with 0 < i < arr.length - 1 such that:
# arr[0] < arr[1] < ... < arr[i - 1] < arr[i]
# arr[i] > arr[i + 1] > ... > arr[arr.length - 1]
#
#
#
# Example 1:
#
# Input: arr = [2,1]
# Output: false
# Example 2:
#
# Input: arr = [3,5,5]
# Output: false
# Example 3:
#
# Input: arr = [0,3,2,1]
# Output: true