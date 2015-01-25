#!/usr/bin/env python

from bs4 import BeautifulSoup,SoupStrainer
import urllib2
import re
import os, sys
import glob
import platform


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
def clone_wiki(url):
	clone_command = "git clone "+url
	os.system(clone_command)
	files = glob.glob('SystemProgramming.wiki/*.md')
	print files
	for file in files:
		print file,file.replace("-"," ") 
		os.rename(file, file.replace("-"," "))
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

			pandoc_command = "pandoc -f markdown_github -t latex -V links-as-notes \"%s\" -o  \"%s\"" % (md_path, tex_path) 
			os.system(pandoc_command)
			
			# Replace subsection -> subsubsection, then section -> subsection
			tex_file = open(tex_path, "r+")
			tex_content = tex_file.read()
			tex_content.replace("\subsection", "\subsubsection")
			tex_content.replace("\section", "\subsection")
			tex_file.seek(0) # assumes replaced content is longer so that write() will replace entire file

			output = ""
			if is_first_section: # insert chapter name before the 1st section
				output += "\chapter{%s}" % chapter.chapter_name
				is_first_section = False
			else:
				output += tex_content

			tex_file.write(output)
			tex_file.close()


def main():
	response = urllib2.urlopen("https://github.com/angrave/SystemProgramming/wiki")
	html = response.read()
	soup = BeautifulSoup(html)
	table_of_contents = soup.find(id="wiki-body")
	links = table_of_contents.find_all('a',class_="internal present")
	clone_wiki("https://github.com/angrave/SystemProgramming.wiki.git")
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

	print "Processing book"
	process_book(book, "SystemProgramming.wiki/", "tex_source/")
    
	print "Adding includes"
	base_modified = open("./tex_source/base.tex", 'w')

	print add_includes(book, "base.tex")

	base_modified.write(add_includes(book, "base.tex"))

	base_modified.close()

	# print "Compiling"
	# os.system("pdflatex ./tex_source/base.tex")
if __name__ == '__main__':
    main()

