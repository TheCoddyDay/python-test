# https://discord.gg/qeEXh5gD6k

# febonacci series in python

def fib(n):
    """
    :n: interger
    """
    a, b = 0, 1
    c = []
    for i in range(n):
        a,b = b, a+b
        c.append(a)
    else:
        print("done")
        return c

# getting fibbonacci list till 10 number
fib_ = fib(10)
print(fib_)
