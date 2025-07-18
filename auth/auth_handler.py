# app/auth/auth_handler.py

import time
from typing import Dict

import jwt
from decouple import config


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(apiKey: str) -> Dict[str, str]:
    payload = {
        "apiKey": apiKey,
        "expires": time.time() + 3.154e+7
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}