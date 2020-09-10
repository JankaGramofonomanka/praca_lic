from proof_stuff.source.data import cases
from proof_stuff.source.proof_loops import prove_target_set, prove_1_to_1

for case in cases:

    case['upper'].substitute(n=case['n'], inplace=True)
    case['lower'].substitute(n=case['n'], inplace=True)

big_sep = "\n" + 79*"#" + "\n"
small_sep = 49*"*"

print(big_sep)
print((
        "Checking the status of the statement "
        + "\n\t0 <= f(t,i) <= 2n for all f, t, i, in all cases"
    ))
print(big_sep)

for case in cases:
    print(small_sep)

    for k_form in case['k_forms']:

        print(30*'-')
        print(f"case n == {case['n']}, k == {k_form}")

        prove_target_set(case, k_form)

print(big_sep)
print((
        "Checking the status of the statement "
        + "\n\tf1(t,i) == f2(t, j) for all f1, f2, t, i, j, in all cases"
    ))
print(big_sep)

for case in cases[:]:
    print(small_sep)

    for k_form in case['k_forms']:
        print(30 * '-')
        print(f"case n == {case['n']}, k == {k_form}")

        prove_1_to_1(case, k_form)

print("Press Enter to exit.")
input()
