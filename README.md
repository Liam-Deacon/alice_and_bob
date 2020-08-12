![Python CI](https://github.com/Liam-Deacon/alice_and_bob/workflows/Python%20package/badge.svg)

# Alice and Bob information sharing code challenge
Diffie-Hellman coding challenge for secret information exchange using public/private keys

## Background

Alice and Bob use the Diffie-Hellman key exchange algorithm to share secret information. Alice and Bob start with prime numbers, pick private keys, generate and share public keys, finally they then generate a shared secret key.

Your code module should take in two prime numbers, **p** and **g** and output the value of p and g, the private key a for Alice and b for Bob. Finally your program should print out the Shared Secret key for Alice and Bob.

If your implementation is correct, the Shared Secret keys should match.

Note: This challenge requires you to perform calculations on large numbers. Further information can be found at 
https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange

## Code requirements

- Ensure that your code is clean and uses good practice (e.g. error handling) and is commented well.
- Ensure that your code can work cross platform and across different versions of Python.
- Feel free to add as many bells and whistles as you so desired (e.g. Unit Tests)

# Running the code

```bash
git clone https://github.com/Liam-Deacon/alice_and_bob
cd alice_and_bob
python3 -m alice_and_bob.key_share --help
```
