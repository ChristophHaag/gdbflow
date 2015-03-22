#include <stdio.h>

int bar(int c) {
        int d = c + 5;
        d = d - 2;
        return d;
}

int foo(int a) {
        int c = a * 2 - bar(a);
        for (int i = 0; i < 5; i++) {
                c = c - 1;
                c = c * bar(c);
        }
        return c;
}

int main(int argc, char** args) {
        int a = 15;
        int b = foo(a);
        printf("%d\n", b);
        return 0;
}
