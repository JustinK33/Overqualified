from app.auth import hashed
import bcrypt

def test_hashed(password:bytes):
    passed = hashed(password)

    if bcrypt.checkpw(password, passed):
        print("it matches!")
    else:
        print("not a match")

test_hashed(b"asdasdsa")