import sys
from bookCollaborativeFiltering import BookCollaborativeFiltering

#example of how to use arguments for map reduce and select the number of instances
#cos_job2 = BookCollaborativeFiltering(args=['BX-Book-Ratings-1000.csv', '--num-ec2-instances', '5', '-r', 'emr'])
cos_job = BookCollaborativeFiltering(args=['../Data/NONUSA_60to71.csv'])

with cos_job.make_runner() as runner:
    runner.run()
    #print 'START NEW RUN******************************'
    for line in runner.stream_output():
        key, value = cos_job.parse_output_line(line)
        print '_'.join(key).encode('utf-8').strip(), value