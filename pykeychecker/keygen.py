import unicodedata
import sys
import bitcoin
import pysodium
from pyblake2 import blake2b
from hashlib import sha256
import binascii


if __name__ == '__main__':
    mnemonic = ' '.join(bitcoin.mnemonic.entropy_to_words(pysodium.randombytes(32)))
    seed = bitcoin.mnemonic_to_seed(mnemonic)[:32]
    pk, sk = pysodium.crypto_sign_seed_keypair(seed)
    pkh = bitcoin.bin_to_b58check(blake2b(pk,20).digest(), magicbyte=434591)
    secret_key = bitcoin.bin_to_b58check(seed, magicbyte=219101703)
    print "mnemonic: %s" % mnemonic
    print "secret seed: %s" % secret_key
    print "public key hash: %s" % pkh
