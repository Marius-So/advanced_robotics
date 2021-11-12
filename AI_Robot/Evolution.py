import numpy as np
from agent_evaluation import Rater
# import evaluter ->
ROWS = 4
COLUMNS = 4

class agent():
    def __init__(self):
        size = ROWS*COLUMNS
        self.phenotype = np.random.random(size)
        self.fitness = 0

    def __repr__(self) -> str:
        return str(self.phenotype) + " Fitness: " + str(self.fitness)

    def update_fitness(self, fitness):
        self.fitness = fitness

    def get_genotype(self):
        return np.reshape(self.phenotype, (ROWS, COLUMNS))


class Evolution():
    def __init__(self) -> None:
        # pass in evaluation tool
        self.gen_count = 0
        self.pheno_size = 0
        self.generation_size = 0
        self.population = []
        self.evaluater = Rater()
        # self. max_fitness

    def init_population(self, generation_size, pheno_size):
        self.pheno_size = pheno_size
        self.generation_size = generation_size
        self.population = [agent() for i in range(self.generation_size)]
        print(self.population)

    def eval_generation(self):
        for agent in self.population:
            # evaluate agent
            print(agent.get_genotype())
            temp_fitness = self.evaluater.evaluate_agent(agent.get_genotype())
            agent.update_fitness(temp_fitness)

    def gen_next_generation():
        # do wee keep the fittest
        # do we generate
        pass


evo = Evolution()
evo.init_population(10, 16)
evo.eval_generation()
