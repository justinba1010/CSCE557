# RSA Implementation

## Approach

I wanted to be able to encrypt any file. So I read everything in as bytes, and then convert to an integer to encrypt. However, I did not want to deal at the moment with base64 for prettiness. So instead the public and private keys are stored as line delimitted integers in ascii text. However the file gets encrypted to some ciphertext that is just binary data. And the decryption takes the binary data back to the original binary data.

## RSA Algorithm

First generate two primes. I used probabilistic prime generation, but with a variable in `globally.py` I can turn on and off whether I verify this prime NOT to be a Carmichael number with the sieve of erasthothenes. I use these two primes to generate a modulus that is part of the public and private key. I then choose any number, preferably large, Wikipedia says small numbers suffer in certain cases as my public key. I have a markdown viewer with LaTeX enabled, so
