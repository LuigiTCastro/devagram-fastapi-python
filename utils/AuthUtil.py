from passlib.context import CryptContext
# Was necessary to use 'pip install bcrypt' too

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


class AuthUtil:
    def encrypt_password(self, password): # ITS REQUIRED TO HAVE THE 'SELF' PARAMETER
        return pwd_context.hash(password)

    def decrypt_password(self, password, encrypted_password):
        return pwd_context.verify(password, encrypted_password)
