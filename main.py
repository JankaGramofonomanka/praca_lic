from proof_stuff.data import cases
from proof_stuff.encryption_decryption import get_names, print_equation
from proof_stuff.comparison import compare


for case in cases[:]:
    print(79*'-')

    print(f"case: n == {case['n']}")
    print(f"\t upper pattern == {case['upper']}")
    print(f"\t lower pattern == {case['lower']}")
    names = get_names(case)

    truths = 0
    falsehoods = 0
    unknowns = 0

    prev = ''
    for name_1 in names:
        curr = name_1[1:3]
        if curr != prev:
            print(60*'-')

        for name_2 in names:
            if name_1 == name_2 and (name_1[2] == 'c' or name_1[1] == 'm'):
                # only one vertex/edge has this formula assigned
                continue

            status = compare(name_1, name_2, case)
            if status == 'true':
                truths += 1
                print(f'{name_1} == {name_2} - TRUE!!!!!!!!!!!!!!!!!!!!!')
            elif status == 'false':
                falsehoods += 1
            elif status == 'unknown':
                unknowns += 1
                print(f"status unknown: {name_1} == {name_2}\n{59*'-'}")

                #print_equation(name_1, name_2, case, no_spaces=4)
            else:
                print(f'THERE IS A TYPO SOMEWHERE, status == {status}')

        prev = curr

    print(f'truths: {truths}')
    print(f'falsehoods: {falsehoods}')
    print(f'unknowns: {unknowns}')

