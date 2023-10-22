#include <cstdio>
#include <cstring>
#include <string>
using namespace std;
const int MOD = 19260817;
const int M = 13337;
// a6e3i1o6u0
const int v[] = {11, 22, 33, 44, 55};
const char c[] = "AEIOU";
int qpow(int a,int b) {
    int r = 1;
    for(;b;b>>=1) {
        if(b&1) r = 1LL * r * a % MOD;
        a = 1LL * a * a % MOD;
    }
    return r;
}
long long pow_(int a, int b)  {
    // not mod
    long long r = 1;
    for(;b;b>>=1) {
        if(b&1) r = r * a;
        a = a * a;
    }
    return r;
}
void up(int &x, int y) {
    if((x += y) >= MOD) x -= MOD;
}
void down(int &x, int y) {
    if((x -= y) < 0) x += MOD;
}

int ch[16] = {0};

int ans = 7748521;

int __cnt = 0;
int __sols = 0;

void judge() {
    printf("check %d\n", ++__cnt);
    int ret = 0;
    for(int i = 0;i < 16;i++) {
        ret = 1LL * ret * M % MOD;
        up(ret, ch[i] * 11);
    }
    ret = 1LL * ret * M % MOD;
    if(ret == ans) {
        ++__sols;
        for(int i = 0;i < 16;i++) {
            fprintf(stderr,"%c", c[ch[i] - 1]);
        }
        fprintf(stderr,"\n");
    }
}

void insert_e() {
    // insert e * 4
    for(int i = 0; i < 16;i++) if(!ch[i]) ch[i] = 2;
    // replace one i
    for(int i = 0;i < 16;i++) {
        if(ch[i] == 2) {
            ch[i] = 3;
            judge();
            ch[i] = 2;
        }
    }
    // restore e
    for(int i = 0; i < 16;i++) if(ch[i] == 2) ch[i] = 0;
}

void dfs_o(int p, int cnt) {
    if(p == 16) {
        if(cnt != 6) return;
        insert_e();
        return;
    }
    if(!ch[p] && cnt < 6) {
        ch[p] = 4;
        dfs_o(p + 1, cnt + 1);
        ch[p] = 0;
    }
    dfs_o(p + 1, cnt);
}

void dfs_a(int p, int cnt) {
    if(p == 16) {
        if(cnt != 6) return;
        dfs_o(0, 0);
        return;
    }
    if(!ch[p] && cnt < 6) {
        ch[p] = 1;
        dfs_a(p + 1, cnt + 1);
        ch[p] = 0;
    }
    dfs_a(p + 1, cnt);
}

int main() {
    
    down(ans, 1337LL * qpow(M, 17) % MOD);
    down(ans, 66);
    // c1 * M16 + ... + c16 * M1 === ans mod MOD
    dfs_a(0,0);
    printf("sols = %d\n", __sols);
    return 0;
}