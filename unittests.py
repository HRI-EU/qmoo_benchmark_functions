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
import functools
import os
import qmoo_benchmark_functions as prob

def test_val(value,expected):
    if np.fabs(value-expected)>1.e-9:
        return 1
    else:
        return 0
    
#################################
## qudit configurations and search variables for testing:
qudits_x_pairs = [
    ( np.asarray( [2]*12), np.asarray([1]*12 ),  ) , 
    ( np.asarray( [3]*8),  np.asarray([2]*8 ) ) , 
    ( np.asarray( [5]*5), np.asarray([3]*5 ) ) 
]

# 
seed = 7

fail_count = 0


# ignore this, this is only for generating new test samples
#results= {
#    'problem_linear_corr-0.5' : dict(),
#    'problem_FM_AFM_two_objs' : dict(),
#    'problem_quadratic_AFM_two_objs' : dict(),
#    'problem_FM_AFM_three_objs' : dict(),
#    'problem_quadratic_five_objs' : dict()
#    }


# expected results:
# problem: qudits: (obj1,...objK)  
results = {
    'problem_linear_corr-0.5': {
        '[2 2 2 2 2 2 2 2 2 2 2 2]': (0.5299207486221158, 0.46819389176618303),
        '[3 3 3 3 3 3 3 3]': (0.5134698087890803, 0.48675929062013473),
        '[5 5 5 5 5]': (0.5744136504323764, 0.41629234591062914)
        },
    'problem_FM_AFM_two_objs': {
        '[2 2 2 2 2 2 2 2 2 2 2 2]': (0.8748351766376586, 0.006685361633740233),
        '[3 3 3 3 3 3 3 3]': (0.891989333170222, 0.005502660363565879),
        '[5 5 5 5 5]': (0.5920781457403532, 0.4204486884663538)
        },
    'problem_quadratic_AFM_two_objs': {
        '[2 2 2 2 2 2 2 2 2 2 2 2]': (0.8833598084348937, 0.7721574937964575),
        '[3 3 3 3 3 3 3 3]': (0.8997683696913392, 0.6994100588539806),
        '[5 5 5 5 5]': (0.599202809978191, 0.46540277828209553)
        },
    'problem_FM_AFM_three_objs': {
        '[2 2 2 2 2 2 2 2 2 2 2 2]': (0.9403246189826114, 0.18401814046572845, 0.17228043235461238),
        '[3 3 3 3 3 3 3 3]': (0.9501086051862085, 0.181370780462223, 0.2963314334078799),
        '[5 5 5 5 5]': (0.8485526768957755, 0.22253597408955578, 0.3143213019074601)
        },
    'problem_quadratic_five_objs': {'[2 2 2 2 2 2 2 2 2 2 2 2]': (0.9403246189826114, 0.18401814046572845, 0.17228043235461238, 0.7949882951874528, 0.2927554594291931),
                                    '[3 3 3 3 3 3 3 3]': (0.9501086051862085, 0.181370780462223, 0.2963314334078799, 0.8219090668361857, 0.2813725046869244),
                                    '[5 5 5 5 5]': (0.8796375241588196, 0.24270514072663257, 0.3143213019074601, 0.8021127572699365, 0.3049538414048848)
                                    }
    }


