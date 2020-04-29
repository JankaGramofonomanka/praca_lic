
from numbering_patterns import LinearRelation
from numbering_patterns import LinearFormula
from proof_helpers import Validator, validate

from .encryption_decryption import get_data
from .misc import get_variable_bounds


def equation_true(equation, custom_info=None):
    """Says if <equation> is true"""

    if custom_info is None:
        custom_info = "trivial solution"

    return equation.status(), custom_info


def equivalent_to_the_same_vertex_or_edge(info_1, info_2):
    """Returns 'true' if the equation is equivalent to the fact that the
    formulas in question are assigned to the same vertex / edge"""

    if info_1['name'] != info_2['name']:
        # the vertices / edges cannot be the same if the names are not the
        # same
        return 'false', "names different"

    try:
        # if the 3-rd (counting from 0) character of the name is a number,
        # that means we are dealing with a formula from a recursive sequence,
        # so the formulas may be the same but they can refer to different
        # edges / vertices
        int(info_1['name'][3])

    except ValueError:
        # the names are the same and they don't refer to formulas from any of
        # the recursive sequences, therefore they appear only once in the
        # pattern
        return 'true', "names the same, appear only once"

    equation_1 = LinearRelation(
        info_1['formula'], info_2['formula'], relation='==')
    equation_2 = LinearRelation(
        info_1['ntuple_index'], info_2['ntuple_index'], relation='==')

    if equation_1.equivalent(equation_2):
        return 'true', f"names the same, only true if the same vertex / edge"
    else:
        return 'false', "can be true for different vertices / edges"


def bounds_dont_contradict(info_1, info_2):
    """Says if the thesis contradicts the bounds of the variables"""

    formula_1 = info_1['formula']
    formula_2 = info_2['formula']

    # solve the equation -----------------------------------------------------
    equation = LinearRelation(formula_1, formula_2, relation='==').solve()
    zero = equation.left

    # find the bounds --------------------------------------------------------
    lower_bounds, upper_bounds, order = get_variable_bounds(info_1, info_2)

    less_than_zero, more_than_zero = zero.get_bounds(
        lower_bounds=lower_bounds,
        upper_bounds=upper_bounds ,
        order=order
    )

    rel_1 = LinearRelation(less_than_zero, 0, relation='<=')
    rel_2 = LinearRelation(more_than_zero, 0, relation='>=')

    if rel_1.status() == 'false' or rel_2.status() == 'false':
        # 'status' == 'true' doesn't tell us anything, 'unknown' also
        return 'false', "can't be true for t >= 2"

    # if all code above fails, return the default ----------------------------
    return 'unknown'


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






