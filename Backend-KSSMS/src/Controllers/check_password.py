import bcrypt

def verify_password(password,hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'),hashed_password.encode('utf-8'))

# print(verify_password("1234567890*","$2b$12$ID1eA8aTEyg2kPVZLtaPfeJ981zIfUz6aUkdP.WcV3eZqzXSSWAUO"))