# QMOO_benchmark_functions

## Description
This package provides the benchmark functions used in the paper
Linus Ekstrom, Hao Wang, Sebastian Schmitt *Variational Quantum Multi-Objective Optimization* [arXiv:2312.14151](https://arxiv.org/abs/2312.14151)

It contains three files:
- `qmoo_benchmark_functions.py` This file contains the actual defintion of the benchmark functions.
- `example_generate_problem_instances.py` This file shows how to use the benchmark problems. 
As an application, it iterates over all problems, various random seeds and several qudit configurations and creates all solution files for each problem instance and stores them in subfolders which it creates.

Each problem function functions take as input the list of qudits and a random seed. 
For each value of the random seed a different problems is generated. 
It returns the matrix and linear coefficients for each objective stored in a list   

A typical code example is

    import qmoo_benchmark_functions as problems
    import functools
    import numpy as np

    qudits = np.asarray([3,3,3,3,3,3,3,3])
    seed = 7

    ## generate the matriices, linea coefficients and offsets for the two objectives of the FM-AFM problem: 
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
    # calculate objectives / cost for given sample: 
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

