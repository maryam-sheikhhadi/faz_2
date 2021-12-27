import hashlib


def make_pw_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_pw_hash(password, hash):
    if make_pw_hash(password) == hash:
        return True
    return False

# p = 'asdfhghytfhtyfy'
# a = print(make_pw_hash(p))
#
# p = 'asdfhghytfhtyfy'
# b = print(make_pw_hash(p))
#
# p = 'asdfhghytfhtyfy'
# c = print(make_pw_hash(p))
#
# print(a == b)
# print(a == c)
# print(c == b)