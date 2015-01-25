from bs4 import BeautifulSoup,SoupStrainer
import urllib2
import re
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

main()