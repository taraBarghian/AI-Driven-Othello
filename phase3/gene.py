import random
import numpy as np

class Gene:
    bound=50
    def __init__(self, vec=None):
        self.vector = vec
        self.score=0

    def recombine(self, g2):
        temp_vec = [9999]  # a move that results a player losing all pieces
        for i in range(1, 7):
            temp = []
            for j in range(0, 5):
                temp.append((self.vector[i][j] + g2.vector[i][j]) / 2)
            temp_vec.append(temp)
        return temp_vec

    def mutate(self):
        noise = np.random.normal(0, 10, 30)
        k = 0
        for i in range(1, 7):
            for j in range(0, 5):
                self.vector[i][j] += noise[k]
                self.vector[i][j]=round(self.vector[i][j],3)
                k += 1


    def random_gene(self):
        temp_vec = [9999]  # a move that results a player losing all pieces
        for i in range(1, 7):
            temp = []
            for j in range(0, 5):
                temp.append(random.randint(-Gene.bound, Gene.bound))
            temp_vec.append(temp)
        self.vector = temp_vec
