#include <bits/stdc++.h>

using i64 = int64_t;
using u32 = uint32_t;
using u64 = uint64_t;
const int N = 1 << 18;
const int P = 998244353;
struct mint {
    int x;
    constexpr mint(int x = 0) : x(x) {}
    mint operator-() const { return x > 0 ? P - x : 0; }
    mint operator+(mint o) const { return x + o.x < P ? x + o.x : x + o.x - P; }
    mint operator-(mint o) const { return x - o.x < 0 ? x - o.x + P : x - o.x; }
    mint operator*(mint o) const { return int(u64(x) * o.x % P); }
    mint &operator+=(mint o) { return *this = *this + o; }
    mint &operator-=(mint o) { return *this = *this - o; }
    mint &operator*=(mint o) { return *this = *this * o; }
    friend std::istream &operator>>(std::istream &stream, mint &o) {
        return stream >> o.x;
    }
    friend std::ostream &operator<<(std::ostream &stream, const mint o) {
        return stream << o.x;
    }
    mint pow(auto k) const {
        mint a = x, b = 1;
        for (; k; k >>= 1) {
            if (k & 1)
                b *= a;
            a *= a;
        }
        return b;
    }
};

mint w[N], inv[N];
int secret1[N] = {
    3318,      382207753, 141261786, 100396702, 617742273, 385313506,
    368063237, 562832377, 857094849, 53657966,  669496487, 605913203,
    29815074,  762568211, 133958153, 223410103, 39956957,  937802638,
    229055941, 767816204, 13414714,  795034084, 184947163, 171452954,
    272370098, 484621960, 430570773, 639750081, 695262892, 144991146,
    292318513, 573477240, 867813853, 798543925, 12064634,  874910184};
// int secret1[N] = {
//     3248,      378307500, 220035540, 36217053,  15037521,  636731203,
//     253121527, 962303647, 924420392, 374460793, 552722193, 955571243,
//     936236148, 541274684, 239908146, 352193242, 766365341, 741498875,
//     14235004,  479253734, 430434674, 619359145, 740978925, 827954630,
//     508083751, 161220016, 250049968, 670378662, 326051547, 97412815,
//     939103629, 761483063, 256003299, 591972456, 169239199, 718023480,
//     260041569, 361895413};
int secret2[N] = {
    3913,      289,       834948607, 163295812, 164439607, 161387332, 974222553,
    696438338, 539639385, 986903620, 106289859, 404416193, 805106158, 179213337,
    538371828, 433037208, 770311363, 143811316, 405961750, 926667225, 154723882,
    917997195, 940817662, 220282765, 132546338, 59755894,  849443454, 596045415,
    942514135, 799299172, 80733054,  45046108,  553902994, 355906234, 474404409,
    186060267, 553954109, 860251876, 223543265, 340419654, 606850118, 935293719,
    61439386,  993172762, 119863683, 517515582, 635476920, 403840414, 774901779,
    274609474, 928702211, 85357822,  717387150, 891458018, 928871940, 864971562,
    210679787, 793989340, 552081800, 905298318, 141898642, 215002345, 400512085,
    462537392,
};
// int secret2[N] = {
//     4044,      260,       122280849, 875963624, 219400745, 657072241,
//     916977347, 203038309, 521851449, 32763016,  34212743,  918793169,
//     89493553,  885306356, 309363029, 202949944, 721197810, 300609449,
//     143350168, 750845327, 272042532, 164024995, 701532933, 83154836,
//     744443470, 973308676, 544323870, 457464214, 825703669, 568880617,
//     935272952, 798045435, 561448197, 41562541,  272875159, 210026489,
//     774400145, 665322830, 948362770, 551564167, 469640431, 25402613,
//     627224338, 151035716, 676022843, 782921964, 140098468, 352832577,
//     993313509, 710416883, 706388258, 365470131, 731174119, 929040156,
//     778290095, 828248253, 190074940, 116670606, 155192638, 951619328,
//     862784259, 374197252, 786152945, 240378421};
int key[N] = {0x77, 0x65, 0x6c, 0x63, 0x6f, 0x6d, 0x65, 0x20, 0x74,
              0x6f, 0x20, 0x74, 0x68, 0x65, 0x20, 0x77, 0x6f, 0x72,
              0x6c, 0x64, 0x20, 0x6f, 0x66, 0x20, 0x70, 0x6f, 0x6c,
              0x79, 0x6e, 0x6f, 0x6d, 0x69, 0x61, 0x6c};
