#include <stdio.h>
#include <stdlib.h>

// int NUM = 1000000;
int NUM = 1000;

int main() {
    int *prime; 
    prime = malloc(sizeof(int) * NUM);

    for (int i = 2; i <= NUM; i++) {
        prime[i] = 1;
    }

	for (int i=2; i * i <= NUM; i++) {
        if (prime[i] == 1) {
            for (int j = i * i; j < NUM + 1; j = j + i) {
                prime[j] = 0;
            }
        }
    }
    
    int count = 0;
	for (int i = 2; i <= NUM; i++) {
		if (prime[i]) {
			count++;
		}
	}

	printf("No. of primes <= %d: %d", NUM, count);
	return 0;
}
