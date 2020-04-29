import unittest

from numbering_patterns import LinearRelation
from ..source.related_statements import equation_true
from ..source.related_statements import equivalent_to_the_same_vertex_or_edge
from ..source.related_statements import bounds_dont_contradict

class TestRelatedStatements(unittest.TestCase):

    def test_eq_true(self):

        test_data = [
            ('a == a', 'true'),
            ('1 == 0', 'false'),
            ('a == b', 'unknown'),
        ]

        for info in test_data:
            eq = LinearRelation(info[0])
            expected_result = info[1]

            result, info = equation_true(eq)
            self.assertEqual(result, expected_result)
            self.assertEqual(info, 'trivial solution')

            result, info = equation_true(eq, 'custom info')
            self.assertEqual(result, expected_result)
            self.assertEqual(info, 'custom info')

    def test_equivalent(self):

        test_data = [
            # name      formula     ntuple index
            (('vlr0',   'p',        'p'),
             ('vlr1',   'q',        'q'),
             # status   info
             'false',   "names different"),

            (('vlr0',   'p',        'p'),
             ('vlr0',   'q',        'q'),
             'true', "names the same, only true if the same vertex / edge"),

            (('vlr0',   'p + k',    'p'),
             ('vlr0',   'q + k',    'q'),
             'true', "names the same, only true if the same vertex / edge"),

            (('vlr0',   'p + 4',    'p'),
             ('vlr0',   'q + 4',    'q'),
             'true', "names the same, only true if the same vertex / edge"),

            (('vlr0',   '3k',       'p'),
             ('vlr0',   '3k',       'q'),
             'false',   "can be true for different vertices / edges"),

            (('vlcc',   '3k',       'p'),
             ('vlcc',   '3k',       'q'),
             'true',    "names the same, appear only once"),

            (('emll',   '3k',       'p'),
             ('emll',   '3k',       'q'),
             'true',    "names the same, appear only once"),

            (('emll',   '3k',       'p'),
             ('emrr',   '3k',       'q'),
             'false',   "names different"),
        ]

        for info in test_data:

            # prepare data
            info_1 = {}
            info_2 = {}

            info_1['name'] = info[0][0]
            info_1['formula'] = info[0][1]
            info_1['ntuple_index'] = info[0][2]

            info_2['name'] = info[1][0]
            info_2['formula'] = info[1][1]
            info_2['ntuple_index'] = info[1][2]

            expected_status = info[2]
            expected_message = info[3]

            # run the function
            status, message = equivalent_to_the_same_vertex_or_edge(
                info_1, info_2)

            # check results
            self.assertEqual(status, expected_status)
            self.assertEqual(message, expected_message)

    def test_bounds(self):

        test_data = [
            # formula   ntuple index <= bound
            (('p',      'p',            '3t'),
             ('6t',     'q'),
             # status
             'false'),

            (('-p',     'p',            '3t'),
             ('-6t',    'q'),
             # status
             'false'),

            (('p - 6t', 'p',            '3t'),
             ('-q',     'q',            '2t'),
             'false'),

            (('6t - p', 'p',            '3t'),
             ('q',      'q',            '2t'),
             'false'),

            (('6t',     'p'),
             ('q',      'q',            '3t'),
             'false'),

            (('p - 6t', 'p',            '15t'),
             ('-q',     'q',            '15t'),
             'unknown'),

            (('6t',     'p'),
             ('-2',     'q'),
             'false'),

            (('p + 6t', 'p',            '3t'),
             ('-2',     'q'),
             'false'),

            (('-6t',    'p'),
             ('2',      'q'),
             'false'),

            (('-6t',    'p',            '150t'),
             ('2',      'q'),
             'false'),
        ]

        for info in test_data:

            # prepare data
            info_1 = {}
            info_2 = {}

            info_1['formula'] = info[0][0]
            info_1['ntuple_index'] = info[0][1]
            if len(info[0]) > 2:
                info_1['bound'] = info[0][2]

            info_2['formula'] = info[1][0]
            info_2['ntuple_index'] = info[1][1]
            if len(info[1]) > 2:
                info_2['bound'] = info[1][2]

            expected_status = info[2]

            # run the function
            result = bounds_dont_contradict(info_1, info_2)

            # unpack the results
            if type(result) == tuple:
                status, message = result
            else:
                status = result

            # check results
            self.assertEqual(status, expected_status)
