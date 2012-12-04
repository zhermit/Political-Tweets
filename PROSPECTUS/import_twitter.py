import urllib
import simplejson
import sys
import DBWrite
from calendar import Calendar
import datetime
from datetime import date
import time

urlHost = "http://otter.topsy.com/"
ApiKey = "CA5577686E0942479918E96E58DAAEB6"
urlApi = "&apikey=" + ApiKey
#strsearchTerm = ""

class TwitterSearch(object):

	def __init__(self, argv):
#		print "Initializing " + argv
		strArgs = str.split(argv)
		self.strsearchTerm = strArgs[0]
		
	def BuildSearch(self, day, month, year, offset=0):
		BeginSearchDay = datetime.datetime(year, month, day, 0,0,0)
		BeginSearchDayUnix = str(time.mktime(BeginSearchDay.timetuple()))
		print BeginSearchDay

		EndSearchDay = datetime.datetime(year, month, day, 23,59,59)
		print EndSearchDay
		EndSearchDayUnix =  str(time.mktime(EndSearchDay.timetuple()))
		strQuery = "search.json?q=" + str(self.ConvertString(self.strsearchTerm)) 
		strQuery = strQuery + "&perpage=100&mintime=" + BeginSearchDayUnix
		strQuery = strQuery + "&maxtime=" + EndSearchDayUnix
		if (offset > 0):
			strQuery = strQuery + "&offset=" + str(offset)
		strQuery = strQuery + urlApi
		return strQuery

	def ConvertString(self, strConvert):
		return strConvert.replace(" ", "+")

	def GetDaysInMonth(self, monthNum, YearNum):
		if monthNum == 12:
			daysNum = (date(YearNum+1, (1), 1) - date(YearNum, monthNum, 1)).days
		else:
			daysNum = (date(YearNum, (monthNum+1), 1) - date(YearNum, monthNum, 1)).days
		return daysNum

	def PerformSearch(self, day, month, year, offset=0):
		urlFull = urlHost + self.BuildSearch(day, month, year, offset)
		print urlFull
		# simplejson.load(urllib.urlopen(urlFull))
		result = simplejson.load(urllib.urlopen(urlFull))
		return result

	def DailySearch(self):
		SearchMonth = 1
		SearchYear = 2011
		cal = Calendar()
		currdate = datetime.datetime.now()

		while not (SearchMonth == currdate.month and SearchYear == currdate.year):
			month_days = self.GetDaysInMonth(SearchMonth, SearchYear)
			for SearchDay in range(month_days):
				if not SearchDay == 0:
					#print "Performing Search for " + str(SearchDay)
					offset = -1
					totalResults = 0

					# A day can have multiple pages of results.
					# Limited to one page of 100 per query.
					# So need to grab 100, rest, grab the next 100, until the day is done

					while (offset < totalResults):
						try:
							QueryResults = self.PerformSearch(SearchDay, SearchMonth, SearchYear, offset)
							tp = TwitterProcessing(QueryResults)
							TweetResultSet = tp.ProcessTweets()
							# this should auto-increment 100 everytime
							old_offset = offset
							offset = tp.GetOffset()
							# Really only need to get this once, but not a big deal
							totalResults = tp.GetCount()

							print "		Processing Results for %i - %i of %i " % (old_offset, offset, totalResults) 

							# Save To DB
							DB = DBWrite.DBTwitterWrite(self.strsearchTerm)
							DB.WriteList(TweetResultSet)
						except Exception:
							print "Error in module for offset " + str(old_offset)
							print "Date:" + str(SearchMonth) + "-" + str(SearchDay) + "-" + str(SearchYear)
							sys.exc_clear()

						# And Rest
						print "Sleeping..."
						time.sleep(60)
						


			# Increment search
			if SearchMonth == 12:
				SearchMonth = 1
				SearchYear = SearchYear + 1
			else:
				SearchMonth = SearchMonth + 1


	def execute(self):
		try:
			if self.function:
				self.function(*self.args)
		except Exception, e:
			sys.stderr.write("%s %s\n" % ("TwitterSearch#execute", e))
			pass


class TwitterProcessing(object):
	def __init__(self, FullResults):
		self.ResponseSet = FullResults

	def GetOffset(self):
		return self.ResponseSet["response"]["last_offset"]

	def GetCount(self):
		return self.ResponseSet["response"]["total"]

	def ProcessTweets(self):
		#print simplejson.dumps(self.ResponseSet)
		self.TweetsList = self.ResponseSet["response"]["list"]
		# print self.ResponseSet
#		print self.TweetsList[0]["hits"]
		return self.TweetsList
	


if __name__ == "__main__":
	import sys
	ts = TwitterSearch(sys.argv[1])
	ts.DailySearch()
#	ResultSet = ts.PerformSearch()
#	print ResultSet

#	tp = TwitterProcessing("TwitterTaxes.txt")
#	tp.ProcessTweets()
#	DB = DBWrite.DBTwitterWrite()
#	DB.WriteList(tp.ProcessTweets())

 # twitterResults.PerformSearch("taxes")	