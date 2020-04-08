from numbering_patterns.numbering_patterns.source.linear_formula import \
    LinearFormula
from numbering_patterns.numbering_patterns.source.linear_relation import \
    LinearRelation
from proof_stuff.misc import get_common_edge


def get_names(case):

    names = []

    names.append('emll')            # edge middle left

    for i in range(case['upper'].left_seq.n - 1, -1, -1):
        names.append(f'eul{i}')     # edge   upper left i
        names.append(f'vul{i}')     # vertex upper left i

    names.append(f'eucl')           # edge   upper center left
    names.append('vucc')            # vertex upper center
    names.append(f'eucr')           # edge   upper center right

    for i in range(case['upper'].right_seq.n):
        names.append(f'vur{i}')     # vertex upper right i
        names.append(f'eur{i}')     # edge   upper right i

    names.append('emrr')

    for i in range(case['lower'].right_seq.n - 1, -1, -1):
        names.append(f'elr{i}')     # edge   lower right i
        names.append(f'vlr{i}')     # vertex lower right i

    names.append(f'elcr')           # edge   lower center right
    names.append('vlcc')            # vertex lower center
    names.append(f'elcl')           # edge   lower center left

    for i in range(case['lower'].left_seq.n):
        names.append(f'vll{i}')     # vertex lower left i
        names.append(f'ell{i}')     # edge   lower left i

    return names

def get_data(name, case, k_form, ntuple_index='i'):

    # "terminology":
    # vertex:  center  |v_1 v_2 ... v_n|v_n+1   v_n+2   ... v_2n|   ...
    # index:        0  |1   2   ... n  |n+1     n+2     ... 2n  |   ...
    # ntuple_index     |0   0   ... 0  |1       1       ... 1   |   ...
    # formula_index    |0   1   ... n-1|0       1       ... n-1 |   ...

    # in other words:
    # index == the index of a vertex,
    #   where the 0-th vertex is the central vertex
    # formula_index == (index - 1) % n
    # ntuple_index == (index - 1) // 3

    result = {'name': name, 'ntuple_index': ntuple_index, 'k_form': k_form}

    if name[1] == 'm':
        # this means we want one of the edges between the upper and lower
        # patterns
        upper_pattern = case['upper'].substitute(n=case['n'])
        lower_pattern = case['lower'].substitute(n=case['n'])
        if name[2] == 'r':
            # we want the right middle edge
            formula = get_common_edge(
                seq_1=upper_pattern.right_seq.substitute(k=k_form),
                seq_2=lower_pattern.right_seq.substitute(k=k_form),
            )

        elif name[2] == 'l':
            # we want the left middle edge
            formula = get_common_edge(
                seq_1=upper_pattern.left_seq.substitute(k=k_form),
                seq_2=lower_pattern.left_seq.substitute(k=k_form),
            )

        result['formula'] = formula.zip()
        return result

    if name[1] == 'u':
        # we want a formula form the upper pattern
        pattern = case['upper'].copy()
    elif name[1] == 'l':
        # we want a formula form the lower pattern
        pattern = case['lower'].copy()

    pattern.substitute(n=case['n'], inplace=True)
    pattern.substitute(k=k_form, inplace=True)

    if name[2] == 'c':
        # we want the central vertex or one of the edges coming from the
        # center
        if name[0] == 'v':
            # we want the central vertex
            formula = pattern.center
        elif name[0] == 'e':
            # we want one of the central edges
            if name[3] == 'l':
                # we want the center left edge
                formula = pattern.get_edge('left', 'center')
            elif name[3] == 'r':
                # we want the center right edge
                formula = pattern.get_edge('right', 'center')

        result['formula'] = formula.zip()

    else:
        if name[2] == 'l':
            # we want one of the formulas from the left sequence
            seq = pattern.left_seq

        elif name[2] == 'r':
            # we want one of the formulas from the right sequence
            seq = pattern.right_seq

        last_formula_index_mod_n = (seq.get_length_mod_n() - 1) % seq.n
        formula_index = int(name[3])

        # prepare the bound of <ntuple_index>

        bound = seq.get_ntuple_index_bound(no_formula=formula_index)
        if name[0] == 'e' and formula_index == last_formula_index_mod_n:
            # that means there is a formula with the 'ntuple index'
            # incremented, so the bound can be decremented
            bound -= 1

        # prepare the formula
        if name[0] == 'v':
            # we want the <formula_index>-th formula from te sequence
            formula = seq.formulas[formula_index].copy()

        elif name[0] == 'e':
            # we want the formula assigned to the edge between the
            # (k*n + <formula_index>)-th and the
            # (k*n + <formula_index> + 1)-th vertices of the sequence

            formula = seq.get_edge(formula_index)

        formula.substitute(
            **{seq.ntuple_index: ntuple_index}, inplace=True)

        result['formula'] = formula.zip()
        result['bound'] = bound.zip()

    return result


def print_equation(name_1, name_2, case, no_spaces=0):

    if 1 == 1:
        for i in range(len(case['k_forms'])):
            k_form = case['k_forms'][i]
            info_1 = get_data(name_1, case, ntuple_index='p', k_form=k_form)
            info_2 = get_data(name_2, case, ntuple_index='q', k_form=k_form)
            formula_1 = info_1['formula']
            formula_2 = info_2['formula']

            equation = LinearRelation(formula_1, formula_2, relation='==')

            if i == 0:
                print(f"{no_spaces*' '}{equation}")
            else:
                print(f"{no_spaces*' '}or {equation}")



