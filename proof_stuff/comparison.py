from numbering_patterns.numbering_patterns.source.linear_relation import LinearRelation

from proof_stuff.encryption_decryption import get_data
from proof_stuff.misc import get_formula_with_index


def basic_solution(equation):

    # simple comparison
    status = equation.status()
    if status != 'unknown':
        # <status> == 'false' ==> we've got what we want
        # <status> == 'true' ==> the theorem is false or formulas are the same
        return status

    # comparison modulo
    for m in [2, 3]:
        status = equation.modulo(m).status()
        if status == 'false':
            # <status> == 'true' doesn't tell us anything, 'unknown' also
            return status

    return 'unknown'


def check_inequalities(info_1, info_2, n='n', fund_var='k'):

    formula_1 = info_1['formula'].substitute(n=n)
    formula_2 = info_2['formula'].substitute(n=n)

    # use the fact that 1 <= 'index' <= 'length' -----------------------------

    # set up kwargs
    upper_bounds = {}
    lower_bounds = {}
    if 'index' in info_1.keys():
        formula_1 = get_formula_with_index(
            formula_1, info_1['index'], 'index_1')
        upper_bounds['index_1'] = info_1['index bound']
        lower_bounds['index_1'] = 1

    if 'index' in info_2.keys():
        formula_2 = get_formula_with_index(
            formula_2, info_2['index'], 'index_2')
        upper_bounds['index_2'] = info_2['index bound']
        lower_bounds['index_2'] = 1

    # solve the equation
    equation = LinearRelation(formula_1, formula_2, relation='==').solve()
    zero = equation.left

    # find the bounds
    less_than_zero, more_than_zero = zero.get_bounds(
        lower_bounds=lower_bounds, upper_bounds=upper_bounds)

    rel_1 = LinearRelation(less_than_zero, 0, relation='<=')
    rel_2 = LinearRelation(more_than_zero, 0, relation='>=')

    if rel_1.status() == 'false' or rel_2.status() == 'false':
        # 'status' == 'true' doesn't tell us anything, 'unknown' also
        return 'false'

    # use the fact that <fund_var> >= 0 --------------------------------------
    less_than_zero, _ = less_than_zero.get_bounds(lower_bounds={fund_var: 0})
    _, more_than_zero = more_than_zero.get_bounds(lower_bounds={fund_var: 0})

    rel_1 = LinearRelation(less_than_zero, 0, relation='<=')
    rel_2 = LinearRelation(more_than_zero, 0, relation='>=')

    if rel_1.status() == 'false' or rel_2.status() == 'false':
        # 'status' == 'true' doesn't tell us anything, 'unknown' also
        return 'false'

    print(equation)
    print(rel_1.solve())
    print(rel_2.solve())
    print()

    # if all code above fails, return the default ----------------------------
    return 'unknown'


def compare(name_1, name_2, case):

    if name_1[:2] != 'em' and name_2[:2] != 'em':

        info_1 = get_data(name_1, case, ntuple_index='p')
        info_2 = get_data(name_2, case, ntuple_index='q')

        formula_1 = info_1['formula'].substitute()
        formula_2 = info_2['formula'].substitute()

        equation = LinearRelation(formula_1, formula_2, relation='==')
        equation.solve(inplace=True)

        if name_1 == name_2 and equation.equivalent('p == q'):
            return 'false'

        # simple comparison, modulo comparison -------------------------------
        status = basic_solution(equation)
        if status != 'unknown':
            return status

        # split into cases and compare each ----------------------------------
        statuses = []
        for k_form in case['k_forms']:
            equation = LinearRelation(
                formula_1.substitute(k=k_form),
                formula_2.substitute(k=k_form),
                relation='=='
            )

            status = basic_solution(equation)

            if status == 'true':
                # nothing else needed
                return status

            statuses.append(status)

        if set(statuses) == {'false'}:
            # only if every case was false, we can say that the equation is
            # false
            return 'false'

        # check if the equation doesn't contradict the fact that
        # 1 <= 'index' <= 'length' or that 0 <= 'k' --------------------------
        status = check_inequalities(info_1, info_2, n=case['n'])

        if status == 'false':
            # <status> == 'true' doesn't tell us anything, 'unknown' also
            return status

    else:

        # split into cases and compare each ----------------------------------
        statuses = []
        for k_form in case['k_forms']:

            info_1 = get_data(name_1, case, ntuple_index='p', k=k_form)
            info_2 = get_data(name_2, case, ntuple_index='q', k=k_form)

            formula_1 = info_1['formula'].substitute()
            formula_2 = info_2['formula'].substitute()

            equation = LinearRelation(formula_1, formula_2, relation='==')
            equation.solve(inplace=True)

            # simple comparison, modulo comparison ---------------------------
            status = basic_solution(equation)
            if status == 'true':
                # nothing else needed
                return status

            if status == 'false':
                # no need to check the inequalities
                statuses.append(status)
                continue

            # check if the equation doesn't contradict the fact that
            # 1 <= 'index' <= 'length' or that 0 <= 'k' ----------------------
            status = check_inequalities(
                info_1, info_2, n=case['n'], fund_var='t')

            if status == 'true':
                # nothing else needed
                return status

            statuses.append(status)

        if set(statuses) == {'false'}:
            # only if every case was false, we can say that the equation is
            # false
            return 'false'

    # if all code above fails, return the default ----------------------------
    return 'unknown'
