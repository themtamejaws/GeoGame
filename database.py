
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
        fileout = open("sorted2.txt", 'w')
        for entry in self.data:
            population_difficulty =  (22315475 - int(entry.population) ) / 223155
            gameplay_difficulty = 100 - ( 3000 - float(entry.avgdistance) )/ 30
            new_difficulty = (population_difficulty + ( int(entry.numplays) * gameplay_difficulty ) ) / ( int(entry.numplays) + 1)
            entry.difficulty = new_difficulty
            seq = (entry.id, entry.cityname, entry.xcord, entry.ycord, entry.country, entry.population, entry.numplays, entry.avgdist, entry.difficulty)
            seq = "\t".join(seq)
            fileout.write(seq)
            fileout.write("\n")

    def to_string(self, city):
        members = [attr for attr in dir(city) if not callable(attr) and not attr.startswith("__")]
        for entry in members:
            setattr(city, entry, str(getattr(city, entry)))
        print type(city.id)
    

class City(object):

    def __init__(self, data):
        self.id = data[0]
        self.cityname = data[1]
        self.xcord = data[2]
        self.ycord = data[3]
        self.country = data[4]
        self.population = data[5]
        self.numplays = data[6]
        self.avgdist = data[7]
        self.difficulty = data[8]

if __name__ == "__main__":
    b = Database()
    b.to_string(b.data[0])
