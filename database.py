import random
class Database(object):

    def __init__(self):

        self.data = self.load_file()


    def load_file(self):
        opened_file = open('sorted2.txt', 'r').readlines()
        data = []
        for line in opened_file:
            line = [x.strip() for x in line.split("\t")]
            city = City(line)
            data.append(city)
        return data

    def close(self):
        fileout = open("sorted3.txt", 'w')
        for entry in self.data:
            population_difficulty =  (22315475 - int(entry.population) ) / 223155
            gameplay_difficulty = 100 - ( 3000 - float(entry.avgdist) )/ 30
            new_difficulty = (population_difficulty + ( int(entry.numplays) * gameplay_difficulty ) ) / ( int(entry.numplays) + 1)
            entry.difficulty = new_difficulty
            entry.to_string()
            seq = (entry.id, entry.cityname, entry.xcord, entry.ycord, entry.country, entry.population, entry.numplays, entry.avgdist, entry.difficulty)
            seq = "\t".join(seq)
            fileout.write(seq)
            fileout.write("\n")

    def choose_city(self, asked_index, difficulty):
        citylength  = len(self.data)
        self.number = citylength + 1
        while self.number > citylength:
            while self.number in asked_index:
                self.number = abs(int(random.gauss(difficulty,50)))
        asked_index.append(self.number)
        return self.data[self.number], asked_index
    

class City(object):

    def __init__(self, data):
        self.id = data[0]
        self.cityname = data[1]
        self.ycord = data[2]
        self.xcord = data[3]
        self.country = data[4]
        self.population = data[5]
        self.numplays = data[6]
        self.avgdist = data[7]
        self.difficulty = data[8]

    def update_difficulty(self, dist):
        self.avgdist = (float(self.avgdist)*float(self.numplays) + dist) / (float(self.numplays) + 1)
        self.numplays = int(self.numplays)+1

    def to_string(self):
        members = [attr for attr in dir(self) if not callable(attr) and not attr.startswith("__")]
        for entry in members:
            setattr(self, entry, str(getattr(self, entry)))

if __name__ == "__main__":
    b = Database()
    
