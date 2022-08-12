

a, b = input().split()
def cf(num1, num2):
    listtemp = []
    for i in range(1, min(num1, num2) + 1):
        if num1 % i == num2 % i == 0:
            listtemp.append(i)
    return  listtemp
print(cf(int(a), int(b)))

