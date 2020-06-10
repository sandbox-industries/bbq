import functools

# Pythonized version of Egnor's

N = 51

l = [1]*N 

for i in range(1, N):
    l[i] = sum(l[max(0, i-4):i])

print(l[-1])

# Memory efficient version

def foo(n):
    i, a, b, c, d = 0, 1, 1, 2, 4
    while i < n:
        i, a, b, c, d = i+1, b, c, d, a+b+c+d
    return a

print(foo(50))

# Sanity deficient version

print(functools.reduce(lambda fa, fb: lambda a, b, c, d: fa(*fb(a, b, c, d)), [lambda a, b, c, d: (b, c, d, a+b+c+d)]*50, lambda a, b, c, d: (a, b, c, d))(1, 1, 2, 4)[0])

