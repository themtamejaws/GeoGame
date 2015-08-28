f = open("codes.txt", 'r').readlines()

data = {}

for line in f:
    line = line.split()
    line = line[0:-3]
    line[0:-1] = [" ".join(line[0:-1])]
    data[line[1]] = line[0]
    print line

print data['RS']

g = open("out2.txt", 'r').readlines()
h = open("out3.txt", 'w')

for line in g:
    line = line.split('\t')
    #print line
    line[4] = data[line[4]]
    seq = "\t".join(line[:])
    h.write(seq)
