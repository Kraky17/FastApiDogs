from enum import Enum
from http.client import HTTPException

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get("/")
def read_root():
    return "Welcome to the dog service"


@app.post("/dog")
async def create_dog(dog: Dog):
    dogs_db[dog.pk] = dog
    return {"message": "Dog created successfully"}


@app.post("/post")
async def get_post(timestamp: Timestamp):
    return timestamp


@app.get("/dogs/")
def read_dogs():
    return dogs_db


@app.get("/dogs/{pk}")
def read_dog(pk: int):
    if pk not in dogs_db:
        raise HTTPException()
    return dogs_db[pk]


@app.get("/dog")
def read_dogs_by_kind(kind: DogType):
    result = []
    for dog in dogs_db.values():
        if dog.kind == kind:
            result.append(dog)
    return result


@app.patch("/dogs/{pk}")
def update_dog(pk: int, dog: Dog):
    if pk not in dogs_db:
        raise HTTPException()
    dogs_db[pk] = dog
    return {"message": "Dog updated successfully"}
