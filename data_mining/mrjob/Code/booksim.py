#-*-coding: utf-8 -*-
from mrjob.job import MRJob
from math import sqrt
from itertools import combinations



def jaccard(users_in_common, total_users1, total_users2):
    '''
    The Jaccard Similarity between 2 two vectors
    |Intersection(A, B)| / |Union(A, B)|
    '''
    union = total_users1 + total_users2 - users_in_common

    return (users_in_common / (float(union))) if union else 0.0

class BooksSimilarities(MRJob):

    def steps(self):
        return [self.mr(self.group_by_user_rating,
                         self.count_ratings_users_freq),
                self.mr(self.pairwise_items, self.calculate_similarity)]#,
                #self.mr(self.calculate_ranking, self.top_similar_items)
                #]

    def group_by_user_rating(self, key, line):

        user_id, item_id, rating, ratings_count = line.split('|')
        ratings_count , dump = ratings_count.split(" ")
        yield  user_id, (item_id, float(rating), ratings_count)

    def count_ratings_users_freq(self, user_id, values):
        item_count = 0
        item_sum = 0
        final = []
        for item_id, rating, ratings_count in values:
            item_count += 1
            item_sum += rating
            final.append((item_id, rating, ratings_count))

        yield user_id, (item_count, item_sum, final)

    def pairwise_items(self, user_id, values):
        item_count, item_sum, ratings = values
        for item1, item2 in combinations(ratings, 2):
            yield (item1[0], item2[0]), \
                    (item1[1], item2[1], item1[2], item2[2])

    def calculate_similarity(self, pair_key, lines):
        sum_xx, sum_xy, sum_yy, sum_x, sum_y, n = (0.0, 0.0, 0.0, 0.0, 0.0, 0)
        n_x, n_y = 0, 0
        item_pair, co_ratings = pair_key, lines
        item_xname, item_yname = item_pair
        for item_x, item_y, nx_count, ny_count in lines:
            sum_xx += item_x * item_x
            sum_yy += item_y * item_y
            sum_xy += item_x * item_y
            sum_y += item_y
            sum_x += item_x
            n += 1
            n_x = int(ny_count)
            n_y = int(nx_count)

        jaccard_sim = jaccard(n, n_x, n_y)

        yield (item_xname,"_",item_yname),  jaccard_sim, n)

    def calculate_ranking(self, item_keys, values):
        jaccard_sim, n = values
        item_x, item_y = item_keys
        if int(n) > 0:
            yield (item_x, jaccard_sim), (item_y, n)

    def top_similar_items(self, key_sim, similar_ns):
        item_x, jaccard_sim = key_sim
        for item_y, n in similar_ns:
            yield '%s;%s;%f;%d' % (item_x, item_y,jaccard_sim, n), None

if __name__ == '__main__':
    BooksSimilarities.run()