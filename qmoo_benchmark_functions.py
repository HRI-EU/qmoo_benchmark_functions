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


def getCorrelatedRand( x , corr : float, scale: float =1.0):
    """
    Helper function which adds a random vector with entries drawn from a uniform distribution in the interval [-1,1] to a given vector with specified relative contribution.
    """
    if type(x) == float :
        sz = 1
    elif type(x) == np.ndarray:
        sz = len(x)
    else:
        print(f'error: type: {type(x)}')
        sys.exit(8)
    if np.fabs(corr)>1 :
        print (f"WARNING parameter corr has larger absolute value than 1: corr={corr}!")
        sys.exit(8)
    return np.array(corr * x + (1.-np.fabs(corr)) * scale* np.random.uniform(-1.,1. ,sz))
     



def calculate_cost_function_linear(x: np.array, c, m=0.):
    """
    This function takes calculates a linear cost-function from a given search vector and cost coefficients
    """
    f = np.dot(x, c) + m
    return f


def calculate_cost_function_quadratic(x: np.array, J, c, m):
    """
    calculates one quadratic cost function from give interaction matrix J_ij, lienar cost coefficient c_i, and constant offset m
    These problem specs a generated by functuions below (e.g., generate_problem_ferromagnetic_antiferromagnetic_two_objectives)
    """
    f = np.dot(x, c + np.dot(J, x)) + m
    return f


def get_reference_point_for_qudit_config_and_problem_name(problem_name):
    """
    returns the reference vecotr for each problem (which is always the K-dimensional vectors with all ones, r=(1,1,....,1)^T )
    """
    ref_norm = {
            'problem_linear_corr-0.5': [1., 1.],
            'problem_leading_trailing_two_objs': [1., 1.],
            'problem_FM_AFM_two_objs': [1., 1.],
            'problem_quadratic_AFM_two_objs' : [1.,1.],
            'problem_FM_AFM_three_objs' : [1.,1.,1.] ,    
            'problem_quadratic_five_objs' : [1.,1.,1.,1.,1.] ,
    }
    return ref_norm[problem_name]


def generate_problem_linear_corr05(qudits_list: np.array, seed=3):
    """
    two objective linear cost function where the two objectives have anticorrelated objectives
    for a given seed, the problem is always the same
    """
    # objectives (minimize)
    dimq = len(qudits_list)
    cnt = seed
    np.random.seed(cnt)

    cost_1 = np.random.uniform(low=-1., high=1., size=dimq)
    cost_2 = getCorrelatedRand(cost_1, -0.5, 1.)
    A=np.sum(qudits_list-1.)
    #print(f"A {A}")

    return [[ 0.5*cost_1/A , 0.5 ], [0.5*cost_2/A ,0.5]]


def generate_problem_ferromagnetic_antiferromagnetic_two_objectives(qudits_list: np.array, seed=12):
    """
    two-objective cost function
    for a given seed, the problem is always the same
    obj1 = randomized predominantly anti-ferromagentic all-to-all coupling: AFM
    obj2 = randomized predominantly ferromagentic all-to-all coupling: FM
    """
    m = 0.5*(np.array(qudits_list)-1.)

    dimq = len(qudits_list)
    d_1 = qudits_list[0]-1
    if np.sum(qudits_list-1) != dimq*d_1:
        print(f'ERROR: heterogenous qudit system, benchmark norm not implemented!')
        sys.exit(8) 
    # transform qudit search variable to spin x \in [0,d-1] =>  s \in [ -(d-1)/2, (d-1)/2]

    c1max=2.
    c2max=0.1

    J1max=4.
    J2max=5.


    Aafm = 2*c1max*np.sum(m)
    Bafm = -(dimq*dimq-dimq)*J1max*d_1*d_1*0.25 -2.*c1max*np.sum(m)-0.25*c1max*c1max*dimq/(J1max*(dimq-1.))

    Afm =  (dimq*dimq-dimq)*J2max*d_1*d_1*0.25 +2.*c2max*np.sum(m)+0.75*c2max*c2max*dimq/(J2max*(dimq-1.))
    Bfm = -2*c2max*np.sum(m)

    
    cnt = seed  # 12
    np.random.seed(cnt)
    # objectives (minimize)
    cost_1 = c1max * np.random.uniform(low=-1., high=1., size=dimq)
    cost_2 = c2max * np.random.uniform(low=-1., high=1., size=dimq)
    J_1 = np.random.uniform(low=0.2, high=J1max, size=(dimq, dimq))
    J_2 = np.random.uniform(low=-1.*J2max, high=-0.2, size=(dimq, dimq))
    for d in range(dimq):
        J_1[d, d] = 0.
        J_2[d, d] = 0.
    # make interaction matrices symmetric
    J_1 = 0.5 * (J_1 + J_1.T) 
    J_2 = 0.5 * (J_2 + J_2.T) 

    # transform from qudits to spins:
    c_1 = (cost_1 - 2. * np.dot(J_1, m)) / (Aafm-Bafm)
    c_2 = (cost_2 - 2. * np.dot(J_2, m)) / (Afm-Bfm)

    J_1 = J_1 / (Aafm-Bafm)
    J_2 = J_2 / (Afm-Bfm)
    
    m_1 = - Bafm / (Aafm-Bafm)
    m_2 = - Bfm /(Afm-Bfm)

    return [[J_1, c_1, m_1], [J_2, c_2, m_2]]



