import unicodedata
import sys
import bitcoin
import pysodium
from pyblake2 import blake2b
from hashlib import sha256

def bitcoin_address(pkh):
    bitcoin_keys = [
        '\x02\xc0T!\xaa\x00\x13\xee\xd38T#\xb6<\xd2\x89' +
        '\xc3BR\x118\xaa\xffj\x91U\xb3\xc7\xc8t\xc3\x1e\xa9',
        '\x03\xb3\xb1|\xe2\x13\xe4\xed\xb9\xf1\x7f\x0e\x11' +
        '\xf5h\x80\xa8\x96r\xd2 4\x83\xbb\x7fu\xb1\x1a%_\x08\xdc\x96'
       ]
    script = bitcoin.serialize_script(
        [pkh.digest(), 117,  2] + bitcoin_keys + [2, 174])
    return bitcoin.p2sh_scriptaddr(script)

def ethereum_data(pkh):
    checksum = sha256(sha256(pkh.digest()).digest()).hexdigest()[:8]
    return "0x946941ec" + pkh.hexdigest() + checksum

def tezos_pkh(pkh):
    return bitcoin.bin_to_b58check(pkh.digest(), magicbyte=434591)

def ethdata_to_tz1(ethdata):
    return ethdata[10:-8]

if __name__ == '__main__':

    if len(sys.argv) != 18:
        print("Usage: python keychecker.py garage absurd steak ...  email password")
        exit(1)
    mnemonic = ' '.join(sys.argv[1:16]).lower()
    email = sys.argv[16]
    password = sys.argv[17]
    salt = unicodedata.normalize(
        "NFKD", (email + password).decode("utf8")).encode("utf8")
    try:
        seed = bitcoin.mnemonic_to_seed(mnemonic, salt)
    except:
        print("Invalid mnemonic")
        exit(1)
    pk, sk = pysodium.crypto_sign_seed_keypair(seed[0:32])
    pkh = blake2b(pk,20)

    print "public key hash: ", tezos_pkh(pkh) 
    print "Ethereum data:   ", ethereum_data(pkh)
    print "bitcoin address: ", bitcoin_address(pkh)