int secret3[N] = {
    12138,  23154,  33467,  43816,  57530,  66609,  77128,  80804,
    92175,  105292, 108483, 118540, 131954, 142177, 136857, 152451,
    156192, 168826, 175099, 187544, 186035, 203933, 213144, 216764,
    224357, 238205, 246551, 252961, 272640, 272928, 289956, 292370,
    301678, 307801, 329797, 329318, 345550, 349216, 369630, 378192,
    373474, 366332, 365461, 368764, 359672, 359946, 359613, 372215,
    353554, 362287, 364071, 372007, 365423, 365794, 367037, 371337,
    366876, 358828, 357300, 359051, 371182, 363212, 371618, 373912};
// int secret3[N] = {
//     9996,   17052,  26459,  32650,  42395,  49613,  63179,  69122,
//     77704,  85131,  87333,  100644, 107416, 111941, 115375, 131468,
//     130516, 144179, 155752, 169303, 166639, 174194, 190180, 192094,
//     199325, 199918, 212672, 221850, 226439, 236878, 254711, 257231,
//     274507, 286052, 291166, 312436, 322142, 323713, 327209, 337494,
//     343489, 341338, 347061, 349708, 338284, 348734, 347322, 342320,
//     337503, 348914, 340330, 343701, 350243, 353463, 339164, 332328,
//     352040, 347480, 345419, 339799, 347503, 343569, 352145, 350800};

void __attribute__((constructor)) init() {
    w[N / 2] = 1;
    mint g = mint(3).pow(P / N);
    for (int i = N / 2 + 1; i < N; i++)
        w[i] = w[i - 1] * g;
    for (int i = N / 2 - 1; i > 0; --i)
        w[i] = w[i << 1];

    inv[0] = inv[1] = 1;
    for (int i = 2; i < N; i++)
        inv[i] = inv[P % i] * (P - P / i);
}

void fft(mint f[], int n) {
    int k = n;
    while (k > 1) {
        k /= 2;
        for (int i = 0; i < n; i += k * 2)
            for (int j = 0; j < k; ++j) {
                mint w1 = w[j + k];
                mint x0 = f[i + j], x1 = f[i + j + k];
                f[i + j] = (x0 + x1);
                f[i + j + k] = (x0 - x1) * w1;
            }
    }
}

void ift(mint f[], int n) {
    int k = 1;
    while (k * 2 <= n) {
        for (int i = 0; i < n; i += k * 2)
            for (int j = 0; j < k; ++j) {
                mint w1 = w[j + k];
                mint x0 = f[i + j], x1 = f[i + j + k] * w1;
                f[i + j] = x0 + x1;
                f[i + j + k] = x0 - x1;
            }
        k *= 2;
    }
    mint inv = P - (P - 1) / n;
    std::reverse(f + 1, f + n);
    for (int i = 0; i < n; i++)
        f[i] *= inv;
}

