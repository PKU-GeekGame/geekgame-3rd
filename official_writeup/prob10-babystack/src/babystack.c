#include <stdio.h>

void backdoor() {
    system("/bin/sh");
}

void get_line(char* buffer, int size) {
    unsigned int i = 0;
    for (i = 0; i < size - 1; i++) {
        read(0, buffer + i, 1);
        if (buffer[i] == '\n') {
            buffer[i] = '\0';
            break;
        }
    }
}

void __init__() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int main() {
    __init__();
    char buffer[100] = "\0";
    printf("Welcome to babystack:)\n");
    int size;
    printf("input the size of your exploitation string:(less than 100 chars with the ending \\n or EOF included!)\n");
    scanf("%d", &size);
    if ((size > 100) || (size < 0)) {
        printf(":(\n");
        return 0;
    }
    printf("please input your string:\n");
    get_line(buffer, size);
    return 0;
}