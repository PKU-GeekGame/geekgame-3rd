#include <iostream>
#include <algorithm>

int B[36] = {0x00000cf6,0x16c80709,0x086b7bda,0x05fbee9e,
0x24d1ffc1,0x16f76ae2,0x15f03305,0x218c23f9,
0x33163ac1,0x0332c16e,0x27e7b4a7,0x241d8073,
0x01c6f122,0x2d73de13,0x07fc0a09,0x0d50f7b7,
0x0261b1dd,0x37e5bb8e,0x0da71dc5,0x2dc3f20c,
0x00ccb13a,0x2f6341e4,0x0b0611db,0x0a382a1a,
0x103c09b2,0x1ce2be88,0x19a9fd15,0x2621cfc1,
0x2970deac,0x08a463aa,0x116c6d31,0x222e9178,
0x33b9c9dd,0x2f98d035,0x00b8177a,0x342611e8};

int A[36][36];

const int M = 998244353;

int qpow(int a, int b) {
    int r = 1;
    for(;b;b >>= 1) {
        if(b & 1) r = 1ll * r * a % M;
        a = 1ll * a * a % M;
    }
    return r;
}

int x[36];

void gauss() {
    // gauss elimination on mod M, solve Ax = B
    for(int i = 0;i < 36;i++) {
        int p = i;
        for(int j = i + 1;j < 36;j++) {
            if(A[j][i] > A[p][i]) p = j;
        }
        for(int j = 0;j < 36;j++) {
            std::swap(A[i][j], A[p][j]);
        }
        std::swap(B[i], B[p]);
        int inv = qpow(A[i][i], M - 2);
        for(int j = i + 1;j < 36;j++) {
            int t = 1ll * A[j][i] * inv % M;
            for(int k = i;k < 36;k++) {
                A[j][k] = (A[j][k] - 1ll * t * A[i][k]) % M;
                if(A[j][k] < 0) A[j][k] += M;
            }
            B[j] = (B[j] - 1ll * t * B[i]) % M;
            if(B[j] < 0) B[j] += M;
        }
    }
    for(int i = 35;i >= 0;i--) {
        int t = B[i];
        for(int j = i + 1;j < 36;j++) {
            t = (t - 1ll * A[i][j] * x[j]) % M;
            if(t < 0) t += M;
        }
        x[i] = 1ll * t * qpow(A[i][i], M - 2) % M;
    }
}

int main() {
    for(int i = 0;i < 36;i++) {
        int r = 1;
        for(int j = 0;j < 36;j++) {
            A[i][j] = r;
            r = 1ll * r * (i + 1) % M;
        }
    }
    gauss();
    for(int i = 0;i < 36;i++) {
        std::cout << char(x[i]);
    }
    std::cout << std::endl;
    return 0;
}