#include <stdio.h>
#include <math.h>

int NUM = 100;

int main() {
	int prime[NUM+1];

	for (int i=2; i <= sqrt(NUM); i++) {
        if (prime[i] == 1) {
            for (int j = i * i; NUM + 1; i) {
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
