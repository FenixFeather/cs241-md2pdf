#/usr/bin/env python

import platform
import autobook
import os, sys
import unittest

if sys.version_info < (2, 7):
    print "EWS sucks."

class TestRegexFunctions(unittest.TestCase):
    def setUp(self):
        self.latex_text = """\chapter{Deadlock}
\section{Resource Allocation Graph}
\subsection{What is a Resource Allocation
Graph?}\label{what-is-a-resource-allocation-graph}

A resource allocation graph tracks which resource is held by which
process and which process is waiting for a resource of a particular
type. It is very powerful and simple tool to illustrate how interacting
processes can deadlock.

If there is a cycle in the Resource Allocation Graph then the processes
will deadlock. For example, if process 1 holds resource A, process 2
holds resource B and process 1 is waiting for B and process 2 is waiting
for A, then process 1 and 2 process will be deadlocked.

Here's another example, that shows Processes 1 and 2 acquiring resources
1 and 2 while process 3 is waiting to acquire both resources. In this
example there is no deadlock because there is no circular dependency.

\includegraphics{https://raw.githubusercontent.com/wiki/angrave/SystemProgramming/ResourceAllocationGraph-Ex1.png}

Todo: More complicated example"""
        self.tex_path = "test_tex_path"

    def test_find_simple_url(self):
        # make sure the shuffled sequence does not lose any elements
        result = autobook.include_images(self.latex_text, self.tex_path)
        self.assertEqual(unicode(result), unicode("""\chapter{{Deadlock}}
\section{{Resource Allocation Graph}}
\subsection{{What is a Resource Allocation
Graph?}}\label{{what-is-a-resource-allocation-graph}}

A resource allocation graph tracks which resource is held by which
process and which process is waiting for a resource of a particular
type. It is very powerful and simple tool to illustrate how interacting
processes can deadlock.

If there is a cycle in the Resource Allocation Graph then the processes
will deadlock. For example, if process 1 holds resource A, process 2
holds resource B and process 1 is waiting for B and process 2 is waiting
for A, then process 1 and 2 process will be deadlocked.

Here's another example, that shows Processes 1 and 2 acquiring resources
1 and 2 while process 3 is waiting to acquire both resources. In this
example there is no deadlock because there is no circular dependency.

\\includegraphics[width=\linewidth]{{{0}/images/ResourceAllocationGraph-Ex1.png}}

Todo: More complicated example""".format(self.tex_path)))

    # def test_choice(self):
    #     element = random.choice(self.seq)
    #     self.assertTrue(element in self.seq)

    # def test_sample(self):
    #     with self.assertRaises(ValueError):
    #         random.sample(self.seq, 20)
    #     for element in random.sample(self.seq, 5):
    #         self.assertTrue(element in self.seq)

class TestChapterFunctions(unittest.TestCase):
    def setUp(self):
        self.latex_subchapters = [autobook.SubChapter(name, "") for name in
                                  ["Want a quick introduction to C?",
                                   "Crash course intro to C",
                                  """How do you write a complete hello world program in
C?"""]]

    def test_subchapter_label(self):
        self.assertEqual([subchapter.latex_label() for subchapter in self.latex_subchapters],
                         ["want-a-quick-introduction-to-c",
                          "crash-course-intro-to-c",
                          "how-do-you-write-a-complete-hello-world-program-in-c"])

class TestInternalLinkFunctions(unittest.TestCase):
    def setUp(self):
        """Set up two styles of internal link, raw link and link with description."""
        self.decorated_internal_link = """\item
  Then see the {[}{[}C Gotchas wiki page\\textbar{}C Programming, Part 3:
  Common Gotchas{]}{]}."""

        self.raw_internal_link = """As already discussed in {[}{[}Synchronization, Part 3: Working with
Mutexes And Semaphores{]}{]}, there are critical parts of our code that
can only be executed by one thread at a time. We describe this
requirement as `mutual exclusion'; only one thread (or process) may have
access to the shared resource."""

    def test_raw_internal_link(self):
        self.assertEqual(unicode(autobook.convert_internal_links(self.raw_internal_link)), unicode("""As already discussed in \Fref{{sec:{0}}}, there are critical parts of our code that
can only be executed by one thread at a time. We describe this
requirement as `mutual exclusion'; only one thread (or process) may have
access to the shared resource.""".format(autobook.SubChapter("Working with Mutexes And Semaphores", "").latex_label())))

    def test_decorated_internal_link(self):
        self.assertEqual(unicode(autobook.convert_internal_links(self.decorated_internal_link)), unicode("""\item
  Then see the C Gotchas wiki page on page \pageref{{sec:{0}}}.""".format(autobook.SubChapter("Common Gotchas", "").latex_label())))


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestRegexFunctions)
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestChapterFunctions)
    # unittest.TextTestRunner(verbosity=2).run(suite)

# def main():

#     book = []

#     chapter1 = Chapter("C Programming", book)
#     chapter1.add_subchapters(
#         # SubChapter("Introduction", "C Programming,-Part-1--Introduction"),
#         SubChapter("Text Input And Output", "C Programming, Part 2: Text Input And Output"),
#         SubChapter("Common Gotchas", "C Programming, Part 3: Common Gotchas"),
#         SubChapter("Debugging", "C Programming, Part 4: Debugging")
#     )

#     chapter2 = Chapter("Forking", book)
#     chapter2.add_subchapters(
#         SubChapter("Introduction", "Forking, Part 1: Introduction"),
#         SubChapter("Fork, Exec, Wait Kill", "Forking, Part 2: Fork, Exec, Wait Kill")
#     )

