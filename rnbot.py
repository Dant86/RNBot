from ics import Calendar
from urllib.request import urlopen
import sqlite3
import unicodedata
import html
import speech_recognition as sr 
from datetime import datetime

def parseDate():
	now = datetime.now()
	parsed = str(now.year)+"-"+"0"+str(now.month)+"-"+"0"+str(now.day)+":"+str(now.hour)+":"+str(now.minute)
	return parsed

def connect():
	global c,conn
	conn = sqlite3.connect('events.db')
	c = conn.cursor()

def getCal():
	url = 'http://latinschool.myschoolapp.com/podium/feed/iCal.aspx?z=lkwkXqIS41wpJD%2fJAv7roO8t3i98I5crYsXgdHfen0ux1SyszIvUFziEJKW3iGNuv36o5c9CgNrBmLmSvEsZyg%3d%3d'
	return Calendar(urlopen(url).read().decode('iso-8859-1'))

def date(event):
    return str(event.begin.year) + "-" + str(event.begin.month).zfill(2) + "-" + str(event.begin.day).zfill(2) + ":" + str(event.begin.hour).zfill(2) + ":" + str(event.begin.minute).zfill(2)

def exist(event):
	global c,conn
	comm = u"select * from event where start = '{}'".format(html.unescape(date(event)))
	c.execute(comm)
	if not c.fetchall():
		return False
	else:
		return True

def exist_name(name):
	global c,conn
	comm = u"select * from event where name = '{}'".format(name)
	c.execute(comm)
	if not c.fetchall():
		return False
	else:
		return True

def getEventDate(name,date):
	# if(not exist_name(name)):
	# 	return None
	comm = u"select start from event where name = '{}' limit 1".format(name)
	c.execute(comm)
	return c.fetchall()[0]

def addEventsfromCal(cal):
	for i in cal.events:
		if(not exist(i)):
			print("%s: %s %s" % (i.name,i.begin,i.description))
			comm = u"insert into event (start,name) values('{}', '{}')".format(html.unescape(date(i)),html.unescape(i.name))
			print(comm)
			c.execute(comm)

def speechRecognize():
	r2 = sr.Recognizer()
	with sr.Microphone() as source:
		print("What class would you like to know more about?")
		audio = r2.listen(source)
		res = r2.recognize_google(audio)
	return res

#connect to database
connect()
#get calendar from file on romannet
cal = getCal()
#parse calendar to database
addEventsfromCal(cal)
#save changes to database
conn.commit()
#get user response
foo = speechRecognize()
#parse response
if("Biology" in foo or "biology" in foo):
	print(getEventDate("Hon Biology - 9310Y.1 (A0)","2017-04-10:12:40"))
if("BC calculus" in foo):
	print(getEventDate("AP Calculus BC - 853Y.1 (D1)",parseDate()))
if("English" in foo or "english" in foo):
	print(getEventDate("English 11: Silenced America - 2124Y.2 (G0)",parseDate()))
if("College counseling" in foo or "college counseling" in foo):
	print(getEventDate("College Counseling 11 - 0041S.5(LP) (E0)",parseDate()))
if("History" in foo or "history" in foo):
	print(getEventDate("U.S. Social History - 351Y.3 (B1)",parseDate()))
if("Computer science" in foo or "computer science" in foo):
	print(getEventDate("Web Application Development (sem 2) - 6014S.1 (F1)",parseDate()))
if("French" in foo or "french" in foo):
	print(getEventDate("AP French Language - 452Y.1 (H0)",parseDate()))
#print(foo)
print(parseDate())
print(foo)



