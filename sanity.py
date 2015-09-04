import math

f = open("cities15000.txt", 'r').readlines()
out2 = open("out2.txt", 'w')

counter = 0
for line in f:
	line = line.split('\t')
	fromtop = str(int((90 - float(line[4]))*33.333))
	fromleft = str(int((float(line[5]) + 180)*33.333))
	out2.write(line[0] + "\t" + line[1] + "\t" + fromtop + "\t" + fromleft + "\t" + line[8] + "\t" + line[14] + '\n')
	counter += 1
print counter
