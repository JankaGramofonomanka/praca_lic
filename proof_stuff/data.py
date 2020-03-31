from numbering_patterns.numbering_patterns.source.ntr_sequence import NTermRecursionSequence
from numbering_patterns.numbering_patterns.source.cv_numbering import CentralVertexNumbering


A_l = NTermRecursionSequence('6i+1', '6i+4', '2n-14-12i')
A_r = NTermRecursionSequence('6j+2', '2n-8-12j', '6j+3', ntuple_index='j')
A = CentralVertexNumbering('2n-2', A_l, A_r)

B_l = NTermRecursionSequence('n-3-6i', '12i+6', 'n-6-6i')
B_r = NTermRecursionSequence('n-2-6j', 'n-7-6j', '12j+12', ntuple_index='j')
B = CentralVertexNumbering('n-1', B_l, B_r)

C_l = NTermRecursionSequence('n-3-6i', 'n-6-6i', '12i+12')
C_r = NTermRecursionSequence('n-4-6j', '12j+6', 'n-5-6j', ntuple_index='j')
C = CentralVertexNumbering('n', C_l, C_r)

case_a = {
    'n': '6k+4',
    'upper': A.set_lengths('2k', '2k'),
    'lower': B.set_lengths('k+1', 'k+1'),
    'k_forms': ['3t', '3t+1', '3t+2']
}

case_b = {
    'n': '6k+1',
    'upper': A.set_lengths('2k', '2k'),
    'lower': C.set_lengths('k-1', 'k'),
    'k_forms': ['3t', '3t+1', '3t+2']
}

case_c = {
    'n': '6k',
    'upper': A.set_lengths('2k-1', '2k'),
    'lower': C.reverse().set_lengths('k', 'k-1'),
    'k_forms': ['3t']
}

case_d = {
    'n': '6k',
    'upper': A.set_lengths('2k', '2k-1'),
    'lower': C.reverse().set_lengths('k', 'k-1'),
    'k_forms': ['3t+1', '3t+2']
}

case_e = {
    'n': '6k+3',
    'upper': A.set_lengths('2k', '2k+1'),
    'lower': B.reverse().set_lengths('k', 'k'),
    'k_forms': ['3t+1']
}

case_f = {
    'n': '6k+3',
    'upper': A.set_lengths('2k+1', '2k'),
    'lower': B.set_lengths('k+1', 'k-1'),
    'k_forms': ['3t', '3t+2']
}

cases = [case_a, case_b, case_c, case_d, case_e, case_f]
