"""Module for naively performing Diffie-Helman key exchange."""
from argparse import ArgumentError, ArgumentParser
from collections import namedtuple

import sys
import secrets

from .primes import Prime

Keys = namedtuple('Keys', 'public_key_pair private_key_a private_key_b')

class PrivateKey:
    DEFAULT_BITS = 512

    @classmethod
    def generate_private_key(cls, size: int = None) -> int:
        """Return the private key"""
        return int('0x' + secrets.token_hex(size or cls.DEFAULT_BITS), 16)


def diffie_hellman(p: Prime, g: Prime) -> Keys:
    """Generate public and private keys for primes p and g using Diffie-Hellman algorithm.

    Parameters
    ----------
    p: Prime
        First prime number, acting as prime modulus value.
    g: Prime
        Second prime number, acting as prime base value.

    Returns
    -------
    Named Tuple of shared public key generated from p & g, private key a, and private key b.

    Or more simply: 

    ((public_a, public_b), private_a, private_b)  


    References
    ----------
    [1] https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
    [2] https://en.wikipedia.org/wiki/RSA_(cryptosystem)
    [3] https://security.stackexchange.com/questions/45963/diffie-hellman-key-exchange-in-plain-english

    """
    # create private keys for alice and bob
    a = PrivateKey.generate_private_key()
    b = PrivateKey.generate_private_key()

    # generate public keys by mixing primes 
    A = pow(g, a, p)  # share this with Bob
    B = pow(g, b, p)  # share this with Alice

    return Keys((A, B), a, b)


def get_cli_parser():
    parser = ArgumentParser(description="CLI options for Alice and Bob key share")
    parser.add_argument('-p', help='Prime p for information exchange', type=int)
    parser.add_argument('-g', help='Prime g for information exchange', type=int)
    parser.add_argument('--bits', help="The number of bits for the private encryption key", type=int, default=512)
    return parser


def cli_main(argv=sys.argv):
    """This is the main entry for command line execution of the program.
    
    Run with `python -m alice_and_bob.key_share --help` for more details."
    
    """
    parser = get_cli_parser()
    args, _ = parser.parse_known_args(argv)
    PrivateKey.DEFAULT_BITS = args.bits
    main(args.p, args.g)


def main(p: Prime, g: Prime):
    """Perform actions requested by coding challenge.
    
    Briefly, perform the following:

    1. Generate public key pair from Diffie-Helmann algorithm
    2. Using public key pair, calculate shared secret key for both Alice and Bob
    3. Check shared secret is the same and print to console.

    """
    try:
        p, g = Prime(p), Prime(g)
    except ValueError:
        raise ArgumentError("Encryption is only secure if p and q are prime numbers.")


    # do Diffie-Hellman key exchange by mixing primes
    keys = diffie_hellman(p, g)
    A, B = keys.public_pair

    # get secret key
    alice_shared_secret = pow(B, keys.private_a, p)
    bob_shared_secret = pow(A, keys.private_b, p)

    if alice_shared_secret != bob_shared_secret:
        raise ValueError('Shared secret keys for Alice and Bob must match '
                         f'(got {alice_shared_secret}, {bob_shared_secret})')

    print(f'Shared secret key: {alice_shared_secret}')

    # print(keys.public_pair)

if __name__ == '__main__':
    cli_main()
