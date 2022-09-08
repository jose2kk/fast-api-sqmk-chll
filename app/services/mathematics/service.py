from math import gcd


def get_lcm(numbers):
    lcm = 1
    for i in numbers:
        lcm = (lcm * i)//gcd(lcm, i)
    return lcm