// std::string flag1 = "flag{yoU_Are_THE_mA$T3r_of_l@gR4nGe}";
// std::string flag1 = "THUCTF{Y0u_aRe_7H3_mAs7Er_OF_lA6R4nge}";
int challenge1() {
    std::cout << "Welcome to the challenge1!" << std::endl;

    std::string input;
    std::cout << "Please input the flag: ";
    std::cin >> input;

    int len = input.length();
    if (len != 36) {
        // if (len != 38) {
        std::cout << "Failed, please try again!" << std::endl;
        return 1;
    }

    mint *a = (mint *)malloc(len * sizeof(mint));
    memset(a, 0, len * sizeof(mint));
    for (int i = 0; i < len; i++)
        a[i] = input[i];

    for (int x = 1; x <= len; x++) {
        mint ans = 0, tmp = 1;
        for (int i = 0; i < len; i++) {
            ans += a[i] * tmp;
            tmp *= x;
        }
        if (ans.x != secret1[x - 1]) {
            std::cout << "Failed, please try again!" << std::endl;
            return 1;
        }
        // std::cout << ans.x << ", ";
    }
    std::cout << "Congratulations! You got the flag1!" << std::endl;

    free(a);
    return 0;
}

// std::string flag2 = "flag{yOU_kN0w_wH47_1S_f4$t_fOuRiEr_7r4n$F0RM}"
// std::string flag2 = "THUCTF{Y0U_kNow_WhaT_1s_fA$t_F0uri3R_TR@n$F0rM}"
int challenge2() {
    std::cout << "Welcome to the challenge2!" << std::endl;

    std::string input;
    std::cout << "Please input the flag: ";
    std::cin >> input;

    int len = input.length();
    if (len != 45) {
        // if (len != 47) {
        std::cout << "Failed, please try again!" << std::endl;
        return 1;
    }

    int m = len;
    int n = 2 << std::__lg(m);
    mint *a = (mint *)malloc(n * sizeof(mint));
    memset(a, 0, n * sizeof(mint));
    for (int i = 0; i < len; i++)
        a[i] = input[i];

    fft(a, n);
    for (int i = 0; i < n; i++) {
        if (a[i].x != secret2[i]) {
            std::cout << "Failed, please try again!" << std::endl;
            return 1;
        }
        // std::cout << a[i].x << ", ";
    }
    std::cout << "Congratulations! You got the flag2!" << std::endl;

    free(a);
    return 0;
}

// std::string flag3 = "flag{Welcome_t0_7hE_WorlD_Of_Po1YNoMi@l}";
// std::string flag3 = "THUCTF{wELCoME_T0_thE_W0r1D_0f_poLynoM141}";
int challenge3() {
    std::cout << "Welcome to the challenge3!" << std::endl;

    std::string input;
    std::cout << "Please input the flag: ";
    std::cin >> input;

    int len = input.length();
    if (len != 40) {
        // if (len != 42) {
        std::cout << "Failed, please try again!" << std::endl;
        return 1;
    }

    int m = len;
    int n = 2 << std::__lg(m);
    mint *a = (mint *)malloc(n * 2 * sizeof(mint));
    mint *b = (mint *)malloc(n * 2 * sizeof(mint));
    memset(a, 0, n * 2 * sizeof(mint));
    memset(b, 0, n * 2 * sizeof(mint));
    for (int i = 0; i < m; i++)
        a[i] = input[i];
    for (int i = 0; i < n; i++)
        b[i] = key[i % 34];

    fft(a, n * 2);
    fft(b, n * 2);
    for (int i = 0; i < n * 2; i++)
        a[i] *= b[i];
    ift(a, n * 2);
    for (int i = 0; i < n; i++) {
        if (a[i].x != secret3[i]) {
            std::cout << "Failed, please try again!" << std::endl;
            return 1;
        }
        // std::cout << a[i].x << ", ";
    }
    std::cout << "Congratulations! You got the flag3!" << std::endl;

    free(a);
    free(b);
    return 0;
}

int main() {
    std::cout << "Welcome to the world of polynomial!" << std::endl;
    std::cout << "1. baby_poly" << std::endl;
    std::cout << "2. easy_poly" << std::endl;
    std::cout << "3. hard_poly" << std::endl;
    std::cout << "Please choose the challenge you want to solve: ";

    int choice;
    std::cin >> choice;
    switch (choice) {
    case 1:
        return challenge1();
    case 2:
        return challenge2();
    case 3:
        return challenge3();
    default:
        std::cout << "Invalid choice!" << std::endl;
        return 1;
    }

    return 0;
}
