from collections import namedtuple
from alice_and_bob.key_share import (
    Keys, PrivateKey, diffie_hellman, get_cli_parser, cli_main, main
)

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


def test_diffie_hellman_output():
    output = diffie_hellman(2, 3)
    assert len(output) == 3
    assert hasattr(output, 'public_key_pair')
    
    assert all(map(lambda x: isinstance(x, int), output[0]))
    assert isinstance(output[1], int)
    assert isinstance(output[2], int) 