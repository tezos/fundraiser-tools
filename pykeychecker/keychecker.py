import unicodedata
import sys
import bitcoin
import pysodium
from pyblake2 import blake2b
from hashlib import sha256
import binascii

def bitcoin_address(digest):
    bitcoin_keys = [
        '\x02\xc0T!\xaa\x00\x13\xee\xd38T#\xb6<\xd2\x89' +
        '\xc3BR\x118\xaa\xffj\x91U\xb3\xc7\xc8t\xc3\x1e\xa9',
        '\x03\xb3\xb1|\xe2\x13\xe4\xed\xb9\xf1\x7f\x0e\x11' +
        '\xf5h\x80\xa8\x96r\xd2 4\x83\xbb\x7fu\xb1\x1a%_\x08\xdc\x96'
       ]
    script = bitcoin.serialize_script(
        [digest, 117,  2] + bitcoin_keys + [2, 174])
    return bitcoin.p2sh_scriptaddr(script)

def ethereum_data(digest, hexdigest):
    checksum = sha256(sha256(digest).digest()).hexdigest()[:8]
    return "0x946941ec" + hexdigest + checksum

def tezos_pkh(digest):
    return bitcoin.bin_to_b58check(digest, magicbyte=434591)

def ethdata_to_tz1(ethdata):
    return ethdata[10:-8]

if __name__ == '__main__':
    tz_input = sys.argv[1]
    assert(tz_input == bitcoin.bin_to_b58check(bitcoin.b58check_to_bin(tz_input)[2:], magicbyte=434591))
    
    digest = bitcoin.b58check_to_bin(tz_input)[2:]
    hexdigest = binascii.hexlify(digest)

    print "public key hash: ", tezos_pkh(digest)
    print "Ethereum data:   ", ethereum_data(digest, hexdigest)
    print "bitcoin address: ", bitcoin_address(digest)
