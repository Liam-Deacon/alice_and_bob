from alice_and_bob.primes import Prime

def test_known_prime():
    prime = Prime(3)
    assert isinstance(prime, int)
    assert prime == 3

def test_raises_value_error_when_not_prime():
    try:
        not_prime = Prime(4)
    except ValueError:
        pass
    else:
        raise AssertionError('ValueError not raise for non-prime')
