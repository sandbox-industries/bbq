# All math credit goes to Egnor and Daul
print([((a * (1000 // sum([a,b,c]))) * (b * (1000 // sum([a,b,c]))) * (c * (1000 // sum([a,b,c])))) for a, b, c in [((2 * x), (x ** 2 - 1), (x ** 2 + 1)) for x in range(1,5)] if 1000 % sum([a,b,c]) == 0][1])
