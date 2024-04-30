import numpy as np

class Bot:
    def __init__(self, matrix = np.random.random([8,4])):
        self.matrix = matrix
    
    def __str__(self):
        print(self.matrix)
    
    def action(self, observation):
        """Returns bot's choosen action."""
        results = np.matmul(observation, self.matrix)
        return np.argmax(results)

    def reward(self, reward):
        """Rewards bot acording to his action."""
        self.sum_reward += reward
    
    def performance(self):
        """Returns evaluated performance - sum of all rewards."""
        return self.sum_reward