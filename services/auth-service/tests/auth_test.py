from app.auth import hashed, register
import bcrypt

def test_hashed(password: str):
    passed = hashed(password)

    if bcrypt.checkpw(password.encode("utf-8"), passed):
        print("it matches!")
    else:
        print("not a match")

# test_hashed("asdasdsa")