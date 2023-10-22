
from random import Random
import secrets
import signal

banner = '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⠄⠐⠒⠒⠒⠒⠂⠠⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠈⣀⠤⠐⠒⠒⠒⠒⠒⠒⠂⠄⡀⠑⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡅⠘⠄⣀⣀⣀⣀⣀⣀⡀⣀⡀⠄⠘⢀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠒⠤⠄⣀⣀⣀⣀⣀⣀⣀⣀⠤⠐⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  Hi! I'm a Smol Tako!
⠀⠀⢀⣤⣦⣤⡀⠀⠀⠀⢀⣠⣶⠾⠟⠛⠋⠉⠉⠉⠉⠛⠛⠿⢷⣦⣀⠀⠀⠀⣠⣴⣶⣦⡀⠀⠀
⠀⠀⣾⡟⠉⠙⠿⣷⣤⣼⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢷⠾⠟⠛⠉⠀⢹⣷⠀⠀
⠀⠀⢻⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠀⠀
⠀⠀⠀⠻⢷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⡾⠋⠀⠀⠀  Recently, I discovered a cookie jar in
⠀⠀⠀⠀⢀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⡀⠀⠀⠀⠀  the deep sea, protected by the Ancient
⠀⠀⠀⠀⣾⡏⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣧⠀⠀⠀⠀  Tako.
⠀⠀⠀⢀⣿⠃⠀⠀⢀⣤⣶⠿⠛⠋⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⢶⣦⠀⠀⠀⠀⠀⣿⡄⠀⠀⠀
⠀⠀⠀⢸⡿⠀⠀⠀⠈⣩⣤⣄⠀⠀⠐⢦⡴⠶⢦⣤⡶⠀⠀⢠⣶⣶⡄⠀⠀⠀⠀⠀⢸⣧⠀⠀⠀  I asked for the cookie, but I couldn't
⠀⠀⠀⣾⡇⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⠀⠀⠀  understand his words.
⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡆⠀⠀
⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⠀⠀
⠀⣠⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣧⠀  Can you help me?
⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⠀⠀⠀⠀⢻⡇
⠈⠿⣾⣤⣴⣾⣿⣿⣿⣷⣦⣀⡀⠀⣀⣤⣶⣿⣿⣿⣷⣤⣀⢀⢀⣠⣾⣿⣿⣿⣿⡷⣦⣤⣤⣿⠇
⠀⠀⠀⠀⠀⠀⠈⠋⠛⠋⠉⠛⠛⠛⠛⠋⠉⠙⠛⠋⠁⠉⠉⠛⠛⠋⠁⠈⠉⠉⠁⠀⠈⠉⠉⠀⠀
'''

print(banner)

while True:
    print('There\'re three sizes of cookies. Which one do you want?')

    print('1. Smol')
    print('2. Big')
    print('3. SUPA BIG')

    option = input('Choose one: ')
    print()

    try:
        option = int(option)
    except ValueError:
        continue

    if option in [1, 2, 3, 4]:
        break


def xor_arrays(a, b, *args):
    if args:
        return xor_arrays(a, xor_arrays(b, *args))
    return bytes([x ^ y for x, y in zip(a, b)])

if option == 1:
    # [THE ANCIENT TAKO HAS HIJACKED THE CODE]
    the_void = Random(secrets.randbits(256))

    smol_cookie = open('flag1', 'rb').read()
    words = b'\0' * 2500 + smol_cookie
    ancient_words = xor_arrays(words, the_void.randbytes(len(words)))

    # [We've regained control of the code!]
    print('*You heard a obscure voice coming from the void*')
    print(ancient_words.hex())

elif option == 2:
    # [Not again!]
    seed1 = secrets.randbits(256)

    print('Ƀēħꝋłđ, ⱦħīꞥē ēɏēꞩ đꝋꞩⱦ ȼⱥⱦȼħ ⱥ ӻɍⱥꞡᵯēꞥⱦ ꝋӻ ēꞩꝋⱦēɍīȼ ēꞥīꞡᵯⱥ, ⱥ ᵯēɍē ꞡłīᵯᵯēɍ ⱳīⱦħīꞥ ⱦħē ӻⱥⱦħꝋᵯłēꞩꞩ ⱥƀɏꞩꞩ.')
    print(f'<{seed1:x}>')
    print()

    print('Ⱳħⱥⱦ ɍēꞩꝑꝋꞥꞩē đꝋꞩⱦ ⱦħꝋᵾ ꝑɍꝋӻӻēɍ, ꝑᵾꞥɏ ᵯꝋɍⱦⱥł?')
    seed2 = int(input('> '), 16)
    print()

    if seed1 == seed2:
        print('Ӻēēƀłē ᵯīᵯīȼɍɏ ꝋӻ ⱦɍᵾē ꞩⱥꞡⱥȼīⱦɏ.')
        print('NO COOKIES FOR YOU!')

        quit()

    void1 = Random(seed1)
    void2 = Random(seed2)
    void3 = Random(secrets.randbits(256))

    entropy = secrets.randbits(22)
    void1.randbytes(entropy)
    void2.randbytes(entropy)

    big_cookie = open('flag2', 'rb').read()
    words = b'\0' * 2500 + big_cookie
    n = len(words)
    ancient_words = xor_arrays(words, void1.randbytes(
        n), void2.randbytes(n), void3.randbytes(n))

    # [We've regained control of the code!]
    print('*You heard a more obscure voice coming from the void*')
    print(ancient_words.hex())

elif option == 3:
    # [THE ANCIENT TAKO HAS HIJACKED THE CODE, FOR THE LAST TIME]
    signal.alarm(10)
    print('Ⱦħē đⱥɏ ꝋӻ ɍēȼҟꝋꞥīꞥꞡ đɍⱥⱳēⱦħ ꞥīꞡħ ⱳīⱦħ ħⱥꞩⱦē. Ħⱥꞩⱦēꞥ, ꝋɍ ӻꝋɍӻēīⱦ ⱥłł.')

    rounds_of_curses = 100
    curses = [secrets.randbits(256) for _ in range(rounds_of_curses)]

    print('<' + ','.join(map(hex, curses)) + '>')
    print()

    print('Ⱳħⱥⱦ ɍēꞩꝑꝋꞥꞩē đꝋꞩⱦ ⱦħꝋᵾ ꝑɍꝋӻӻēɍ, ꝑᵾꞥɏ ᵯꝋɍⱦⱥł?')
    its_seeds = map(lambda x: int(x, 16), input('> ').split(','))

    for curse, its_seed in zip(curses, its_seeds):
        t1 = Random(curse).randbytes(2500)
        t2 = Random(its_seed).randbytes(2500)
        if t1 != t2:
            print('YOU DEMISE HAS OCCURRED.')
            quit()

    print('Good job, Smol Tako! Here\'s your delicious SUPA BIG cookie! uwu')
    print(open('flag3', 'r').read())

else:
    print('What is this? https://www.youtube.com/watch?v=nC-DQZsAY1o')
