# from jose import jwt, JWTError
# from datetime import datetime, timedelta
# Create the bare minimal JWT.
import jwt
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta

private_key = open('./app/security/id_rsa', 'r').read()
public_key = open('./app/security/id_rsa.pub', 'r').read()

def encoding(user_id: str):
    """
    Encodes the user_id into a JWT token.
    """
    # Define the payload with an expiration time
    payload = {
        "user_id": str(user_id),
        # "exp": datetime.utcnow() + timedelta(minutes=30)  # Token expires in 30 minutes
    }
    
    # Getting Private key
    pvt_key = serialization.load_ssh_private_key(private_key.encode(), password=b'12345678')
# >>> keyserialization.load_pem_private_key(
#         private_key.encode(),
#         password=b'12345678'
#     )
    
    # Encode the payload to create the JWT token
    token = jwt.encode(payload, key=pvt_key, algorithm="RS256")
    
    return token

def decoding(token: str):
    """
    Decodes the JWT token and returns the user_id.
    """
    try:
        # Getting Public key
        pub_key = serialization.load_ssh_public_key(
            public_key.encode()
        )
        
        # Decode the token using the public key
        payload = jwt.decode(token, pub_key, algorithms=["RS256"])
        
        return {"data": payload["user_id"], "status": 0}
    
    except jwt.ExpiredSignatureError:
        return {"data":"Token has expired", "status": 1}
    except jwt.InvalidTokenError:
        return {"data":"Invalid token", "status" : 2}
    except Exception as e:
        return {"data": str(e), "status":3}
    
# 0 -> Token decoded successfully
# 1 -> Token expired
# 2 -> Invalid token
# 3 -> Other errors
    