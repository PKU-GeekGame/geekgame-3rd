def main():
    out = []
    out.append(r"把【(?s)^(.)】替换成【--5f30f0eb--\n\1】喵")
    out.append(r"把【\n*$】替换成【\n】喵")
    for i in range(1, 874):
        out.append(rf"重复把【(?s)(--5f30f0eb--.*\n)([^\n]{{{i}}}\n)】替换成【\2\1】喵")
    out.append("把【(?s)--5f30f0eb--.*$】替换成【】喵")
    out.append("谢谢喵")
    print("\n".join(out))

main()
