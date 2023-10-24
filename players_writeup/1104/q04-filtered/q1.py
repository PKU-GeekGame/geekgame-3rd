def main():
    out = []
    out.append("重复把【[^a]】替换成【a】喵")

    out.append("如果没看到【a】就跳转到【空】喵")

    a = ord("a")
    for x, y in zip(map(chr, range(a, a+10)),
                    map(chr, range(a+1, a+11))):
        out.append(f"重复把【{x}{{10}}】替换成【{y}】喵")

    for char in map(chr, range(a+10, a-1, -1)):
        out.append(f"如果看到【{char}】就跳转到【{char}】喵")
        out.append(r"把【(?<=\d)(?=[a-z]|$)】替换成【0】喵")
        out.append(f"{char}：")
        for i in range(9, 0, -1):
            out.append(f"把【{char}{{{i}}}】替换成【{i}】喵")

    out.append("空：")
    out.append("把【^$】替换成【0】喵")

    out.append("谢谢喵")
    print("\n".join(out))

main()
