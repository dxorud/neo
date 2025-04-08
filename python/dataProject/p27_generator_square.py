#!/usr/bin/env python

def square_number(nums):
    for i in nums:
        yield i ** i

mynum = [1, 2, 3, 4, 5]
result = square_number(mynum)

for i in range(len(mynum)):
    print(f'Squsre number: {mynum[i]} ^ {mynum[i]} : {next(result)}')