from passlib.context import CryptContext

# Configure passlib to use bcrypt for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Returns a bcrypt hash of the given plaintext password
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    # Verifies a plaintext password against a stored bcrypt hash
    return pwd_context.verify(plain, hashed)