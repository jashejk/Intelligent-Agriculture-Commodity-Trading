import bcrypt


def gen_salt():
    return bcrypt.gensalt()


def hash_password(password):
    salt = gen_salt()
    hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), salt=salt)
    return hashed_pwd, salt


def validate_password(pwd, hashed_pwd):
    return bcrypt.checkpw(pwd, hashed_pwd)
