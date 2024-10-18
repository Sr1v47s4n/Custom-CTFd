import bcrypt
import hashlib
from CTFd.utils import string_types


def sha256(p):
    if isinstance(p, string_types):
        p = p.encode("utf-8")
    return hashlib.sha256(p).hexdigest()


def hash_password(plaintext):
    # Hash the password with bcrypt, using a cost factor of 10
    bcrypt_hashed = bcrypt.hashpw(plaintext.encode("utf-8"), bcrypt.gensalt(10))

    # Return the bcrypt-hashed password as a UTF-8 string
    return bcrypt_hashed.decode("utf-8")


def verify_password(plaintext, hashed_password):
    # Use bcrypt's checkpw to verify the password
    return bcrypt.checkpw(plaintext.encode("utf-8"), hashed_password.encode("utf-8"))
