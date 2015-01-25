## The introduction

The reader-writer problem appears in many different contexts. For example a web server cache needs to quickly serve the same static page for many thousands of requests. Occasionally however an author may decide to update the page.

We will examine one specific form of the reader-writer problem where there are many readers and some occasional writers and we need to ensure that a writer gets exclusive access. For performance however readers should be able to perform the read without waiting for another reader. 

See [[Synchronization,-Part-7:-The-Reader-Writer-Problem]] for part 1

## Candidate solution #3
Candidate solutions 1 and 2 are discussed in [[part 1|Synchronization,-Part-7:-The-Reader-Writer-Problem]].


In the code below for clarity `lock` and `cond_wait` are shortened versions `pthread_mutex_lock` and `pthread_cond_wait` etc. respectively

Also remember that `pthread_cond_wait` performs *Three* actions. Firstly it atomically unlocks the mutex and then sleeps (until it is woken by `pthread_cond_signal` or `pthread_cond_broadcast`). Thirdly the awoken thread must re-acquire the mutex lock before returning. Thus only one thread can actually be running inside the critical section defined by the lock and unlock() methods.

Implementation #3 below ensures that a reader will enter the cond_wait if there are any writers writing.
```C
read() {
    lock(&m)
    while (writing)
        cond_wait(&cv, &m)
    reading++;

/* Read here! */

    reading--
    cond_signal(&cv)
    unlock(&m)
}
```
However only one reader a time can read because candidate #3 did not unlock the mutex. A better version unlocks before reading :
```C
read() {
    lock(&m);
    while (writing)
        cond_wait(&cv, &m)
    reading++;
    unlock(&m)
/* Read here! */
    lock(&m)
    reading--
    cond_signal(&cv)
    unlock(&m)
}
```
Does this mean that a writer and read could read and write at the same time? No! First of all, remember cond_wait requires the thread re-acquire the  mutex lock before returning. Thus only one thread can be executing code inside the critical section (marked with **) at a time!
```C
read() {
    lock(&m);
**  while (writing)
**      cond_wait(&cv, &m)
**  reading++;
    unlock(&m)
/* Read here! */
    lock(&m)
**  reading--
**  cond_signal(&cv)
    unlock(&m)
}
```


Writers must wait for everyone. Mutual exclusion is assured by the lock. 
```C
write() {
    lock(&m);
**  while (reading || writing)
**      cond_wait(&cv, &m);
**  writing++;
**
** /* Write here! */
**  writing--;
**  cond_signal(&cv);
    unlock(&m);
}
```

Candidate #3 above also uses `pthread_cond_signal` ; this will only wake up one thread. For example, if many readers are waiting for the writer to complete then only one sleeping reader will be awoken from their slumber. The reader and writer should use `cond_broadcast` so that all threads should wake up and check their while-loop condition.


## Starving writers
Candidate #3 above suffers from starvation. If readers are constantly arriving then a writer will never be able to proceed (the 'reading' count never reduces to zero). This is known as *starvation* and would be discovered under heavy loads. Our fix is to implement a bounded-wait for the writer. If a writer arrives they will still need to wait for existing readers however future readers must be placed in a "holding pen" and wait for the writer to finish. The "holding pen" can be implemented using a variable and a condition variable (so that we can wake up the threads once the writer has finished).

Our plan is that when a writer arrives, and before waiting for current readers to finish, register our intent to write (by incrementing a counter 'writer'). Sketched below - 

```C
write() {
    lock()
    writer++

    while (reading | writing)
    cond_wait
    unlock()
  ...
}
```

And incoming readers will not be allowed to continue while writer is nonzero. Notice 'writer' indicates a writer has arrived, while 'reading' and 'writing' counters indicate there is an _active_ reader or writer.
```C
read() {
    lock()
    // readers that arrive *after* the writer arrived will have to wait here!
    while(writer)
    cond_wait(&cv,&m)

    // readers that arrive while there is an active writer
    // will also wait.
    while (writing) 
        cond_wait(&cv,&m)
    reading++
    unlock
  ...
}
```

## Candidate solution #4
Below is our first working solution to the Reader-Writer problem. 
Note if you continue to read about the "Reader Writer problem" then you will discover that we solved the "Second Reader Writer problem" by giving writers preferential access to the lock. This solution is not optimal. However it satisfies our original problem (N active readers, single active writer, avoids starvation of the writer if there is a constant stream of readers). 

Can you identify two improvements? Is any of the code superfluous? For example, how would you improve the code so that we only woke up readers or one writer? 
```C
reader() {
    mutex_lock(&m)
    while (writers)
        cond_wait(&turn, &m)
    while (writing)
        cond_wait(&turn, &m)
    reading++
    unlock(&m)

  // perform reading here

    lock(&m)
    reading--
    cond_broadcast(&turn)
    unlock(&m)
}

writer(){
    lock(&m)  
    writers++  
    while (reading || writing)   
        cond_wait(&turn, &m)  
    writing++  
    unlock(&m)  
    // perform writing here  
    lock(&m)  
    writing--  
    writers--  
    cond_broadcast(&turn)  
    unlock(&m)  
}
```