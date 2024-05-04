from .bot import Bot
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

    def reset_rewards(self):
        for bot in self.bots:
            bot.sum_reward = 0
    
    def get_best_fitness(self):
        best_fitness = -10000000.0

        for bot in self.bots:
            fitness = bot.fitness()
            if fitness > best_fitness:
                best_fitness = fitness

        return best_fitness

    def crossover(self):
        # choose top num_surviving bots
        self.bots = sorted(self.bots, key=lambda bot : bot.fitness(), reverse=True)
        self.bots = self.bots[:self.num_surviving]
        new_generation = self.bots

        # generate new bots
        for i in range(self.num_new):
            # choose parents and cross point
            first_parent = random.choice(self.bots).matrix.flatten()
            second_parent = random.choice(self.bots).matrix.flatten()
            cross_point = random.randint(1, 32)

            # crossover
            offspring = np.concatenate((first_parent[:cross_point], second_parent[cross_point:]))
            offspring = offspring.reshape((8,4))
            
            new_generation.append(Bot(offspring))
    
    def mutation(self, probability=0.2):
        for bot in self.bots:
            matrix = bot.matrix.flatten()
            
            for i in range(32):
                if random.random() <= probability:
                    val = random.random()
                    matrix[i] += val
            
            matrix = matrix.reshape((8,4))
            bot.matrix = matrix



if __name__ == '__main__':
    pop = Population(num_surviving=1, num_new=1)
    print(pop)
    print('\n-------------------------------------------------------')
    pop.mutation(0.5)
    print(pop)