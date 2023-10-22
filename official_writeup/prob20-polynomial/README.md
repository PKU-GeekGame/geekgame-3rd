# [Binary] 绝妙的多项式

- 命题人：Yasar
- Baby：250 分
- Easy：250 分
- Hard：200 分

## 题目描述

<blockquote>
<p>Welcome to the world of polynomial!</p>
</blockquote>
<p>小Y是一个计算机系的同学，但是非常不幸的是他需要上很多的数学专业课。</p>
<p>某一天，他正看着书上一堆式子发呆的时候，突然灵光一闪，想到几个绝妙的多项式。</p>
<p>他想考考你能不能猜出多项式是多少？</p>
<p><em>当然大家都不会读心术，小Y给了你一些信息</em></p>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>ChatGPT 或许能帮你辨认出小 Y 给的信息。</li>
<li>如何在 Zp 空间中进行除法，对多项式是否有类似的方法？</li>
</ul>
</div>

**[【附件：下载题目附件（prob20-poly.zip）】](attachment/prob20-poly.zip)**

## 预期解法

将输入的 `flag` 转化成次数为 `n = len(flag)` 的多项式 `f(x)`，给出了一些信息，需要还原多项式。

题目源码见 [src](src/) 目录。

### flag1

给出了 `x=1, 2, 3, ..., n` 时 `f(x)` 的取值，存在唯一的 `n` 次多项式满足这些条件，可以用拉格朗日插值法还原多项式。

```python
t = sympy.Symbol("t")
poly = sympy.poly(0, t, domain=GF(mod))
for i in range(n):
    tmp = sympy.poly(y[i], t, domain=GF(mod))
    for j in range(n):
        if i != j:
            tmp *= sympy.poly(t - x[j], t, domain=GF(mod)) * sympy.poly(
                pow(x[i] - x[j], mod - 2, mod),
                t,
                domain=GF(mod),
            )
    poly += tmp
```

### flag2

```cpp
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
```

将 `f(x)` 传入一个函数进行了某种操作，自行分析函数或将反编译的伪代码询问 ChatGPT 可以得知这是快速数论变换(NTT)，进行逆变换即可还原多项式，也可以直接调用二进制程序中的逆变换函数。

```cpp
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
```

### flag3

```cpp
...
    fft(a, n * 2);
    fft(b, n * 2);
    for (int i = 0; i < n * 2; i++)
        a[i] *= b[i];
    ift(a, n * 2);
...
```

这里是使用快速数论变换(NTT)实现了多项式乘法，$f(x), g(x) \in \Z_p[x]$，已知 $g(x)$ 和 $f(x) * g(x) \bmod x^n$，需要求 $g(x)$ 在模 $x^n$ 下的逆元。

可以使用 $O(n\log n)$ 的多项式求逆，也可以直接 $O(n^2)$

```cpp
void Inv(const mint a[], mint f[], int n) {
    if (n == 1) {
        f[0] = a[0].inv();
    } else {
        Inv(a, f, n / 2);
        mint *A = (mint *)malloc(n * 2 * sizeof(mint));
        mint *F = (mint *)malloc(n * 2 * sizeof(mint));
        memset(A, 0, n * 2 * sizeof(mint));
        memset(F, 0, n * 2 * sizeof(mint));

        for (int i = 0; i < n; i++)
            A[i] = a[i];
        for (int i = 0; i < n / 2; i++)
            F[i] = f[i];

        fft(A, n * 2);
        fft(F, n * 2);
        for (int i = 0; i < n * 2; i++)
            F[i] = F[i] * (mint(2) - A[i] * F[i]);
        ift(F, n * 2);

        for (int i = n / 2; i < n; i++)
            f[i] = F[i];

        free(A);
        free(F);
    }
}
```