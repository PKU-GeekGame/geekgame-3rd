#include <stdio.h>
#include <string.h>

void init() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
}
int main() {
    init();
    char flag[32];
    puts("please enter your flag~(less than 0x20 characters)");
    scanf("%s", flag);
    int t = strlen(flag);
    if (t > 32) {
        puts("byebye~");
        return 0;
    }
    printf("this is your flag: ");
    printf(flag);
    puts("\nWhat will you do to capture it?:");
    char capture[64];
    scanf("%s", capture);
    printf("so you want to \n");
    printf(capture);
    printf("\n and your flag again? :");
    scanf("%s", flag);
    puts(flag);
    puts("go0d_j0b_und_go0d_luck~:)");
    return 0;
}