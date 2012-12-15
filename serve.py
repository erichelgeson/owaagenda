from bottle import run, response, template, request, abort, get
from owaagenda import *

baseurl = "https://mail.example.com/owa/?ae=Folder&t=IPF.Appointment"
@get('/day')
def day():
	dy = request.GET.get('dy', '').strip()
	mn = request.GET.get('mn', '').strip()
	yr = request.GET.get('yr', '').strip()
	user = request.GET.get('user', '').strip()
	pwd = request.GET.get('pwd', '').strip()

	url = baseurl + "&yr=%s&mn=%s&dy=%s" % (yr, mn, dy)
	return getAgenda(url,user,pwd)

@get('/')
def index():
	user = request.GET.get('user', '').strip()
	pwd = request.GET.get('pwd', '').strip()
	return getAgenda(baseurl,user,pwd)

def getAgenda(url,user,pwd):
	html = getHtml(url,user,pwd)
        if html == None:
                return '[{"errror": "bad html from owa"}]'
        agenda = scrapeAgenda(html)
        resp = dataFormatter(agenda)
        return resp

run(host='0.0.0.0', port=8070, reloader=True)
