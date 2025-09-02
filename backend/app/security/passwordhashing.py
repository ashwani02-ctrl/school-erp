import hashlib

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.
    
    Args:
        password (str): The password to hash.
        
    Returns:
        str: The hashed password in hexadecimal format.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def random_password_generator() -> str:
    """
    Generate a random password.
    
    Returns:
        str: A random password.
    """
    import random
    import string
    
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    
    return password