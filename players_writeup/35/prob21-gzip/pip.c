#include <unistd.h>
#include <signal.h>
#include <stdio.h>

const int BSIZE = 1 << 20;
char buf[BSIZE];

long long bc = 0;
const long long S = 7 * (1LL << 40);

void sig_handler(int sig) {
    fprintf(stderr, "size=%lld, %.3lf%%\n", bc, 1.0 * bc / S);
}

int main() {
    signal(SIGUSR1, sig_handler);
    for(int s; s = read(STDIN_FILENO, buf, BSIZE); ) {
        bc += s;
        int p = 0;
        for(;p < s && !buf[p];p++);
        if(p >= s) continue;
        for(;p < s && buf[p];p++) {
            write(STDOUT_FILENO, buf + p, 1);
        }
        if(p >= s) {
            char c;
            while(read(STDIN_FILENO, &c, 1) && c) {
                write(STDOUT_FILENO, &c, 1);
            }
        }
        break;
    }
    return 0;
}

// 23:02
// 3:38