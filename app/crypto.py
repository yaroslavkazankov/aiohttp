
import hashlib

F_KEY = {'a': 'o',
         'b': 'e',
         'c': 'j',
         'd': 'z',
         'e': 'f',
         'f': 't',
         'g': 'y',
         'h': 'p',
         'i': 'u',
         'j': 'r',
         'k': 'l',
         'l': 'a',
         'm': 'b',
         'n': 'q',
         'o': 'x',
         'p': 'c',
         'q': 'h',
         'r': 'd',
         's': 'k',
         't': 'v',
         'u': 'g',
         'v': 'i',
         'w': 'n',
         'x': 'w',
         'y': 's',
         'z': 'm'
         }


SECRET_KEY = "gslkmgkpooitr02349i5okgsl;,vop3i4-02oe][qd'acx.;gk233or1[]r;lql"


class Crypto():

    def cryptor(pas: str) -> bytes:
        result = SECRET_KEY
        for let in pas:
            if let.istitle:
                if let in F_KEY:
                    let = F_KEY[let.lower()].upper()
            else:
                let = F_KEY[let]
            result += let
        out = hashlib.md5(result.encode()).hexdigest()
        return out
