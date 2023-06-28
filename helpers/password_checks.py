import bcrypt


def hash_password(plain_password):
    # generate salt
    salt = bcrypt.gensalt()
    # hash password using the salt
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
