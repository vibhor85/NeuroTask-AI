from fastapi import FastAPI

app = FastAPI()

@app.get("/modify-todo")
def get():
    return {"message:":"Hello world"}