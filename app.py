from fastapi import FastAPI
from routes.user import user


app = FastAPI(
    title="REST API with MongoDB",
    description= "thist is a simple  REST API using fastapi and mongodb"
)

app.include_router(user)