def generate_problem_quadratic_antiferromagnetic_two_objectives(qudits_list: np.array, seed=12):
    """
    two-objective cost function
    for a given seed, the problem is always the same
    obj1 = randomized predominantly anti-ferromagentic all-to-all coupling: AFM
    obj2 = quadratic coupling ~ (x - 1.8)**2
    """
    dimq = len(qudits_list)

    # transform qudit search variable to spin x \in [0,d-1] =>  s \in [ -(d-1)/2, (d-1)/2]
    m = 0.5*(np.array(qudits_list)-1.)

    d_1 = qudits_list[0]-1
    if np.sum(qudits_list-1) != dimq*d_1:
        print(f'ERROR: heterogenous qudit system, benchmark norm not implemented!')
        sys.exit(8) 

    c1max=0.5

    J1max=1.1
    Jqmax=2.
    Jqmin=0.5
    
    cnt = seed  # 12
    np.random.seed(cnt)
    # objectives (minimize)
    cost_1 = c1max * np.random.uniform(low=-1., high=1., size=dimq)
    cost_2 = (np.array(qudits_list) - 1.8)
    c2max = cost_2[0]

    Aafm = 2.*c1max*np.sum(m)
    Bafm = -(dimq*dimq-dimq)*J1max*d_1*d_1*0.25 -2.*c1max*np.sum(m)-0.25*c1max*c1max*dimq/(J1max*(dimq-1.))

    tq1 = d_1*d_1*Jqmax*dimq - 2.*Jqmax*dimq*d_1*c2max
    tq2 = - dimq*Jqmax*c2max**2
    Aq = np.maximum(np.maximum(0.,tq1),tq2)
    Bq = np.minimum(np.minimum(0.,tq1),tq2)


    J_1 = np.random.uniform(low=0.1, high=J1max, size=(dimq, dimq))
    J_2 = np.eye(dimq)

    for d in range(dimq):
        J_1[d, d] = 0.
        J_2[d, d] *= np.random.uniform(low=Jqmin,high=Jqmax,size=1)
    # make interaction matrices symmetric
    J_1 = 0.5 * (J_1 + J_1.T) 

    # transform from qudits to spins:
    c_1 = (cost_1 - 2. * np.dot(J_1, m)) / (Aafm-Bafm) 
    c_2 = - 2. * np.dot(J_2,cost_2) / (Aq-Bq) 

    J_1 = J_1 / (Aafm-Bafm) 
    J_2 = J_2 / (Aq-Bq) 

    m_1 =  -Bafm / (Aafm-Bafm) 
    m_2 =  -Bq / (Aq-Bq) 

    return [[J_1, c_1, m_1], [J_2, c_2, m_2]]


