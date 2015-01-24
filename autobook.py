from bs4 import BeautifulSoup
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