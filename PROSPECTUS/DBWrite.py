#!/usr/bin/env python
# 

import MySQLdb
import datetime
import sys

dbHostName = "127.0.0.1"
dbUserName = "root"
dbUserPW = ""
dbTwitterDatabase = "Twitter"


class DBTwitterWrite(object):

	def __init__(self, searchStr):
		self.db = MySQLdb.connect(dbHostName, dbUserName, dbUserPW, dbTwitterDatabase)
		self.cursor = self.db.cursor()
		self.strSearch = searchStr
		
	def StripQuotes(self, strContent):
		return self.db.escape_string(strContent)

	def WriteList(self, TweetList):
		# Assumes the following structure:
		for x in TweetList:
			sqlStr = "INSERT INTO Tweets(search_term, hits, trackback_date, title, url, \
				trackback_permalink, topsy_author_img, topsy_trackback_url, \
				target_birth_date, content, score, trackback_author_nick, \
				trackback_author_url, trackback_total,  \
				topsy_author_url, trackback_author_name, firstpost_date) \
				VALUES (\"%s\", %s, \'%s\', \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", %s, \"%s\", \"%s\", \
				%s, \"%s\", \"%s\", \"%s\")" % (self.strSearch, str(x["hits"]), str(datetime.datetime.fromtimestamp(int(x["trackback_date"])).strftime('%Y-%m-%d %H:%M:%S')), self.StripQuotes(x["title"].encode('utf-8')), self.StripQuotes(x["url"].encode('utf-8')), self.StripQuotes(x["trackback_permalink"].encode('utf-8')), self.StripQuotes(x["topsy_author_img"].encode('utf-8')), self.StripQuotes(x["topsy_trackback_url"].encode('utf-8')), str(datetime.datetime.fromtimestamp(int(x["target_birth_date"])).strftime('%Y-%m-%d %H:%M:%S')), self.StripQuotes(x["content"].encode('utf-8')), x["score"], self.StripQuotes(x["trackback_author_nick"].encode('utf-8')), self.StripQuotes(x["trackback_author_url"].encode('utf-8')), x["trackback_total"], self.StripQuotes(x["topsy_author_url"].encode('utf-8')), self.StripQuotes(x["trackback_author_name"].encode('utf-8')), str(datetime.datetime.fromtimestamp(int(x["target_birth_date"])).strftime('%Y-%m-%d %H:%M:%S')))

			try:
				# Execute SQL
				# print sqlStr
				self.cursor.execute(sqlStr)
				#self.cursor.execute("INSERT INTO Tweets(hits, trackback_date, title, url, \
				#trackback_permalink, topsy_author_img, topsy_trackback_url, \
				#target_birth_date, content, score, trackback_author_nick, \
				#trackback_author_url, trackback_total,  \
				#topsy_author_url, trackback_author_name, firstpost_date) \
				#VALUES (%s, \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", %s, \"%s\", \"%s\", \
				#%s, \"%s\", \"%s\", \"%s\")", (str(x["hits"]), str(datetime.datetime.fromtimestamp(int(x["trackback_date"])).strftime('%Y-%m-%d %H:%M:%S')), x["title"].encode('utf-8'),  x["url"].encode('utf-8'), x["trackback_permalink"].encode('utf-8'), x["topsy_author_img"].encode('utf-8'), x["topsy_trackback_url"].encode('utf-8'),str(datetime.datetime.fromtimestamp(int(x["target_birth_date"])).strftime('%Y-%m-%d %H:%M:%S')), x["content"].encode('utf-8'), x["score"], x["trackback_author_nick"].encode('utf-8'), x["trackback_author_url"].encode('utf-8'), x["trackback_total"], x["topsy_author_url"].encode('utf-8'), x["trackback_author_name"].encode('utf-8'), str(datetime.datetime.fromtimestamp(int(x["target_birth_date"])).strftime('%Y-%m-%d %H:%M:%S'))))

				# And Commit changes
				self.db.commit()
			except Exception, err:
				#Rollback if problems
				sys.stderr.write('ERROR: %s\n' % str(err))
				self.db.rollback()
		
		self.db.close()

	def enquote(self, strNeedsQuotes):
		return "'" + strNeedsQuotes + "'"


			
