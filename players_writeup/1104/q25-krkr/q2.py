import math
import itertools

import tqdm


def iter_all_cases():
    seats = set(range(16))
    for a_seats in itertools.combinations(seats, 6):
        for o_seats in itertools.combinations(seats.difference(a_seats), 6):
            other_seats = seats.difference(a_seats, o_seats)
            for i_seat in other_seats:
                seq = ["E"] * 16
                for ind in a_seats:
                    seq[ind] = "A"
                for ind in o_seats:
                    seq[ind] = "O"
                seq[i_seat] = "I"
                yield seq


def main():
    total = math.comb(16, 6) * math.comb(10, 6) * math.comb(4, 3)
    for seq in tqdm.tqdm(iter_all_cases(), total=total):
        mapping = {"A": 11, "E": 22, "I": 33, "O": 44, "U": 55, "}": 66}
        flag_hash = 1337

        seq.append("}")
        for c in seq:
            flag_hash *= 13337
            flag_hash += mapping[c]
            flag_hash %= 19260817

        if flag_hash == 7748521:
            tqdm.tqdm.write("flag{" + "".join(seq))
            break
    else:
        raise RuntimeError("not found")


main()
