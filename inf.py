import time

t = time.perf_counter()
ar = [0]*10**9
for n in range(1, 10**9-1, 2):
    ar[n] = ar[n-1]+1
    ar[n+1] = ar[(n+1)//2]
print(ar.count(3))
t2 = time.perf_counter()

print(t2-t)