from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "",
                "email": "",
                "password": ""
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "",
                "password": ""
            }
        }

class ApiKeySchema(BaseModel):
    apikey:str=Field(...)

    class Config:
        schema_extra={
            "example":{
                "apiKey":""
            }
        }
