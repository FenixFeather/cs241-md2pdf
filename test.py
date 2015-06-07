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

class TestIndexFunctions(unittest.TestCase):
    def setUp(self):
        """Set up an index file and some book test"""
        with open("temp.txt", 'w') as index_file:
            index_file.write("mutex\nsemaphore\nthread\nsynchronization")
        self.book_text = """As already discussed in Synchronization, Part 3: Working with
Mutexes And Semaphores, there are critical parts of our code that
can only be executed by one thread at a time. We describe this
requirement as `mutual exclusion'; only one thread (or process) may have
access to the shared resource."""

    def test_basic_indexing(self):
        self.assertEqual(unicode(autobook.generate_index("temp.txt", "I like thread.")), unicode("I like \\index{thread}."))

    def case_insensitive_indexing(self):
        self.assertEqual(unicode(autobook.generate_index("temp.txt", "Thread is cool.")), unicode("\\index{Thread} is cool."))

    def tearDown(self):
        os.remove("temp.txt")

if __name__ == '__main__':
    unittest.main(verbosity=2)
