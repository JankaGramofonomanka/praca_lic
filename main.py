from proof_stuff.source.data import cases
from proof_stuff.source.proof_loops import prove_target_set, prove_1_to_1

for case in cases:

    case['upper'].substitute(n=case['n'], inplace=True)
    case['lower'].substitute(n=case['n'], inplace=True)

for case in cases:
    print(79*'#')

    for k_form in case['k_forms']:

        print(30*'-')
        print(f"case n == {case['n']}, k == {k_form}")

        prove_target_set(case, k_form)

for case in cases[:]:
    print(79 * '#')

    for k_form in case['k_forms']:
        print(30 * '-')
        print(f"case n == {case['n']}, k == {k_form}")

        prove_1_to_1(case, k_form)

