
from numbering_patterns import LinearRelation

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

