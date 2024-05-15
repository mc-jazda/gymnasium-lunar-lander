import gymnasium as gym
import keyboard
from gymnasium.utils.seeding import np_random
import random
from .bot import Bot
from .population import Population

def train_bot(num_generations=100, num_surviving=20, num_new=80, mut_prob=0.2, bots=None, seed=0):
    """Train bot to pass lunar lander problem. Training is done using genetic algorithm.
    Parameters:
        num_generations: number of generations used to train bot
        num_surviving: number of bots that live unchanged to the next generation
        num_new: number of new bots generated in every generation
        mut_prob: probability of mutation per bot
        bots: list of bots that will be the first generation. If bots are None they initialized randomly
    Returns:
        bot with the highest fitness function score in the last generation
    """
    env = gym.make("LunarLander-v2")

    rng, seed = np_random(seed)

    population = Population(num_surviving=num_surviving, num_new=num_new, bots=bots)

    for gen in range(num_generations): # number of generations
        seed = int(rng.integers(low=0, high=num_generations))
        observation, info = env.reset(seed=seed)

        for bot in population.bots:
            while True:
                action = bot.action(observation)

                observation, reward, terminated, truncated, info = env.step(action)
                bot.reward(reward)

                if terminated or truncated:
                    observation, info = env.reset()
                    break
        
        print(f'Best fitness score in generation number {gen+1}: {population.get_best_fitness()}')
        population.crossover()
        population.mutation(mut_prob)
        population.reset_rewards()

    env.close()
    return population.get_best_bot()