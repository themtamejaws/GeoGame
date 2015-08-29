

f = open("out2.txt", 'r').readlines()
g = open("country_codes.txt", 'r').readlines()

countrys = {}

for line in g:
    line = line.split()
    for i in range(3):
        if len(line[2]) != 2:
            line[0:2] = [" ".join(line[0:2])]
            print line
