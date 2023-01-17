import time
import math
import requests
from bs4 import BeautifulSoup

class Journal():

	def __init__(self, arg_name):
		self.name = arg_name
		self.url = ''
		self.separator = ''
		self.publisher = ''
		self.year = 0
		self.issues = []
		self.papers = []
		self.auths = []

	def init_url(self, arg_url, arg_separator):
		self.url = arg_url
		self.separator = arg_separator

	def init_publisher(self, arg_publisher, arg_start_year):
		self.publisher = arg_publisher
		self.year = arg_start_year

	def init_issues(self, arg_first_volume, arg_last_volume, arg_issues_per_volume):
		for volume in range(int(arg_last_volume), int(arg_first_volume) + 1):
			if arg_issues_per_volume > 1:
				for issue in range(1, arg_issues_per_volume + 1):
					if self.publisher == 'John Wiley & Sons':
						issue_url = self.url + "/" + str(self.year) + "/" + str(volume) + self.separator + str(issue)
						if issue == 6:
							self.year += 1

					elif self.publisher == 'De Gruyter':
						issue_url = self.url + "/" + str(volume) + self.separator + str(issue) + "/html"

					else:
						issue_url = self.url + "/" + str(volume) + self.separator + str(issue)

					self.issues.append(issue_url)

			else:
				issue_url = self.url + "/" + str(volume)
				self.issues.append(issue_url)

	def progress_bar(self, counter):
		length = 50
		no_issues = len(self.issues)

		print("\r", end="")
		print("  Issues " + str((counter)) + "/" + str(no_issues+1) + "   [" + (math.ceil((counter*length)/(no_issues+1)))*"#" + (length - math.ceil((counter*length)/(no_issues+1)))*"_" + "]", end="")

	def print_info(self):
		print(self.name + "  (" + self.publisher + ")")
		print("    Scraped issues: " + str(len(self.issues)))
		print("    Scraped papers: " + str(len(self.papers)))


class Elsevier(Journal):

	def __init__(self, arg_name, arg_url):
		self.name = arg_name
		self.url = 'sciencedirect.com/journal/' + arg_url +'/vol'
		self.publisher = 'Elsevier'
		self.issues = []
		self.papers = []
		self.auths = []

	def init_issues(self, arg_first_volume, arg_last_volume, arg_issues_per_volume):
		for volume in range(int(arg_last_volume), int(arg_first_volume) + 1):
			issue_url = self.url + "/" + str(volume) + "/suppl/C"
			self.issues.append(issue_url)

	def scrape(self):
		counter = 0 
		print("\nScraping '" + self.name + "' (" + self.publisher + ")")
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
		for issue in self.issues:
			counter+=1
			self.progress_bar(counter)
			webpage = requests.get("http://" + issue, headers=headers)
			soup = BeautifulSoup(webpage.content, 'html.parser')
			
			papers_list = [a.text for a in soup.find_all('span', class_='js-article-title')]
			for paper in papers_list:
				self.papers.append(paper)

			auths_list = [a.text for a in soup.find_all('div', class_='text-s u-clr-grey8 js-article__item__authors')]
			for auth in auths_list:
				self.auths.append(auth)

			time.sleep(1.0)

		self.progress_bar(len(self.issues)+1)

		


class Springer(Journal):

	def __init__(self, arg_name, arg_url):
		self.name = arg_name
		self.url = 'link.springer.com/journal/' + arg_url +'/volumes-and-issues'
		self.publisher = 'Springer'
		self.issues = []
		self.papers = []
		self.auths = []

	def init_issues(self, arg_first_volume, arg_last_volume, arg_issues_per_volume):
		for volume in range(int(arg_last_volume), int(arg_first_volume) + 1):
			if arg_issues_per_volume > 1:
				for issue in range(1, arg_issues_per_volume + 1):
					issue_url = self.url + "/" + str(volume) + '-' + str(issue)
					self.issues.append(issue_url)

	def scrape(self):
		counter = 0 
		print("\nScraping '" + self.name + "' (" + self.publisher + ")")
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
		for issue in self.issues:
			counter+=1
			self.progress_bar(counter)
			webpage = requests.get("http://" + issue, headers=headers)
			soup = BeautifulSoup(webpage.content, 'html.parser')

			papers_list = [a.text for a in soup.find_all('a', href=lambda href: href and href.startswith('https://link.springer.com/article'))]
			for paper in papers_list:
				self.papers.append(paper)

			auths_list = [a.li.text for a in soup.find_all('ul', class_='c-author-list c-author-list--compact u-text-sm')]
			for auth in auths_list:
				self.auths.append(auth)

			time.sleep(1.0)

		self.progress_bar(len(self.issues)+1)


