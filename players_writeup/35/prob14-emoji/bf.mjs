import ky from 'ky'

const url = 'https://prob14.geekgame.pku.edu.cn/level1'

var chizu = new Array(64).fill("")
var cnt = 0

// a set of emoji


function getChizu() {
    const mae = "⬜⬜👼💁👦👗💊💊👱👇👔💆👺⬜👓👳👔👉👞💄👧👘💃👺👸👴⬜👙👵💆👩👽👛👓👦👝👢💃💅👶👅💈👈💅👼👁👃💂👆👄⬜👳👲👢💆👤👜👆👺👱👺👛👆👡"
    for(var i = 0;i < 64;i++) {
        chizu[i] = mae[i*2]+mae[i*2+1]
        cnt += 1
        if(chizu[i] === "⬜") {
            chizu[i] = ""
            cnt -= 1
        }
    }
    console.log(chizu.join(''))
    console.log(cnt)
}


var reditem = new Set()
var yellowitem = new Set()



async function query() {
    const resp1 = await ky.get(url)
    const text1 = await resp1.text()
    // want to find placeholder="...." and fetch the value
    var placeholder = (text1.match(/placeholder="(.+)"/)[1]).split("")
    
    for(var i = 0; i < 64;i++) {
        if(chizu[i] !== "") {
            placeholder[i*2] = chizu[i][0]
            placeholder[i*2+1] = chizu[i][1]
        }
    }

    const resp2 = await ky.get(url, {
        searchParams: { guess: placeholder.join("") }
    })
    const text2 = await resp2.text()
    // console.log(text2)
    // want to find results.push("....") and fetch the value
    const result = text2.match(/results.push\("(.+)"\)/)[1]
    // console.log(placeholder, result)
    return { placeholder, result }
}


async function calc() {
    const { placeholder, result } = await query()
    for(var i = 0;i < 64;i++) {
        if(result[i*2] + result[i*2+1] === '🟩') {
            chizu[i] = placeholder[i*2]+placeholder[i*2+1]
            cnt+=1
        } else if(result[i] === '🟥') {
            reditem.add(placeholder[i*2]+placeholder[i*2+1])
        } else {
            yellowitem.add(placeholder[i*2]+placeholder[i*2+1])
        }
    }
    console.log(chizu.map(x => x === "" ? '⬜' : x).join(''))
}

let sleepFun = (time) => new Promise((resolve) => setTimeout(resolve, time));

async function main() {
    getChizu()
    for(var i = 0;i < 2560;i++) {
        await calc()
        await sleepFun(1000)
        if(cnt === 64) {
            break
        }
    }
    console.log("reditem", reditem)
    console.log("yellowitem", yellowitem)
}

main()