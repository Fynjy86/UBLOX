import time

def t (f):
    f = f%1*1000000
    return ((f * 10**0) // 1) / 10**0

x = time.time()
print(x)
print(x%1)
print(t(x))
