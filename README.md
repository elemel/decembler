# decembler
ElfCode disassembler for Advent of Code 2018


## Example

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
