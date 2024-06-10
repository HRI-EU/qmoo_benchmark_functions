# -*- coding: utf-8 -*-
#
# Copyright (C)
# Honda Research Institute Europe GmbH
# Carl-Legien-Str. 30
# 63073 Offenbach/Main
# Germany
#
# UNPUBLISHED PROPRIETARY MATERIAL.
# ALL RIGHTS RESERVED.
#
# Sebastian Schmitt, 2024


import numpy as np
import sys
import os
import functools
import qmoo_benchmark_functions as prob

def calc_all_states(cost:list, quditst:np.array):
    """
    full enumeration for classical solutions 
    """
    hilbert_space_dimensiont = np.prod(quditst)
    numObjs = len(cost)
    numParams = len(quditst)
    all_energies = np.zeros((hilbert_space_dimensiont, numParams + numObjs))

    dim_tuple = tuple( i for i in quditst)

    for i1 in range(hilbert_space_dimensiont): # loops through all entries of the state vector
        tconfig = np.array(list(np.unravel_index(i1, dim_tuple)),dtype=int) # get corresponding config for each state vector 
        all_energies[i1,0:numParams] = tconfig
        all_energies[i1,numParams:numParams+numObjs] = np.asarray([ ob(tconfig) for ob in cost]) 
    return all_energies




## all problem names:
problem_names = [
    'problem_linear_corr-0.5',
    'problem_FM_AFM_two_objs',
    'problem_quadratic_AFM_two_objs',
    'problem_FM_AFM_three_objs',
    'problem_quadratic_five_objs',
]

## qudit configurations to consider:
qudits_list =[
    np.asarray( [2]*12),
    np.asarray( [2]*13),
    np.asarray( [2]*14),
    #np.asarray( [2]*15),
    np.asarray( [3]*8), 
    np.asarray( [4]*6),
    np.asarray( [5]*5),
    np.asarray( [7]*4),
    ]

