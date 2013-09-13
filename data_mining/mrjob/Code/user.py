import sqlite3 as lite
from random import randrange
from collections import defaultdict
import random
import subprocess


d= { 0:(5,19),
	1:(5,19),
	2:(20,29),
	3:(30,39),
	4:(40,59),
	5:(40,59),
	6:(60,71),
	7:(60,71)
	}

def filepath(age,loc):
	f=""
	if age<20:
		f = "5to19.csv"
	elif (age>=20 and age < 30):
		f = "20to29.csv"
	elif (age>=30 and age <40):
		f = "30to39.csv"
	elif (age>=40 and age < 60):
		f = "40to59.csv"
	elif (age>=60 and age < 72):
		f = "60to71.csv"


	if loc ==1:
		path = "../Similarity/USA_"+f
	else:
		path = "../Similarity/NONUSA_"+f
	return path

def selectbooks(age,loc):
	booksdict = defaultdict()
	con = lite.connect("../Database/Books.db")
	cur = con.cursor()
	a = d[age/10]
	if loc==1:
		query = "select b.ISBN FROM BXBooksRating b JOIN BXUsers u on u.UserID = b.UserID where Location like '%usa%' and age>="+str(a[0])+" and age <="+str(a[1])+" and b.rating>0 GROUP BY ISBN HAVING COUNT(u.UserID)>5"
	else:
		query="select b.ISBN FROM BXBooksRating b JOIN BXUsers u on u.UserID = b.'UserID' where Location not like '%usa%' and age>="+str(a[0])+" and age <="+str(a[1])+" and b.rating>0 GROUP BY ISBN HAVING COUNT(u.UserID)>5"
	cur.execute(query)
	rows=list(cur.fetchall())
	print "RATE THE FOLLOWING BOOKS"
	print "************************"
	books = random.sample(range(len(rows)), 5)
	for i in books:
		#print "Select Title, Author,pubyea from BXBooks where ISBN = '"+str(rows[i][0])+"'"
		cur.execute("Select Title, Author,pubyear from BXBooks where ISBN = '"+str(rows[i][0])+"'")
		
		bl= list(cur.fetchall())
		print "-----------------------------"
		print "Book Title: "+ str(bl[0][0])
		print "Author: "+ str(bl[0][1])
		print "Year of Publication: "+ str(bl[0][2])
		print "-----------------------------"
		rating= input("Enter Rating between 1-10: ")
		while True:	
			if (int(rating)>=1 and int(rating) <=10):
				break
			else:
				print "Invalid rating enter again!"
				rating= input("Enter Rating between 1-10: ")
		booksdict[str(rows[i][0])]= int(rating)
	return booksdict


if __name__ =='__main__':

	age = input("Enter your age: ")
	location = input("Enter your location:1.USA, 2.NonUSA : " )
	name = raw_input("Enter your first name: ")
	while True:
		if (age > 71 or age < 5):
			print ("Sorry no data exists, re-enter the age between 5 and 71:")
			age = input("Enter your age: ")
		else:
			break
		print location
		if (location !=1 and location !=2):
			print ("Invalid selection!")
			location = input("Enter your location:1.USA, 2.NonUSA : " )
		else:
			break;
 	path = filepath(int(age),location)
 	print path
 	books = selectbooks(age,location)
 	argsbook=""
 	for id,value in books.iteritems():
 		if value>5:
 			argsbook=argsbook+id+","
 		else:
 			pass
 	if(len(argsbook)==0):
 		print "For effective recommendations atleast one highly rated books is required, try again next time!!!"
 	else:
 		argsbook[:-1]
 		child = subprocess.Popen("python Recommend.py --inputbooks='"+argsbook[:-1]+"' "+path+" > ../Recommendations/recommendations_"+name+".txt", shell=True)


