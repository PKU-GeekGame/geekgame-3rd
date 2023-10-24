import itertools


def main():
    data = input(">>> ")
    data_list = [x.encode() for x in data.split("x1RDgzRF")[1:]]

    table = ["".join(x) for x in itertools.product("MNOQR", "1FVl")][1:17]
    table[table.index("QV")] = "RF"
    table[table.index("Ql")] = "RV"
    table[table.index("N1")] = "M1"
    table[table.index("Q1")] = "Ql"
    table[table.index("R1")] = "Rl"
    table_map = {x: i for i, x in enumerate(table)}
    table_map["N1"] = 7
    table_map["QV"] = 0xa
    table_map["Q1"] = 0xc

    table2_map = {'z': 3, '0': 4, '1': 5, '2': 6, '3': 7, '4': 8, '5': 9, '6': 10}

    xxx = ["😅"] * 64
    for i, x in enumerate(data_list):
        try:
            xxx[i] = chr(0x1f400
                         + 0x10 * (table2_map[x[-3:-2].decode()])
                         + table_map[x[-2:].decode()])
        except LookupError:
            print(f"{i:3} {x!r}")
    print("".join(xxx))

main()
