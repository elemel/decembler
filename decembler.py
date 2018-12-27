# ElfCode disassembler


from collections import defaultdict
from sys import argv, stdin


def get_next_instructions(i, opcode, a, b, c, ip):
    if c == ip:
        if opcode == 'addr':
            if a == ip and b == ip:
                return [i + i + 1]
            elif a == ip:
                # Assume b in [0, 1]
                return [i + 1, i + 2]
            elif b == ip:
                # Assume b in [0, 1]
                return [i + 1, i + 2]
        elif opcode == 'addi':
            if a == ip:
                return [i + b + 1]
        elif opcode == 'mulr':
            if a == ip and b == ip:
                return [i * i + 1]
        elif opcode == 'seti':
            return [a + 1]

    return [i + 1]


def format_instruction_elfcode(i, n, opcode, a, b, c, inputs, outputs):
    if opcode == 'addr':
        return f'addr {inputs[a]} {inputs[b]} {outputs[c]}'
    elif opcode == 'addi':
        return f'addi {inputs[a]} {b} {outputs[c]}'
    elif opcode == 'mulr':
        return f'mulr {inputs[a]} {inputs[b]} {outputs[c]}'
    elif opcode == 'muli':
        return f'muli {inputs[a]} {b} {outputs[c]}'
    elif opcode == 'banr':
        return f'banr {inputs[a]} {inputs[b]} {outputs[c]}'
    elif opcode == 'bani':
        return f'bani {inputs[a]} {b} {outputs[c]}'
    elif opcode == 'borr':
        return f'borr {inputs[a]} {inputs[b]} {outputs[c]}'
    elif opcode == 'bori':
        return f'bori {inputs[a]} {b} {outputs[c]}'
    elif opcode == 'setr':
        return f'setr {inputs[a]} _ {outputs[c]}'
    elif opcode == 'seti':
        return f'seti {a} _ {outputs[c]}'
    elif opcode == 'gtir':
        return f'gtir {a} {inputs[b]} {outputs[c]}'
    elif opcode == 'gtri':
        return f'gtri {inputs[a]} {b} {outputs[c]}'
    elif opcode == 'gtrr':
        return f'gtrr {inputs[a]} {inputs[b]} {outputs[c]}'
    elif opcode == 'eqir':
        return f'eqir {a} {inputs[b]} {outputs[c]}'
    elif opcode == 'eqri':
        return f'eqri {inputs[a]} {b} {outputs[c]}'
    elif opcode == 'eqrr':
        return f'eqrr {inputs[a]} {inputs[b]} {outputs[c]}'
    else:
        raise ValueError(f'Unknown opcode: {opcode}')


def format_instruction_c(i, n, opcode, a, b, c, inputs, outputs):
    if opcode == 'addr':
        if a == c:
            if outputs[c] == 'ip':
                return f'if ({inputs[b]} == 1) goto i{i + 2};'
            else:
                return f'{outputs[c]} += {inputs[b]};'
        elif b == c:
            if outputs[c] == 'ip':
                return f'if ({inputs[a]} == 1) goto i{i + 2};'
            else:
                return f'{outputs[c]} += {inputs[a]};'
        else:
            return f'{outputs[c]} = {inputs[a]} + {inputs[b]};'
    elif opcode == 'addi':
        if a == c:
            if outputs[c] == 'ip':
                return f'goto i{i + b + 1};'
            else:
                return f'{outputs[c]} += {b};'
        else:
            return f'{outputs[c]} = {inputs[a]} + {b};'
    elif opcode == 'mulr':
        if a == b and b == c and outputs[c] == 'ip':
            j = min(i * i, n)
            return f'goto i{j};'
        elif a == c:
            return f'{outputs[c]} *= {inputs[b]};'
        elif b == c:
            return f'{outputs[c]} *= {inputs[a]};'
        else:
            return f'{outputs[c]} = {inputs[a]} * {inputs[b]};'
    elif opcode == 'muli':
        if a == c:
            return f'{outputs[c]} *= {b};'
        else:
            return f'{outputs[c]} = {inputs[a]} * {b};'
    elif opcode == 'banr':
        if a == c:
            return f'{outputs[c]} &= {inputs[b]};'
        elif b == c:
            return f'{outputs[c]} &= {inputs[a]};'
        else:
            return f'{outputs[c]} = {inputs[a]} & {inputs[b]};'
    elif opcode == 'bani':
        if a == c:
            return f'{outputs[c]} &= {b};'
        else:
            return f'{outputs[c]} = {inputs[a]} & {b};'
    elif opcode == 'borr':
        if a == c:
            return f'{outputs[c]} |= {inputs[b]};'
        elif b == c:
            return f'{outputs[c]} |= {inputs[a]};'
        else:
            return f'{outputs[c]} = {inputs[a]} | {inputs[b]};'
    elif opcode == 'bori':
        if a == c:
            return f'{outputs[c]} |= {b};'
        else:
            return f'{outputs[c]} = {inputs[a]} | {b};'
    elif opcode == 'setr':
        return f'{outputs[c]} = {inputs[a]};'
    elif opcode == 'seti':
        if outputs[c] == 'ip':
            return f'goto i{a + 1};'
        else:
            return f'{outputs[c]} = {a};'
    elif opcode == 'gtir':
        return f'{outputs[c]} = {a} > {inputs[b]} ? 1 : 0;'
    elif opcode == 'gtri':
        return f'{outputs[c]} = {inputs[a]} > {b} ? 1 : 0;'
    elif opcode == 'gtrr':
        return f'{outputs[c]} = {inputs[a]} > {inputs[b]} ? 1 : 0;'
    elif opcode == 'eqir':
        return f'{outputs[c]} = {a} == {inputs[b]} ? 1 : 0;'
    elif opcode == 'eqri':
        return f'{outputs[c]} = {inputs[a]} == {b} ? 1 : 0;'
    elif opcode == 'eqrr':
        return f'{outputs[c]} = {inputs[a]} == {inputs[b]} ? 1 : 0;'
    else:
        raise ValueError(f'Unknown opcode: {opcode}')


