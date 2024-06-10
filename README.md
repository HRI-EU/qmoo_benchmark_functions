# QMOO_benchmark_functions

## Description
This package provides the benchmark functions used in the paper
Linus Ekstrom, Hao Wang, Sebastian Schmitt *Variational Quantum Multi-Objective Optimization* [arXiv:2312.14151](https://arxiv.org/abs/2312.14151)

The two main files are:
- `qmoo_benchmark_functions.py` This file contains the actual defintion of the benchmark functions.
- `example_generate_problem_instances.py` This file shows how to use the benchmark problems. 
As an application, it iterates over all problems, various random seeds and several qudit configurations and creates all solution files for each problem instance and stores them in subfolders which it creates.

Each problem function takes as input the list of qudits and a random seed. 
For each value of the random seed a different problem instance is generated. 
It returns the matrix and linear coefficient vector for each objective stored in a list.   

A typical code example is

    import qmoo_benchmark_functions as problems
    import functools
    import numpy as np

    qudits = np.asarray([3,3,3,3,3,3,3,3])
    seed = 7

    ## generate the matrices, linear coefficients and offsets for the two objectives of the FM-AFM problem: 
    cost_coefficients = problems.generate_problem_ferromagnetic_antiferromagnetic_two_objectives(qudits, seed)    

    ## make a first quadratic cost function where the matrix, linear coefficients and offset are given by the first set of entries calculated by the above problem:
    first_objective_partial = functools.partial(
                                                problems.calculate_cost_function_quadratic,
                                                J=cost_coefficients[0][0],
                                                c=cost_coefficients[0][1],
                                                m=cost_coefficients[0][2],
                                            )

    ## make a second quadratic cost function where the matrix, linear coefficients and offset are given by the second set of entries calculated by the above problem:
    second_objective_partial = functools.partial(
                                                problems.calculate_cost_function_quadratic,
                                                J=cost_coefficients[1][0],
                                                c=cost_coefficients[1][1],
                                                m=cost_coefficients[1][2],
                                            )
    # calculate objectives / costs for a given sample: 
    x = np.asarray([1,1,2,1,0,2,1,1])
    obj1 = first_objective_partial(x) ## equals: 4.451314632617248135e-01 
    obj2 = second_objective_partial(x) ## equals: 4.850679296801390095e-01


## Installation
Just copy the file `qmoo_benchmark_functions.py` to where you want to use the functions or include the appropriate path into PYTHONPATH variable.

## Authors and acknowledgment
Sebastian Schmitt (HRI-EU) and Linus Ekstrom (HRI-EU) 

## Terms of usage
Please cite the original work when using these functions: 
    Linus Ekstrom, Hao Wang, Sebastian Schmitt *Variational Quantum Multi-Objective Optimization* [arXiv:2312.14151](https://arxiv.org/abs/2312.14151)

## License
The project is licensed under the [BSD-3-Clause License](LICENSE.md).

 ## Acknowledgements 
 The authors acknowledge funding from the European Union under Horizon Europe Programme, Grant Agreement 101080086 -- [NeQST](https://neqst-he.eu/). Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Commission. Neither the European Union nor the granting authority can be held responsible for them.

<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cda-tum/mqt-qudits/main/docs/_static/eu_funded_dark.svg" width="25%">
<img src="https://raw.githubusercontent.com/cda-tum/mqt-qudits/main/docs/_static/eu_funded_light.svg" width="25%" alt="Funded by the European Union">
</picture>
