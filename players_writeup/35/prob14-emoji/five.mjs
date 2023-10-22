import ky from 'ky'

const url = 'https://prob14.geekgame.pku.edu.cn/level1'


var emojilib = new Set()

async function enrich() {
    // randomly select 5 emoji
    const resp1 = await ky.get(url)
    const text1 = await resp1.text()
    // want to find placeholder="...." and fetch the value
    var placeholder = (text1.match(/placeholder="(.+)"/)[1]).split("")
    
    for(var i = 0; i < 64;i++) {
        const word = placeholder[i*2] + placeholder[i*2+1]
        emojilib.add(word)
    }
}

function Payload(s) {
    return `💈💅👼💁👦👗💊💊👱👇👔💆👺👦👓👳👔👉👞💄👧👘💃👺👸👴${s[0]}👙👵💆👩👽👛👓👦👝👢💃💅👶👅💈👈💅👼👁👃💂👆👄👂👳👲👢💆👤👜👆👺👱👺👛👆👡`
}

async function query(c) {
    const payload = Payload([c])
    const resp2 = await ky.get(url, {
        searchParams: { guess: payload }
    })
    const text2 = await resp2.text()
    const result = text2.match(/results.push\("(.+)"\)/)[1]
    return { payload, result }
}


async function calc(c) {
    const { payload, result } = await query(c)
    var cnt = 0;
    for(var i = 0;i < 64;i++) {
        const me = result[i*2] + result[i*2+1]
        const p = payload[i*2] + payload[i*2+1]
        if(me === '🟩') {
            cnt+=1
        } else if(me === '🟥') {
            emojilib.delete()
        }
    }
    console.log(payload)
    console.log(result, cnt)
    return cnt == 64
}

let sleepFun = (time) => new Promise((resolve) => setTimeout(resolve, time));

async function main() {
    for(var i = 0;emojilib.size < 128;i++) {
        await enrich();
        console.log("enrich", i, emojilib.size)
        await sleepFun(1000)
    }
    
    const emojis = Array.from(emojilib)

    for(var i = 0;i < 128;i++) {
        if(await calc(emojis[i])) break;
        await sleepFun(1000)
    }
}

main()
