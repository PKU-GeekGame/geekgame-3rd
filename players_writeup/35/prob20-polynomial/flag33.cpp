#include <iostream>
#include <algorithm>

int G[64] = {0x00002f6a,0x00005a72,0x000082bb,0x0000ab28,
0x0000e0ba,0x00010431,0x00012d48,0x00013ba4,
0x0001680f,0x00019b4c,0x0001a7c3,0x0001cf0c,
0x00020372,0x00022b61,0x00021699,0x00025383,
0x00026220,0x0002937a,0x0002abfb,0x0002dc98,
0x0002d6b3,0x00031c9d,0x00034098,0x00034ebc,
0x00036c65,0x0003a27d,0x0003c317,0x0003dc21,
0x00042900,0x00042a20,0x00046ca4,0x00047612,
0x00049a6e,0x0004b259,0x00050845,0x00050666,
0x000545ce,0x00055420,0x0005a3de,0x0005c550,
0x0005b2e2,0x000596fc,0x00059395,0x0005a07c,
0x00057cf8,0x00057e0a,0x00057cbd,0x0005adf7,
0x00056512,0x0005872f,0x00058e27,0x0005ad27,
0x0005936f,0x000594e2,0x000599bd,0x0005aa89,
0x0005991c,0x000579ac,0x000573b4,0x00057a8b,
0x0005a9ee,0x00058acc,0x0005aba2,0x0005b498};

const int M2[64] = {0x00000077,0x00000065,0x0000006c,0x00000063,
0x0000006f,0x0000006d,0x00000065,0x00000020,
0x00000074,0x0000006f,0x00000020,0x00000074,
0x00000068,0x00000065,0x00000020,0x00000077,
0x0000006f,0x00000072,0x0000006c,0x00000064,
0x00000020,0x0000006f,0x00000066,0x00000020,
0x00000070,0x0000006f,0x0000006c,0x00000079,
0x0000006e,0x0000006f,0x0000006d,0x00000069,
0x00000061,0x0000006c,0x00000077,0x00000065,
0x0000006c,0x00000063,0x0000006f,0x0000006d,
0x00000065,0x00000020,0x00000074,0x0000006f,
0x00000020,0x00000074,0x00000068,0x00000065,
0x00000020,0x00000077,0x0000006f,0x00000072,
0x0000006c,0x00000064,0x00000020,0x0000006f,
0x00000066,0x00000020,0x00000070,0x0000006f,
0x0000006c,0x00000079,0x0000006e,0x0000006f};

const int MOD = 998244353;

int qpow(int a, int b) {
	int r = 1;
	for(;b;b >>= 1) {
		if(b & 1) r = 1LL * a * r % MOD;
		a = 1LL * a * a % MOD;
	}
	return r;
}

int inv(int x) {
	return qpow(x, MOD - 2);
}



int A[64][64] = {};
int x[64] = {};

int main() {
//     int magic = 0xc4800000 / 128;
//     magic += MOD;
//     magic = inv(magic);
//     magic = 1LL * inv(magic) * inv(128) % MOD;
//     std::cout << magic << "\n";
    const int magic = 1LL * inv(0x3b090001) * inv(128) % MOD;

	for(int i = 0;i < 64;i++) G[i] = 1LL * G[i] * magic % MOD;
	for(int i = 0;i < 64;i++) {
		for(int j = 0;j < 64;j++) {
			if(i - j >= 0) A[i][j] = M2[i - j];
		}
	}

    //Gauss elimination on mod M, solve Ax = B
    for(int i = 0;i < 64;i++) {
        int p = i;
        for(int j = i + 1;j < 64;j++) {
            if(A[j][i] > A[p][i]) p = j;
        }
        for(int j = 0;j < 64;j++) {
            std::swap(A[i][j], A[p][j]);
        }
        std::swap(G[i], G[p]);
        int inv = ::inv(A[i][i]);
        for(int j = i + 1;j < 64;j++) {
            int t = 1LL * A[j][i] * inv % MOD;
            for(int k = i;k < 64;k++) {
                A[j][k] = (A[j][k] - 1LL * t * A[i][k]) % MOD;
                if(A[j][k] < 0) A[j][k] += MOD;
            }
            G[j] = (G[j] - 1LL * t * G[i]) % MOD;
            if(G[j] < 0) G[j] += MOD;
        }
    }
    for(int i = 63;i >= 0;i--) {
        int t = G[i];
        for(int j = i + 1;j < 64;j++) {
            t = (t - 1LL * A[i][j] * x[j]) % MOD;
            if(t < 0) t += MOD;
        }
        x[i] = 1LL * t * inv(A[i][i]) % MOD;
    }
	
	for(int i = 0;i < 40;i++) std::cout << x[i] << " ";
    std::cout << std::endl; std::cout << std::endl;
    for(int i = 0;i < 40;i++) std::cout << char(x[i]);
    std::cout << std::endl;
    return 0;
}

//flag{Welcome_t0_7hE_WorlD_Of_Po1YNoMi@l}
