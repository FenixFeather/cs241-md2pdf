## What is a pipe?

A POSIX pipe is almost like its real counterpart - you can stuff bytes down one end and they will appear at the other end in the same order. Unlike real pipes however, the flow is always in the same direction, one file descriptor is used for reading and the other for writing. The `pipe` system call is used to create a pipe.
```C
int filedes[2];
pipe (filedes);
printf("read from %d, write to %d\n", filedes[0], filedes[1]);
```

These file descriptors can be used with `read` -
```C
// To read...
char buffer[80];
int bytesread = read(filedes[0], buffer, sizeof(buffer));
```
And `write` - 
```C
write(filedes[1], "Go!", 4);
```

## How can I use pipe to communicate with a child process?
A common method of using pipes is to create the pipe before forking.
```C
int filedes[2];
pipe (filedes);
pid_t child = fork();
if (child > 0) { /* I must be the parent */
    char buffer[80];
    int bytesread = read(filedes[0], buffer, sizeof(buffer));
    // do something with the bytes read    
}
```

The child can then send a message back to the parent:
```C
if (child == 0) {
   write(filedes[1], "done", 4);
}
```
## Can I use pipes inside a single process?
Short answer: Yes, but I'm not sure why you would want to LOL!

Here's an example program that sends a message to itself:
```C
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int main() {
    int fh[2];
    pipe(fh);
    FILE *reader = fdopen(fh[0], "r");
    FILE *writer = fdopen(fh[1], "w");
    // Hurrah now I can use printf rather than using low-level read() write()
    printf("Writing...\n");
    fprintf(writer,"%d %d %d\n", 10, 20, 30);
    fflush(writer);
    
    printf("Reading...\n");
    int results[3];
    int ok = fscanf(reader,"%d %d %d", results, results + 1, results + 2);
    printf("%d values parsed: %d %d %d\n", ok, results[0], results[1], results[2]);
    
    return 0;
}
```

The problem with using a pipe in this fashion is that writing to a pipe can block i.e. the pipe only has a limited buffering capacity. If the pipe is full the writing process will block! The maximum size of the buffer is system dependent; typical values from  4KB upto 128KB.

```C
int main() {
    int fh[2];
    pipe(fh);
    int b = 0;
    #define MESG "..............................."
    while(1) {
        printf("%d\n",b);
        write(fh[1], MESG, sizeof(MESG))
        b+=sizeof(MESG);
    }
    return 0;
}
```

See [[Pipes, Part 2: Pipe programming secrets]]
