def number_of_prime_numbers_in(n):
    non_primes = []
    num_of_primes = 0
    for num in range(2, n + 1):
        if num in non_primes:
            continue
        add_multiples_to_non_primes(non_primes, num, n)
        num_of_primes += 1
    return num_of_primes

def add_multiples_to_non_primes(non_primes, num, n):
    multiply_with = 1
    while num * multiply_with <= n:
        non_primes.append(num * multiply_with)
        multiply_with += 1

print (number_of_prime_numbers_in(1000))

# todo: create a dictionary of already calculated nums.. decrease the time
