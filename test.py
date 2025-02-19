def isPalindrome(x: int) -> bool:
    if x <= 0:
        return False

    result = 0
    num = x
    while num:
        rest = num % 10
        result = result * 10 + rest
        num = num // 10

    print(result == x)
    return result ^ x == 0

isPalindrome(121)