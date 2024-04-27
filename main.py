import gymnasium as gym
import keyboard
from gymnasium.utils.seeding import np_random

env = gym.make("LunarLander-v2", render_mode="human")

rng, seed = np_random(0)
print(seed)

observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

    if keyboard.is_pressed('q'):
        break

env.close()