def format_instruction_python(i, n, opcode, a, b, c, inputs, outputs):
    if opcode == 'addr':
        if a == c:
            if outputs[c] == 'ip':
                return f'if {inputs[b]} == 1: goto.i{i + 2}'
            else:
                return f'{outputs[c]} += {inputs[b]}'
        elif b == c:
            if outputs[c] == 'ip':
                return f'if {inputs[a]} == 1: goto.i{i + 2}'
            else:
                return f'{outputs[c]} += {inputs[a]}'
        else:
            return f'{outputs[c]} = {inputs[a]} + {inputs[b]}'
    elif opcode == 'addi':
        if a == c:
            if outputs[c] == 'ip':
                return f'goto.i{i + b + 1}'
            else:
                return f'{outputs[c]} += {b}'
        else:
            return f'{outputs[c]} = {inputs[a]} + {b}'
    elif opcode == 'mulr':
        if a == b and b == c and outputs[c] == 'ip':
            j = min(i * i, n)
            return f'goto.i{j}'
        elif a == c:
            return f'{outputs[c]} *= {inputs[b]}'
        elif b == c:
            return f'{outputs[c]} *= {inputs[a]}'
        else:
            return f'{outputs[c]} = {inputs[a]} * {inputs[b]}'
    elif opcode == 'muli':
        if a == c:
            return f'{outputs[c]} *= {b}'
        else:
            return f'{outputs[c]} = {inputs[a]} * {b}'
    elif opcode == 'banr':
        if a == c:
            return f'{outputs[c]} &= {inputs[b]}'
        elif b == c:
            return f'{outputs[c]} &= {inputs[a]}'
        else:
            return f'{outputs[c]} = {inputs[a]} & {inputs[b]}'
    elif opcode == 'bani':
        if a == c:
            return f'{outputs[c]} &= {b}'
        else:
            return f'{outputs[c]} = {inputs[a]} & {b}'
    elif opcode == 'borr':
        if a == c:
            return f'{outputs[c]} |= {inputs[b]}'
        elif b == c:
            return f'{outputs[c]} |= {inputs[a]}'
        else:
            return f'{outputs[c]} = {inputs[a]} | {inputs[b]}'
    elif opcode == 'bori':
        if a == c:
            return f'{outputs[c]} |= {b}'
        else:
            return f'{outputs[c]} = {inputs[a]} | {b}'
    elif opcode == 'setr':
        return f'{outputs[c]} = {inputs[a]}'
    elif opcode == 'seti':
        if outputs[c] == 'ip':
            return f'goto.i{a + 1}'
        else:
            return f'{outputs[c]} = {a}'
    elif opcode == 'gtir':
        return f'{outputs[c]} = int({a} > {inputs[b]})'
    elif opcode == 'gtri':
        return f'{outputs[c]} = int({inputs[a]} > {b})'
    elif opcode == 'gtrr':
        return f'{outputs[c]} = int({inputs[a]} > {inputs[b]})'
    elif opcode == 'eqir':
        return f'{outputs[c]} = int({a} == {inputs[b]})'
    elif opcode == 'eqri':
        return f'{outputs[c]} = int({inputs[a]} == {b})'
    elif opcode == 'eqrr':
        return f'{outputs[c]} = int({inputs[a]} == {inputs[b]})'
    else:
        raise ValueError(f'Unknown opcode: {opcode}')


