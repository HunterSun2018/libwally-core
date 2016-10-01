import unittest
from util import *
from ctypes import create_string_buffer

# NIST cases from http://www.di-mgt.com.au/sha_testvectors.html
# SHA-256d vectors from https://www.dlitz.net/crypto/shad256-test-vectors/SHAd256_Test_Vectors.txt
sha2_cases = {
    'abc':
        ['ba7816bf 8f01cfea 414140de 5dae2223 b00361a3 96177a9c b410ff61 f20015ad',
         'ddaf35a193617aba cc417349ae204131 12e6fa4e89a97ea2 0a9eeee64b55d39a'
         '2192992a274fc1a8 36ba3c23a3feebbd 454d4423643ce80e 2a9ac94fa54ca49f',
         '4f8b42c22dd3729b519ba6f68d2da7cc5b2d606d05daed5ad5128cc03e6c6358'],

    '':
        ['e3b0c442 98fc1c14 9afbf4c8 996fb924 27ae41e4 649b934c a495991b 7852b855',
         'cf83e1357eefb8bd f1542850d66d8007 d620e4050b5715dc 83f4a921d36ce9ce'
         '47d0d13c5d85f2b0 ff8318d2877eec2f 63b931bd47417a81 a538327af927da3e',
         '5df6e0e2761359d30a8275058e299fcc0381534545f55cf43e41983f5d4c9456' ],

    'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq':
        ['248d6a61 d20638b8 e5c02693 0c3e6039 a33ce459 64ff2167 f6ecedd4 19db06c1',
         '204a8fc6dda82f0a 0ced7beb8e08a416 57c16ef468b228a8 279be331a703c335'
         '96fd15c13b1b07f9 aa1d3bea57789ca0 31ad85c7a71dd703 54ec631238ca3445',
         '0cffe17f68954dac3a84fb1458bd5ec99209449749b2b308b7cb55812f9563af'],

    'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmn'
    'hijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu':
        ['cf5b16a7 78af8380 036ce59e 7b049237 0b249b11 e8f07a51 afac4503 7afee9d1',
         '8e959b75dae313da 8cf4f72814fc143f 8f7779c6eb9f7fa1 7299aeadb6889018'
         '501d289e4900f7e4 331b99dec4b5433a c7d329eeb6dd2654 5e96e55b874be909',
         None],

    'a' * 1000000:
        ['cdc76e5c 9914fb92 81a1c7e2 84d73e67 f1809a48 a497200e 046d39cc c7112cd0',
         'e718483d0ce76964 4e2e42c7bc15b463 8e1f98b13b204428 5632a803afa973eb'
         'de0ff244877ea60a 4cb0432ce577c31b eb009c5c2c49aa2e 4eadb217ad8cc09b',
         '80d1189477563e1b5206b2749f1afe4807e5705e8bd77887a60187a712156688'],
}


class SHA2Tests(unittest.TestCase):

    SHA256_LEN, SHA512_LEN = 32, 64

    def make_outbuf(self, fn):
        buf_len = self.SHA512_LEN if fn == wally_sha512 else self.SHA256_LEN
        buf = create_string_buffer(buf_len)
        return buf, buf_len


    def doSHA(self, fn, hex_in):
        buf, buf_len = self.make_outbuf(fn)
        in_bytes, in_bytes_len = make_cbuffer(hex_in)
        ret = fn(in_bytes, in_bytes_len, buf, buf_len)
        self.assertEqual(ret, 0)
        return h(buf)


    def test_vectors(self):
        for in_msg, values in sha2_cases.items():
            msg = h(utf8(in_msg))
            for i, fn in enumerate([wally_sha256, wally_sha512, wally_sha256d]):
                if values[i] is not None:
                    result = self.doSHA(fn, msg)
                    expected = utf8(values[i].replace(' ', ''))
                    self.assertEqual(result, expected)


    def test_invalid_args(self):
        in_bytes, in_bytes_len = make_cbuffer(h(utf8('abc')))
        for fn in [wally_sha256, wally_sha512, wally_sha256d]:
            buf, buf_len = self.make_outbuf(fn)
            for args in [(None,     in_bytes_len, buf,  buf_len),
                         (in_bytes, in_bytes_len, None, buf_len),
                         (in_bytes, in_bytes_len, buf,  buf_len + 1)]:
                self.assertEqual(fn(args[0], args[1], args[2], args[3]),
                                 WALLY_EINVAL)


if __name__ == '__main__':
    unittest.main()
