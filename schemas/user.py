from pydantic import BaseModel


class Schema_User(BaseModel):
    # Modelo de autenticación de usuario con campos de correo electrónico y contraseña
    email:str
    password:str