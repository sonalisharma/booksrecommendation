from mrjob.job import MRJob
from itertools import combinations
from itertools import izip
from math import sqrt
import os
import sqlite3 as lite
#import metrics

#Method to get book details
def getbookname(book_id):
    #change the path to the absolute path of the database
    filepath="/Users/sonali/Documents/Ischool/INFODMA/Project/bookhunters/data_mining/mrjob/Database/Books.db"
    #filepath = os.path.join(os.pardir, "Database","Books.db")
    con = lite.connect(filepath)
    cur = con.cursor()
    cur.execute("Select Title, Author,pubyear from BXBooks where ISBN = '"+book_id+"'")
    bl= list(cur.fetchall())
    bookname = str(bl[0][0])+" by "+str(bl[0][1])+", "+str(bl[0][2])
    return bookname
    #return filepath

class Recommend(MRJob):

    #Fetching books similar to input books
    def fetch_books(self, key, line):
        """
        Group all user ratings together
        """
        bookpair, rating = line.split(' ')
        books = bookpair.split("_")
        #inputbooks = ['0345339703','0451524934']
        inputbooks = self.options.inputbooks.split(",")
        if (float(rating) > 0.5):
            if(books[0] in inputbooks):
                yield  "com", (books[0]+'_'+books[1],rating)

    #Reading command line arguments in mrjob
    def configure_options(self):
        super(Recommend, self).configure_options()
        self.add_passthrough_option(
        '--inputbooks', type='string', default='', help='...') #checkout optionparser

    #Grouping books    
    def books_grouped(self, book_id, books):
        yield "com",list(books)
        
    #sorting list in descending oder of similarity    
    def combine_book_pairs(self, book_id, books):
        sorted_by_second = sorted(books, key=lambda tup: tup[1])
        yield "com", sorted_by_second[::-1][:5]

    #provide recommendations
    def merge_books(self, book_id, books_set):
        recommendations = list()
        for i in books_set:
            for j in i:   
                original,recom = j[0].split('_')
                #recommendations.append(getbookname(str(recom))
                #recommendations.append(getbookname(recom))
                yield "Reco:",getbookname(recom)

        #yield ["Recommendations",recommendations[:5]]

    def steps(self):
        return [self.mr(mapper=self.fetch_books, reducer=self.books_grouped),
                self.mr(mapper=self.combine_book_pairs, reducer=self.merge_books)]

if __name__ == '__main__':
    Recommend.run()