def format_instruction(target, i, n, opcode, a, b, c, inputs, outputs):
    if target == 'elfcode':
        return format_instruction_elfcode(
            i, n, opcode, a, b, c, inputs, outputs)
    elif target == 'c':
        return format_instruction_c(i, n, opcode, a, b, c, inputs, outputs)
    elif target == 'python':
        return format_instruction_python(i, n, opcode, a, b, c, inputs, outputs)
    else:
        raise ValueError(f'Unknown target: {target}')


def parse_instruction(line):
    opcode, a, b, c = line.split()
    return opcode, int(a), int(b), int(c)


def main():
    ip_line, *program_lines = stdin.read().splitlines()
    ip = int(ip_line.split()[-1])
    program = [parse_instruction(line) for line in program_lines]
    outputs = list('abcdef')
    outputs[ip] = 'ip'
    inputs = list(outputs)

    target = 'elfcode'

    if '--target=c' in argv:
        target = 'c'

    if '--target=python' in argv:
        target = 'python'

    indented = '--indent' in argv

    n = len(program)

    gotos = []

    for i, (opcode, a, b, c) in enumerate(program):
        for i2 in get_next_instructions(i, opcode, a, b, c, ip):
            if i2 != i + 1:
                i2 = min(i2, n)
                gotos.append((i, i2))

    labels = set()

    for i1, i2 in gotos:
        labels.add(i2)

    indentations = defaultdict(int)

    for i1, i2 in gotos:
        for i in range(i2 + 1, i1):
            indentations[i] += 1

    if target == 'c':
        variables = ', '.join(
            f'{name} = 0' for name in outputs if name != 'ip')

        print('#include <stdio.h>')
        print()
        print('int main(int arc, char **argv) {')
        print(f'    int {variables};')
        print()
    elif target == 'python':
        variables = '; '.join(
            f'{name} = 0' for name in outputs if name != 'ip')

        print('from goto import with_goto')
        print()
        print()
        print('@with_goto')
        print('def main():')
        print(f'    {variables}')
        print()

    for i, (opcode, a, b, c) in enumerate(program):
        inputs[ip] = i

        indentation = '' if target == 'elfcode' else '    '

        if indented:
            if target == 'elfcode':
                indentation += 2 * indentations[i] * ' '
            else:
                indentation += 4 * indentations[i] * ' '

        number = ''
        label = ''

        instruction = format_instruction(
            target, i, n, opcode, a, b, c, inputs, outputs)

        comment = ''

        if target == 'elfcode':
            width = max(1, len(str(n - 1)))
            number = f'{i:0{width}}  '

        if i in labels:
            if target == 'c':
                label = f'i{i}: '
            elif target == 'python':
                label = f'label.i{i}; '

        if target == 'elfcode':
            if opcode == 'addi' and a == ip and c == ip:
                comment = f' -- goto {i + b + 1}'
            elif opcode == 'addr' and a == ip and c == ip:
                comment = ' -- branch'
            elif opcode == 'addr' and b == ip and c == ip:
                comment = ' -- branch'
            elif opcode == 'mulr' and a == ip and b == ip and c == ip:
                comment = f' -- goto {i * i + 1}'
            elif opcode == 'seti' and c == ip:
                comment = f' -- goto {a + 1}'
            elif opcode.startswith('eq') or opcode.startswith('gt'):
                comment = ' -- condition'

        if i in labels and target == 'python' and ':' in instruction:
            print(f'{indentation}label.i{i}')
            print(f'{indentation}{instruction}')
        else:
            print(f'{number}{indentation}{label}{instruction}{comment}')

    if target == 'c':
        print(f'    i{n}:')
        print()
        print(f'    printf("%d\\n", a);')
        print(f'    return 0;')
        print('}')
    elif target == 'python':
        print(f'    label.i{n}')
        print()
        print(f'    print(a)')
        print()
        print()
        print("if __name__ == '__main__':")
        print('    main()')


if __name__ == '__main__':
    main()
