import numpy as np
from AgentEvaluator import AgentEvaluator
import random
# import evaluter ->
ROWS = 4
COLUMNS = 4
mut_prob = 0.1 # okay so max one per individial
cross_prob = 0
# elitism

class agent():
    def __init__(self, phenotype = None):
        self.size = ROWS*COLUMNS
        self.phenotype = np.random.random(self.size)
        self.fitness = 0
        if phenotype is not None:
            self.phenotype = phenotype

    def __repr__(self) -> str:
        return str(self.phenotype) + " Fitness: " + str(self.fitness)

    def copy(self):
        return agent(self.phenotype)

    def update_fitness(self, fitness):
        self.fitness = fitness

    def get_genotype(self):
        return np.reshape(self.phenotype, (ROWS, COLUMNS))

    def mutate(self):
        idx = np.random.randint(0, self.size - 1)
        self.phenotype[idx] = np.random.random()

    def crossover(self, other):
        child = self.copy()
        idx = np.random.randint(0,self.size - 1)
        if np.random.random() < 0.5:
            child.phenotype[idx:] = other.phenotype[idx:]
        else:
            child.phenotype[:idx] = other.phenotype[:idx]
        return child


class Evolution():
    def __init__(self) -> None:
        # pass in evaluation tool
        self.gen_count = 0
        self.pheno_size = 0
        self.generation_size = 0
        self.population = []
        self.evaluater = AgentEvaluator()
        # self. max_fitness

    def init_population(self, generation_size, pheno_size):
        # is done i guess
        self.pheno_size = pheno_size
        self.generation_size = generation_size
        self.population = [agent() for i in range(self.generation_size)]

    def eval_generation(self):
        for agent in self.population:
            # evaluate agent and update fitness
            agent.update_fitness(self.evaluater.evaluate_agent(agent.get_genotype()))
        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def gen_next_generation(self):
        # do wee keep the fittest
        # do we generate
        # keep 10% percent fittest
        # mutate the remaining population from the best one
        new_gen = [agent.copy() for agent in self.population[:self.generation_size//10]]
        #print('new_gen')
        #print(new_gen)
        for i in range((self.generation_size//10), self.generation_size):
            if np.random.random() < mut_prob: # 0.3
                self.population[i].mutate()
                child = self.population[i]

            elif np.random.random() < cross_prob: # 0.5
                # crossover from the best ones or just at random
                child = self.population[i].crossover(random.sample(self.population,1)[0])
            else:
                child = self.population[i]

            new_gen.append(child)
        self.population = new_gen
        print(self.population[0])

    def train(self, generations):
        for i in range(generations):

            self.gen_next_generation()
            self.eval_generation()
            print(f'size = {len(self.population)}')
            print(f'best fitness =  {self.population[0].fitness}')


evo = Evolution()
evo.init_population(10, 16)
evo.train(10)
