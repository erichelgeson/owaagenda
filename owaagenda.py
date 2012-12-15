"""
Screen scrape a single day view of OWA calendar
	example call
	python agenda.py "https://mail.example.com/owa/?ae=Folder&t=IPF.Appointment" username
"""
import sys, json, requests, logging
from bs4 import BeautifulSoup

def getHtml(url, user, pwd):
	html = None
	try:
		logging.debug("debug getHtml:url:" + url)
		request = requests.get(url, auth=(user, pwd))
		request.raise_for_status()
		html = request.text 
	except HTTPError, e:
		logging.error("failed to connect to owa: " + request.status_code)
	return html

def scrapeAgenda(html):
	bs = BeautifulSoup(html)
	agenda = []
	for td in bs.find_all("td", {"class": "txt"}):
		for a in td.find_all("a"):
			#TODO - fix this with better parsing (time, description, location)
			tm, desc = a["title"].split(",")[0], a["title"].split(',')[1:]
			desc = ','.join(desc)
			s = desc.find(";")
			if s > 0:
				desc, loc = desc[:s], desc[s+1:]
			else:
				loc = ""
			d = dict(time=tm.strip(), description=desc.strip(),location=loc.strip())
			agenda.append(d)
	return agenda

def dataFormatter(thelist, formatType="json"):
	if(formatType=="json"):
		return json.dumps(thelist)	
	else:
		thelist = ["%s: %s - %s<br>" % (x['time'],x['description'],x['location']) for x in thelist]
        	return "\n".join(thelist)
