#This module is used to create input files based on age group and location. The data is read from sqlite3 database
#Following age groups were provided both for USA and NON-USA based location to created input file.
#These files are then used by the mrjob to calculate pair wise book similarity.
#README.md file has details to run the program

import sqlite3 as lite
import os
import sys
from itertools import islice
from pandas import DataFrame

#Create input file for usa based users. This module takes from age, to age and location as an input.
#It then runs a database query to fetch userid, book isbn and rating for the given age range and creates a csv
#file. This csv file is then used by bookCollaboration mr job to calculate pairwise similarity for USA based records
def createfileusa(fromage,toage,location):
	con = lite.connect("../Database/Books.db")
	c = con.cursor()
	query = "SELECT u.UserID,b.ISBN,b.rating FROM BXUsers u join BXBooksRating b on u.UserID = b.UserID where Location like lower('%"+ location +"%') and age>="+str(fromage)+" and age <="+str(toage) +" and b.rating>0 and b.ISBN in (select b.ISBN FROM BXBooksRating b JOIN BXUsers u on u.UserID = b.'UserID' where Location like lower('%"+location+"%') and age>="+str(fromage) +" and age <="+ str(toage)+" and b.rating>0 GROUP BY ISBN HAVING COUNT(u.UserID)>5)"
	print query
	c.execute(query)
	rows = c.fetchall()
	df = DataFrame(rows,columns=['UserId','ISBN','Rating'])
	df = df.set_index('UserId')
	df.to_csv("../Data/"+location+"_"+str(fromage)+"to"+str(toage)+".csv",sep=",",header=False,line_terminator='\n')


#Create input file for usa based users. This module takes from age, to age and location as an input.
#It then runs a database query to fetch userid, book isbn and rating for the given age range and creates a csv
#file. This csv file is then used by bookCollaboration mr job to calculate pairwise similarity for NON-USA based records
def createfilenonusa(fromage,toage,location):
	con = lite.connect("../Database/Books.db")
	c = con.cursor()
	query = "SELECT u.UserID,b.ISBN,b.rating FROM BXUsers u join BXBooksRating b on u.UserID = b.UserID where Location not like lower('%"+ location +"%') and age>="+str(fromage)+" and age <="+str(toage) +" and b.rating>0 and b.ISBN in (select b.ISBN FROM BXBooksRating b JOIN BXUsers u on u.UserID = b.'UserID' where Location not like lower('%"+location+"%') and age>="+str(fromage)+" and age <="+ str(toage)+" and b.rating>0 GROUP BY ISBN HAVING COUNT(u.UserID)>5)"
	print query
	c.execute(query)
	rows = c.fetchall()
	df = DataFrame(rows,columns=['UserId','ISBN','Rating'])
	df = df.set_index('UserId')
	df.to_csv("../Data/NON"+location+"_"+str(fromage)+"to"+str(toage)+".csv",sep=",",header=False,line_terminator='\n')

if __name__ =='__main__':
	n = raw_input("Create more files Yes/No: ")
	while (n.lower()=="y"):
		loc =input("enter location 1. usa 2. nonusa: ")
		fromage = input("Enter from age: ")
		toage = input("enter to age: ")

		if(loc==1):
			createfileusa(fromage,toage,'USA')
		elif(loc==2):
			createfilenonusa(fromage,toage,'USA')
		else:
			print "Sorry invalid location value"
		n = raw_input("Create more files Yes/No: ")