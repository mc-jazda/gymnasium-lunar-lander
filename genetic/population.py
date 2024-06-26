from .bot import Bot
import random
import numpy as np

class Population:
    """Population of bots used in genetic algorithm.
    Attributes:
        num_bots: total number of bots in population
        num_surviving: number of bots that live unchanged to the next generation
        num_new: number of new bots generated in every generation
        bots: list of all bots in generation
    """
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
        """Resets sum of rewards for every bot in population. Used when moving to the next generation."""
        for bot in self.bots:
            bot.sum_reward = 0
    
    def get_best_fitness(self):
        """Returns greatest fitness value in the current generation"""
        best_fitness = -10000000.0

        for bot in self.bots:
            fitness = bot.fitness()
            if fitness > best_fitness:
                best_fitness = fitness

        return best_fitness

    def get_worst_fitness(self):
        """Returns smallest fitness value in the current generation"""
        worst_fitness = 1000000.0

        for bot in self.bots:
            fitness = bot.fitness()
            if fitness < worst_fitness:
                worst_fitness = fitness
        
        return worst_fitness
    
    def get_best_bot(self):
        """Returns bot with greatest fitness value in current generation"""
        best_fitness = -10000000.0
        best_bot = None

        for bot in self.bots:
            fitness = bot.fitness()
            if fitness > best_fitness:
                best_fitness = fitness
                best_bot = bot
        
        return best_bot

    def normalize_fitness(self):
        """Normalizes fitness scores in order to conduct roulette selection."""
        worst_fitness = self.get_worst_fitness()
        
        if worst_fitness < 0:
            for bot in self.bots:
                bot.reward(1 - worst_fitness)

    def get_total_score(self):
        """Returns sum of fitness scores of all bots in the current generation."""
        total_score = 0
        for bot in self.bots:
            total_score += bot.fitness()   

        return total_score
    
    def roulette_selection(self):
        """Roulette selection algorithm. Part of genetic algorithm.
        Returns:
            tuple of selected parents
        """
        self.normalize_fitness()
        total_score = self.get_total_score()

        relative_score = [bot.fitness() / total_score for bot in self.bots]
        cumulative_probability = [sum(relative_score[:i+1]) for i in range(len(relative_score))]

        first_parent = None
        second_parent = None
        rand1 = random.random()
        rand2 = random.random()

        for i, cp in enumerate(cumulative_probability):
            if first_parent == None and rand1 <= cp:
                first_parent = self.bots[i]
            if second_parent == None and rand2 <= cp:
                second_parent = self.bots[i]

        return (first_parent, second_parent)

    def crossover(self):
        """Creates new bots out of crossover of two other bots. Part of genetic algorithm."""
        # choose top num_surviving bots
        self.bots = sorted(self.bots, key=lambda bot : bot.fitness(), reverse=True)
        self.bots = self.bots[:self.num_surviving]
        new_generation = self.bots

        # generate new bots
        for i in range(self.num_new):
            # choose parents and cross point
            parents = self.roulette_selection()
            first_parent = parents[0].matrix.flatten()
            second_parent = parents[1].matrix.flatten()
            cross_point = random.randint(1, 32)

            # crossover
            offspring = np.concatenate((first_parent[:cross_point], second_parent[cross_point:]))
            offspring = offspring.reshape((8,4))
            
            new_generation.append(Bot(offspring))
        
        self.bots = new_generation
    
    def mutation(self, probability=0.2):
        """Randomly alters an entry in bots' matrix. Part of genetic algorithm.
        probability: probability of mutation per bot"""
        for bot in self.bots:
            matrix = bot.matrix.flatten()
            
            for i in range(32):
                if random.random() <= probability:
                    val = random.random()
                    matrix[i] += val
            
            matrix = matrix.reshape((8,4))
            bot.matrix = matrix