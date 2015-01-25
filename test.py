#/usr/bin/env python

import platform
from autobook import *
import os, sys

def main():

	book = []

	chapter1 = Chapter("C Programming", book)
	chapter1.add_subchapters(
		# SubChapter("Introduction", "C Programming,-Part-1--Introduction"),
		SubChapter("Text Input And Output", "C Programming, Part 2: Text Input And Output"),
		SubChapter("Common Gotchas", "C Programming, Part 3: Common Gotchas"),
		SubChapter("Debugging", "C Programming, Part 4: Debugging")
	)

	chapter2 = Chapter("Forking", book)
	chapter2.add_subchapters(
		SubChapter("Introduction", "Forking, Part 1: Introduction"),
		SubChapter("Fork, Exec, Wait Kill", "Forking, Part 2: Fork, Exec, Wait Kill")
	)

	chapter3 = Chapter("Memory", book)
	chapter3.add_subchapters(
		SubChapter("Heap Memory Introduction", "Memory, Part 1: Heap Memory Introduction"),
		SubChapter("Implementing a Memory Allocator", "Memory, Part 2: Implementing a Memory Allocator"),
		SubChapter("Smashing the Stack Example", "Memory, Part 3: Smashing the Stack Example")
	)

	chapter4 = Chapter("Pthreads", book)
	chapter3.add_subchapters(
		SubChapter("Introduction", "Pthreads, Part 1: Introduction"),
		SubChapter("Usage in Practice", "Pthreads, Part 2: Usage in Practice")
	)

	chapter5 = Chapter("Synchronization", book)
	chapter5.add_subchapters(
		SubChapter("Mutex Locks", "Synchronization, Part 1: Mutex Locks"),
		SubChapter("Counting Semaphores", "Synchronization, Part 2: Counting Semaphores"),
		SubChapter("Working with Mutexes And Semaphores", "Synchronization, Part 3: Working with Mutexes And Semaphores"),
		SubChapter("The Critical Section Problem", "Synchronization, Part 4: The Critical Section Problem"),
		SubChapter("Condition Variables", "Synchronization, Part 5: Condition Variables"),
		# SubChapter("Implementing a barrier", "Synchronization, Part 6: Implementing a barrier"),
		SubChapter("The Reader Writer Problem", "Synchronization, Part 7: The Reader Writer Problem"),
		SubChapter("Ring Buffer Example", "Synchronization, Part 8: Ring Buffer Example"),
		# SubChapter("The Reader Writer Problem (part 2)", "Synchronization, Part 9: The Reader Writer Problem (part 2)")
	)
	
	chapter6 = Chapter("Deadlock", book)
	chapter6.add_subchapters(
		SubChapter("Resource Allocation Graph", "Deadlock, Part 1: Resource Allocation Graph"),
		SubChapter("Deadlock Conditions", "Deadlock, Part 2: Deadlock Conditions")
	)

	# chapter7 = Chapter("Virtual Memory", book)
	# chapter7.add_subchapters(
	# 	# SubChapter("Introduction to Virtual Memory", "Virtual Memory, Part 1: Introduction to Virtual Memory")
	# )

	# chapter8 = Chapter("Pipes", book)
	# chapter8.add_subchapters(
	# 	# SubChapter("Introduction to pipes", "Pipes, Part 1: Introduction to pipes"),
	# 	SubChapter("Pipe programming secrets", "Pipes, Part 2: Pipe programming secrets")
	# )

	# chapter9 = Chapter("Files", book)
	# chapter9.add_subchapters(
	# 	SubChapter("Working with files", "Files, Part 1: Working with files")
	# )

	# chapter10 = Chapter("POSIX", book)
	# chapter10.add_subchapters(
	# 	SubChapter("Error handling", "POSIX Error handling")
	# )

	# chapter11 = Chapter("Networking", book)
	# chapter11.add_subchapters(
	# 	SubChapter("Introduction", "Networking, Part 1: Introduction"),
	# 	SubChapter("Using getaddrinfo", "Networking, Part 2: Using getaddrinfo"),
	# 	subchapter("Building a simple TCP Client", "Networking, Part 3: Building a simple TCP Client"),
	# 	SubChapter("Building a simple TCP Server", "Networking, Part 4: Building a simple TCP Server"),
	# 	SubChapter("Reusing ports", "Networking, Part 5: Reusing ports"),
	# 	SubChapter("Creating a UDP server", "Networking, Part 6: Creating a UDP server")
	# )

	# chapter12 = Chapter("File System", book)
	# chapter12.add_subchapters(
	# 	SubChapter("Introduction", "File System, Part 1: Introduction"),
	# 	SubChapter("Files are inodes (everything else is just data...)", "File System, Part 2: Files are inodes (everything else is just data...)"),
	# 	SubChapter("Permissions", "File System, Part 3: Permissions"),
	# 	SubChapter("Working with directories", "File System, Part 4: Working with directories"),
	# 	SubChapter("Virtual file systems", "File System, Part 5: Virtual file systems"),
	# 	SubChapter("Memory mapped files and Shared memory", "File System, Part 6: Memory mapped files and Shared memory"),
	# 	SubChapter("Scalable and Reliable Filesystems", "File System, Part 7: Scalable and Reliable Filesystems"),
	# 	SubChapter("Disk blocks example", "File System, Part 8: Disk blocks example")
	# )

	for chapter in book:
		print chapter.chapter_name
		for sub_chapter in chapter.sub_chapters:
			print "\t{0}".format(sub_chapter.sub_chapter_name)

	print "Processing book"
	process_book(book, "./md_source/", "./tex_source/")

	generate_base_tex(book, "base.tex", "./tex_source/base.tex")
	
	compile_latex("./tex_source/base.tex")

	# print "Adding includes"
	# base_modified = open("./tex_source/base.tex", 'w')

	# base_modified.write(add_includes(book, "base.tex"))

	# base_modified.close()

	# print "Compiling"
	# os.system("pdflatex -output-directory ./tex_source/ -interaction nonstopmode ./tex_source/base.tex")
	# os.system("pdflatex -output-directory ./tex_source/ -interaction nonstopmode ./tex_source/base.tex")
	
if __name__ == '__main__':
	
	main()
