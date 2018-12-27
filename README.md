# decembler
ElfCode disassembler for Advent of Code 2018


## Examples

Command:

```sh
python3 decembler.py --indent < 2018_19.ec
```

Output:

```
00  addi 0 16 ip -- goto 17
01  seti 1 _ b
02      seti 1 _ c
03        mulr b c d
04          eqrr d f d -- condition
05          addr d 5 ip -- branch
06          addi 6 1 ip -- goto 8
07          addr b a a
08          addi c 1 c
09          gtrr c f d -- condition
10          addr 10 d ip -- branch
11        seti 2 _ ip -- goto 3
12        addi b 1 b
13        gtrr b f d -- condition
14        addr d 14 ip -- branch
15      seti 1 _ ip -- goto 2
16      mulr 16 16 ip -- goto 257
17      addi f 2 f
18      mulr f f f
19      mulr 19 f f
20      muli f 11 f
21      addi d 4 d
22      mulr d 22 d
23      addi d 21 d
24      addr f d f
25      addr 25 a ip -- branch
26    seti 0 _ ip -- goto 1
27    setr 27 _ d
28    mulr d 28 d
29    addr 29 d d
30    mulr 30 d d
31    muli d 14 d
32    mulr d 32 d
33    addr f d f
34    seti 0 _ a
35  seti 0 _ ip -- goto 1
```

Command:

```sh
python3 decembler.py --target=c --indent < 2018_19.ec
```

Output:

```c
#include <stdio.h>

int main(int arc, char **argv) {
    int a = 0, b = 0, c = 0, d = 0, f = 0;

    goto i17;
    i1: b = 1;
            i2: c = 1;
                i3: d = b * c;
                    d = d == f ? 1 : 0;
                    if (d == 1) goto i7;
                    goto i8;
                    i7: a += b;
                    i8: c += 1;
                    d = c > f ? 1 : 0;
                    if (d == 1) goto i12;
                goto i3;
                i12: b += 1;
                d = b > f ? 1 : 0;
                if (d == 1) goto i16;
            goto i2;
            i16: goto i36;
            i17: f += 2;
            f *= f;
            f *= 19;
            f *= 11;
            d += 4;
            d *= 22;
            d += 21;
            f += d;
            if (a == 1) goto i27;
        goto i1;
        i27: d = 27;
        d *= 28;
        d += 29;
        d *= 30;
        d *= 14;
        d *= 32;
        f += d;
        a = 0;
    goto i1;
    i36:

    printf("%d\n", a);
    return 0;
}
```

```sh
python3 decembler.py --target=python < 2018_21.ec
```

Output:

```python
from goto import with_goto


@with_goto
def main():
    a = 0; b = 0; c = 0; d = 0; f = 0

    b = 123
    label.i1; b &= 456
    b = int(b == 72)
    if b == 1: goto.i5
    goto.i1
    label.i5; b = 0
    label.i6; f = b | 65536
    b = 8586263
    label.i8; c = f & 255
    b += c
    b &= 16777215
    b *= 65899
    b &= 16777215
    c = int(256 > f)
    if c == 1: goto.i16
    goto.i17
    label.i16; goto.i28
    label.i17; c = 0
    label.i18; d = c + 1
    d *= 256
    d = int(d > f)
    if d == 1: goto.i23
    goto.i24
    label.i23; goto.i26
    label.i24; c += 1
    goto.i18
    label.i26; f = c
    goto.i8
    label.i28; c = int(b == a)
    if c == 1: goto.i31
    goto.i6
    label.i31

    print(a)


if __name__ == '__main__':
    main()
```
