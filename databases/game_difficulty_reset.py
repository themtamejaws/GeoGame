#resets the number of plays column (element 6) and average distance column (element 7)

f = open('sorted2.txt', 'r').readlines()
g = open('out.txt', 'w')

for line in f:
	line = line.strip('\n')
	line = line.split('\t')
	line[6] = '1'
	line[7] = '100'
	seq = "\t".join(line[:8])
	g.write(seq)
	g.write('\n')