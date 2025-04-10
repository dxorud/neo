#!/usr/bin/env python

def gcd(a, b):
    while b != 0:
        r = a % b
        a = b
        b = r
    return a

a = int(input("Input First Number : "))
b = int(input("Input Second Number : "))

print(f'gcd({a}, {b}) of {a}, {b} = {gcd(a,b)}')
