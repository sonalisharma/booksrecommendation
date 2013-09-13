import sys
from booksim import BooksSimilarities

#example of how to use arguments for map reduce and select the number of instances
#cos_job2 = BookCollaborativeFiltering(args=['BX-Book-Ratings-1000.csv', '--num-ec2-instances', '5', '-r', 'emr'])
cos_job = BooksSimilarities(args=['/Users/sonali/Documents/Ischool/INFODMA/Project/Data/20to30tmp.csv'])

with cos_job.make_runner() as runner:
    runner.run()
    #print 'START NEW RUN******************************'
    for line in runner.stream_output():
        key, value = cos_job.parse_output_line(line)
        print ''.join(key).encode('utf-8').strip(), value