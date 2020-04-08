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

def get_data(name, case, ntuple_index='i', k='k'):

    if name[1] == 'm':
        # this means we want one of the edges between the upper and lower
        # patterns
        upper_pattern = case['upper'].substitute(n=case['n'])
        lower_pattern = case['lower'].substitute(n=case['n'])
        if name[2] == 'r':
            # we want the right middle edge
            formula = get_common_edge(
                seq_1=upper_pattern.right_seq.substitute(k=k),
                seq_2=lower_pattern.right_seq.substitute(k=k),
                len_1=upper_pattern.right_len.substitute(k=k),
                len_2=lower_pattern.right_len.substitute(k=k),
            )

        elif name[2] == 'l':
            # we want the left middle edge
            formula = get_common_edge(
                seq_1=upper_pattern.left_seq.substitute(k=k),
                seq_2=lower_pattern.left_seq.substitute(k=k),
                len_1=upper_pattern.left_len.substitute(k=k),
                len_2=lower_pattern.left_len.substitute(k=k),
            )

        return {'formula': formula.zip()}

    elif name[1] == 'u':
        # we want a formula form the upper pattern
        pattern = case['upper'].substitute(n=case['n'])
    elif name[1] == 'l':
        # we want a formula form the lower pattern
        pattern = case['lower'].substitute(n=case['n'])


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
                formula = pattern.center + pattern.evaluate(-1)
            elif name[3] == 'r':
                # we want the center right edge
                formula = pattern.center + pattern.evaluate(1)

        return {'formula': formula.substitute(k=k).zip()}
    else:
        if name[2] == 'l':
            # we want one of the formulas from the left sequence
            seq = pattern.left_seq
            bound = pattern.left_len.copy()
        elif name[2] == 'r':
            # we want one of the formulas from the right sequence
            seq = pattern.right_seq
            bound = pattern.right_len.copy()

        j = int(name[3])
        if name[0] == 'v':
            # we want the <j>-th formula from te sequence
            formula = seq.formulas[j].copy()
        elif name[0] == 'e':
            # we want the formula assigned to the edge between the
            # (k*n + <j>)-th and the (k*n + <j> + 1)-th vertices of the
            # sequence
            this_vertex_number = seq.formulas[j]
            if j < seq.n - 1:
                next_vartex_number = seq.formulas[j + 1]
            else:
                # the <ntuple_index> variable in the next ntuple is
                # incremented
                next_vartex_number = seq.formulas[0].substitute(
                    **{seq.ntuple_index: LinearFormula(seq.ntuple_index) + 1})

            # the next index is less than <bound> and
            # 'next index' == 'index' + 1 so 'index' <= <bound> - 1
            bound -= 1

            formula = this_vertex_number + next_vartex_number


        formula.substitute(
            **{seq.ntuple_index: ntuple_index}, inplace=True)

        index = seq.n*LinearFormula(ntuple_index) + j + 1

    return {
        'formula': formula.substitute(k=k).zip(),
        'index': index.substitute(k=k).zip(),
        'index bound': bound.substitute(k=k).zip()
    }


def print_equation(name_1, name_2, case, no_spaces=0):

    if name_1[1] == 'm' or name_2[1] == 'm':
        for i in range(len(case['k_forms'])):
            k_form = case['k_forms'][i]
            info_1 = get_data(name_1, case, ntuple_index='p', k=k_form)
            info_2 = get_data(name_2, case, ntuple_index='p', k=k_form)
            formula_1 = info_1['formula']
            formula_2 = info_2['formula']

            equation = LinearRelation(formula_1, formula_2, relation='==')

            if i == 0:
                print(f"{no_spaces*' '}{equation}")
            else:
                print(f"{no_spaces*' '}or {equation}")

    else:
        formula_1 = get_data(name_1, case, ntuple_index='p')['formula']
        formula_2 = get_data(name_2, case, ntuple_index='p')['formula']
        equation = LinearRelation(formula_1, formula_2, relation='==')

        print(f"{no_spaces*' '}{equation}")