def generate_problem_ferromagnetic_antiferromagnetic_three_objectives(qudits_list: np.array, seed = 32):
    """
    three-objective cost function
    for a given seed, the problem is always the same
    obj1 = randomized predominantly anti-ferromagentic nearest-neightbor coupling: AFM
    obj2 = randomized predominantly ferromagentic nearest-neightbor coupling: FM
    obj3 = quadratic coupling ~ (x - c )**2
    """
    # objectives (minimize)
    dimq = len(qudits_list)
    m = 0.5 * (qudits_list - 1.)
    d_1 = qudits_list[0]-1
    if np.sum(qudits_list-1) != dimq*d_1:
        print(f'ERROR: heterogenous qudit system, benchmark norm not implemented!')
        sys.exit(8) 

    c1max=0.2
    c2max=0.1

    cnt = seed # 32

    np.random.seed(cnt)
    cost_1 = c1max*np.random.uniform(low=-1., high=1., size=dimq)
    cost_2 = c2max*np.random.uniform(low=-1., high=1., size=dimq)
    cost_3 = np.random.uniform(qudits_list-0.5)

    c3max = qudits_list[0]-0.5
    c3min=0.

    A1 = 2.*c1max*np.sum(m)
    B1 = -(dimq*dimq-dimq)*d_1*d_1*0.25 -2.*c1max*np.sum(m)-0.25*c1max*c1max*dimq/(dimq-1.)


    A2 = (dimq*dimq-dimq)*d_1*d_1*0.25 +2.*c2max*np.sum(m)+0.75*c2max*c2max*dimq/(dimq-1.)
   
    B2 = np.minimum(
                -2.*c2max*np.sum(m),
                -(dimq*dimq-dimq)*0.2*d_1*d_1*0.25 -2.*c2max*np.sum(m)-0.25*c2max*c2max*dimq/(0.2*(dimq-1.))
                )


    t31 = d_1*d_1*dimq - 2.*dimq*d_1*c3max
    t31a = d_1*d_1*dimq - 2.*dimq*d_1*c3min
    t32 = - dimq*c3max**2
    A3 = np.maximum(np.maximum(np.maximum(0.,t31),t32),t31a)
    B3 = np.minimum(np.maximum(np.minimum(0.,t31),t32),t31a)


    J_1 = np.zeros((dimq, dimq))
    J_2 = np.zeros((dimq, dimq))

    for d in range(dimq):
        J_1[d, (d+1) % dimq] = np.random.uniform(low=0.2, high=1., size=1)
        J_2[d, (d+1) % dimq] = np.random.uniform(low=-1., high=0.2, size=1)

    J_1 = 0.5 * (J_1 + J_1.T)
    J_2 = 0.5 * (J_2 + J_2.T)
    J_3 = np.eye(dimq)

    c_1 = (cost_1 - 2. * np.dot(J_1, m)) /(A1-B1)
    c_2 = (cost_2 - 2. * np.dot(J_2, m)) /(A2-B2)
    c_3 = (- 2. * cost_3 )/ (A3-B3)

    J_1 = J_1 /(A1-B1)
    J_2 = J_2 /(A2-B2)
    J_3 = J_3 /(A3-B3)

    m_1 = -B1/(A1-B1) 
    m_2 = -B2/(A2-B2) 
    m_3 = -B3/(A3-B3)

    return [ [J_1, c_1, m_1], [J_2, c_2, m_2], [J_3, c_3, m_3] ]




