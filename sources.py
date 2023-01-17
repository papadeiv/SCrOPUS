import csv
import time
from journal import *
from input import start_year, sources

class Sources():

	def __init__(self):
		self.total_issues = 0
		self.total_papers = 0
		self.list = []
		for source in sources:
			match source['publisher']:
				case "Elsevier":
					journal = Elsevier(source['name'], source['url'])
					journal.init_issues(source['first_volume'], source['last_volume'], source['issues_per_volume'])
					self.list.append(journal)

				case "Springer":
					journal = Springer(source['name'], source['url'])
					journal.init_issues(source['first_volume'], source['last_volume'], source['issues_per_volume'])
					self.list.append(journal)

				case "Society for Industrial and Applied Mathematics":
					journal = SIAM(source['name'], source['url'])
					journal.init_issues(source['first_volume'], source['last_volume'], source['issues_per_volume'])
					self.list.append(journal)

				case "De Gruyter":
					journal = DeGruyter(source['name'], source['url'])
					journal.init_issues(source['first_volume'], source['last_volume'], source['issues_per_volume'])
					self.list.append(journal)

				case "John Wiley & Sons":
					journal = Wiley(source['name'], source['url'], start_year)
					journal.init_issues(source['first_volume'], source['last_volume'], source['issues_per_volume'])
					self.list.append(journal)
			
				case _:
					journal = Journal(source['name'])
					journal.init_url(source['url'], source['separator'])
					journal.init_publisher(source['publisher'], start_year)
					journal.init_issues(source['first_volume'], source['last_volume'], source['issues_per_volume'])
					self.list.append(journal)

	def scrape(self):
		for journal in self.list:
			journal.scrape()
			self.total_issues += len(journal.issues)
			self.total_papers += len(journal.papers)

			time.sleep(3.0)

	def export(self):
		with open('output.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(['Publisher', 'Journal', 'Paper', 'Authors'])
			for journal in self.list:
				for paper in journal.papers:
					writer.writerow([journal.publisher, journal.name, paper])

	def print_info(self):
		print("\n\n  SC(R)OPUS terminated succesfully! Printing summary\n")
		print(50*"-")
		for journal in self.list:
			journal.print_info()

		print(50*"-")