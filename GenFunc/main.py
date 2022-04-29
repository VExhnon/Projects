import random
from copy import deepcopy
from function import *
import time

class DNA:
    def __init__(self, limits: list) -> None:
        self.limits = limits
        self.chromosome = self.generateRandomChromosome()
        self.fitness = 0
    
    def generateRandomChromosome(self) -> list:
        chromosome = []
        for i in range(2):
            chromosome.append(self.generateRandomGene())
        return chromosome
    
    def generateRandomGene(self) -> float:
        return random.uniform(self.limits[0], self.limits[1])

def generateInitialPopulation(POPULATION_SIZE: int, limits: list) -> list:
    population = []
    for i in range(POPULATION_SIZE):
        population.append(DNA(limits))
    return population

def selection(population: list, type: str) -> list:
    k = 20
    parent1 = population[random.randint(0, len(population)-1)]
    for i in range(k):
        temp = random.randint(0, len(population)-1)
        if(type=="min"):
            if (population[temp].fitness < parent1.fitness):
                parent1 = population[temp]
        else:
            if (population[temp].fitness > parent1.fitness):
                parent1 = population[temp]

    parent2 = population[random.randint(0, len(population)-1)]
    for i in range(k):
        temp = random.randint(0, len(population)-1)
        if(type=="min"):
            if (population[temp].fitness < parent2.fitness):
                parent2 = population[temp]
        else:
            if (population[temp].fitness > parent2.fitness):
                parent2 = population[temp]
    return [parent1, parent2]

def crossover(parent1: DNA, parent2: DNA) -> list:
    child1 = DNA(parent1.limits)
    child2 = DNA(parent1.limits)
    crossoverPoint = random.randint(0, len(parent1.chromosome))
    child1.chromosome = parent1.chromosome[:crossoverPoint] + parent2.chromosome[crossoverPoint:]
    child2.chromosome = parent2.chromosome[:crossoverPoint] + parent1.chromosome[crossoverPoint:]
    return [child1, child2]

def mutation(child: DNA, MUTATION_RATE: float) -> None:
    for i in range(len(child.chromosome)):
        if (random.random()<MUTATION_RATE):
            child.chromosome[i] = child.chromosome[i] + random.uniform(child.limits[0], child.limits[1])
            if(child.chromosome[i]<child.limits[0]):
                child.chromosome[i] = child.limits[0]
            if(child.chromosome[i]>child.limits[1]):
                child.chromosome[i] = child.limits[1]

def generateNewPopulation(population: list, MUTATION_RATE: float, type: str) -> list:
    newPopulation = []
    for i in range(len(population)//2):
        parent1, parent2 = selection(population, type)
        child1, child2 = crossover(parent1, parent2)
        mutation(child1, MUTATION_RATE)
        mutation(child2, MUTATION_RATE)
        newPopulation.append(child1)
        newPopulation.append(child2)
    return newPopulation

def fitness(individual, choice):
    if(choice==1):
        individual.fitness = easom(individual.chromosome)
    elif(choice==2):
        individual.fitness = styblinski(individual.chromosome)
    else:
        individual.fitness = crossInTray(individual.chromosome)


def runGenetic(POPULATION_SIZE: int, MAX_GENERATIONS: int, MUTATION_RATE: float, limits: list, choice: int, type: str):
    population = generateInitialPopulation(POPULATION_SIZE, limits)
    bestIndividual = population[0]
    print("Generation\t\tBest Fitness\t\t\t\tAverage Fitness")
    for i in range(0, MAX_GENERATIONS):
        averageFitness = 0
        for individual in population:
            fitness(individual, choice)
            averageFitness += individual.fitness
        averageFitness /= POPULATION_SIZE
        for individual in population:
            if(type=="min"):
                if(individual.fitness < bestIndividual.fitness):
                    bestIndividual = deepcopy(individual)
            else:
                if(individual.fitness > bestIndividual.fitness):
                    bestIndividual = deepcopy(individual)
        print(f"\t{i}\t\t\t{bestIndividual.fitness}\t\t\t{averageFitness}")
        population = generateNewPopulation(population, MUTATION_RATE, type)





# def plotResults(averageYPlot, bestYPlot, MAX_GENERATIONS):
#     X = [*range(MAX_GENERATIONS)]
#     figure, axis = plt.subplots(1, 2)
    
#     axis[0].plot(X, bestYPlot)
#     axis[1].plot(X, averageYPlot)

#     axis[0].legend(["Best Fitness Plot"])
#     axis[1].legend(["Average Fitness Plot"])

#     axis[0].set_xlabel("Generation")
#     axis[0].set_ylabel("Fitness")
#     axis[1].set_xlabel("Generation")
#     plt.tight_layout()
#     plt.show()

if __name__ == '__main__':
    POPULATION_SIZE = 100
    MAX_GENERATIONS = 100
    MUTATION_RATE = 0.05
    limits = []
    choice = int(input())
    type = int(input())
    if(type==1):
        type = "min"
    else:
        type = "max"
    if(choice==1):
        limits = [-100, 100]
    elif(choice==2):
        limits = [-5, 5]
    else:
        limits = [-10, 10]
    start_time = time.time()
    runGenetic(POPULATION_SIZE, MAX_GENERATIONS, MUTATION_RATE, limits, choice, type)
    print("--- %s seconds ---" % (time.time() - start_time))