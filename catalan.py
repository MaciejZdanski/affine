# N-ty wyraz ciągu Catalana
def catalan(n):
    b = 0
    if n == 0:
        return 1
    else:
        for i in range (n):
            b += (catalan(i))*(catalan(n-1-i))
    return b

print(catalan(26))