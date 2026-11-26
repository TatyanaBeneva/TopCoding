def largestPerimeter(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    if len(nums) < 3:
        return 0

    perimeters = []

    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            for k in range(j + 1, len(nums)):
                max_side = nums[i]
                sum_sides = nums[k] + nums[j]
                if nums[j] > max_side:
                    max_side = nums[j]
                    sum_sides = nums[i] + nums[k]
                if nums[k] > max_side:
                    max_side = nums[k]
                    sum_sides = nums[i] + nums[j]

                if sum_sides > max_side:
                    perimeters.append(sum_sides + max_side)

        if len(nums) - 3 == i:
            break

    return max(perimeters) if len(perimeters) > 0 else 0

print(largestPerimeter([2,1,2]))
print(largestPerimeter([1,2,1,10]))

# Given an integer array nums, return the largest perimeter of a triangle with a non-zero area, formed from three of these lengths. If it is impossible to form any triangle of a non-zero area, return 0.
#
#
#
# Example 1:
#
# Input: nums = [2,1,2]
# Output: 5
# Explanation: You can form a triangle with three side lengths: 1, 2, and 2.
# Example 2:
#
# Input: nums = [1,2,1,10]
# Output: 0
# Explanation:
# You cannot use the side lengths 1, 1, and 2 to form a triangle.
# You cannot use the side lengths 1, 1, and 10 to form a triangle.
# You cannot use the side lengths 1, 2, and 10 to form a triangle.
# As we cannot use any three side lengths to form a triangle of non-zero area, we return 0.