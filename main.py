from proof_stuff.data import cases
from proof_stuff.encryption_decryption import get_names, print_equation, get_data
from proof_stuff.comparison import compare, in_target_set

def display(case, k_form):

    names = get_names(case)
    for name in names:
        info = get_data(name, case, k_form)
        print(f"{name}: {info['formula']}")
        if 'bound' in info.keys():
            if name[1:3] == 'ul':
                seq = case['upper'].left_seq.substitute(k=k_form)
            if name[1:3] == 'ur':
                seq = case['upper'].right_seq.substitute(k=k_form)
            if name[1:3] == 'll':
                seq = case['lower'].left_seq.substitute(k=k_form)
            if name[1:3] == 'lr':
                seq = case['lower'].right_seq.substitute(k=k_form)

            length = seq.length
            length_mod_n = seq.get_length_mod_n()

            print(f"\t  i <= {info['bound']}, ")
            print(f"\t  length == {length.substitute(k=k_form)}"
                  + f" == {length_mod_n} mod n")
            print(40*'-')

    print()

def prove_1_to_1(case, k_form):

    print("numbering is 1 to 1")
    print("desired status: false")

    truths = 0
    falsehoods = 0
    unknowns = 0

    names = get_names(case)

    prev = ''
    for i in range(len(names)):
        name_1 = names[i]

        curr = name_1[1:3]
        if curr != prev:
            # print(30*'#-')
            pass

        for name_2 in names[i:]:
            if name_1 == name_2 and (name_1[2] == 'c' or name_1[1] == 'm'):
                # only one vertex/edge has this formula assigned
                continue

            status, info = compare(name_1, name_2, case, k_form)
            # print(info)
            if status == 'true':
                truths += 1
                print(f'{name_1} == {name_2} - TRUE!!!!!!!!!!!!!!!!!!!!!')

            elif status == 'false':
                falsehoods += 1

            elif status == 'unknown':
                unknowns += 1
                print(f"status unknown: {name_1} == {name_2}")

                print_equation(name_1, name_2, case, no_spaces=4)
                print(59 * '-')
            else:
                print(f'THERE IS A TYPO SOMEWHERE, status == {status}')
        # """

        prev = curr

    print(f'truths: {truths}')
    print(f'falsehoods: {falsehoods}')
    print(f'unknowns: {unknowns}')
    print()

def prove_target_set(case, k_form):

    print("formulas in target set")
    print("desired status: true")

    truths = 0
    falsehoods = 0
    unknowns = 0

    for name in get_names(case):

        status = in_target_set(name, case, k_form)
        if status == 'false':
            falsehoods += 1
            print(f'{name} in target set - FALSE!!!!!!!!!!!!!!!!!!!!!')

        elif status == 'true':
            truths += 1

        elif status == 'unknown':
            unknowns += 1
            print(f"status unknown: {name} in target set")

            print(59 * '-')
        else:
            print(f'THERE IS A TYPO SOMEWHERE, status == {status}')


    print(f'truths: {truths}')
    print(f'falsehoods: {falsehoods}')
    print(f'unknowns: {unknowns}')
    print()

for case in cases[:]:
    print(79*'#')

    print(f"case: n == {case['n']}")
    print(f"\t upper pattern == {case['upper']}")
    print(f"\t lower pattern == {case['lower']}")
    print()

    case['upper'].substitute(n=case['n'])
    case['lower'].substitute(n=case['n'])

    for k_form in case['k_forms']:

        print(30*'-')
        print(f"case n == {case['n']}, k == {k_form}")

        #display(case, k_form)
        prove_target_set(case, k_form)
        prove_1_to_1(case, k_form)