# for each problem and configuration, one problem-instance for each random seed is generated
for seed in range(20):
    for problem_name in problem_names:
        for qudits in qudits_list:
            print(f'seed{seed}, {problem_name} qudits: {qudits}')
            if problem_name == 'problem_linear_corr-0.5':
                cost_coefficients = prob.generate_problem_linear_corr05(qudits, seed)
                #print(f'{problem_name}: coefficients length {len(cost_coefficients)}, arrays: {cost_coefficients}')
                
                first_objective_partial = functools.partial(
                    prob.calculate_cost_function_linear,
                    c=cost_coefficients[0][0],
                    m=cost_coefficients[0][1],
                )
                second_objective_partial = functools.partial(
                    prob.calculate_cost_function_linear,
                    c=cost_coefficients[1][0],
                    m=cost_coefficients[1][1],
                )
                objective_functions = [first_objective_partial, second_objective_partial]

            elif problem_name == 'problem_FM_AFM_two_objs':
                cost_coefficients = prob.generate_problem_ferromagnetic_antiferromagnetic_two_objectives(qudits, seed)    
                #print(f'{problem_name}: coefficients length {len(cost_coefficients)}, arrays: {cost_coefficients}')

                
                first_objective_partial = functools.partial(
                    prob.calculate_cost_function_quadratic,
                    J=cost_coefficients[0][0],
                    c=cost_coefficients[0][1],
                    m=cost_coefficients[0][2],
                )
                second_objective_partial = functools.partial(
                    prob.calculate_cost_function_quadratic,
                    J=cost_coefficients[1][0],
                    c=cost_coefficients[1][1],
                    m=cost_coefficients[1][2],
                )
                objective_functions = [first_objective_partial, second_objective_partial]

            elif problem_name == 'problem_quadratic_AFM_two_objs':
                cost_coefficients = prob.generate_problem_quadratic_antiferromagnetic_two_objectives(qudits, seed)    
                #print(f'{problem_name}: coefficients length {len(cost_coefficients)}, arrays: {cost_coefficients}')
                
                first_objective_partial = functools.partial(
                    prob.calculate_cost_function_quadratic,
                    J=cost_coefficients[0][0],
                    c=cost_coefficients[0][1],
                    m=cost_coefficients[0][2],
                )
                second_objective_partial = functools.partial(
                    prob.calculate_cost_function_quadratic,
                    J=cost_coefficients[1][0],
                    c=cost_coefficients[1][1],
                    m=cost_coefficients[1][2],
                )
                objective_functions = [first_objective_partial, second_objective_partial]


            elif problem_name == 'problem_FM_AFM_three_objs':

                cost_coefficients = prob.generate_problem_ferromagnetic_antiferromagnetic_three_objectives(qudits, seed)
                #print(f'{problem_name}: coefficients length {len(cost_coefficients)}, arrays: {cost_coefficients}')

                
                first_objective_partial = functools.partial(
                    prob.calculate_cost_function_quadratic,
                    J=cost_coefficients[0][0],
                    c=cost_coefficients[0][1],
                    m=cost_coefficients[0][2],
                )
                second_objective_partial = functools.partial(
                    prob.calculate_cost_function_quadratic,
                    J=cost_coefficients[1][0],
                    c=cost_coefficients[1][1],
                    m=cost_coefficients[1][2],
                )
                third_objective_partial = functools.partial(
                    prob.calculate_cost_function_quadratic,
                    J=cost_coefficients[2][0],
                    c=cost_coefficients[2][1],
                    m=cost_coefficients[2][2],
                )
                objective_functions = [first_objective_partial, second_objective_partial, third_objective_partial]

            
            elif problem_name == 'problem_quadratic_five_objs':
                cost_coefficients = prob.generate_problem_quadratic_five_objectives(qudits, seed)
                #print(f'{problem_name}: coefficients length {len(cost_coefficients)}, arrays: {cost_coefficients}')


                first_objective_partial = functools.partial(
                    prob.calculate_cost_function_quadratic,
                    J=cost_coefficients[0][0],
                    c=cost_coefficients[0][1],
                    m=cost_coefficients[0][2],
                )
                second_objective_partial = functools.partial(
                    prob.calculate_cost_function_quadratic,
                    J=cost_coefficients[1][0],
                    c=cost_coefficients[1][1],
                    m=cost_coefficients[1][2],
                )
                third_objective_partial = functools.partial(
                    prob.calculate_cost_function_quadratic,
                    J=cost_coefficients[2][0],
                    c=cost_coefficients[2][1],
                    m=cost_coefficients[2][2],
                )
                fourth_objective_partial = functools.partial(
                    prob.calculate_cost_function_quadratic,
                    J=cost_coefficients[3][0],
                    c=cost_coefficients[3][1],
                    m=cost_coefficients[3][2],
                )
                fifth_objective_partial = functools.partial(
                    prob.calculate_cost_function_quadratic,
                    J=cost_coefficients[4][0],
                    c=cost_coefficients[4][1],
                    m=cost_coefficients[4][2],                )

                objective_functions = [first_objective_partial, second_objective_partial, third_objective_partial,fourth_objective_partial, fifth_objective_partial]

            #################################################################
            else:
                print(f'problem {problem_name}  not defined')
                sys.exit()


            reference_point = prob.get_reference_point_for_qudit_config_and_problem_name(problem_name)
            #print(reference_point)

            hilbert_space_dimension = np.prod(qudits)
            qudits_str = "_".join(str(qq) for qq in qudits)
            numParams = len(qudits)
            numObjs = len(objective_functions)


            odir = f'setup_data'+os.sep+f'{problem_name}_normalized_{qudits_str}'
            os.makedirs(odir, exist_ok=True)
            pofn = odir+os.sep+f"{problem_name}_qudits_{qudits_str}_seed{seed}_all_energies.dat"
        
            all_e = calc_all_states( objective_functions, qudits )

            hdr=" ".join(f"q{i}" for i in range(numParams) )+' '+' '.join(f"obj{i}" for i in range(numObjs))
            np.savetxt(pofn, all_e, header = hdr)


            ## if you would like to get the Pareto frontier from all solutions, add the code to extract the Pareto frontier here.
            ## If you use the is_pareto_efficient() function given here: https://stackoverflow.com/questions/32791911/fast-calculation-of-pareto-front-in-python
            ## this looks like the following:
            ##
            ## pof_PF = odir+os.sep+f"{problem_name}_qudits_{qudits_str}_seed{seed}_ParetoFront.dat"
            ## pof_PF_mask = odir+os.sep+f"{problem_name}_qudits_{qudits_str}_seed{seed}_ParetoFrontMask.dat"

            ## pop_obj_vectors = all_e[:,numParams:]
            ## efficient_points, efficient_points_mask = is_pareto_efficient(pop_obj_vectors, return_mask=True)
            ## true_pf = pop_obj_vectors[efficient_points_mask]
            ## np.savetxt(pof_PF, true_pf)
            ## np.savetxt(pof_PF_mask, efficient_points_mask,  fmt="%d")

        
        

