import numpy as np
import json

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

    def save_to_json(self, filename):
        """Saves bot's matrix to json. Used after training to save best bot."""
        mat = self.matrix.tolist()

        with open(filename, 'w') as file:
            json.dump(mat, file)
    
    def load_from_json(self, filename):
        """Initializes bot with matrix from a json file."""
        with open(filename, 'r') as file:
            mat = json.load(file)
        
        self.matrix = np.array(mat)