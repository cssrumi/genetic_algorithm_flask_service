import random
# import sys
# import os
# sys.path.append(os.path.abspath("."))
# sys.path.append(os.path.abspath("../"))
import data_cy

from data.data_mapper import DataMapper

cdef class CyGenotype(data_cy.CyData):
    gen_list = list(DataMapper.get_default_mapping().keys())
    gen_len = len(gen_list)
    mid_gen = int(gen_len / 2)

    @staticmethod
    def get_random_genotype():
        cdef int _from = -1
        cdef int _to = 1
        return CyGenotype(
            *[random.uniform(_from, _to) for _ in CyGenotype.gen_list]
        )


class Genotype(CyGenotype):
    pass
