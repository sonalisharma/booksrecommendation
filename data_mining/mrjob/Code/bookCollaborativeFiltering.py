from mrjob.job import MRJob
from itertools import combinations
from math import sqrt
import copy
#import metrics

class BookCollaborativeFiltering(MRJob):

    ###
    # TODO: write the functions needed to
    # 1) find potential matches, 
    # 2) calculate the Jaccard between users, with a user defined as a set of
    # reviewed businesses
    ##/

    def group_by_user_rating(self, key, line):
        """
        Group all user ratings together
        """
        try:
            user_id, isbn, rating = line.split(',')
            if float(rating) > 0.0:
                yield  user_id, (isbn, float(rating))
        except:
            yield line

            
    def user_metrics_ratings_grouped(self, user_id, ratings):
        rating_count = 0
        rating_sum = 0
        user_ratings = []
        for isbn, rating in ratings:
            rating_count += 1
            rating_sum += rating
            user_ratings.append((isbn, rating))
            
        # output the user metrics
        # calculating the average rating vs. giving the count and sum
        user_avg_rating = float(rating_sum) / rating_count if rating_count else 0.0
        yield [user_id, (user_avg_rating, user_ratings)]
        
    def combine_book_pairs(self, user_id, user_avg_ratings):
        """
        Group book pairs and list ratings.
        """
        user_avg_rating, ratings = user_avg_ratings
        for isbn1, isbn2 in combinations(ratings, 2):
            yield [(isbn1[0], isbn2[0]), (user_avg_rating, (isbn1[1], isbn2[1]))]

    def calculate_adjusted_cosine_similarity(self, isbn_pair_key, rating_set):
        """
        Given a list of isbn pairs: .
        """
        # initialize variables for looping through ratings on an isbn
        adj_rating0, adj_rating1, sum_adj_dot_product, sum_adj_rating0, sum_adj_rating1 \
        = (0.0, 0.0, 0.0, 0.0, 0.0)
        count =0
        #countset=copy.deepcopy(rating_set)
        #count = sum(1 for j in countset)
        # # cycle through set of ratings for same two isbns
        for user_avg_rating,ratings in rating_set:        
            adj_rating0 = ratings[0] - user_avg_rating
            adj_rating1 = ratings[1] - user_avg_rating
            sum_adj_dot_product += adj_rating0 * adj_rating1
            sum_adj_rating0 += adj_rating0 * adj_rating0 
            sum_adj_rating1 += adj_rating1 * adj_rating1
            count+=1
    # # calculate adjusted cosine similarity
            denom = (sqrt(sum_adj_rating0)*sqrt(sum_adj_rating1))
            adj_cos_sim = sum_adj_dot_product / denom if denom else 0.0 
            x = float(abs(ratings[0]-ratings[1]))
            y = (float((float(-2)/9))*x)+1.00
            sing_adj_cos_sim = y
           
        # #if (adj_cos_sim<1 and adj_cos_sim >-1 and adj_cos_sim!=0):
        if count==1:
            yield [isbn_pair_key, sing_adj_cos_sim]
        else:
            yield [isbn_pair_key, adj_cos_sim]
        #yield [isbn_pair_key, list(rating_set)]
                
    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        extract_users: <line, record> => <user_id, business_ids>
        set_businesses: <user_id, [business_ids]> => <user_id, businesses>
        aggregate_users: <user_id, businesses> => <"USER", [user_id, [businesses]]>
        user_pair: <"USER", [user_user_businesses]> => <"USER", first, second]> # users to compare
        calculate_jaccard: <first, second> => <jac, first[0], second[0]> # jaccard score and user ids
        """
        return [self.mr(mapper=self.group_by_user_rating, reducer=self.user_metrics_ratings_grouped),
                self.mr(mapper=self.combine_book_pairs, reducer=self.calculate_adjusted_cosine_similarity)]
               # self.mr(mapper=self.calculate_jaccard)]

if __name__ == '__main__':
    BookCollaborativeFiltering.run()