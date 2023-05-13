from jwt import encode, decode

# Creación de función para generar el token
def create_token(data:dict):
    token:str = encode(payload= data, key="my secret key", algorithm="HS256")
    return token 

# Creación de función para validar el token
def validate_token(token:str) -> dict:
    data: dict = decode(token, key="my secret key", algorithms=['HS256'])
    return data