class SIAM(Journal):

	def __init__(self, arg_name, arg_url):
		self.name = arg_name
		self.url = 'epubs.siam.org/toc/' + arg_url
		self.publisher = 'SIAM'
		self.issues = []
		self.papers = []
		self.auths = []

	def init_issues(self, arg_first_volume, arg_last_volume, arg_issues_per_volume):
		for volume in range(int(arg_last_volume), int(arg_first_volume) + 1):
			if arg_issues_per_volume > 1:
				for issue in range(1, arg_issues_per_volume + 1):
					issue_url = self.url + "/" + str(volume) + '/' + str(issue)
					self.issues.append(issue_url)

	def scrape(self):
		counter = 0 
		print("\nScraping '" + self.name + "' (" + self.publisher + ")")
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
		for issue in self.issues:
			counter+=1
			self.progress_bar(counter)
			webpage = requests.get("http://" + issue, headers=headers)
			soup = BeautifulSoup(webpage.content, 'html.parser')


			papers_list = [a.text for a in soup.find_all('a', href=lambda href: href and href.startswith('/doi/'), id=True)]
			for paper in papers_list:
				self.papers.append(paper)

			auths_list = [a.span.text for a in soup.find_all('a', href=lambda href: href and href.startswith('/author/'))]
			for auth in auths_list:
				self.auths.append(auth)

			time.sleep(1.0)

		self.progress_bar(len(self.issues)+1)


class DeGruyter(Journal):

	def __init__(self, arg_name, arg_url):
		self.name = arg_name
		self.url = 'degruyter.com/journal/key/' + arg_url
		self.publisher = 'De Gruyter'
		self.issues = []
		self.papers = []
		self.auths = []

	def init_issues(self, arg_first_volume, arg_last_volume, arg_issues_per_volume):
		for volume in range(int(arg_last_volume), int(arg_first_volume) + 1):
			if arg_issues_per_volume > 1:
				for issue in range(1, arg_issues_per_volume + 1):
					issue_url = self.url + "/" + str(volume) + "/" + str(issue) + "/html"
					self.issues.append(issue_url)

	def scrape(self):
		counter = 0 
		print("\nScraping '" + self.name + "' (" + self.publisher + ")")
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
		for issue in self.issues:
			counter+=1
			self.progress_bar(counter)
			webpage = requests.get("http://" + issue, headers=headers)
			soup = BeautifulSoup(webpage.content, 'html.parser')

			papers_list = [a.text for a in soup.find_all('h4', class_='titleSearchPageResult mb-0')]
			for paper in papers_list:
				self.papers.append(paper)

			auths_list = [a.text for a in soup.find_all('div', class_='contributors me-2 metadataAndContributorsFont')]
			for auth in auths_list:
				self.auths.append(auth)

			time.sleep(1.0)

		self.progress_bar(len(self.issues)+1)


class Wiley(Journal):

	def __init__(self, arg_name, arg_url, arg_start_year):
		self.name = arg_name
		self.url = 'onlinelibrary.wiley.com/toc/' + arg_url
		self.publisher = 'John Wiley & Sons'
		self.year = arg_start_year
		self.issues = []
		self.papers = []
		self.auths = []

	def init_issues(self, arg_first_volume, arg_last_volume, arg_issues_per_volume):
		volume_counter = 1
		for volume in range(int(arg_last_volume), int(arg_first_volume) + 1):
			if arg_issues_per_volume > 1:
				for issue in range(1, arg_issues_per_volume + 1):
					issue_url = self.url + "/" + str(self.year) + "/" + str(volume) + "/" + str(issue)
					if self.name == "Internation Journal for Numerical Methods in Engineering":
						if self.year < 2020 and issue > 13:
							volume_counter += 1
							if volume_counter > 4:
								self.year += 1
								volume_counter = 1
								break

							else:
								break

						elif self.year >= 2020 and issue == arg_issues_per_volume:
							self.year += 1
							break

					elif issue == arg_issues_per_volume:
						self.year += 1

					self.issues.append(issue_url)

	def scrape(self):
		import cloudscraper

		counter = 0 
		print("\nScraping '" + self.name + "' (" + self.publisher + ")")
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
		for issue in self.issues:
			counter+=1
			self.progress_bar(counter)
			scraper = cloudscraper.create_scraper(delay=10,   browser={'custom': 'ScraperBot/1.0',})
			webpage = scraper.get("http://" + issue, headers=headers)
			soup = BeautifulSoup(webpage.content, 'html.parser')

			papers_list = [a.h2.text for a in soup.find_all('a', class_='issue-item__title visitable')]
			for paper in papers_list:
				self.papers.append(paper)

			auths_list = [a.text for a in soup.find_all('span', class_='author-style')]
			for auth in auths_list:
				self.auths.append(auth)

			time.sleep(1.0)

		self.progress_bar(len(self.issues)+1)