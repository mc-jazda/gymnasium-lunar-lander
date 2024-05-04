import gymnasium as gym
import keyboard
from gymnasium.utils.seeding import np_random
import random
from .bot import Bot
from .population import Population



def train_bot(num_generations=100):
    env = gym.make("LunarLander-v2")

    rng, seed = np_random(0)

    population = Population()

    for gen in range(num_generations): # number of generations
        seed = int(rng.integers(low=0, high=num_generations))
        observation, info = env.reset(seed=seed)

        for bot in population.bots:
            while True:
                action = bot.action(observation)

                observation, reward, terminated, truncated, info = env.step(action)
                bot.reward(reward)

                if terminated or truncated:
                    observation, info = env.reset(seed=seed)
                    break

        population.crossover()
        population.mutation(0.3)
        print(f'Best fitness score in generation number {gen+1}: {population.get_best_fitness()}')
        population.reset_rewards()

    env.close()
    return population.get_best_bot()