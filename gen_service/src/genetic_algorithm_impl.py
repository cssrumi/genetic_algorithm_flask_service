from math import fabs

from gen_service.src.phenotype import Phenotype
from gen_service.src.signs import signs_dict


class GeneticAlgorithmImpl:
    def __init__(self, test_cases, population_size=100, max_generation=100):
        self.test_cases = test_cases.get_tests()
        self.population_size = population_size
        self.max_generation = max_generation
        self.population = []
        self.bests = []
        self.populate()
        self.one_tenth = int(population_size / 10)

    def run(self):
        for i in range(self.max_generation):
            self.evolve_population()

    def get_best(self):
        return self.bests[0]

    def populate(self):
        for _ in range(self.population_size):
            self.population.append(Phenotype())

    # @timer
    def evolve_population(self):
        self.calculate_scores()
        self.set_bests()
        self.population = [self.get_best()]
        for mother in self.bests:
            for father in self.bests:
                self.population.append(mother.crossover(father))

    def set_bests(self):
        self.population.sort(key=lambda a: a.score, reverse=False)
        self.bests = self.population[:self.one_tenth]

    # @timer
    def calculate_scores(self):
        sd = signs_dict
        for p in self.population:
            _final_score = 0
            test_type = p.genes.get('test_type')
            a = test_type.get('a')
            b = test_type.get('b')
            c = test_type.get('c')
            a_1 = p.genes.get('a_1')
            b_1 = p.genes.get('b_1')
            c_1 = p.genes.get('c_1')
            a_b = p.genes.get('a_b')
            sd_a_b = sd.get(a_b)
            sd_b_c = sd.get(p.genes.get('b_c'))
            for case in self.test_cases:
                if a_b not in ('sub', 'add'):
                    score = sd_a_b(
                        case.get(a) * a_1,
                        case.get(b) * b_1
                    )
                    score = sd_b_c(
                        score,
                        case.get(c) * c_1
                    )
                else:
                    score = sd_b_c(
                        case.get(b) * b_1,
                        case.get(c) * c_1
                    )
                    score = sd_a_b(
                        case.get(a) * a_1,
                        score
                    )
                score = fabs(case.get(test_type.get('res')) - score)
                _final_score += score
            p.score = _final_score
