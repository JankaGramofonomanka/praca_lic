
from numbering_patterns import LinearRelation
from numbering_patterns import LinearFormula
from proof_helpers import Validator, validate

from .related_statements import equation_true
from .related_statements import equivalent_to_the_same_vertex_or_edge
from .related_statements import bounds_dont_contradict
from .encryption_decryption import get_data
from .misc import get_variable_bounds

def compare(name_1, name_2, case, k_form):

    # set up data ------------------------------------------------------------
    info_1 = get_data(name_1, case, k_form, ntuple_index='p')
    info_2 = get_data(name_2, case, k_form, ntuple_index='q')

    formula_1 = info_1['formula']
    formula_2 = info_2['formula']

    equation = LinearRelation(formula_1, formula_2, relation='==')
    equation.solve(inplace=True)

    # set up validators ------------------------------------------------------
    the_same_number = Validator('contradictory',
        equivalent_to_the_same_vertex_or_edge, info_1, info_2
    )

    trivial = Validator('equivalent', equation_true, equation)

    modulos = [
        Validator('implied', equation_true, equation.modulo(m), f"modulo {m}")
        for m in [2, 3]
    ]

    bounds = Validator('implied', bounds_dont_contradict, info_1, info_2)

    # run the validators -----------------------------------------------------
    status, reason = validate(the_same_number, trivial, *modulos, bounds)

    return status, reason

def in_target_set(name, case, k_form):

    n = LinearFormula(case['n']).substitute(k=k_form)
    info = get_data(name, case, k_form, ntuple_index='i')
    formula = info['formula']

    lower_bounds, upper_bounds, order = get_variable_bounds(info)

    # 1 <= formula <= 2n should be always true
    more_than_zero_values = [formula - 1, 2*n - formula]
    statuses = [None, None]

    for i in range(2):
        more_than_zero = more_than_zero_values[i].zip()

        more_than_zero, _ = more_than_zero.get_bounds(
            lower_bounds=lower_bounds,
            upper_bounds=upper_bounds,
            order=order
        )

        rel = LinearRelation(0, more_than_zero, relation='<=').solve()
        statuses[i] = rel.status()

    status_1 = statuses[0]
    status_2 = statuses[1]

    if status_1 == status_2 == 'true':
        return 'true'

    elif status_1 == 'false' or status_2 == 'false':
        return 'false'

    else:
        return 'unknown'






