import sqlite3
import os
import sys

class DBconnect:
	def __init__(self):
		self.conn = None
		self.fname = None
		self.cursor = None

	def getConnection(self,fname):
		try:
			self.conn = sqlite3.connect(fname)
			self.fname = fname
			print(sqlite3.version)

		except sqlite3.Error as err:
			print(err)


	def putQuery(self,query):
		try:
			self.cursor = self.conn.cursor()
			self.cursor.execute(query)

		except sqlite3.Error as err:
			print(err)

	def getQuery(self,query):
		try:
			self.cursor = self.conn.cursor()
			self.cursor.execute(query)

			rows = self.cursor.fetchall()
			return rows

		except sqlite3.Error as err:
			print(err)
			return None

	def closeConnection(self):
		self.conn.commit()
		self.conn.close()

# obj = DBconnect()
# if(__name__== "__main__"):
# 	obj.getConnection('./connection.db')
# 	#obj.putQuery("CREATE TABLE projects (id integer PRIMARY KEY, name text NOT NULL, start_date text, end_date text);")
# 	while(True):
# 		print("enter type of query")
# 		types = int(input())
# 		if(types==0):
# 			query=input()
# 			obj.putQuery(query)
# 		elif(types==1):
# 			query=input()
# 			query=obj.getQuery(query)
# 			print(query)
# 		else:
# 			break
# 	obj.closeConnection()
