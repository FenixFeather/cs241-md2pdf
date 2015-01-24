from bs4 import BeautifulSoup,SoupStrainer
import urllib2
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
	
	print(table_of_contents.prettify())

main()