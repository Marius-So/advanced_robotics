import numpy as np

class agent():
    def __init__(self, size):
        self.phenotype = np.random.random(size)
        self.fitness = 0

    def __repr__(self) -> str:
        return str(self.phenotype) + " Fitness: " + str(self.fitness)

    def update_fitness(self, fitness):
        self.fitness = fitness

class Evolution():
    def __init__(self) -> None:
        self.gen_count = 0
        self.pheno_size = 0
        self.generation_size = 0
        self.population = []

    def init_population(self, generation_size, pheno_size):
        self.pheno_size = pheno_size
        self.generation_size = generation_size
        self.population = [agent for i in range(self.generation_size)]
        print(self.population)

    def eval_generation(self):
        for fitness, agent in self.population:



evo = Evolution()
evo.init_population(5, 5)
