from proof_stuff.data import cases
from proof_stuff.encryption_decryption import get_names, print_equation, get_data
from proof_stuff.comparison import compare


for case in cases[:]:
    print(79*'#')

    print(f"case: n == {case['n']}")
    print(f"\t upper pattern == {case['upper']}")
    print(f"\t lower pattern == {case['lower']}")
    names = get_names(case)

    case['upper'].substitute(n=case['n'])
    case['lower'].substitute(n=case['n'])

    for k_form in case['k_forms']:

        print(f"\ncase n == {case['n']}, k == {k_form}")

        truths = 0
        falsehoods = 0
        unknowns = 0

        prev = ''
        for i in range(len(names)):
            name_1 = names[i]

            curr = name_1[1:3]
            if curr != prev:
                #print(30*'#-')
                pass

            """
            for k_form in case['k_forms']:
                info = get_data(name_1, case, k_form)
                print(f"{name_1}: {info['formula']}")
                if 'bound' in info.keys():
                    if name_1[1:3] == 'ul':
                        seq = case['upper'].left_seq.substitute(k=k_form)
                    if name_1[1:3] == 'ur':
                        seq = case['upper'].right_seq.substitute(k=k_form)
                    if name_1[1:3] == 'll':
                        seq = case['lower'].left_seq.substitute(k=k_form)
                    if name_1[1:3] == 'lr':
                        seq = case['lower'].right_seq.substitute(k=k_form)
    
                    length = seq.length
                    length_mod_n = seq.get_length_mod_n()
    
                    print(f"\t  i <= {info['bound']}, ")
                    print(f"\t  length == {length.substitute(k=k_form)}"
                          + f" == {length_mod_n} mod n")
                    print(40*'-'
                             '')
    
            """
            for name_2 in names[i:]:
                if name_1 == name_2 and (name_1[2] == 'c' or name_1[1] == 'm'):
                    # only one vertex/edge has this formula assigned
                    continue

                status, info = compare(name_1, name_2, case, k_form)
                #print(info)
                if status == 'true':
                    truths += 1
                    print(f'{name_1} == {name_2} - TRUE!!!!!!!!!!!!!!!!!!!!!')
                elif status == 'false':
                    falsehoods += 1
                elif status == 'unknown':
                    unknowns += 1
                    print(f"status unknown: {name_1} == {name_2}")

                    print_equation(name_1, name_2, case, no_spaces=4)
                    print(59*'-')
                else:
                    print(f'THERE IS A TYPO SOMEWHERE, status == {status}')
            #"""

            prev = curr

        print(f'truths: {truths}')
        print(f'falsehoods: {falsehoods}')
        print(f'unknowns: {unknowns}')

