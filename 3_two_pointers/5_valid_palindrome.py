def validPalindrome(s):
    """
    :type s: str
    :rtype: bool
    """
    def is_palindrome(l, r):
        while l < r:
            if s[l] != s[r]:
                return False

            l += 1
            r -= 1

        return True

    left = 0
    right = len(s) - 1

    while left < right:
        if s[left] != s[right]:
            return is_palindrome(left+1, right) or is_palindrome(left, right-1)
        left += 1
        right -= 1

    return True

print(validPalindrome("aba"))
print(validPalindrome("abca"))
print(validPalindrome("abc"))

# Given a string s, return true if the s can be palindrome after deleting at most one character from it.
#
#
#
# Example 1:
#
# Input: s = "aba"
# Output: true
# Example 2:
#
# Input: s = "abca"
# Output: true
# Explanation: You could delete the character 'c'.
# Example 3:
#
# Input: s = "abc"
# Output: false