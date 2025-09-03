from cryptography.hazmat.primitives import serialization

private_key = open('./app/security/id_rsa', 'r').read()

payload = {
        "uid": "abc",
        "role":"admin"
        # "exp": datetime.utcnow() + timedelta(minutes=30)  # Token expires in 30 minutes
    }
pvt_key = serialization.load_ssh_private_key(data = private_key.encode(),password=None)
print(pvt_key)

import jwt
print(jwt.encode(payload, key=pvt_key, algorithm="RS256"))