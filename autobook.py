from bs4 import BeautifulSoup,SoupStrainer
import urllib2
import re
import os, sys


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
	def __init__(self, sub_chapter_name, md_name):
		self.sub_chapter_name = sub_chapter_name
		self.md_name = md_name


def process_book(book, src_dir, out_dir):
	for chapter in book:
		is_first_section = True
		print chapter.chapter_name
		for sub_chapter in chapter.sub_chapters:
			md_path = src_dir + sub_chapter.md_name + ".md"
			tex_path = out_dir + sub_chapter.md_name + ".tex"
			pandoc_command = "pandoc -f markdown_github -t latex -V links-as-notes -o \"%s\" \"%s\"" % (tex_path, md_path) 
			os.system(pandoc_command)
			
			# Replace subsection -> subsubsection, then section -> subsection
			tex_file = open(tex_path, "r+")
			tex_content = file_tex.read()
			tex_content.replace("\subsection", "\subsubsection")
			tex_content.replace("\section", "\subsection")
		    tex_file.seek(0) # assumes replaced content is longer so that write() will replace entire file

		    output = ""
		    if is_first_section: # insert chapter name before the 1st section
		    	output += "\chapter{%s}" % chapter.chapter_name
		    	is_first_section = False
		   	else:
		   		output += replace_chap_with_subchap(tex_content)

			tex_file.write(output)
			tex_file.close()


def main():
	response = urllib2.urlopen("https://github.com/angrave/SystemProgramming/wiki")
	html = response.read()
	soup = BeautifulSoup(html)
	table_of_contents = soup.find(id="wiki-body")
	links = table_of_contents.find_all('a',class_="internal present")
	# for link in links:
	# 	print link

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

	process_book(book, "./", "./tex_out/")

main()