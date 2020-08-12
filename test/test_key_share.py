from collections import namedtuple
from alice_and_bob.key_share import (
    Keys, PrivateKey, diffie_hellman, get_cli_parser, cli_main, main
)
from io import StringIO
from contextlib import redirect_stdout

import re


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