from fastapi import APIRouter, Response, status
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import User
from passlib.hash import  sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()

@user.get('/users', response_model=list[User], tags=["users"])
def Find_All_User():
    return usersEntity(conn.Fastapi.user.find())

@user.post('/users', response_model=User, tags=["users"])
def Create_User( user: User):
    new_user = dict(user)
    new_user['password'] = sha256_crypt.encrypt(new_user['password'])
    del new_user['id']
    id = conn.Fastapi.user.insert_one(new_user).inserted_id
    user = conn.Fastapi.user.find_one({"_id": id})
    return userEntity(user)

@user.get('/users/{id}', response_model=User, tags=["users"])
def Find_user(id:str):
    return userEntity(conn.Fastapi.user.find_one({"_id": ObjectId(id)}))

@user.put('/users/{id}', response_model=User, tags=["users"])
def Update_User(id: str, user: User):
    conn.Fastapi.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
    return userEntity(conn.Fastapi.user.find_one({"_id": ObjectId(id)}))

@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def Delete_User(id: str):
        userEntity(conn.Fastapi.user.find_one_and_delete({"_id": ObjectId(id)}))
        return Response(status_code=HTTP_204_NO_CONTENT)


