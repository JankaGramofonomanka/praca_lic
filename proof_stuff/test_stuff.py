import unittest

from numbering_patterns import LinearFormula
from numbering_patterns import NTermRecursionSequence
from numbering_patterns import CentralVertexNumbering

from proof_stuff.encryption_decryption import get_data

class TestStuff(unittest.TestCase):

    def test_decryption(self):

        left = NTermRecursionSequence('i', '2i', '3i')
        right = NTermRecursionSequence('6i+4', '5i', '4i')
        upper = CentralVertexNumbering(
            1, left, right, left_len='3ull', right_len='3url')
        lower = CentralVertexNumbering(
            1, left, right, left_len='3lll', right_len='3lrl')

        case = {
            'n': '6k+4',
            'upper': upper,
            'lower': lower,
            'k_forms': ['3t', '3t+1', '3t+2']
        }

        # vertices
        info = get_data('vul0', case, 'k')
        self.assertEqual(info['formula'], LinearFormula('1i'))

        info = get_data('vucc', case, 'k')
        self.assertEqual(info['formula'], LinearFormula(1))

        info = get_data('vur1', case, 'k')
        self.assertEqual(info['formula'], LinearFormula('5i'))

        info = get_data('vlr2', case, 'k')
        self.assertEqual(info['formula'], LinearFormula('4i'))

        # edges
        info = get_data('eul0', case, 'k')
        self.assertEqual(info['formula'], LinearFormula('3i'))

        info = get_data('eul1', case, 'k')
        self.assertEqual(info['formula'], LinearFormula('5i'))

        info = get_data('eul2', case, 'k')
        self.assertEqual(info['formula'], LinearFormula('4i+1'))


        info = get_data('eucl', case, 'k')
        self.assertEqual(info['formula'], LinearFormula(1))

        info = get_data('eucr', case, 'k')
        self.assertEqual(info['formula'], LinearFormula(5))

        # middle edges
        upper.set_lengths('3k + 3', '3k + 5', inplace=True)
        lower.set_lengths('3k + 4', '3k + 2', inplace=True)

        case['upper'] = upper
        case['lower'] = lower

        info = get_data('emll', case, 'k')
        self.assertEqual(info['formula'], LinearFormula('4k+1'))

        info = get_data('emrr', case, 'k')
        self.assertEqual(info['formula'], LinearFormula('10k+5'))






