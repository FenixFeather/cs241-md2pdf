We've already seen [open](http://angrave.github.io/sysassets/web/chapter1.html) and fopen (todo link here) so let's look at some more advanced concepts.

#How do I tell how large a file is?
For files less than the size of a long use fseek and ftell is a simple way to accomplish this:

Move to the end of the file and find out the current position.
```C
fseek(f, 0, SEEK_END);
long pos = ftell(f);
```
This tells us the current position in the file in bytes - i.e. the length of the file!

`fseek` can also be used to set the absolute position.
```C
fseek(f, 0, SEEK_SET); // Move to the start of the file 
fseek(f, posn, SEEK_SET);  // Move to 'posn' in the file.
```
All future reads and writes in the parent or child processes will be honor this position.
Note writing or reading from the file will change the current position.

See the man pages for fseek and ftell for more information.

## What happens if a child process closes a filestream using `fclose` or `close`?
Unlike position, closing a file stream is unique to each process. Other processes can continue to use their own file-handle.


