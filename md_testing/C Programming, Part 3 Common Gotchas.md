What common mistakes do C programmers make?

# Memory mistakes
## String constants are constant
```C
char array[] = "Hi!"; // array contains a mutable copy
strcpy(array, "OK");

char *ptr = "Can't change me"; // ptr points to some immutable memory
strcpy(ptr, "Will not work");
```

## Buffer overflow/ underflow
```C
#define N (10)
int i = N, array[N];
for( ; i >= 0; i--) array[i] = i;
```
C does not check that pointers are valid. The above example writes into `array[10]` which is outside the array bounds. This can cause memory corruption because that memory location is probably being used for something else.
In practice, this can be harder to spot because the overflow/underflow may occur in a library call e.g.
```C
gets(array); // Let's hope the input is shorter than my array!
```


## Returning pointers to automatic variables
```C
int *f() {
    int result = 42;
    static int imok;
    return &imok; // OK - static variables are not on the stack
    return &result; // Not OK
}
```
Automatic variables are bound to stack memory only for the lifetime of the function.
After the function returns it is an error to continue to use the memory.
## Insufficient memory allocation 
```C
struct User {
   char name[100];
};
typedef struct User user_t;

user_t *user = (user_t *) malloc(sizeof(user));
```
In the above example, we needed to allocate enough bytes for the struct. Instead we allocated enough bytes to hold a pointer. Once we start using the user pointer we will corrupt memory. Correct code is show bellow.
```C
struct User {
   char name[100];
};
typedef struct User user_t;

user_t * user = (user_t *) malloc(sizeof(user_t));
```
## Using uninitialized variables
```C
int myfunction() {
  int x;
  int y = x + 2;
...
```
Automatic variables hold garbage (whatever bit pattern happened to be in memory). It is an error to assume that it will always be initialized to zero.

## Assuming Uninitialized memory will be zeroed
```C
void myfunct() {
   char array[10];
   char *p = malloc(10);
```
Automatic (temporary variables) are not automatically initialized to zero.
Heap allocations using malloc are not automatically initialized to zero.

## Double-free
```C
  char *p = malloc(10);
  free(p);
//  .. later ...
  free(p); 
```
It is an error to free the same block of memory twice.
## Dangling pointers
```C
  char *p = malloc(10);
  strcpy(p, "Hello");
  free(p);
//  .. later ...
  strcpy(p,"World"); 
```
Pointers to freed memory should not be used. A defensive programming practice is to set pointers to null as soon as the memory is freed.

It is a good idea to turn free into the following snippet that automatically sets the freed variable to null right after:(vim - ultisnips)  
```Vim
snippet free "free(something)" b
free(${1});
$1 = NULL;
${2}
endsnippet
```


# Logic and Program flow mistakes
## Forgetting break
```C
int flag = 1; // Will print all three lines.
switch(flag) {
  case 1: printf("I'm printed\n");
  case 2: printf("Me too\n");
  case 3: printf("Me three\n");
}
```
Case statements without a break will just continue onto the code of the next case statement. Correct code is show bellow. The break for the last statements is unnecessary because there are no more cases to be executed after the last one. However if more are added, it can cause some bugs.
```C
int flag = 1; // Will print all three lines.
switch(flag) {
  case 1: 
    printf("I'm printed\n");
    break;
  case 2: 
    printf("Me too\n");
    break;
  case 3: 
    printf("Me three\n");
    break; //unnecessary
}
```
## Equal vs equality
```C
int answer = 3; // Will print out the answer.
if (answer = 42) { printf("I've solved the answer! It's %d", answer);}
```

## Undeclared or incorrectly prototyped functions
```C
time_t start = time();
```
The system function 'time' actually takes a parameter (the pointer to some memory that can receive the time_t structure. The compiler did not catch this error because the programmer did not provide a valid function prototype by including `time.h`

## Extra Semicolons
```C
for(int i = 0; i < 5; i++) ; printf("I'm printed once");
while(x < 10); x++ ; // X is never incremented
```
However, the following code is perfectly OK.
```C
for(int i = 0; i < 5; i++){
    printf("%d\n", i);;;;;;;;;;;;;
}
```
It is OK to have this kind of code, because the C language uses semicolons (;) to separate statements. If there is no statement in between semicolons, then there is nothing to do and the compiler moves on to the next statement
# Other Gotchas
## C Preprocessor macros and side-effects
```C
#define min(a,b) ((a)<(b) ? (a) : (b))
int x = 4;
if(min(x++, 100)) printf("%d is six", x);
```
Macros are simple text substitution so the above example expands to `x++ < 100 ? x++ : 100` (parenthesis omitted for clarity)

## C Preprocessor macros and precedence
```C
#define min(a,b) a<b ? a : b
int x = 99;
int r = 10 + min(99, 100); // r is 100!
```
Macros are simple text substitution so the above example expands to `10 + 99 < 100 ? 99 : 100`