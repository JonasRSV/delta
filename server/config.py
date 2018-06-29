import configparser
import sys
import datetime
import time
import jwt
from hashlib import blake2b
from hmac import compare_digest


config = None

try:
    config = configparser.ConfigParser()
    config.read("server.config")
except Exception as e:
    sys.stderr.write("Unable to read config because: {}".format(str(e)))
    sys.stderr.write("\nTerminating Program...")
    sys.exit(1)



jwt_expiration = int(config["jwt"]["expiration"])
jwt_lock       = None
jwt_key        = None
jwt_obj        = jwt.JWT()

try:
    private_file = config["secret"]["jwt_private"]
    public_file  = config["secret"]["jwt_public"]

    with open(private_file, "rb") as private,\
         open(public_file, "rb") as public:
             jwt_lock  = private.read()
             jwt_key  = public.read()

             jwt_lock  = jwt.jwk_from_pem(jwt_lock)
             jwt_key = jwt.jwk_from_pem(jwt_key)

except Exception as e:
    raise Exception("Unable to read config {} and {}, error {}"\
            .format(private_file, public_file, str(e)))


hash_key  = None
hash_auth = None

try:
    hash_file = config["hash"]["key"]

    with open(hash_file, "rb") as hash:
        hash_key  = hash.read()
        hash_auth = int(config["hash"]["auth"])

except Exception as e:
    raise Exception("Unable to read hash key {}, error {}"\
            .format(hash_file, str(e)))




def write_server_log(message):
    timestamp = datetime.datetime.now()
    file_url  = config["logs"]["server"]

    with open(file_url, "a") as server_log:
        server_log.write("\n{}       --".format(message, str(timestamp)))


        server_log.flush()

    return None
        
def issue_token(user_id):
    expiration = time.time() + jwt_expiration

    token = {
        "exp": expiration,
        "sub": user_id
    }



    compact_jws = jwt_obj.encode(token, jwt_lock, "RS256")

    return compact_jws

def decode_token(token):
    token = jwt_obj.decode_token(token, jwt_key)

    expired = True
    if token["exp"] > time.time():
        expired = False

    return token["sub"], valid

def sign_password(password):
    password = bytes(password, "utf-8")
    h = blake2b(digest_size=hash_auth, key=hash_key)
    h.update(password)
    return h.hexdigest()

def verify_password(password, sig):
    password = bytes(password, "utf-8")
    sig      = bytes(sig, "utf-8")
    good_sig = sign_password(password)
    return compare_digest(good_sig, sig)



