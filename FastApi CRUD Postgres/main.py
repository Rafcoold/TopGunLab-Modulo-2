from fastapi import FastAPI, HTTPException, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from model.user_connection import UserConnection
from schema.user_schema import UserSchema

app = FastAPI()
conn = UserConnection()


@app.get("/", status_code=HTTP_200_OK)
def root():
    items = []
    for data in conn.read_all():
        dict_data = {"id": data[0], "name": data[1], "age": data[2], "species": data[3], "breed": data[4]}
        items.append(dict_data)
    return items


@app.get("/vet/user/{id}", status_code=HTTP_200_OK)
def select_one(id: str):
    data = conn.select_one(id)
    dict_data = {"id": data[0], "name": data[1], "age": data[2], "species": data[3], "breed": data[4]}
    return dict_data


@app.post("/vet/insert", status_code=HTTP_201_CREATED)
def insert(user_data: UserSchema):
    data = user_data.dict()
    data.pop("id")
    conn.write(data)
    return Response(status_code=HTTP_201_CREATED)


@app.put("/vet/update/{id}", status_code=HTTP_204_NO_CONTENT)
def update(user_data: UserSchema, id: str):
    data = user_data.dict()
    data["id"] = id
    conn.update(data)
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.delete("/vet/delete/{id}", status_code=HTTP_204_NO_CONTENT)
def delete(id: str):
    conn.delete(id)
    return Response(status_code=HTTP_204_NO_CONTENT)
