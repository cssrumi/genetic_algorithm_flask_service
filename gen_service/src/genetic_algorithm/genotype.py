import random

from data.data import Data
from data.data_mapper import DataMapper


class Genotype(Data):

    gen_list = list(DataMapper.get_default_mapping().keys())
    gen_len = len(gen_list)
    mid_gen = int(gen_len / 2)

    @staticmethod
    def get_random_genotype(_from=-1, _to=1):
        return Genotype(
            *[random.uniform(_from, _to) for _ in Genotype.gen_list]
        )
