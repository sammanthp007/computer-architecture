def number_of_prime_numbers_in(n):
    non_primes = []
    primes = []
    for num in range(2, n + 1):
        if num not in non_primes:
            primes.append(num)
            for j in xrange(num * num, n + 1, num):
                non_primes.append(j)
    return len(primes)

print (number_of_prime_numbers_in(100000))

# todo: create a dictionary of already calculated nums.. decrease the time
