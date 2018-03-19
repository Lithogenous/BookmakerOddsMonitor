# -*- coding: UTF-8 -*-
'''
author: Lithogenous

GameList:which contain all the suitable Game
OddList:

'''
import urllib2
import requests
from bs4 import BeautifulSoup
import time
import lxml
import random





class Odds(object):
    def __init__(self, host, draw, vist):
    	self.hostOdds = host
    	self.drawOdds = draw
    	self.vistOdds = vist
    	self.ret = 1.0/float(self.hostOdds) + 1.0/ float(self.drawOdds) + 1.0/ float(self.vistOdds)

    def isEqu(self, odd2):
    	if self.hostOdds == odd2.hostOdds and \
    	self.drawOdds == odd2.drawOdds and \
    	self.vistOdds == odd2.vistOdds:
    		return 1
    	else:
    		return 0

    def __str__(self):
    	return str(self.hostOdds) + " " + str(self.drawOdds) + " " + str(self.vistOdds) + " " + str(self.ret)


class Game(object):  

	def __init__(self, gameID, GameLeague):
		self.gameID = gameID
		self.OddsDic = {}  
		self.GameLeague = GameLeague


    
	def addOdds(self, host, draw, vist, compId):
		
		changeOdds = Odds(host, draw, vist)
		if compId in self.OddsDic and self.OddsDic[compId].isEqu(changeOdds):
			return 0
		else:
			self.OddsDic[compId] = changeOdds
			return 1
		
	def getMaxOdds(self):
		hostOddList = []
		drawOddList = []
		vistOddList = []

		for eachodd in self.OddsDic.values():
			hostOddList.append(eachodd.hostOdds)
			drawOddList.append(eachodd.drawOdds)
			vistOddList.append(eachodd.vistOdds)
		
		maxOdds = Odds(max(hostOddList), max(drawOddList), max(vistOddList))
		return maxOdds




	def getOdds(self):
		return self.OddsDic  
    
  
	def __str__(self):  
		return self.gameID  +" in " + self.GameLeague


def getAllOdds(gameId, compId):
	'''
	query the odds of a given game and given company
	'''
	url = "http://data.310win.com/changeDetail/1x2.aspx?id=" + \
		str(gameId) + "&companyid=" + str(compId) + "&l=0"

	html = httpRequest(url)
	bsObj = BeautifulSoup(html, "lxml")
#	time.sleep(0.3)
	#print bsObj.prettify()

	TableList = bsObj.find_all("tr")
	try:

		row = TableList[1].find_all("td")
		changeOdds = Odds(float(row[0].string), float(row[1].string), float(row[2].string))
		return changeOdds


	except:
		#print "failed to get"
		changeOdds = Odds(0.1, 0.1, 0.1)
		return changeOdds



def httpRequest(url, proxy = None):
    '''
    hold a http request
    '''  
    try:
 		headers = {
        	'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        	'Content-Type': 'application/x-www-form-urlencoded',
        	'Connection' : 'Keep-Alive',
        	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
		}
		ret = requests.get(url, headers=headers)
		return ret.text
    except:
    	return None

BaseUrl = "http://vip.win007.com/changedetail/lastchange.aspx?ot=2&gsID="


LeagueNameList = [
				"#006633", #xijia# 
				"#990099",#dejia#
				"#0088FF", #yijia#
				"#FF3333", #yingchao#
				"#663333", #fajia#
				"#0066FF", #zhongchao#


				"#F75000", #ouguan#
				"#0000DB"#, #yaguan#

				#"#660000" #shijiebei#
				
				]

compList = [
			'9',  #weilian#
			'14',  #weide#
#			'3', #huangguan#
#			'4',   ##ladbrokes##
			'12', #yishengbo#
#			'1',  #aomen#
			'8',  #bet365#
#			'19',  #interwetten#
			'45',   #manbetx#
			'23', #jinbaobo#
			'22', #10bet#
			'24', #12bet#
#			'31', #liji# 
#			'35',  #yinghe#
			'42'#, #18bet#
			]

GameDic = {}
bestDic = {}

#getAllOdds("1507473", compList[5])
companyUrl = ""
for i in compList:
	companyUrl = companyUrl + i + ','

companyUrl = companyUrl[:-1]
Url = BaseUrl + companyUrl
print Url

while True:


	html = httpRequest(Url)
	if html is None:
		break

	bsObj = BeautifulSoup(html, "lxml")
	#print bsObj.prettify()

	TableList = bsObj.find_all("tr")

#	oldGameDic = GameDic
	oddChangeFlag = 0

	##find the odd change game in the table of the web
	for i in TableList[1:]:

		try:
			gameid =  i.attrs['scheduleid']   ###Game ID got it!!
			companyid =  i.attrs['companyid']   ##Bet Company Got it!!
			s =  i.find_all('td')
			leagueId = s[1].attrs['bgcolor']  #Game League got it!!
			leagueId = leagueId.upper()
#			hostname = s[2].string

			hostOdd = float(s[3].string)
			drawOdd = float(s[4].string)
			vistOdd = float(s[5].string)

#			vistname = s[6].string
			changeTime = s[7].string

		except IndexError,e:
			pass


		## the game in a selected league?
		if leagueId in LeagueNameList:
			pass
		else:
			continue

		##new game get
		if gameid not in GameDic:
			newGame = Game(gameid, leagueId)
			newGame.addOdds(hostOdd, drawOdd, vistOdd, companyid)

			for eachcomp in compList:
				odd = getAllOdds(gameid, eachcomp)
				newGame.addOdds(odd.hostOdds, odd.drawOdds, odd.vistOdds, eachcomp)
			
			oddChangeFlag = 1
			GameDic[gameid] = newGame

		##the game is exist in the dic
		else:

			if GameDic[gameid].addOdds(hostOdd, drawOdd, vistOdd, companyid):
				oddChangeFlag = 1



	print "\n"
	print time.ctime()
	print "\n"
	if oddChangeFlag == 0:
		print len(GameDic)
	else:
		print len(GameDic)
		for i in GameDic:
			odddic = GameDic[i].getOdds()

			maxodds = GameDic[i].getMaxOdds()

			mon = 1.0/ maxodds.hostOdds + 1.0/ maxodds.drawOdds + 1.0/maxodds.vistOdds
			if mon < 1.08:
				print "@@@@@@@@@@@@@@@@@@@@@@@"
				print GameDic[i]
				for j in odddic:
					print j, odddic[j]

				print "-----------------------"
				print "max odds:", GameDic[i].getMaxOdds(), mon
				print "~~~~~~~~~~~~~~~~~~~~~~~"
			else :
				pass

			

#	print type(TableList)
	
	time.sleep(4)

#	print TableList
#	print len(TableList)
#	print TableList[-1]
#	for i in TableList:
#		print i["scheduleid"]

















#	break