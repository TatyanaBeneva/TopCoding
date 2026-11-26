def reverseWords(s):
    """
    :type s: str
    :rtype: str
    """
    words = s.split()
    reversed_words = []
    for word in words:
        reversed_words.append(word[::-1])

    return " ".join(reversed_words)



print(reverseWords("Let's take LeetCode contest"))
print(reverseWords("Mr Ding"))

# Given a string s, reverse the order of characters in each word within a sentence while still preserving whitespace and initial word order.
#
#
#
# Example 1:
#
# Input: s = "Let's take LeetCode contest"
# Output: "s'teL ekat edoCteeL tsetnoc"
# Example 2:
#
# Input: s = "Mr Ding"
# Output: "rM gniD"
#