import gymnasium as gym
import keyboard
from gymnasium.utils.seeding import np_random
import random
from genetic.bot import Bot
from genetic.population import Population



env = gym.make("LunarLander-v2", render_mode='human')
#env = gym.make("LunarLander-v2")

population = Population()
for _ in range(100):
    for bot in population.bots:
        rng, seed = np_random(0)
        observation, info = env.reset(seed=seed)

        while True:
            action = bot.action(observation)

            observation, reward, terminated, truncated, info = env.step(action)
            bot.reward(reward)

            if terminated or truncated:
                seed = int(rng.integers(low=0, high=1000))
                observation, info = env.reset(seed=seed)
                break

            if keyboard.is_pressed('q'):
                exit(0)

    population.crossover()
    population.mutation(0.3)
    print(population.get_best_fitness())
    population.reset_rewards()

env.close()