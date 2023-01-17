n = int(input())
f_list = [1, 1]
def Fibonacci(n: int):
    if n == 1 or n == 2:
        return 1
    else:
        for i in range(3, n+1):
            new = f_list[i-2] + f_list[i-3]
            f_list.append(new)
        return f_list[n-1]
