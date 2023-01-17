def Prime(number: int):
    result = []
    if number == 2:
        return [2]
    else:
        for i in range(2, number+1):
            isPrime = True
            for j in range(2, i//2+1):
                if i % j == 0:
                    isPrime = False
                    break
            if isPrime:
                result.append(i)
        return result


print(Prime(50))






