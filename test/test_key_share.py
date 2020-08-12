from collections import namedtuple
from alice_and_bob.key_share import (
    Keys, PrivateKey, diffie_hellman, get_cli_parser, cli_main, main
)
from io import StringIO
from contextlib import redirect_stdout

import re
import random


def test_keys_named_tuple():
    assert issubclass(Keys, tuple)

    keys = Keys((1, 2), 3, 4)
    assert hasattr(keys, 'public_key_pair')
    assert hasattr(keys, 'private_key_a')
    assert hasattr(keys, 'private_key_b')

    assert len(keys) == 3

    assert keys.public_key_pair == keys[0] == (1, 2)
    assert keys.private_key_a == keys[1] == 3
    assert keys.private_key_b == keys[2] == 4


def test_diffie_hellman_output_types():
    output = diffie_hellman(2, 3)
    assert len(output) == 3
    assert hasattr(output, 'public_key_pair')

    assert all(map(lambda x: isinstance(x, int), output[0]))
    assert isinstance(output[1], int)
    assert isinstance(output[2], int)

def test_main_with_non_prime_p_and_g():
    try:
        main(4, 6)
    except RuntimeError:
        pass
    else:
        raise AssertionError('RuntimeError exception expected')

def test_main_output():
    with StringIO() as fake_stdout:
        with redirect_stdout(fake_stdout):
            main(88937, 194729)  # two randomly select primes

        assert re.match('Shared secret key: [0-9]+', fake_stdout.getvalue())

def test_generate_private_key():
    random.seed(0)

    keys = []
    for i in range(1000):
        key = PrivateKey.generate_private_key()
        assert key not in keys
        keys.append(key)


def test_generate_private_key_bit_length():
    random.seed(0)

    keys1 = []
    for i in range(10):
        key = PrivateKey.generate_private_key(256)
        assert key not in keys1
        keys1.append(key)

        random.seed(0)

    # second part: double check function is repeatable (needed to verify for next check below)
    random.seed(0)  # reset

    keys2 = []
    for i in range(10):
        key = PrivateKey.generate_private_key(256)
        assert key not in keys2
        keys2.append(key)

    assert keys1 == keys2

    # final part: try different number of bits when generating private key
    random.seed(0)

    keys3 = []
    for i in range(10):
        key = PrivateKey.generate_private_key(512)
        assert key not in keys2
        keys2.append(key)

    assert all((keys2[i] != keys3[i] for i in range(len(keys2))))
