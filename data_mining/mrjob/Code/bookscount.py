from mrjob.job import MRJob


class BooksCount(MRJob):

    def mapper(self, key, line):
        """
        Mapper: send score from a single movie to
        other movies
        """
        user_id, isbn, rating = line.split(',')
        yield isbn,(user_id, float(rating))

    def reducer(self, book, values):
        #yield(movie, sum(values))
        total = 0
        final = []
        for user_id, rating in values:
            total += 1
            final.append((user_id, rating))

        for user_id, rating in final:
            yield '%s|%s|%.2f|%d' % (user_id, book, rating, total),None

    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        extract_users: <line, record> => <user_id, business_ids>
        set_businesses: <user_id, [business_ids]> => <user_id, businesses>
        aggregate_users: <user_id, businesses> => <"USER", [user_id, [businesses]]>
        user_pair: <"USER", [user_user_businesses]> => <"USER", first, second]> # users to compare
        calculate_jaccard: <first, second> => <jac, first[0], second[0]> # jaccard score and user ids
        """
        return [self.mr(mapper=self.mapper, reducer=self.reducer)]

if __name__ == '__main__':
    BooksCount.run()