def generate_problem_quadratic_five_objectives(qudits_list: np.array, seed = 32):
    """"
    five-objective cost function
    for a given seed, the problem is always the same
    obj1 = randomized predominantly anti-ferromagentic nearest-neightbor coupling: AFM
    obj2 = randomized predominantly ferromagentic  nearest-neightbor coupling: FM
    obj3 = quadratic coupling ~ (x - c )**2
    obj4 = AFM nearest-neightbor coupling in first half of variables, FM coupling in second half
    obj5 = FM nearest-neightbor coupling in first half of variables, AFM coupling in second half
    """
    # objectives (minimize)
    dimq = len(qudits_list)
    m = 0.5 * (qudits_list - 1.)
    d_1 = qudits_list[0]-1
    if np.sum(qudits_list-1) != dimq*d_1:
        print(f'ERROR: heterogenous qudit system, benchmark norm not implemented!')
        sys.exit(8) 

    c1max=0.2
    c2max=0.1
    
    cnt = seed # 32

    np.random.seed(cnt)
    cost_1 = c1max*np.random.uniform(low=-1., high=1., size=dimq)
    cost_2 = c2max*np.random.uniform(low=-1., high=1., size=dimq)
    cost_3 = np.random.uniform(qudits_list-0.5)
    
    c3max = qudits_list[0]-0.5
    c3min=0.
    
    cost_4 = getCorrelatedRand(cost_2, -0.5, 1.)
    cost_5 = getCorrelatedRand(cost_1, -0.5, 1.)
    
    c4max=1
    c5max=1

    A1 = 2.*c1max*np.sum(m)
    B1 = -(dimq*dimq-dimq)*d_1*d_1*0.25 -2.*c1max*np.sum(m)-0.25*c1max*c1max*dimq/(dimq-1.)


    A2 = (dimq*dimq-dimq)*d_1*d_1*0.25 +2.*c2max*np.sum(m)+0.75*c2max*c2max*dimq/(dimq-1.)
   
    B2 = np.minimum(
                -2.*c2max*np.sum(m),
                -(dimq*dimq-dimq)*0.2*d_1*d_1*0.25 -2.*c2max*np.sum(m)-0.25*c2max*c2max*dimq/(0.2*(dimq-1.))
                )


    t31 = d_1*d_1*dimq - 2.*dimq*d_1*c3max
    t31a = d_1*d_1*dimq - 2.*dimq*d_1*c3min
    t32 = - dimq*c3max**2
    A3 = np.maximum(np.maximum(np.maximum(0.,t31),t32),t31a)
    B3 = np.minimum(np.maximum(np.minimum(0.,t31),t32),t31a)

    A4 = 2.*c4max*np.sum(m)
    B4 = np.minimum(
        -2.*c4max*np.sum(m),
        -(dimq*dimq-dimq)*d_1*d_1*0.25 -2.*c4max*np.sum(m)-0.25*c4max*c1max*dimq/(dimq-1.)
    )


    A5 = (dimq*dimq-dimq)*d_1*d_1*0.25 +2.*c5max*np.sum(m)+0.75*c5max*c5max*dimq/(dimq-1.)
   
    B5 = np.minimum(
                -2.*c5max*np.sum(m),
                -(dimq*dimq-dimq)*0.2*d_1*d_1*0.25 -2.*c5max*np.sum(m)-0.25*c5max*c5max*dimq/(0.2*(dimq-1.))
                )

    J_1 = np.zeros((dimq, dimq))
    J_2 = np.zeros((dimq, dimq))

    J_4 = np.zeros((dimq, dimq))
    J_5 = np.zeros((dimq, dimq))

    sign=1.
    for d in range(dimq):
        J_1[d, (d+1) % dimq] = np.random.uniform(low=0.2, high=1., size=1)
        J_2[d, (d+1) % dimq] = np.random.uniform(low=-1., high=0.2, size=1)
        if d > 0.5*(dimq-1.):
            sign =-1.
        J_4[d, (d+1) % dimq] = sign * np.random.uniform(low=0.2, high=1., size=1)
        J_5[d, (d+1) % dimq] = -1.*sign* np.random.uniform(low=0.2, high=1., size=1)


    J_1 = 0.5 * (J_1 + J_1.T)
    J_2 = 0.5 * (J_2 + J_2.T)
    J_3 = np.eye(dimq)
    J_4 = 0.5 * (J_4 + J_4.T)
    J_5 = 0.5 * (J_5 + J_5.T)

    c_1 = (cost_1 - 2. * np.dot(J_1, m)) /(A1-B1)
    c_2 = (cost_2 - 2. * np.dot(J_2, m)) /(A2-B2)
    c_3 = (- 2. * cost_3 )/(A3-B3)
    c_4 = (cost_4 - 2. * np.dot(J_4, m)) / (A4-B4)
    c_5 = (cost_5 - 2. * np.dot(J_5, m)) / (A5-B5)

    J_1 = J_1/(A1-B1)
    J_2 = J_2/(A2-B2)
    J_3 = J_3/(A3-B3)
    J_4 = J_4 /(A4-B4)
    J_5 = J_5 /(A5-B5)

    m_1 = -B1/(A1-B1)
    m_2 = -B2/(A2-B2)
    m_3 = -B3/(A3-B3)
    m_4 = -B4/(A4-B4)
    m_5 = -B5/(A5-B5)
    

    return [ [J_1, c_1, m_1] ,
             [J_2, c_2, m_2] ,
             [J_3, c_3, m_3] ,
             [J_4, c_4, m_4] , 
             [J_5, c_5, m_5] 
            ]



