#include <stdio.h>
#include <pthread.h>

void* thread_func(void* arg) {
    int thread_id = *(int*)arg;
    printf("Thread %d is running on core %ld\n", thread_id, (long)pthread_self());
    return NULL;
}

int main() {
    pthread_t thread1, thread2;
    int id1 = 1, id2 = 2;

    pthread_create(&thread1, NULL, thread_func, &id1);
    pthread_create(&thread2, NULL, thread_func, &id2);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    printf("Both threads completed.\n");
    return 0;
}