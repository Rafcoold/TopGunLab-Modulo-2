from fastapi import FastAPI, HTTPException
from database import Base, engine, Animal
from sqlalchemy.orm import Session
from animal_class import AnimalRequest


# Create DB
Base.metadata.create_all(engine)

app = FastAPI()


# Create Read Update Delete
@app.get("/")
def root():
    return {'Vet_CRUD'}


# Create
@app.post('/Vet_CRUD')
def create_animal(animal: AnimalRequest):
    # Create DB session
    session = Session(bind=engine, expire_on_commit=False)

    # create instance of the DB
    animaldb = Animal(name=animal.name, age=animal.age, breed=animal.breed, species=animal.species)

    session.add(animaldb)
    session.commit()

    # getting the created task id
    id = animaldb.id

    session.close()

    return {"id": id, "name": animal.name, "age": animal.age, "breed": animal.breed, "species": animal.species}


# Read
@app.get('/Vet_CRUD/{id}')
def read_animal(id: int):
    # Create db session
    session = Session(bind=engine, expire_on_commit=False)

    animal = session.query(Animal).get(id)

    session.close()

    if not animal:
        raise HTTPException(status_code=404, detail=f"Animal item with id {id} not found")

    return {"id": id, "name": animal.name, "age": animal.age, "breed": animal.breed, "species": animal.species}


# Update
@app.put('/Vet_CRUD/{id}')
def update_animal(id: int, name: str, age: int, breed: str, species: str):
    # Create db session
    session = Session(bind=engine, expire_on_commit=False)

    animal = session.query(Animal).get(id)

    if animal:
        animal.name = name
        animal.age = age
        animal.breed = breed
        animal.species = species
        session.commit()

    session.close()

    if not animal:
        raise HTTPException(status_code=404, detail=f"Animal item with id {id} not found")

    return animal


# Delete
@app.delete('/Vet_CRUD/{id}')
def delete_todo(id: int):
    session = Session(bind=engine, expire_on_commit=False)

    animal = session.query(Animal).get(id)

    if animal:
        session.delete(animal)
        session.commit()

    session.close()

    if not animal:
        raise HTTPException(status_code=404, detail=f"Animal item with id {id} not found")

    return animal


# Get All
@app.get('/Vet_CRUD')
def read_all_animaldb():
    # Create db session
    session = Session(bind=engine, expire_on_commit=False)

    animal = session.query(Animal).all()

    session.close()

    return animal
