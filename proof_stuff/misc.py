from numbering_patterns import LinearFormula

def get_common_edge(seq_1, seq_2):

    no_formula_1 = (seq_1.get_length_mod_n() - 1) % seq_1.n
    no_formula_2 = (seq_2.get_length_mod_n() - 1) % seq_2.n

    ntuple_index_1 = ((seq_1.length - 1) - ((seq_1.length - 1) % seq_1.n))
    ntuple_index_1.zip(inplace=True)
    ntuple_index_1 /= seq_1.n

    ntuple_index_2 = ((seq_2.length - 1) - ((seq_2.length - 1) % seq_2.n))
    ntuple_index_2.zip(inplace=True)
    ntuple_index_2 /= seq_2.n

    formula_1 = seq_1.formulas[no_formula_1].substitute(
        **{seq_1.ntuple_index: ntuple_index_1})
    formula_2 = seq_2.formulas[no_formula_2].substitute(
        **{seq_2.ntuple_index: ntuple_index_2})

    formula = formula_1 + formula_2
    formula.zip(inplace=True)

    return formula


def get_formula_with_index(formula, index, index_var):
    m, remainer = formula.separate(index)

    result = m * LinearFormula(index_var) + remainer
    result.zip(inplace=True)

    return result


def get_variable_bounds(*infos):
    upper_bounds = {}
    lower_bounds = {'t': 1}
    order = []

    for info in infos:
        if 'bound' in info.keys():
            upper_bounds[info['ntuple_index']] = info['bound']
            lower_bounds[info['ntuple_index']] = 0
            order.append(info['ntuple_index'])

    order.append('t')

    return lower_bounds, upper_bounds, order





