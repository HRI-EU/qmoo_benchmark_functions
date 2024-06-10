# -*- coding: utf-8 -*-
#
#  Custom package settings
#
#  Copyright (C)
#  Honda Research Institute Europe GmbH
#  Carl-Legien-Str. 30
#  63073 Offenbach/Main
#  Germany
#
#  UNPUBLISHED PROPRIETARY MATERIAL.
#  ALL RIGHTS RESERVED.
#
#



name             = 'qmoo_benchmark_functions'

version          = '1.0'

category         = 'Applications'

sqlevel          = 'basic'

# sqOptOutRules    = [ 'DOC03' ]
# sqOptInRules    = [ ]

# opt-out testcase data that would provoke a failure of SQ check onto this package
#sqOptOutDirs     = [ 'test/SoftwareQuality/CheckRoutine/ReferenceData' ]

#sqComments       = { 'DOC03': 'dont want to create separate directiry for one of two files in the package.',
                     #'10'  : 'do not invoke Klocwork on example files'
#                     }

scripts = { 'unittest': 'unittest.sh' }
# EOF

