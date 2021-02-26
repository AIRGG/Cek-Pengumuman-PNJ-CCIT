import requests as rq
from bs4 import BeautifulSoup
import re, threading, time, sys

class CekPengumuman():
	def __init__(self, baseurl):
		if len(baseurl) > 0 and baseurl[-1] != "/": baseurl += "/"
		self.base_url = baseurl
		self.start_time = time.time()
	
	def getTime(self):
		print("--- %s seconds ---\n" % (time.time() - self.start_time))

	def parseHttp(self):
		html = ''
		try:
			hit = rq.get(self.base_url) 
			html = BeautifulSoup(hit.content, "html.parser")
			return html
		except rq.exceptions.HTTPError as errh:
		    print ("[Error Http]:",errh)
		except rq.exceptions.ConnectionError as errc:
		    print ("[Error Connecting]:",errc)
		except rq.exceptions.Timeout as errt:
		    print ("[Error Timeout]:",errt)
		except rq.exceptions.RequestException as err:
		    print ("[OOps] Something Else",err)
		except TypeError as ex:
			print("[ERROR] Cannot Parse HTML")
		except Exception as ex:
			print("[ERROR]",ex)
		finally:
			return html

	def exeRGX(self, payload, rgx):
		try:
			rgxcomp = re.compile(rgx)
			tmppayload = rgxcomp.findall(payload)
			return tmppayload
		except Exception as ex:
			print("[ERROR]",ex)
			return []

	def getPengumuman(self, wht):
		self.getTime()
		print("="*25,f" {wht.upper()} ","="*25)
		html = self.parseHttp()
		if len(html) > 0:

			if wht in ["ccit", "ccit-mhs"]: # Untuk CCIT
				# url = "https://ccit.eng.ui.ac.id/"
				if wht == "ccit":
					warta = html.find("div", {'id':'event_star_posts_col-3'})
					header = warta.find_all("h3", {'class':'entry-title'})
					for x in reversed(header):
						geta = x.text
						ahref = x.find("a")['href']
						print(f"[INFO] {geta}")
						print(f"[LINK] {ahref}", "\n----------------")
				
				elif wht == "ccit-mhs":
					article = html.find_all("article")
					for x in reversed(article):
						tmph = x.find("h2", {'class':'entry-title'}).find("a")
						title = tmph.text
						ahref = tmph['href']
						timepublish = x.find_all("time")[0].text

						print(f"[INFO] {title}")
						print(f"[DATE] {timepublish}")
						print(f"[LINK] {ahref}", "\n----------------")

			elif wht in ["pnj", "pnjnews"]: # Untuk PNJ
				# baseUrl = "http://pnj.ac.id/"
				# url = f"{self.base_url}beritautamadepanpagination/1"

				if wht == "pnj":
					pengumuman = html.find_all("div", {'class':'latest-posts-classic'})
					for x in reversed(pengumuman):
						tmpdate = x.find("div", {'class':'post-date'})
						tmpcontent = x.find("div", {'class':'post-content'})

						day = tmpdate.find("span", {'class':'day'})
						month = tmpdate.find("span", {'class':'month'})

						getday = ''.join(self.exeRGX(day.text, r"\w+"))
						getmonth = ''.join(self.exeRGX(month.text, r"\w+\s\w+"))

						a = tmpcontent.find("a")
						geta = ''.join(self.exeRGX(a.text, r"\s+\w.*"))
						tmpgeta = geta.split(" ")
						tmpgeta = ' '.join(tmpgeta).split() # Remove '' -> Blank String in List
						geta = ' '.join(tmpgeta).replace("\n","")
						
						print(f"[INFO] {geta}")
						print(f"[DATE] {getday} {getmonth}")
						print(f"[LINK] {self.base_url.replace('http', 'https')}{a['href'][1:]}", "\n----------------")
				
				elif wht == "pnjnews":
					tmpcontent = html.find_all("div", {'class':"widget-content"})
					for content in reversed(tmpcontent):
						tmpa = content.find("a")
						tmpspan = content.find("span").text
						
						ahref = tmpa['href']
						atext = tmpa.text
						span = ''.join(self.exeRGX(tmpspan, r'\w+ |\w+|, |:'))

						print(f"[INFO] {atext}")
						print(f"[DATE] {span}")
						print(f"[LINK] {self.base_url.replace('http', 'https')}{ahref}", "\n----------------")

		self.getTime()

if __name__ == "__main__":
	ccit = CekPengumuman("https://ccit.eng.ui.ac.id/")
	ccit.getPengumuman("ccit")

	ccitmhs = CekPengumuman("https://ccit.eng.ui.ac.id/category/pengumuman-untuk-siswa/page/1/")
	ccitmhs.getPengumuman("ccit-mhs")

	pnj = CekPengumuman("http://pnj.ac.id/")
	pnj.getPengumuman("pnj")
	
	print("==")
	inp = input("Ingin Show Berita PNJ (Y/N) ?\n==\n-> ")
	print()
	
	if str(inp).upper() == "Y":
		pnj.getPengumuman("pnjnews")
	time.sleep(3600)