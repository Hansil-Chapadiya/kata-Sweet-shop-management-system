import bcrypt
#hashed password
def hash_password(password):
    #generate salt
    salt = bcrypt.gensalt()

    #hash the password using the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt)

    #return hashed_password as string
    return hashed_password.decode('utf-8')

# print(hash_password('1234567890**'))