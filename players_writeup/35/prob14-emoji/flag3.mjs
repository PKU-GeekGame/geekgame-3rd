import ky from 'ky'
import Jwt from 'jsonwebtoken'

const url = 'https://prob14.geekgame.pku.edu.cn/level3'

const elib = ["🐐","🐑","🐒","🐓","🐔","🐕","🐖","🐗","🐘","🐙","🐚","🐛","🐜","🐝","🐞","🐟","🐠","🐡","🐢","🐣","🐤","🐥","🐦","🐧","🐨","🐩","🐪","🐫","🐬","🐭","🐮","🐯","🐰","🐱","🐲","🐳","🐴","🐵","🐶","🐷","🐸","🐹","🐺","🐻","🐼","🐽","🐾","🐿","👀","👁","👂","👃","👄","👅","👆","👇","👈","👉","👊","👋","👌","👍","👎","👏","👐","👑","👒","👓","👔","👕","👖","👗","👘","👙","👚","👛","👜","👝","👞","👟","👠","👡","👢","👣","👤","👥","👦","👧","👨","👩","👪","👫","👬","👭","👮","👯","👰","👱","👲","👳","👴","👵","👶","👷","👸","👹","👺","👻","👼","👽","👾","👿","💀","💁","💂","💃","💄","💅","💆","💇","💈","💉","💊","💋","💌","💍","💎","💏"]

async function initial() {
    const resp = await ky.get(url)
    const cookie = resp.headers.get('set-cookie')
    const rawtok = cookie.match(/PLAY_SESSION=([^;]+);/)[1]
    const token = Jwt.decode(rawtok)
    return token.data.seed
}

async function trial(seed, ans) {
    const now = +new Date()
    const token = Jwt.sign({
        data: {
            level: '3',
            start_time: ""+now,
            remaining_guesses: '2',
            seed: seed
        },
        nbf: now / 1000,
        iat: now / 1000
    }, ' ')
    const resp = await ky.get(url, {
        headers: {
            cookie: `PLAY_SESSION=${token}`
        },
        searchParams: { guess: ans }
    })
    const text = await resp.text()
    const rawres = text.match(/results.push\("(.+)"\)/)[1]
    // an array of 64, element i == rawres[i*2] + rawres[i*2+1]
    const result = Array.from({length: 64}, (_, i) => {
        const w = rawres[i*2] + rawres[i*2+1]
        return w == "🟩" ? 1 : (w == "🟥" ? -1 : 0)
    })
    return {
        r: result,
        rr: rawres,
        t: text
    }
}



async function main() {
    var lineno = 0

    const seed = await initial()
    
    var idok = Array.from({length: 128}, (_, i) => i)
    var res = Array.from({length: 64}, () => -1)

    while(1) {
        const { payload, pid } = (() => {
            var content = ""
            var pid = []
            for(var i = 0;i < 64;i++) {
                // randomly fetch an element from okid if res[i] == -1
                const c = res[i] >= 0 ? res[i] :
                    (() => {
                        // randomly select an element from idok
                        const idx = Math.floor(Math.random() * idok.length)
                        return idok[idx]
                    })()
                pid.push(c)
                content += elib[c]
            }
            return {
                payload: content,
                pid: pid
            }
        })()
        console.log(lineno, "trail")
        console.log(payload)
        lineno += 1
        const { r, rr, t } = await trial(seed, payload)
        if(r.every(x => x == 1)) {
            console.log("success", t)
            break
        } else {
            console.log(payload)
            console.log(rr)
            for(var i = 0;i < 64;i++) {
                if(r[i] == 1) res[i] = pid[i]
                else if(r[i] == -1) {
                    // delete pid[i] from idok
                    idok = idok.filter(x => x != pid[i])
                }
            }
            console.log(idok)
        }
    }
}

main()
