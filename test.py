import sys
sys.path.append('/falcon')
from falcon import falcon

sk = falcon.SecretKey(512)
pk = falcon.PublicKey(sk)

sig = sk.sign(b"Hello")
pk.verify(b"Hell", sig)
