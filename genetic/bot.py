import numpy as np

class Bot:
    """Enviroment's actor.
    Attributes:
        matrix: decision matrix, that defines actor
        sum_reward: sum of all rewards gained by actor"""
    def __init__(self, matrix = None):
        if matrix is None:
            matrix = np.random.random([8,4])

        self.matrix = matrix
        self.sum_reward = 0
    
    def __str__(self):
        return str(self.matrix)
    
    def action(self, observation):
        """Returns bot's choosen action."""
        results = np.matmul(observation, self.matrix)
        return np.argmax(results)

    def reward(self, reward):
        """Rewards bot acording to his action."""
        self.sum_reward += reward
    
    def fitness(self):
        """Returns evaluated performance - sum of all rewards."""
        return self.sum_reward