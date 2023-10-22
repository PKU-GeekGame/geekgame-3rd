import ky from 'ky';

const url = 'https://prob13-nuz2zf4r.geekgame.pku.edu.cn/api/run/'

const prefix = 'flag{Ts_fLaG_bETteR_tHAn_PytH0n}'

// dict of number and alphabets and @#$%^&*_+"?~-
const dic = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*_+"?~-'
// const dic = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
var i = 0

const header = 'type FunctionParameters<T> = T extends (...args: infer P) => any ? P : never;type ConstructorReturnType<T> = T extends new () => infer R ? R : never;type ExtractInner<T> = T extends () => (arg: infer P) => unknown ? P : never;type a = ConstructorReturnType<flag2>[\'v\'];type aa = ExtractInner<a>;type aaa = FunctionParameters<aa>[1];type NeverKeys<T, R> = { [K in keyof T]: T[K] extends never ? string : R };type b1 = NeverKeys<aaa, never>;type RemoveIndex<T> = { [ K in keyof T as string extends K ? never : number extends K ? never : symbol extends K ? never : K] : T[K];};type temp = keyof RemoveIndex<b1>;type S<Str extends string, Prefix extends string> = Str extends `${Prefix}${infer Rest}` ? true : Str; '

const p = setInterval(async () => {
    if(i >= dic.length) {
        console.log('done')
        clearInterval(p)
        return
    }
    const now = prefix + dic[i]
    const res = await ky.post(url, {
        json: {
            source: header + `const a: S<temp, '${now}'> = true;` 
        }
    })
    const text = await res.text()
    console.log(now, text)
    i += 1
}, 4000)
