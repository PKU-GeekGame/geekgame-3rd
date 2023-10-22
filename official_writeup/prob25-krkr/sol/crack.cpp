#include <cstdio>
#include <cstring>
using namespace std;

const int MAX_POSSIBLE = 33333333;
const int MAX_LEN = 24;

int hash_init = 1337;
int hash_add[128];
int hash_mul = 13337;
int hash_mod = 19260817;

char possible[MAX_POSSIBLE][MAX_LEN];
char cur_possible[MAX_LEN];
int n_possible;

int n0 = 16, na = 6, ne = 3, ni = 1, no = 6;

void search_fin() {
    if(n_possible<MAX_POSSIBLE)
        memcpy(possible[n_possible], cur_possible, sizeof(cur_possible));
    n_possible++;
}

void search_possible_chars(int c0, int ca, int ce, int ci, int co) {
    if(ca>na || ce>ne || ci>ni || co>no)
        return;
    if(c0==n0) {
        search_fin();
        return;
    }

    cur_possible[c0] = 'A'; search_possible_chars(c0+1, ca+1, ce, ci, co);
    cur_possible[c0] = 'E'; search_possible_chars(c0+1, ca, ce+1, ci, co);
    cur_possible[c0] = 'I'; search_possible_chars(c0+1, ca, ce, ci+1, co);
    cur_possible[c0] = 'O'; search_possible_chars(c0+1, ca, ce, ci, co+1);
}

int calc_hash(char *s) {
    //char *old_s = s;
    unsigned long long h = hash_init;
    for(char c = s[0]; c; c=(++s)[0]) {
        h *= hash_mul;
        h += hash_add[c];
        h %= hash_mod;
    }
    h *= hash_mul;
    h += hash_add['}'];
    h %= hash_mod;
    //printf("hash %s %d\n", old_s, h);
    return int(h);
}

int main() {
    hash_add['A'] = 11;
    hash_add['E'] = 22;
    hash_add['I'] = 33;
    hash_add['O'] = 44;
    hash_add['U'] = 55;
    hash_add['}'] = 66;

    int target_hash = 7748521;

    search_possible_chars(0, 0, 0, 0, 0);

    printf("%d possible, hash is %d\n", n_possible, target_hash);

    if(n_possible>=MAX_POSSIBLE) {
        puts("overflow!");
    }

    for(int i=0; i<n_possible; i++) {
        if(calc_hash(possible[i]) == target_hash)
            printf("found: %s\n", possible[i]);
    }

    return 0;
}