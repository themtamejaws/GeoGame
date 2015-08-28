cities = open("sorted.txt", 'r').readlines()

total = 0
newcities = []

for line in cities:
	line = line.split('\t')
	line.append(line.pop().strip("\n"))
	total += int(line[5])
	line.append(str(total))
	newcities.append(line)

out = open("sorted_cum.txt", 'w')

for line in newcities:
	seq = ((str(x) for x in line))
	out.write("\t".join(seq))
	out.write("\n")
