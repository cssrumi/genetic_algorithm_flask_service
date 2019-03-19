import os

from genetic_algorithm_impl import GeneticAlgorithmImpl
from results import Results
from test_cases import TestCases


# @timer
def main():
    mongo_ip = os.getenv('MONGO_IP', 'localhost')
    mongo_port = os.getenv('MONGO_PORT', '27017')
    mongo_user = os.getenv('MONGO_USER', 'root')
    mongo_password = os.getenv('MONGO_PASSWORD', 'example')
    population_size = int(os.getenv('POPULATION_SIZE', '100'))
    max_generation = int(os.getenv('MAX_GENERATION', '10'))

    t = TestCases(
        ip=mongo_ip,
        port=mongo_port,
        user=mongo_user,
        password=mongo_password
    )
    r = Results(
        ip=mongo_ip,
        port=mongo_port,
        user=mongo_user,
        password=mongo_password
    )

    t.load()
    r.load()

    while True:
        print('loading test cases...')
        t.set_test_cases(
            how_many=TestCases.HOW_MANY.LAST_5,
        )
        g = GeneticAlgorithmImpl(
            test_cases=t,
            population_size=population_size,
            max_generation=max_generation
        )
        g.run()
        best = g.get_best()
        print('saving...')
        r.save(best)


if __name__ == '__main__':
    main()
