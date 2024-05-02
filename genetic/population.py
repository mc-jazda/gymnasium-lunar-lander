from bot import Bot

class Population:
    def __init__(self, num_surviving = 20, num_new = 80, bots = None):
        self.num_surviving = num_surviving
        self.num_new = num_new
        self.num_bots = num_new + num_surviving

        if bots is None:
            self.bots = [Bot() for _ in range(self.num_bots)]
        else:
            self.bots = bots

    def __str__(self):
        str = ''
        for i in range(self.num_bots):
            str += self.bots[i].__str__() + '\n\n'
        return str

    def crossover(self):
        pass


if __name__ == '__main__':
    population = Population(2, 2)
    print(population)