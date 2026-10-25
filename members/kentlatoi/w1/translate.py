"""Member 4 - Return all prime numbers from 2 up to n"""


def primes_up_to(n: int) -> list[int]:
    """Return all primes from 2 through n using a sieve."""
    if n < 2:
        return []

    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False
    p = 2

    while p * p <= n:
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False

        p += 1

    primes = []
    for number in range(2, n + 1):
        if is_prime[number]:
            primes.append(number)

    return primes