#     chapter3 = Chapter("Memory", book)
#     chapter3.add_subchapters(
#         SubChapter("Heap Memory Introduction", "Memory, Part 1: Heap Memory Introduction"),
#         SubChapter("Implementing a Memory Allocator", "Memory, Part 2: Implementing a Memory Allocator"),
#         SubChapter("Smashing the Stack Example", "Memory, Part 3: Smashing the Stack Example")
#     )

#     chapter4 = Chapter("Pthreads", book)
#     chapter3.add_subchapters(
#         SubChapter("Introduction", "Pthreads, Part 1: Introduction"),
#         SubChapter("Usage in Practice", "Pthreads, Part 2: Usage in Practice")
#     )

#     chapter5 = Chapter("Synchronization", book)
#     chapter5.add_subchapters(
#         SubChapter("Mutex Locks", "Synchronization, Part 1: Mutex Locks"),
#         SubChapter("Counting Semaphores", "Synchronization, Part 2: Counting Semaphores"),
#         SubChapter("Working with Mutexes And Semaphores", "Synchronization, Part 3: Working with Mutexes And Semaphores"),
#         SubChapter("The Critical Section Problem", "Synchronization, Part 4: The Critical Section Problem"),
#         SubChapter("Condition Variables", "Synchronization, Part 5: Condition Variables"),
#         # SubChapter("Implementing a barrier", "Synchronization, Part 6: Implementing a barrier"),
#         SubChapter("The Reader Writer Problem", "Synchronization, Part 7: The Reader Writer Problem"),
#         SubChapter("Ring Buffer Example", "Synchronization, Part 8: Ring Buffer Example"),
#         # SubChapter("The Reader Writer Problem (part 2)", "Synchronization, Part 9: The Reader Writer Problem (part 2)")
#     )
    
#     chapter6 = Chapter("Deadlock", book)
#     chapter6.add_subchapters(
#         SubChapter("Resource Allocation Graph", "Deadlock, Part 1: Resource Allocation Graph"),
#         SubChapter("Deadlock Conditions", "Deadlock, Part 2: Deadlock Conditions")
#     )

#     # chapter7 = Chapter("Virtual Memory", book)
#     # chapter7.add_subchapters(
#     #     # SubChapter("Introduction to Virtual Memory", "Virtual Memory, Part 1: Introduction to Virtual Memory")
#     # )

#     # chapter8 = Chapter("Pipes", book)
#     # chapter8.add_subchapters(
#     #     # SubChapter("Introduction to pipes", "Pipes, Part 1: Introduction to pipes"),
#     #     SubChapter("Pipe programming secrets", "Pipes, Part 2: Pipe programming secrets")
#     # )

#     # chapter9 = Chapter("Files", book)
#     # chapter9.add_subchapters(
#     #     SubChapter("Working with files", "Files, Part 1: Working with files")
#     # )

#     # chapter10 = Chapter("POSIX", book)
#     # chapter10.add_subchapters(
#     #     SubChapter("Error handling", "POSIX Error handling")
#     # )

#     # chapter11 = Chapter("Networking", book)
#     # chapter11.add_subchapters(
#     #     SubChapter("Introduction", "Networking, Part 1: Introduction"),
#     #     SubChapter("Using getaddrinfo", "Networking, Part 2: Using getaddrinfo"),
#     #     subchapter("Building a simple TCP Client", "Networking, Part 3: Building a simple TCP Client"),
#     #     SubChapter("Building a simple TCP Server", "Networking, Part 4: Building a simple TCP Server"),
#     #     SubChapter("Reusing ports", "Networking, Part 5: Reusing ports"),
#     #     SubChapter("Creating a UDP server", "Networking, Part 6: Creating a UDP server")
#     # )

#     # chapter12 = Chapter("File System", book)
#     # chapter12.add_subchapters(
#     #     SubChapter("Introduction", "File System, Part 1: Introduction"),
#     #     SubChapter("Files are inodes (everything else is just data...)", "File System, Part 2: Files are inodes (everything else is just data...)"),
#     #     SubChapter("Permissions", "File System, Part 3: Permissions"),
#     #     SubChapter("Working with directories", "File System, Part 4: Working with directories"),
#     #     SubChapter("Virtual file systems", "File System, Part 5: Virtual file systems"),
#     #     SubChapter("Memory mapped files and Shared memory", "File System, Part 6: Memory mapped files and Shared memory"),
#     #     SubChapter("Scalable and Reliable Filesystems", "File System, Part 7: Scalable and Reliable Filesystems"),
#     #     SubChapter("Disk blocks example", "File System, Part 8: Disk blocks example")
#     # )

#     for chapter in book:
#         print chapter.chapter_name
#         for sub_chapter in chapter.sub_chapters:
#             print "\t{0}".format(sub_chapter.sub_chapter_name)

#     print "Processing book"
#     process_book(book, "./md_testing/", "./tex_source/")

#     generate_base_tex(book, "base.tex", "./tex_source/base.tex")
    
#     compile_latex("./tex_source/base.tex")

#     # print "Adding includes"
#     # base_modified = open("./tex_source/base.tex", 'w')

#     # base_modified.write(add_includes(book, "base.tex"))

#     # base_modified.close()

#     # print "Compiling"
#     # os.system("pdflatex -output-directory ./tex_source/ -interaction nonstopmode ./tex_source/base.tex")
#     # os.system("pdflatex -output-directory ./tex_source/ -interaction nonstopmode ./tex_source/base.tex")
    
# if __name__ == '__main__':
    
#     main()
