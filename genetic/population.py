from bot import Bot
import random
import numpy as np

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
        # choose top num_surviving bots
        self.bots = sorted(self.bots, key=lambda bot : bot.fitness(), reverse=True)
        self.bots = self.bots[:self.num_surviving]
        new_generation = self.bots

        # generate new bots
        for i in range(self.num_new):
            first_parent = random.choice(self.bots).matrix.flatten()
            second_parent = random.choice(self.bots).matrix.flatten()
            cross_point = random.randint(1, 32)
            print(cross_point)

            # crossover
            offspring = np.concatenate((first_parent[:cross_point], second_parent[cross_point:]))
            offspring = offspring.reshape((8,4))
            
            new_generation.append(Bot(offspring))


if __name__ == '__main__':
    pop = Population(num_surviving=2, num_new=2)
    print(pop)
    print('\n-------------------------------------------------------')
    pop.crossover()
    print(pop)