type Split<S extends string, D extends string> =
    string extends S ? string[] :
    S extends '' ? [] :
    S extends `${infer T}${D}${infer U}` ? [T, ...Split<U, D>] : [S];
type Foo = Split<flag1, "{">
let [a, b] = "" as unknown as Foo
let foo: "x" = b
