import os

from distutils.core import setup
from setuptools import find_packages, Extension
from Cython.Distutils import build_ext

cython_directives = {"profile": True, "language_level": "3"}
ext_options = {"compiler_directives": cython_directives, "annotate": True}

genetic_algorithm_dir = 'genetic_algorithm'
phenotype_file = 'phenotype_cy.pyx'
genotype_file = 'genotype_cy.pyx'
# data_dir = 'genetic_algorithm.data'
data_dir = genetic_algorithm_dir
data_file = 'data_cy.pyx'

files = [
    (data_dir, data_file),
    # (genetic_algorithm_dir, genotype_file),
    (genetic_algorithm_dir, phenotype_file),
]

ext_modules = [
    Extension(f'{data_dir}.{data_file.replace(".pyx", "")}',
              [f'{os.path.join(data_dir, data_file)}']),
    Extension(f'{genetic_algorithm_dir}.{genotype_file.replace(".pyx", "")}',
              [f'{os.path.join(genetic_algorithm_dir, genotype_file)}']),
    Extension(f'{genetic_algorithm_dir}.{phenotype_file.replace(".pyx", "")}',
              [f'{os.path.join(genetic_algorithm_dir, phenotype_file)}']),
]

for e in ext_modules:
    e.cython_directives = cython_directives

files = {os.path.join(_dir, file) for _dir, file in files}
print(files)

setup(
    # name='app',
    packages=find_packages(),
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    include_dirs=['.', ],
)

# setup(
#     ext_modules=cythonize(files, **ext_options),
#     # ext_modules=cythonize(phenotype, **ext_options),
#     # include_dirs=[genetic_algorithm.data.get_include()]
# )
