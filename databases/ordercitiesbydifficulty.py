from operator import itemgetter

cities = open("sorted2.txt", 'r').readlines()

data = []
for line in cities:
	line = line.strip('\n')
	line = line.split('\t')
	line[8] = (float(line[8]))
	data.append(line)


#x = sorted(x, key=itemgetter(5))
data.sort(key=lambda data: data[8])

out = open("sorted_by_diff.txt", 'w')

for line in data:
	
	print seq
	out.write("\t".join(line[:]))
	out.write("\n")

