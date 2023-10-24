########################################
# POC by Tim Peters
# https://peps.python.org/pep-0506/#id65
# https://mail.python.org/pipermail/python-ideas/2015-September/036077.html

def invert(transform, output, n=100):
    guess = output
    for i in range(n):
        newguess = transform(guess)
        if newguess == output:
            return guess
        guess = newguess
    raise ValueError("%r not invertible in %s tries" %
                     (output, n))

t1 = lambda y: y ^ (y >> 11)
t2 = lambda y: y ^ ((y << 7) & 0x9d2c5680)
t3 = lambda y: y ^ ((y << 15) & 0xefc60000)
t4 = lambda y: y ^ (y >> 18)

def invert_mt(y):
    y = invert(t4, y)
    y = invert(t3, y)
    y = invert(t2, y)
    y = invert(t1, y)
    return y

def guess_state(vec):
    assert len(vec) == 624
    return (3,
            tuple(map(invert_mt, vec)) + (624,),
            None)
