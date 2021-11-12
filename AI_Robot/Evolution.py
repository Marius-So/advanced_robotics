import numpy as np
# import evaluter ->
ROWS = 3
COLUMNS = 3

class agent():
    def __init__(self, size):
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

        # self. max_fitness

    def init_population(self, generation_size, pheno_size):
        self.pheno_size = pheno_size
        self.generation_size = generation_size
        self.population = [agent for i in range(self.generation_size)]
        print(self.population)

    def eval_generation(self):
        for agent in self.population():
            # evaluate agent
            temp_fitness = evaluate(agent.get_genotype())
            agent.update_fitness(temp_fitness)



a = agent(3)
print(a)
print(a.get_genotype())