for (qudits, x) in qudits_x_pairs:
    # ################################
    # problem_linear_corr-0.5'
    cost_coefficients = prob.generate_problem_linear_corr05(qudits, seed)
    
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
    obj1 = first_objective_partial(x) 
    obj2 = second_objective_partial(x) + 1.e-3 

    # ignore this, this is only for generating new test samples:
    # results['problem_linear_corr-0.5'][str(qudits)]=(obj1,obj2) 

    fail_count += test_val(obj1, results['problem_linear_corr-0.5'][str(qudits)][0] )
    fail_count += test_val(obj2, results['problem_linear_corr-0.5'][str(qudits)][1] )
    
    #print('linear_corr-0.5-1',qudits,x,obj1,  results['problem_linear_corr-0.5'][str(qudits)][0])
    #print('linear_corr-0.5-2',qudits,x,obj2,  results['problem_linear_corr-0.5'][str(qudits)][1])

    # ################################
    # problem_FM_AFM_two_objs
    cost_coefficients = prob.generate_problem_ferromagnetic_antiferromagnetic_two_objectives(qudits, seed)    
    
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
    obj1 = first_objective_partial(x)
    obj2 = second_objective_partial(x)

    # ignore this, this is only for generating new test samples:
    # results['problem_FM_AFM_two_objs'][str(qudits)]= (obj1,obj2) 

    fail_count += test_val(obj1, results['problem_FM_AFM_two_objs'][str(qudits)][0] )
    fail_count += test_val(obj2, results['problem_FM_AFM_two_objs'][str(qudits)][1] )


    #print('FM_AFM_two_objs1',qudits,x,obj1, results['problem_FM_AFM_two_objs'][str(qudits)][0])
    #print('FM_AFM_two_objs2',qudits,x,obj2, results['problem_FM_AFM_two_objs'][str(qudits)][1])


    # ################################
    # problem_quadratic_AFM_two_objs'
    cost_coefficients = prob.generate_problem_quadratic_antiferromagnetic_two_objectives(qudits, seed)    
    
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
    obj1 = first_objective_partial(x)
    obj2 = second_objective_partial(x)

    # ignore this, this is only for generating new test samples:
    # results['problem_quadratic_AFM_two_objs'][str(qudits)]=(obj1,obj2)

    fail_count += test_val(obj1, results['problem_quadratic_AFM_two_objs'][str(qudits)][0] )
    fail_count += test_val(obj2, results['problem_quadratic_AFM_two_objs'][str(qudits)][1] )


    #print('quadratic_AFM_two_objs1',qudits,x,obj1 ,results['problem_quadratic_AFM_two_objs'][str(qudits)][0] )
    #print('quadratic_AFM_two_objs2',qudits,x,obj2 ,results['problem_quadratic_AFM_two_objs'][str(qudits)][1] )

    # ################################
    # problem_FM_AFM_three_objs':
    cost_coefficients = prob.generate_problem_ferromagnetic_antiferromagnetic_three_objectives(qudits, seed)
    
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

    obj1 = first_objective_partial(x)
    obj2 = second_objective_partial(x)
    obj3 = third_objective_partial(x)

    # ignore this, this is only for generating new test samples:
    # results['problem_FM_AFM_three_objs'][str(qudits)]= (obj1,obj2,obj3)

    fail_count += test_val(obj1, results['problem_FM_AFM_three_objs'][str(qudits)][0] )
    fail_count += test_val(obj2, results['problem_FM_AFM_three_objs'][str(qudits)][1] )
    fail_count += test_val(obj3, results['problem_FM_AFM_three_objs'][str(qudits)][2] )


    
    #print('FM_AFM_three_objs1',qudits,x,obj1, results['problem_FM_AFM_three_objs'][str(qudits)][0])
    #print('FM_AFM_three_objs2',qudits,x,obj2, results['problem_FM_AFM_three_objs'][str(qudits)][1])
    #print('FM_AFM_three_objs3',qudits,x,obj3, results['problem_FM_AFM_three_objs'][str(qudits)][2])

    # ################################
    # problem_quadratic_five_objs
    cost_coefficients = prob.generate_problem_quadratic_five_objectives(qudits, seed)
    
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
    

    obj1 = first_objective_partial(x)
    obj2 = second_objective_partial(x)
    obj3 = third_objective_partial(x)
    obj4 = fourth_objective_partial(x)
    obj5 = fifth_objective_partial(x)

    # ignore this, this is only for generating new test samples:
    # results['problem_quadratic_five_objs'][str(qudits)] = (obj1,obj2,obj3,obj4,obj5)
 
    fail_count += test_val(obj1, results['problem_quadratic_five_objs'][str(qudits)][0] )
    fail_count += test_val(obj2, results['problem_quadratic_five_objs'][str(qudits)][1] )
    fail_count += test_val(obj3, results['problem_quadratic_five_objs'][str(qudits)][2] )
    fail_count += test_val(obj4, results['problem_quadratic_five_objs'][str(qudits)][3] )
    fail_count += test_val(obj5, results['problem_quadratic_five_objs'][str(qudits)][4] )


    #print('quadratic_five_objs1',qudits,x,obj1, results['problem_quadratic_five_objs'][str(qudits)][0])
    #print('quadratic_five_objs2',qudits,x,obj2, results['problem_quadratic_five_objs'][str(qudits)][1])
    #print('quadratic_five_objs3',qudits,x,obj3, results['problem_quadratic_five_objs'][str(qudits)][2])
    #print('quadratic_five_objs4',qudits,x,obj4, results['problem_quadratic_five_objs'][str(qudits)][3])
    #print('quadratic_five_objs5',qudits,x,obj5, results['problem_quadratic_five_objs'][str(qudits)][4])


if fail_count != 0:
    print (f'ERROR: {fail_count} tests failed!')
    sys.exit(fail_count)

print (f'unittest succeeded!')
sys.exit(0) 
#print(results)    

