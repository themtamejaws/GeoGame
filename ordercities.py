from operator import itemgetter

cities = open("out3.txt", 'r').readlines()

data = []
for line in cities:
	line = line.split('\t')
	line[5] = int(line[5])
	data.append(line)


#x = sorted(x, key=itemgetter(5))
data.sort(key=lambda data: data[5])
data.reverse()

out = open("sorted.txt", 'w')

for line in data:
	seq = (str(line[0]), str(line[1]), str(line[2]), str(line[3]), str(line[4]), str(line[5]))
	out.write("\t".join(seq))
	out.write("\n")

