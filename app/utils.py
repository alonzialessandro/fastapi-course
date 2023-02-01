from passlib.context import CryptContext

# quale algoritmo di hash utilizzare
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

#def generateHash(password: str):
#    return pwd_context.hash(password)

generateHash = lambda password: pwd_context.hash(password)

verify_password = lambda user_password, hash_password: pwd_context.verify(secret=user_password, hash=hash_password)