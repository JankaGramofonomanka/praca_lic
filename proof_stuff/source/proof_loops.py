from .encryption_decryption import get_names, print_equation
from .main_proofs import compare, in_target_set

def prove_1_to_1(case, k_form):

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

    print(f':( truths: {truths}')
    print(f':) falsehoods: {falsehoods}')
    print(f':| unknowns: {unknowns}')
    print()

def prove_target_set(case, k_form):

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

    print(f':) truths: {truths}')
    print(f':( falsehoods: {falsehoods}')
    print(f':| unknowns: {unknowns}')
    print()







