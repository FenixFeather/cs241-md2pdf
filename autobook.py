#!/usr/bin/env python

from bs4 import BeautifulSoup,SoupStrainer
import urllib2
import re
import os, sys
import glob
import platform
import argparse


class Chapter(object):
	"""docstring for Chapter"""
	def __init__(self, chapter_name, book):
		super(Chapter, self).__init__()
		self.chapter_name = chapter_name
		self.sub_chapters = []
		book.append(self)
	def add_subchapters(self, *args):
		for arg in args:
			self.sub_chapters.append(arg)

class SubChapter(Chapter):
	def __init__(self, sub_chapter_name, md_name, windows=None):
		self.sub_chapter_name = sub_chapter_name
		self._md_name = md_name
		self.windows = windows if windows is not None else platform.system() == "Windows"
		
	@property
	def md_name(self):
		if self.windows:
			return self._md_name.replace(":", "")
		else:
			return self._md_name
			
def clone_wiki(url, destination_path):
	clone_command = "git clone {0} {1}".format(url, destination_path)
	os.system(clone_command)
	files = glob.glob('SystemProgramming.wiki/*.md')
	print files
	for file in files:
		print file,file.replace("-"," ").replace("/", " ")
		new_filename = file.replace("-", " ").replace("/", " ")
		os.rename(file, new_filename)
		
def add_includes(book, base_tex_path):
	"""Add the includes to the base tex file based on the tex files in base.tex."""
	base_tex = open(base_tex_path, 'r')
	base_tex_text = base_tex.read()
	base_tex.close()
	return base_tex_text.replace("%includes_here", "\n".join(sum([["\\include{{{{\"{0}\"}}}}".format(subchapter.md_name)
														 for subchapter in chapter.sub_chapters]
														 for chapter in book], [])))
def process_book(book, src_dir, out_dir):

	for chapter in book:
		is_first_section = True
		print chapter.chapter_name
		for sub_chapter in chapter.sub_chapters:
			md_path = src_dir + sub_chapter.md_name + ".md"
			tex_path = out_dir + sub_chapter.md_name + ".tex"
			if not os.path.isfile(md_path):
				print("[IO Error] Skipping %s\n" % (md_path))
				continue

			pandoc_command = "pandoc --listings -f markdown_github -t latex -V links-as-notes \"%s\" -o  \"%s\"" % (md_path, tex_path) 
			os.system(pandoc_command)
			
			# Replace subsection -> subsubsection, then section -> subsection
			tex_file = open(tex_path, "r+")
			tex_content = tex_file.read()
			tex_content.replace("\subsection", "\subsubsection")
			tex_content.replace("\section", "\subsection")
			tex_file.seek(0) # assumes replaced content is longer so that write() will replace entire file

			output = ""
			if is_first_section: # insert chapter name before the 1st section
				output += "\chapter{%s}\n" % chapter.chapter_name
				is_first_section = False

			output += "\section{{{0}}}\n".format(sub_chapter.sub_chapter_name)
			output += tex_content

			tex_file.write(output)
			tex_file.close()


def compile_latex(tex_path):
	print "Compiling"
	for ii in xrange(0,2):
		os.system("pdflatex -output-directory {0} -interaction nonstopmode {1}".format(os.path.dirname(tex_path), tex_path))

def generate_base_tex(book, base_template_path, destination_path):
	print "Adding includes"
	base_modified = open(destination_path, 'w')

	print add_includes(book, base_template_path)

	base_modified.write(add_includes(book, base_template_path))

	base_modified.close()

def scrape_book_structure(book_url):
	"""Scrape and return the structure of the book from Angrave's Wiki."""
	response = urllib2.urlopen(book_url)
	html = response.read()
	soup = BeautifulSoup(html)
	table_of_contents = soup.find(id="wiki-body")
	links = table_of_contents.find_all('a',class_="internal present")
	
	book = []
	found = []
	regex = re.compile("[\w\s]+,[\w\s]+:[\w\s]+")
	for link in links:
		text = link.get_text()
		if regex.match(text):
			# text = text.replace(" ", "")
			raw_split = text.split(": ")
			sub_chapter_name = raw_split[1]
			chapter_part = raw_split[0].split(", ")
			chapter_name = chapter_part[0]
			part = chapter_part[1].split("Part ")[1]
			if chapter_name not in found:
				Chapter(chapter_name, book)
				found.append(chapter_name)
			for chapter in book:
				if chapter.chapter_name == chapter_name:
					chapter.add_subchapters(SubChapter(sub_chapter_name, text))
					break
	for chapter in book:
		print chapter.chapter_name
		for sub_chapter in chapter.sub_chapters:
			print "\t{0}".format(sub_chapter.sub_chapter_name)

	return book

def reorder_book(book):
	return book

def parse_arguments():
	parser = argparse.ArgumentParser()

	parser.add_argument("md_source",
						help="directory where github wiki md files is located")
	parser.add_argument("tex_source",
						help="directory where tex and pdf final should be output")
	parser.add_argument("-c", "--clone",
						help="use this option if you want to clone the mds to md_source",
						action="store_true")
	parser.add_argument("-r", "--reorder",
						help="use this option if you want to reorder the chapters in the book",
						action="store_true")

	return parser.parse_args()
	
	
def main():
	args = parse_arguments()
	
	book = scrape_book_structure("https://github.com/angrave/SystemProgramming/wiki")
	
	if args.reorder:
		book = reorder_book(book)

	if args.clone:
		clone_wiki("https://github.com/angrave/SystemProgramming.wiki.git", args.md_source)

	print "Processing book"
	process_book(book, "{0}/".format(args.md_source), "{0}/".format(args.tex_source))

	generate_base_tex(book, "base.tex", "{0}/base.tex".format(args.tex_source))
	
	compile_latex("{0}/base.tex".format(args.tex_source))
	
if __name__ == '__main__':
	main()

