"""Member 4 - Return all prime numbers from 2 up to n"""
def primes_up_to(n: int) -> list[int]:
    if n < 2:
        return []

    isPrime = [True] * (n + 1)
    isPrime[0] = False
    isPrime[1] = False
    p = 2

    while p * p <= n:
        if isPrime[p]:
            for multiple in range(p * p, n + 1, p):
                isPrime[multiple] = False

        p += 1
 
    primes = []
    for number in range(2, n + 1):
        if isPrime[number]:
            primes.append(number)

    return primes