import unittest

from numbering_patterns.numbering_patterns.source.linear_formula import \
    LinearFormula
from numbering_patterns.numbering_patterns.source.ntr_sequence import \
    NTermRecursionSequence
from numbering_patterns.numbering_patterns.source.cv_numbering import \
    CentralVertexNumbering

from proof_stuff.encryption_decryption import get_data
from proof_stuff.validator import Validator


class TestStuff(unittest.TestCase):

    def test_decryption(self):

        left = NTermRecursionSequence('i', '2i', '3i')
        right = NTermRecursionSequence('6i+4', '5i', '4i')
        upper = CentralVertexNumbering(
            1, left, right, left_len='ull', right_len='url')
        lower = CentralVertexNumbering(
            1, left, right, left_len='lll', right_len='lrl')

        case = {
            'n': '6k+4',
            'upper': upper,
            'lower': lower,
            'k_forms': ['3t', '3t+1', '3t+2']
        }

        # vertices
        info = get_data('vul0', case)
        self.assertEqual(info['formula'], LinearFormula('1i'))
        self.assertEqual(info['index'], LinearFormula('3i+1'))
        self.assertEqual(info['index bound'], LinearFormula('ull'))
        self.assertEqual(
            list(info.keys()), ['formula', 'index', 'index bound'])

        info = get_data('vucc', case)
        self.assertEqual(info['formula'], LinearFormula(1))
        self.assertEqual(list(info.keys()), ['formula'])

        info = get_data('vur1', case)
        self.assertEqual(info['formula'], LinearFormula('5i'))
        self.assertEqual(info['index'], LinearFormula('3i+2'))
        self.assertEqual(info['index bound'], LinearFormula('url'))

        info = get_data('vlr2', case)
        self.assertEqual(info['formula'], LinearFormula('4i'))
        self.assertEqual(info['index'], LinearFormula('3i+3'))
        self.assertEqual(info['index bound'], LinearFormula('lrl'))

        # edges
        info = get_data('eul0', case)
        self.assertEqual(info['formula'], LinearFormula('3i'))
        self.assertEqual(info['index'], LinearFormula('3i+1'))
        self.assertEqual(info['index bound'], LinearFormula('ull - 1'))
        self.assertEqual(
            list(info.keys()), ['formula', 'index', 'index bound'])

        info = get_data('eul1', case)
        self.assertEqual(info['formula'], LinearFormula('5i'))
        self.assertEqual(info['index'], LinearFormula('3i+2'))

        info = get_data('eul2', case)
        self.assertEqual(info['formula'], LinearFormula('4i+1'))
        self.assertEqual(info['index'], LinearFormula('3i+3'))


        info = get_data('eucl', case)
        self.assertEqual(info['formula'], LinearFormula(1))
        self.assertEqual(list(info.keys()), ['formula'])

        info = get_data('eucr', case)
        self.assertEqual(info['formula'], LinearFormula(5))
        self.assertEqual(list(info.keys()), ['formula'])

        # middle edges
        upper.set_lengths('3k + 3', '3k + 5', inplace=True)
        lower.set_lengths('3k + 4', '3k + 2', inplace=True)

        case['upper'] = upper
        case['lower'] = lower

        info = get_data('emll', case)
        self.assertEqual(info['formula'], LinearFormula('4k+1'))
        self.assertEqual(list(info.keys()), ['formula'])

        info = get_data('emrr', case)
        self.assertEqual(info['formula'], LinearFormula('10k+5'))
        self.assertEqual(list(info.keys()), ['formula'])

    def test_rsv(self):

        test_data = [
            # statement     <==>        thesis
            ('true',    'equivalent',   'true'),
            ('unknown', 'equivalent',   'unknown'),
            ('false',   'equivalent',   'false'),

            # statement     <==>    !thesis
            ('true',    'opposite', 'false'),
            ('unknown', 'opposite', 'unknown'),
            ('false',   'opposite', 'true'),

            # statement     ==>     thesis
            ('true',    'implying', 'true'),
            ('unknown', 'implying', 'unknown'),
            ('false',   'implying', 'unknown'),

            # statement     <==     thesis
            ('true',    'implied',  'unknown'),
            ('unknown', 'implied',  'unknown'),
            ('false',   'implied',  'false'),

            #    statement      ==>         !thesis
            # or !statement     <==         thesis
            ('true',    'contradictory',    'false'),
            ('unknown', 'contradictory',    'unknown'),
            ('false',   'contradictory',    'unknown'),
        ]

        def func(status):
            return status

        for info in test_data:

            validator = Validator(info[1], func, info[0])

            self.assertEqual(validator.process_status(info[0]), info[2])
            self.assertEqual(validator.status(), info[2])





