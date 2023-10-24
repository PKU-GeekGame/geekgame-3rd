import random

from crack_mt import guess_state

def main():
    data = bytes.fromhex(input(">>> "))
    arr = memoryview(data)[:2500].cast("I")

    newrand = random.Random()
    newrand.setstate(guess_state(arr[1:]))
    mask = newrand.randbytes(len(data) - 2500)
    plain_text = bytes(x^y for x, y in zip(mask, data[2500:]))
    print(plain_text.strip().decode())

main()
