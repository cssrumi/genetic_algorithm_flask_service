from genetic_algorithm.individual import Individual


def class_test():
    Individual.set_gen_list(['a', 'b', 'c'])
    i1 = Individual()
    i2 = Individual()
    assert Individual._max_vitality == i1._max_vitality
    Individual.set_max_vitality(2)
    assert Individual._max_vitality == 2
    i2.set_max_vitality(3)
    assert Individual._max_vitality == i2._max_vitality
    assert i2.genotype != i1.genotype

    print(Individual._gen_list)
    i3 = i1.crossover(i2)
    print(i3.genotype)
    print(Individual._gen_list)
    print(Individual._gen_len)
    Individual.set_gen_list([])
    print(Individual._gen_len)

if __name__ == '__main__':
    class_test()

