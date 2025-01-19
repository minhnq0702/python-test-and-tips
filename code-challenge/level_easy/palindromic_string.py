"""
https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/palindrome-check-2/
"""
def palidromic_string():
    """
    Input and check if string is palidrome
    """
    s = input()
    print(s == s[::-1] and 'YES' or 'NO')
