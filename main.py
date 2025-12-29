import random
from fastapi import FastAPI, HTTPException
from schemas import Todo

app = FastAPI()

todos = []

def find_todo(id:int):
    for todo in todos:
        if todo['id'] == id:
            return todo
    return None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/seed")
def seed_todos():

    todos.clear()
    
    for i in range(10):
        todos.append(
            {
                'id': i,
                'title': f'This is a {random.choice(['random', 'arbitrary', 'out of the horizon'])} title',
                'description': f'{random.choice(['Today', 'Now', 'Mostly','For sure'])} it is a random description',
                'completed': random.choice([True, False])
            }
        )
    return {"message": "Todos seeded"}


@app.get('/todos', response_model=list[Todo])
def get_todos():
    return todos


@app.get('/todos/{id}', response_model=Todo)
def get_todo(id:int):
    todo = find_todo(id)
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo does not exist.')
    return todo


@app.delete('/todos/{id}')
def delete_todo(id:int):
    todo = find_todo(id)
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo does not exist.')
    todos.remove(todo)
    return {"message":"done"}